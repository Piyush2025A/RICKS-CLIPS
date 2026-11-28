# TEST6S — six-second ElevenLabs narration integration test (run 2026-11-28, user-approved, D036)
Private development test only (ElevenLabs free tier: non-commercial + attribution). Audio is private, never committed.

| Item | Result |
|---|---|
| Approval | user: one generation, David voice, ≤ 150 credits; narration only (no Scribe / timestamps) |
| Voice / model | "David – Deep Audiobook & Documentary" `cCYjmrGZaI86GUJ7F2Nn` (workspace voice, not a clone of the reference narrator) / `eleven_multilingual_v2`, connector default settings, 1 take |
| Script | `script.txt` (original, 22 words, 136 characters) |
| Cost | estimate 136 credits; run reported 136; account counter 5,011 → 5,147 = **136 credits** (≤ 150 ✅). The counter updated a few minutes after the run |
| Flow / generation | flow `ETjzLif8xvbvnGQOFhD7`, generation `0VKDM13aqH8lzRRS9cSA`, ≈ 5 s runtime, 0 failures, no retries |
| Original file | MP3, 44.1 kHz, mono, ≈ 148 kb/s, 131,271 bytes; SHA-256 `63768ec7be62105c34a6c2c43330e51c70fc8c85d9a946b7b9030afaad16927b`; downloaded twice from the signed URL, both copies identical; stored read-only under `~/ricks-clips-private/audio/raw/`; intaken (`pipeline/assets/intake.py --kind audio`) and re-verified (`verify.py --check`: match) |
| Duration | decoded 7.059 s (= ElevenLabs 7.0589 s); container 7.105 s (MP3 padding) |
| Silence | lead 0.08 s, tail 0.27 s; voiced 0.08–6.79 s; pauses 2.09–2.55 s (0.46 s, comma) and 3.69–4.27 s (0.58 s, sentence end); no pause > 0.6 s; voiced fraction 0.79 |
| Pace | 22 words / 6.71 s voiced span = 3.28 words/s ≈ **197 wpm** (target ≈ 220: below; adjust speed/pauses in production) |
| Quality | sample peak −0.74 dBFS, 0 clipped samples; noise floor (p5 of 10 ms RMS) −91 dBFS; 99 % of spectral energy below 3.5 kHz, 99.9 % below 10.6 kHz (MP3 band-limit ≈ 16 kHz not limiting speech) |
| Loudness raw | −14.3 LUFS, LRA 1.4 LU, TP −0.7 dBTP |
| Loudness normalised | linear loudnorm alone reached only −15.3 LUFS (TP-limited) → tool fixed: gain + 4× oversampled limiter. Final VO WAV (48 kHz mono 24-bit): **−14.2 LUFS, TP −2.8 dBTP**; after AAC 128k mux: **−14.3 LUFS, TP −2.2 dBTP** ✅ |
| Sync timings | `beats.json` (no transcription): sentence 1 0.08–3.69 s (frames 2–89 @24), sentence 2 4.27–6.79 s (frames 102–163 @24), both edges measured from pauses; inner commas without a pause are estimated |
| Readiness clip | private 360×640, 24 fps, 169 frames, 7.059 s: intaken Flow plate + normalised VO; one frame viewed (picture intact, Flow watermark visible) |
