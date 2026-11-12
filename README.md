# blender-train-short

**"The 4-Cent Part That Grounded High-Speed Trains"** — a 50-second
@ExplainerMaan short: one tiny washer brings a high-speed rail line to a
dead stop. 122-word script, Warm Pebble voice (50.184 s), 15 shots,
1,506 frames (1080×1920, 30 fps).

Built in Blender with scripted geometry (bpy): own-built 3D sets, flat 2D
Grease Pencil human characters (@RicksClips3000 style), every phrase
literally enacted in its own animated scene. Rendered with Eevee on a
Colab T4 GPU.

## Layout

- `scripts/` — bpy build scripts (`build_all.py` rebuilds the .blend from
  scratch in ~1 min) + `colab_render.py` (frame renderer) + `build_mix.py`
  (sound mix) + `render_stills.py` (validation stills).
- `scenes/train.blend` — the built scene (904 objects, 23,904 polys,
  15 cameras).
- `assets/` — `words.json` (word timings) + `mix.wav` (voice + music/SFX
  bed, 50.184 s, −14.4 LUFS).
- `notebook/train_colab.ipynb` — the Colab render notebook (15 test
  frames, then 3 shards × 502 frames, then assembly).
- `COLAB_RUN.md` — click-path + the mandatory test-frames stop.
- `BUILD_NOTES.md` — per-shot verdicts, fixes, known limits.
- `SHOT_PLAN.md` — the phrase-by-phrase shot plan.

## Render

See `COLAB_RUN.md`. In short: open the notebook in Colab (T4 GPU),
inspect the 15 Eevee test frames (mandatory stop), run the 3 shard cells,
assemble. Final: `train_blender.mp4`, ~50.18 s, 1080×1920, 30 fps,
h264+AAC, ~−14.4 LUFS.
