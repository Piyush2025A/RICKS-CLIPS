"""Stage 3: frame-count reconciliation across ffprobe nb_frames / packets / -count_frames / pts list / decoder."""


def reconcile(probe, decoded):
    v = probe["video"]
    counts = {"nb_frames": v["nb_frames"], "nb_read_packets": v["nb_read_packets"],
              "nb_read_frames": v["nb_read_frames"], "pts_list": len(probe["pts_time"]), "decoded": decoded}
    container_src = "nb_frames" if v["nb_frames"] is not None else "nb_read_packets"
    container = v["nb_frames"] if v["nb_frames"] is not None else v["nb_read_packets"]
    vals = {k: x for k, x in counts.items() if x is not None}
    mism = {k: x for k, x in vals.items() if x != decoded}
    notes = []
    if probe["pts_missing"]:
        notes.append(f"{probe['pts_missing']} frames without pts_time")
    t = probe["timing"]
    if t.get("vfr"):
        notes.append(f"VFR: {t['pts_irregular_deltas']} irregular pts deltas; rates {t['distinct_rates_hz']}")
    if t.get("nonmonotonic"):
        notes.append(f"{t['nonmonotonic']} non-monotonic pts deltas (possible duplicate/out-of-order timestamps)")
    if mism:
        notes.append("MISMATCH vs decoded: " + ", ".join(f"{k}={x}" for k, x in mism.items())
                     + ". Possible causes: edit list / negative-pts frames dropped, duplicated packets, "
                       "decoder flush frames, truncated stream. Investigate before using; never pick one silently.")
    return {"counts": counts, "frames_container": container, "frames_container_source": container_src,
            "frames_decoded": decoded, "status": "ok" if not mism else "mismatch", "mismatches": mism,
            "notes": notes}
