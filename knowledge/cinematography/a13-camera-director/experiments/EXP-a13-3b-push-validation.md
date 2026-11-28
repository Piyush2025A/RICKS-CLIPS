# EXP-a13-3b-push-validation (recorded post hoc, same session; planned and run in one pass)
Question: is the rcpipe-based push magnitude (F-a13-003) correct? Variable: estimator (proxy 320 px sum vs proxy compounded vs native SIFT start-to-end vs native LK chain).
Inputs: 22 non-fast, not-near-candidate push windows (dur >= 20 f, |roll| < 4 deg, <= 2 per video, seed 13) in 16 videos; native 1080x1920 decoded by ffmpeg (select n), scaled to 360x640 gray.
Scripts: data/scripts/push3b.py, push3b_an.py, push3b_sheet.py (venv-analysis, opencv 5.1.0). Output: data/push3b_validation.json (private: cum curves, montages).
Result: see FINDINGS F-a13-100..103. Process note: EXP record written after running, a deviation from the shared rule.
