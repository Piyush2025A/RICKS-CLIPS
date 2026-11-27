# A14 TECHNIQUES: vertical framing guide for original Remotion storyboards (1080x1920)
Derived from FINDINGS.md (manifest SHA fc6f147a...8e06). Targets are bands from RC30 measurements, medium confidence unless noted.

## 1. Safe-zone overlay spec (draw in every storyboard frame and a Remotion debug layer)
| Zone | Rule | Pixels (1080x1920) | Source |
|---|---|---|---|
| Top UI | no face/eyes/key text | y < 154 (0.08) | director assumption (unverified) |
| Right UI | no face, eyes, hands, key prop | x > 918 (0.85) | director assumption (unverified) |
| Bottom UI | no face/eyes/key prop | y > 1536 (0.80) | director assumption (unverified) |
| Caption band (reserve) | no eyes/mouth/key action | y 1290-1420 (0.672-0.740) | reference caption at 1323-1380 (MEASURED, 44/44) |
| Action-safe rectangle | faces, eyes, hands, critical props | x 54-918, y 154-1290 (and torso/props may continue below the band to 1536) | derived |
Optical centre of the safe width is x ~0.43; reference face median x 0.48 (IQR 0.36-0.51), so centre-third default is fine.
Large heads (CU) may let non-critical head outline cross x 0.85 (5/44 in reference); eyes/mouth may not.
Check: for each frame compute face-box overlap with the zones above; fail if eyes in caption band/UI, or if caption-band spectral-residual saliency share > head-box share (script: resize to 128x228, FFT spectral residual, top 10 % pixels).

## 2. Shot-size mix targets (time-weighted, per 60 s short; reference per-video median, IQR)
MS 38 % (32-45) | WS 21 % (12-28) | CU 14 % (8-18) | INSERT 12 % (5-22) | EWS 10 % (2-15). Every short should contain all five at least once; deviations of EWS or INSERT up to ~40 % existed (RC30-25, -08, -27, -16) for concept-driven beats.
Definitions (head height hh): WS < 0.10; MS 0.10-0.20; CU > 0.20; ECU > 0.45; EWS no figure or < 5 %; INSERT prop/screen with no face.

## 3. Placement parameters (reference medians, IQR)
Eye line y 0.38 (0.32-0.47) -> target 0.30-0.47; head top y 0.30 (0.20-0.37); head height 0.21 (0.16-0.26); face x 0.48 (0.36-0.51), off-centre only with a counterweight (prop, second character, sign). Two-character shots: faces at x ~0.33 and ~0.65, eyes within 0.05 in y.

## 4. Hierarchy devices (include >= 1 per shot, record in storyboard)
frame-within-frame (>=16/30 videos), foreground occluder (>=12/30), leading lines (>=13/30), symmetry (>=10/30), dutch (>=8/30, roll <= 5 deg/s, action beats only), white head disc against dark or complementary background.

## 5. In-shot framing change
Define start and end frames. Default slow push-in +10-35 % scale over 1-3 s, subject x held +/-0.05, pan < 0.1 width; both frames pass section 1. Caption never moves. Cross-shot transition: 6-frame crossfade (A27 calibration). Hand to A13.

## 6. Storyboard template (productions/<id>/storyboard/shotNN.md)
shot_id | beat | duration_s | size (EWS/WS/MS/CU/INSERT) | hh | face_x | eye_y | head_top_y | horizon_y | devices | start_frame / end_frame (x,y,scale) | caption_text | safe-zone check (pass/fail) | camera key (for A13) | foreground dressing (for A05)
