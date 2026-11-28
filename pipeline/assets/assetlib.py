"""Shared helpers for asset intake/verify (A24). Read-only analysis; originals are never modified."""
import hashlib, json, os, re, struct, datetime as dt

SCRIPT_VERSION = "1.0.0"
PNG_SIG = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 50 * 1024 * 1024
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp"}
AUDIO_EXT = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}
KINDS = ["character", "expression", "parts", "prop", "texture", "environment", "audio", "other"]
TEXT_CHUNKS = {b"tEXt", b"iTXt", b"zTXt", b"eXIf"}
C2PA_LIKE = {b"caBX"}  # JUMBF/C2PA box carrier in PNG
COLOR_TYPE = {0: "grayscale", 2: "RGB", 3: "palette", 4: "grayscale+alpha", 6: "RGBA"}


def utcnow():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path, bufsize=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(bufsize)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def sniff_format(path):
    with open(path, "rb") as f:
        head = f.read(16)
    if head.startswith(PNG_SIG): return "png"
    if head.startswith(b"\xff\xd8\xff"): return "jpeg"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP": return "webp"
    if head[:4] == b"RIFF" and head[8:12] == b"WAVE": return "wav"
    if head[:4] == b"fLaC": return "flac"
    if head[:4] == b"OggS": return "ogg"
    if head[:3] == b"ID3" or head[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2"): return "mp3"
    return "unknown"


def png_chunks(path):
    """Pure-Python chunk walk. Returns list of {type,length,offset,crc_ok}. Stops at IEND/truncation."""
    out = []
    import zlib
    with open(path, "rb") as f:
        if f.read(8) != PNG_SIG:
            raise ValueError("not a PNG")
        off = 8
        while True:
            hdr = f.read(8)
            if len(hdr) < 8:
                out.append({"type": "TRUNCATED", "length": 0, "offset": off, "crc_ok": False}); break
            ln, typ = struct.unpack(">I4s", hdr)
            data = f.read(ln)
            crc = f.read(4)
            ok = len(data) == ln and len(crc) == 4 and (zlib.crc32(typ + data) & 0xFFFFFFFF) == struct.unpack(">I", crc)[0]
            out.append({"type": typ.decode("latin-1"), "length": ln, "offset": off, "crc_ok": ok})
            off += 12 + ln
            if typ == b"IEND":
                break
    return out


def collapse_chunks(chunks):
    """Collapse consecutive same-type chunks (IDAT runs) for compact sidecars."""
    res = []
    for c in chunks:
        if res and res[-1]["type"] == c["type"] and c["type"] == "IDAT":
            res[-1]["count"] += 1; res[-1]["length"] += c["length"]
            res[-1]["crc_ok"] = res[-1]["crc_ok"] and c["crc_ok"]
        else:
            res.append({"type": c["type"], "length": c["length"], "count": 1, "crc_ok": c["crc_ok"]})
    return res


def alpha_stats(arr_alpha):
    import numpy as np
    a = np.asarray(arr_alpha)
    n = a.size
    transparent = int((a == 0).sum()); opaque = int((a == a.max() if False else a == 255).sum())
    semi = n - transparent - opaque
    ys, xs = np.nonzero(a > 0)
    bbox = None if ys.size == 0 else [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
    return {"fraction_transparent": transparent / n, "fraction_semi_transparent": semi / n,
            "fraction_opaque": opaque / n, "bbox_nonzero_xywh_exclusive": bbox,
            "min": int(a.min()), "max": int(a.max()), "pixels": n}


def analyse_image(path, fmt):
    from PIL import Image
    import numpy as np
    facts = {"format": fmt}
    chunks = None
    with Image.open(path) as im:
        im.load()
        facts["width"], facts["height"] = im.size
        facts["mode"] = im.mode
        info = im.info
        facts["has_icc_profile"] = "icc_profile" in info
        facts["exif_present"] = bool(im.getexif()) if fmt in ("jpeg", "webp", "png") else False
        facts["xmp_present"] = any(k in info for k in ("xmp", "XML:com.adobe.xmp")) or \
            (fmt == "jpeg" and b"http://ns.adobe.com/xap/1.0/" in open(path, "rb").read(1 << 20))
        has_alpha = im.mode in ("RGBA", "LA", "PA") or "transparency" in info
        facts["has_alpha_channel"] = has_alpha
        if has_alpha:
            a = np.asarray(im.convert("RGBA"))[..., 3]
            facts["alpha"] = alpha_stats(a)
        else:
            facts["alpha"] = None
    if fmt == "png":
        raw = png_chunks(path)
        chunks = collapse_chunks(raw)
        with open(path, "rb") as f:
            f.seek(8); f.read(8); ihdr = f.read(13)
        bd, ct, _, _, il = struct.unpack(">BBBBB", ihdr[8:13])
        facts["bit_depth"] = bd
        facts["png_color_type"] = COLOR_TYPE.get(ct, str(ct))
        facts["interlaced"] = bool(il)
        facts["png_chunks"] = chunks
        facts["c2pa_chunks"] = [{"type": c["type"], "length": c["length"]} for c in chunks if c["type"].encode() in C2PA_LIKE]
        facts["text_chunks"] = [{"type": c["type"], "length": c["length"]} for c in chunks if c["type"].encode() in TEXT_CHUNKS]
        facts["png_chunks_crc_all_ok"] = all(c["crc_ok"] for c in chunks)
        if any(c["type"] == "eXIf" for c in chunks): facts["exif_present"] = True
    return facts


def analyse_audio(path, fmt):
    facts = {"format": fmt}
    try:
        import soundfile as sf
        i = sf.info(path)
        facts.update({"sample_rate": i.samplerate, "channels": i.channels,
                      "duration_s": round(i.duration, 6), "subtype": i.subtype})
    except Exception as e:  # noqa
        facts["audio_info_error"] = str(e)[:200]
    return facts


def slugify(s, n=40):
    s = re.sub(r"_[0-9a-f]{8}$", "", s.lower())  # drop Flow's trailing 8-hex id
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return (s[:n].strip("-")) or "asset"


def read_ledger(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]
