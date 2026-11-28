#!/usr/bin/env python3
"""Intake a downloaded asset into the private store. Byte-exact copy; never modifies the original.

Run with: .venv-analysis/bin/python -I pipeline/assets/intake.py <file> --kind ... --request-id ... --store <dir>
"""
import argparse, json, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import assetlib as L

DEFAULT_STORE = os.path.expanduser("~/ricks-clips-private/assets")


def intake(args):
    src = os.path.abspath(os.path.expanduser(args.file))
    if not os.path.isfile(src):
        return 2, {"error": f"not a file: {src}"}
    size = os.path.getsize(src)
    if size > L.MAX_BYTES:
        return 2, {"error": f"refused: {size} bytes exceeds 50 MB limit"}
    ext = os.path.splitext(src)[1].lower()
    fmt = L.sniff_format(src)
    is_img = fmt in ("png", "jpeg", "webp"); is_aud = fmt in ("wav", "flac", "ogg", "mp3")
    if not (is_img or is_aud) and not args.force_type:
        return 2, {"error": f"refused: unsupported type (sniffed '{fmt}', ext '{ext}'); use --force-type"}
    if args.kind == "audio" and is_img or (args.kind != "audio" and is_aud):
        print(f"warning: kind '{args.kind}' does not match sniffed format '{fmt}'", file=sys.stderr)
    store = os.path.abspath(os.path.expanduser(args.store))
    ledger_path = os.path.join(store, "INTAKE_LEDGER.jsonl")
    digest = L.sha256_file(src)

    for e in L.read_ledger(ledger_path):  # idempotency by content hash
        if e.get("sha256") == digest and e.get("event") == "intake":
            return 0, {"status": "already_intaken", "sha256": digest, "stored_path": e["stored_path"]}

    # Validate all inputs BEFORE copying (director fix 2026-11-28: a bad --settings-json used to crash after the copy,
    # leaving an orphan file with no sidecar/ledger line, so the retry stored a duplicate v02).
    prompt = None
    if args.prompt_file:
        with open(os.path.expanduser(args.prompt_file), encoding="utf-8") as f:
            prompt = f.read()
    try:
        sj = args.settings_json
        if sj and os.path.isfile(os.path.expanduser(sj)):   # accept a path to a JSON file as well as inline JSON
            with open(os.path.expanduser(sj), encoding="utf-8") as f:
                sj = f.read()
        settings = json.loads(sj) if sj else None
    except (ValueError, OSError) as e:
        return 2, {"error": f"--settings-json is not valid JSON or a readable JSON file: {e}"}

    facts = (L.analyse_image(src, fmt) if is_img else L.analyse_audio(src, fmt) if is_aud else {"format": fmt})
    date = args.date or L.utcnow()[:10].replace("-", "")
    slug = L.slugify(args.slug or os.path.splitext(os.path.basename(src))[0])
    kind_dir = os.path.join(store, args.kind)
    os.makedirs(kind_dir, exist_ok=True)
    ext_out = ext if ext else "." + fmt
    v = 1
    while os.path.exists(os.path.join(kind_dir, f"{date}_{args.request_id}_{slug}_v{v:02d}{ext_out}")):
        v += 1
    name = f"{date}_{args.request_id}_{slug}_v{v:02d}{ext_out}"
    dest = os.path.join(kind_dir, name)
    shutil.copyfile(src, dest)  # byte copy
    shutil.copystat(src, dest)
    if L.sha256_file(dest) != digest or os.path.getsize(dest) != size:
        os.remove(dest)
        return 3, {"error": "copy verification failed (hash/size mismatch); copy removed"}

    now = L.utcnow()
    events = []
    if args.generated_utc:
        events.append({"event": "generated", "utc": args.generated_utc, "actor": args.provider or "unknown", "detail": "as reported by operator"})
    if args.downloaded_utc:
        events.append({"event": "downloaded", "utc": args.downloaded_utc, "actor": "operator", "detail": args.download_note or ""})
    events.append({"event": "intaken", "utc": now, "actor": "a24/intake.py", "detail": f"copied byte-exact from original path basename '{os.path.basename(src)}'; sha256 verified"})
    for note in (args.event or []):  # e.g. "transferred_via_drive|2026-11-27T16:00:00Z|note"
        p = (note.split("|") + ["", ""])[:3]
        events.append({"event": p[0], "utc": p[1] or now, "actor": "operator", "detail": p[2]})
    c2pa = bool(facts.get("c2pa_chunks"))
    side = {
        "schema_version": 1, "script_version": L.SCRIPT_VERSION,
        "asset_id": f"{date}_{args.request_id}_{slug}_v{v:02d}",
        "kind": args.kind, "request_id": args.request_id,
        "file": {"stored_name": name, "original_basename": os.path.basename(src), "size_bytes": size, "sha256": digest},
        "generation": {"provider": args.provider, "model": args.model, "prompt": prompt,
                       "prompt_file": os.path.basename(args.prompt_file) if args.prompt_file else None,
                       "settings": settings, "credits_consumed": args.credits},
        "protection": {"visible_watermark": args.visible_watermark, "c2pa_chunk_present": c2pa,
                       "synthid_claimed_by_provider": args.synthid, "preserved_unmodified": True},
        "technical": facts,
        "licence_terms_note": args.terms_note,
        "chain_of_custody": events,
    }
    sidecar = dest + ".provenance.json"
    with open(sidecar, "w", encoding="utf-8") as f:
        json.dump(side, f, indent=2, ensure_ascii=False); f.write("\n")
    entry = {"event": "intake", "utc": now, "sha256": digest, "size_bytes": size, "kind": args.kind,
             "request_id": args.request_id, "stored_path": os.path.relpath(dest, store), "sidecar": os.path.relpath(sidecar, store)}
    with open(ledger_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    return 0, {"status": "intaken", "sha256": digest, "stored_path": dest, "sidecar": sidecar,
               "has_alpha": facts.get("has_alpha_channel"), "c2pa_chunk_present": c2pa}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("file")
    p.add_argument("--kind", required=True, choices=L.KINDS)
    p.add_argument("--request-id", required=True)
    p.add_argument("--provider"); p.add_argument("--model")
    p.add_argument("--prompt-file"); p.add_argument("--settings-json")
    p.add_argument("--credits", type=float, default=None)
    p.add_argument("--store", default=DEFAULT_STORE)
    p.add_argument("--slug"); p.add_argument("--date", help="YYYYMMDD override (default today UTC)")
    p.add_argument("--generated-utc"); p.add_argument("--downloaded-utc"); p.add_argument("--download-note")
    p.add_argument("--event", action="append", help="extra custody event 'name|utc|detail' (repeatable)")
    p.add_argument("--visible-watermark", choices=["yes", "no", "unknown"], default="unknown")
    p.add_argument("--synthid", choices=["yes", "no", "unknown"], default="unknown")
    p.add_argument("--terms-note")
    p.add_argument("--force-type", action="store_true")
    a = p.parse_args(argv)
    rc, res = intake(a)
    print(json.dumps(res, indent=2))
    return rc


if __name__ == "__main__":
    sys.exit(main())
