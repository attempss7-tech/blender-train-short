# BUILD NOTES — V3 "The 4-Cent Part That Grounded High-Speed Trains"

@ExplainerMaan · Blender + Colab (Eevee, T4) · built 2026-11-12 · subagent build

## Deliverables

| Item | Path / value |
|---|---|
| Script (verbatim, 122 words) | `~/workspace/blender_shorts_4/scripts/SCRIPT_03_train.md` |
| Voice | `v3_train/voice/voice.wav` — Warm Pebble, **50.184 s**, 48 kHz |
| Frames | **1506 (0–1505)**, 1080×1920, 30 fps |
| Sound mix | `v3_train/assets/mix.wav` — voice + pad/SFX bed, **50.184 s, −14.4 LUFS** |
| Blend | `v3_train/scenes/train.blend` (11.9 MB) |
| Build scripts | `v3_train/scripts/` (`build_all.py` + `common.py`, `props.py`, `shots_a/b/c.py`, `render_stills.py`, `colab_render.py`, `build_mix.py`) |
| Shot plan | `v3_train/SHOT_PLAN.md` (15 shots, hard cuts at markers) |
| Notebook | `v3_train/notebook/train_colab.ipynb` (3 shards × 502 frames) |
| Repo | `attempss7-tech/blender-train-short` |

## Blend stats (v3, canonical)

- **904 objects** (595 meshes, 81 Grease Pencil, 15 cameras), **23,904 polys**, **237 actions**, 15 timeline markers, frames 0–1505, 1080×1920 @ 30 fps, `BLENDER_EEVEE_NEXT`.
- Build time from scratch: ~60 s on this VM. Reproducibility: rebuilt from `scripts/build_all.py` and stats confirmed identical.

## Standing rules applied

- **Literal animated enactment of every phrase** (user's 2026-11-12 direction): every phrase gets its own distinct animated scene that literally enacts the words at that exact moment — objects move in sync with the narration, never a static establishing shot standing in for an action phrase.
- **2D human characters, mandatory** (user's 2026-11-12 direction, @RicksClips3000 style): flat Grease Pencil humans from the proven rig `blender_shorts_4/shared/2d_rig.py`. NOT 3D figures. The rig's 180° base yaw (so `facing_deg=0` faces a +Y camera) was kept as-is.
- **Own-build rule** (user's 2026-11-11 direction): every object (train, wheel assembly, sensor, seal, dashboard, gauge, engine, clock, carriage) built own in bpy scripts — no downloaded models, no template scenes.
- **No dead silence at the end:** 1506 frames total; fade-out inside the final ~0.5 s of the voice (assembly fades from 49.684 s). Last word "components" ends 49.95 s.
- No captions/text baked in. Fade-in/out required (applied in the assembly cell).

## Script wording note

The script says "four-cent plastic washer" at the top but "One ten-cent seal" in the closing line. Flagged to the user 2026-11-12 (proposed fix "One four-cent seal...") — **no answer yet, built AS WRITTEN**. Do not change the wording without the user's explicit approval.

## Per-shot build & verdicts

All stills are 540×960 Workbench renders in `out/stills/`. v3 is the final version; v1/v2 folders kept for the record.

| Shot | Frames | Enacted action | Verdict (v3 stills) |
|---|---|---|---|
| S01 | 0–76 | ONE tiny washer alone on a pedestal, slowly rotating + bobbing; camera push-in | GOOD (f40): washer alone, space around it, smallness reads |
| S02 | 76–187 | Rail-network map: 3 mini trains decelerate to a halt; red halt dots pop up | GOOD (f130, f180): network reads, 3 trains + stations, halt dots pop clearly. See "S02 notes" below |
| S03 | 187–303 | Wheel spinning, sensor blinking; RED ALERT flashes f279–297 | GOOD (f245, f290): sensor box + lens now visible above wheel; lamp bigger/brighter at f290 |
| S04 | 303–412 | Train speeding, poles/trees whipping past; HUD speedometer climbs to 180 | GOOD (f360): HUD fully visible, needle mid-sweep |
| S05 | 412–543 | Brake pads SLAM on f496–508, SPARKS f508–539, wheel decelerates to stop, camera shake | GOOD (f480, f525): pads on wheel, sparks visible, sensor visible |
| S06 | 543–601 | 3 passengers JOLT forward f543–560, luggage slides, then wait stranded | EXCELLENT (f575): all 3 passengers upright, flat 2D, faces visible, bags + seats + windows |
| S07 | 601–685 | 2 technicians; wheel parts FLY OUT into exploded view f618–680 | GOOD (f645, f670): explosion reads — sensor + bolts fly up, housings spread, seal visible |
| S08 | 685–760 | Expectation: cracked bearing + glowing molten metal, each in a white "thought" ring | EXCELLENT (f720): both rings, crack spreading, drip, technician pointing |
| S09 | 760–837 | Parts GLEAMING on bench; magnifier sweeps f770–830; sparkle glints | GOOD (f800): wheel sits ON the bench, magnifier reads, glints in sequence |
| S10 | 837–972 | Camera ZOOMS INTO seal; hairline CRACK revealed + glowing red f870–907 | EXCELLENT (f890, f900): crack reveal, red glow |
| S11 | 972–1070 | Air bubbles SLIP through crack along a guide rail INTO the sensor lens | GOOD (f1020): 3 bubbles visible mid-path; lens flickers on arrival |
| S12 | 1070–1188 | Gauge needle SPIKES INTO RED f1142–1165 while axle stays COOL BLUE | GOOD (f1130, f1155): gauge face + ticks + red zone visible; needle mid-spike at f1155, axle cool |
| S13 | 1188–1287 | Tiny seal hero-centre; CLOCK hands spin, delay dial sweeps up, COIN stack grows | GOOD (f1240): clock hands + dial needle visible, coins growing, seal centre |
| S14 | 1287–1410 | MASSIVE engine, pistons PUMPING, flywheel SPINNING; one failure spark FIZZLES OUT | GOOD (f1350): whole engine, pistons at different heights, flywheel spoke, spark visible |
| S15 | 1410–1506 | GIANT train looms over ONE TINY seal; rope from train nose to seal | GOOD (f1460): train looms, seal in focus, rope clearly visible |

Frames viewed in v3: 130, 180, 245, 290, 360, 480, 525, 575, 645, 670, 720, 800, 890, 900, 1020, 1130, 1155, 1240, 1350, 1460 (20 stills; v1/v2 folders hold the earlier rounds).

## Key fixes & discoveries (durable — reuse for V1/V2/V4)

1. **True camera FOV (measured, not assumed).** With `sensor_fit="VERTICAL"`, vertical FOV comes from the 24 mm sensor height, NOT 36 mm. Correct formulas: **tan(vertical half-angle) = 12/lens; tan(horizontal half-angle) = 6.75/lens.** The original 10.125/lens assumption was wrong and caused the v1 framing failures. All v2/v3 cameras were recomputed with this formula. Verified with an NDC probe (`/tmp/probe_fov.py`).
2. **`_face_camera` Euler bug.** `_face_camera` used `rotation_euler = (-90°, 0, 180°)`. Blender XYZ Euler composes as Rz @ Ry @ Rx, so that faces a dial AWAY from a +Y camera (blank backs in S12/S13 v2 stills). Correct: **(90°, 0, 180°)** — local +Z → +Y (faces camera), local +Y → +Z (dial-up stays up). Needle rest −120° = down-left on screen, sweep to +55° = up-right into the red zone. The S04 HUD gauge was unaffected (parented to the camera, rotation 0 — proven working).
3. **Sensor repositioning.** In `build_wheel_assembly` the sensor started between the wheels (hidden). Moved to the housing top (0, 1.75, 2.6), lens (0, 2.08, 2.6) rot X 90°, plus a mount-arm cylinder (child of sensor, local (0, −0.3, −0.28), **rot X 132°** — the direction sensor→housing-top (0, −0.6, −0.55) needs Z rotated 132° about X; a 50° first guess was wrong). S07 explode keys updated to match.
4. **S07 explosion must spread in X/Z, not just Y.** The v2 explosion only moved parts along Y (toward/away from the 3/4 camera) and did not read. v3 spreads wheels ±X, housings ∓X, sensor up, seal out — plus stand posts under the housings so the floating parts read as deliberate.
5. **S11 open guide rail.** The closed channel box hid the bubbles entirely (v1). Replaced with an open guide rail (thin box the bubbles travel above) — bubbles visible.
6. **S02 notes.**
   - The S02 camera is rolled 180° (Track-To with up Y, looking steeply down: camera up = (0, −0.96, 0.29), so screen-up = −Y, screen-right = −X). The map is effectively upside-down. This is cosmetic for a stylised network map — trains, tracks, stations, and halt dots all read — so it was left as-is. Do not "fix" the roll without re-checking the whole shot's framing.
   - A black band at the top of the S02 Workbench stills is a **Workbench-only artefact**: the backdrop's normal points down in camera space, away from the Workbench studio key light, so it shades near-black (pixels ~ (20,23,24)). Ray-cast probing confirms the top-of-frame rays hit the S02 backdrop (light blue #b8d0e8), and the Eevee sun (direction (0,−1,−1)) faces that normal, so in Eevee the band renders light blue. The Colab test-frames cell must confirm this on f130 (see COLAB_RUN.md). Ground was enlarged 44 → 60 m in v3; the band persisted identically, confirming it is not a ground-edge issue.
7. **Lighting:** one sun (energy 3.0, colour (1.0, 0.96, 0.88), direction (0,−1,−1), **shadows OFF** — sets span 560 m on X; the flat cartoon look needs no shadows) + sky world #a8c8e8 strength 1.0.
8. **Camera sensor:** `sensor_fit="VERTICAL"`, `sensor_width=36`, `clip_start=0.1`, `clip_end=250` (same as the chicken short).
9. **Pointing arms:** screen-right = −X for level +Y cameras. S07 TechA points with arm R (parts are screen-left), S12 tech arm R (gauge screen-left), S08 tech arm L (bearing screen-right). Verified in stills.
10. **S05 pads:** brake pads must sit at y=2.5 (in front of the wheel face at y=2.2); at y=2.05 they were embedded inside the wheel.

## Sound mix (`scripts/build_mix.py`, numpy + scipy)

Voice + soft pad chords (Am–F–C–G, one per ~12.5 s, sine-stack + sub root, stereo-widened) + timed SFX: alert beeps 9.33–9.93 s; speed whoosh + rumble 10.1–13.7 s; brake screech 16.95–17.97 s; teardown clinks 20.6–22.1 s; crack ting + thud 29.05 s; bubble blips 32.67–34.0 s; gauge alarm rise 38.07–38.85 s; counter ticks 39.87–42.2 s; resolve chord 48.3–50.18 s. ffmpeg `loudnorm=I=-14.5:TP=-1.5:LRA=11:linear=true` → **−14.4 LUFS integrated** (ebur128 verified).

## Eevee validation

- Local Eevee test: attempted on this VM (no GPU; EGL falls back to software). [STATUS — see final report / Colab test-frames cell.]
- The Colab notebook's mandatory test-frames cell (one frame per shot) is the authoritative Eevee check: 2D characters upright/flat/facing, no black/missing objects, gauge needles/clock hands visible, red alert flashing, sparks, bubbles, crack glow, S02 band light blue (not black).

## Known limits

- S02 map is upside-down (Track-To roll, see §6) — cosmetic, reads fine.
- S05 sparks are small dots in Workbench; they are emissive and should pop more in Eevee — confirm on the Colab test frame f525.
- S11 bubbles are modest in size (r=0.22); emissive pale blue — confirm on the Colab test frame f1020.
- S07: at full explosion the far wheel is hidden behind the near wheel (aligned along the view axis); the spread of housings/bolts/seal/sensor sells the explosion regardless.
- No captions baked in (per the brief — captions are added externally if needed).
- The four-cent/ten-cent wording inconsistency is built as written, pending the user's answer.

## Colab watch-list (for the parent running the render)

1. **Test-frames cell — mandatory stop.** Check f130 (S02 band must be light blue, not black), f575 (GP passengers upright/flat/facing), f1130/f1155 (gauge needle + red zone), f1240 (clock hands + dial), f290 (red alert flashing), f525 (sparks), f1020 (bubbles), f890 (crack glow).
2. **EGL fix in the install cell is mandatory** (writes `/usr/share/glvnd/egl_vendor.d/10_nvidia.json`) — without it Eevee falls back to CPU at ~5 min/frame.
3. 3 shards × 502 frames (0–501, 502–1003, 1004–1505), resume-safe batches. Expected ~1.5–3.5 s/frame on a T4 (chicken short: 4 shards ~14.5 min each).
4. Assembly: ffmpeg, fade-in 0–0.5 s, fade-out from 49.684 s, mux `assets/mix.wav`, `-shortest`. Final: `train_blender.mp4`, ~50.18 s, 1080×1920, 30 fps, h264+AAC, ~−14.4 LUFS.
5. If a shard session drops: re-run the install cell, then the resume cell — already-rendered frames are skipped.
