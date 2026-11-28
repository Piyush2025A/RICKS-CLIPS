"""Regenerates the JSON fixtures (deterministic). Run: .venv-analysis/bin/python -I pipeline/voice/tests/make_fixtures.py"""
import json, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")

def char_align(text, step=0.05, t0=0.2, zero_idx=()):
    st, en = [], []
    for i, _ in enumerate(text):
        a = round(t0 + i * step, 4); st.append(a); en.append(a if i in zero_idx else round(a + step, 4))
    return {"characters": list(text), "character_start_times_seconds": st, "character_end_times_seconds": en}

edge = '  Hello, world! It\'s a well-known 3.5 rate—really. [whispers] Dug a hole <break time="0.5s" /> now ... end.  '
j = char_align(edge, zero_idx=(0,))
with open(os.path.join(D, "char_alignment_edge.json"), "w") as f: json.dump({"alignment": j}, f, indent=1)

script = "It was a cold morning. The kettle sang, then stopped!"
scribe = {"language_code": "eng", "text": "It was a cold morning The kettle sang then stopped",
 "words": [
  {"text": "It", "start": 0.10, "end": 0.20, "type": "word", "logprob": -0.01},
  {"text": " ", "start": 0.20, "end": 0.22, "type": "spacing"},
  {"text": "was", "start": 0.22, "end": 0.40, "type": "word", "logprob": -0.02},
  {"text": " ", "start": 0.40, "end": 0.42, "type": "spacing"},
  {"text": "a", "start": 0.42, "end": 0.48, "type": "word", "logprob": -0.1},
  {"text": "(sniff)", "start": 0.50, "end": 0.60, "type": "audio_event"},
  {"text": "cold", "start": 0.62, "end": 0.95, "type": "word", "logprob": -0.05},
  {"text": "mourning", "start": 0.97, "end": 1.40, "type": "word", "logprob": -1.2},
  {"text": "The", "start": 1.80, "end": 1.95, "type": "word", "logprob": -0.01},
  {"text": "kettle", "start": 1.97, "end": 2.30, "type": "word", "logprob": -0.03},
  {"text": "sang", "start": 2.32, "end": 2.70, "type": "word", "logprob": -0.02},
  {"text": "then", "start": 2.95, "end": 3.15, "type": "word", "logprob": -0.04},
  {"text": "really", "start": 3.16, "end": 3.40, "type": "word", "logprob": -0.9},
  {"text": "stopped", "start": 3.42, "end": 3.90, "type": "word", "logprob": -0.02}]}
with open(os.path.join(D, "scribe_sample.json"), "w") as f: json.dump(scribe, f, indent=1)
with open(os.path.join(D, "script_sample.txt"), "w") as f: f.write(script)

manifest = {"schema_version": "1.0", "production_id": "TEST6S", "script_version": "v0",
 "voice": {"voice_id": "SYNTHETIC", "name": "Synthetic test", "origin": "library"},
 "model": "eleven_multilingual_v2", "settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.0, "speed": 1.0, "use_speaker_boost": True, "output_format": "mp3_44100_128", "seed": None},
 "text": {"submitted": "Hello there.", "characters": 12, "words": 2, "sha256": "0" * 64},
 "audio": {"file": "narration_raw.mp3", "sha256": "a" * 64, "codec": "mp3", "sample_rate_hz": 44100, "channels": 1, "duration_s": 1.2,
           "loudness": {"integrated_lufs": -20.1, "lra_lu": 2.0, "true_peak_dbtp": -3.0, "stage": "raw"}},
 "timing": {"words_file": "words.json", "source": "scribe", "timing_error_median_ms": None},
 "provenance": {"provider": "elevenlabs", "generated_utc": "2026-11-28T00:00:00Z", "flow_id": None,
                "credits": {"estimated": 120, "actual": None, "scribe_actual": None}, "take": 1, "approval_ref": "SYNTHETIC", "intake_ref": None},
 "licence": {"tier": "free", "commercial_use": "not_allowed", "attribution_required": True}}
with open(os.path.join(D, "manifest_sample.json"), "w") as f: json.dump(manifest, f, indent=1)
