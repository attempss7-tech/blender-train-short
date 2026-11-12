# Running the Blender train short on Colab

The project is built and validated locally. The Colab GPU does the Eevee
render only. The notebook is `notebook/train_colab.ipynb`.

## Click-path

1. Open https://colab.research.google.com.
2. **File > Open notebook > GitHub tab** — paste
   `attempss7-tech/blender-train-short`, open
   `notebook/train_colab.ipynb`. (Or upload the `.ipynb` file
   directly: File > Upload notebook.)
3. **Runtime > Change runtime type > T4 GPU > Save.** The notebook fails
   fast with a clear message if no GPU is attached — do not render on CPU
   (Eevee falls back to software rendering, far too slow).
4. Run the cells **top to bottom, in order**. Do not use "Run all" blindly:
   you must STOP after the Eevee test-frames cell and inspect the 15 frames
   before running any shard cell.
5. The first cell mounts Google Drive — click through the auth prompt.
   Frames go to `MyDrive/train_blender/frames/`, test frames to
   `MyDrive/train_blender/test_frames/`, the final video to
   `MyDrive/train_blender/final/`.

## The mandatory stop: Eevee test frames

**EGL fix (proven 2026-11-12 on the chicken short, baked into the install
cell):** Colab ships the NVIDIA EGL library
(`/usr/lib64-nvidia/libEGL_nvidia.so.0`) but no vendor file for it, so
Blender's EGL context fails (`EGL_BAD_MATCH`) and Eevee silently falls
back to CPU rendering at ~5 min/frame. The install cell writes
`/usr/share/glvnd/egl_vendor.d/10_nvidia.json` before any render; with
it, Eevee uses the T4 at ~1.5–3.5 s/frame (measured on the chicken
short: 13 test frames in 45 s). The vendor file lives only in the live
session — after a session drop, re-running the install cell re-creates
it. If a render ever runs at minutes-per-frame, the vendor file is
missing: stop, re-run the install cell, re-run the render.

Eevee was never validated locally (no GPU there). The test-frames cell
renders 15 frames, one per shot, and displays them inline. Check every one:

- **2D characters upright, flat, facing camera** — f575 (passengers),
  f645 (technicians), f800 (technician), f1130 (technician). No black
  shells, no missing limbs, faces visible.
- **f130 (S02 rail map): the top of the frame must be LIGHT BLUE**
  (the backdrop). A black band here means an Eevee lighting problem —
  stop and report it. (Workbench stills show this band black because of
  a Workbench studio-lighting artefact; in Eevee the sun faces that
  backdrop, so it must render light blue.)
- **Gauge needle + red zone visible** (f1130 needle at rest, f1240 dial
  needle sweeping) and **clock hands visible** (f1240).
- **Red alert lamp bright red** (use the re-render cell for f290),
  **sparks at the brake pads** (f525), **bubbles travelling to the sensor**
  (f1020), **crack glowing red** (f900).
- **Washer alone on its pedestal** (f40); **exploded wheel parts spread**
  (use the re-render cell for f670); no black/missing objects anywhere.

**If anything looks wrong:** stop, note the frame number + what you see,
and do NOT run the shards — report back so the build can be fixed.
**If all 15 look right:** skip the re-render cell and run the 3 shard cells.

## Shards (frames 0–1505 in 3 × 502)

- Shard 1: 0–501 · Shard 2: 502–1003 · Shard 3: 1004–1505.
- Each shard renders in 6 batches of 84 frames and copies each batch to
  Drive immediately. Per-frame timings print as it goes; each shard ends
  with a count check against Drive.
- Expected speed: ~1.5–3.5 s/frame on a T4 (chicken short: 4 shards
  ~14.5 min each) — roughly 15–30 min per shard; re-estimate from the
  test-frames timings.

## If a session drops mid-shard

Colab sessions reset/disconnect (12 h cap, ~90 min idle, GPU preemption).
Nothing is lost beyond the in-progress batch (~5 min of rendering):

1. Reopen the notebook (same file, same account).
2. Re-run the setup cells in order: mount Drive + GPU check, install
   Blender + libs, clone repo (or pull).
3. Re-run the interrupted shard cell. It first syncs that shard's finished
   frames from Drive back to local disk, then renders only the missing
   frames, batch by batch.
4. Continue with the remaining shard cells, then assembly.

Do NOT re-run the test-frames cell unless you changed something — the test
frames are already on Drive.

## Assembly + verification

The assembly cell checks all 1,506 frames are on Drive (and stops, listing
any missing frames, if not), then runs ffmpeg: PNG sequence → h264 mp4
(crf 17), fade-in 0.5 s + fade-out 0.5 s from 49.684 s (inside the voice —
no dead silence at the end; the last word ends 49.95 s), muxed with the
sound mix (`assets/mix.wav`, already −14.4 LUFS). The verification cell
prints ffprobe details + an ebur128 loudness reading.

Expected final: `train_blender.mp4`, ~50.18 s, 1080x1920, 30 fps,
h264 + AAC, ~−14.4 LUFS.

## If the committed .blend fails

The last markdown cell has the rebuild command: it re-runs
`scripts/build_all.py` in Colab (~1 min) to regenerate
`scenes/train.blend` from the scripts, then re-run the
test-frames cell.

## Known limits (from BUILD_NOTES.md)

- S02's rail map is upside-down (Track-To camera roll) — cosmetic, the
  network, trains, stations, and halt dots all read.
- S05's sparks are small dots in Workbench; they are emissive and should
  pop more in Eevee — confirm on the test frame f525.
- S11's bubbles are modest in size (r=0.22), emissive pale blue —
  confirm on the test frame f1020.
- S07: at full explosion the far wheel is hidden behind the near wheel
  (aligned along the view axis); the spread of housings/bolts/seal/sensor
  sells the explosion regardless.
- No captions/text are baked in — captions are a separate overlay step.
- The script says "four-cent" at the top but "ten-cent" in the closing
  line — built as written, pending the user's answer to the flagged
  inconsistency.
