# SHOT PLAN — V3 "The 4-Cent Part That Grounded High-Speed Trains"

Voice: Warm Pebble, 50.184s, 1506 frames (0–1505 @30fps). Last word
"components" ends 49.95s; fade-out inside final ~0.5s (assembly fades from
49.684s). No captions/text baked in. 2D flat humans only (@RicksClips3000
style via shared/2d_rig.py); all 3D objects own-built in bpy.

CORE RULE: every phrase gets its own animated scene that LITERALLY ENACTS
what the voice says at that moment. Something must MOVE in a way that shows
the words — no static establishing shot standing in for an action phrase.
Camera movement in every shot. Hard cuts at shot boundaries (marker-bound
cameras). Each shot is its own set, spaced 40 m apart on X so cameras never
see a neighbouring set; each set has its own ground + backdrop.

Frame ranges are cut at word boundaries from voice/words.json (gap frames
belong to the shot whose phrase they follow).

| # | Frames | Time | Words | Animated enactment (what MOVES) |
|---|---|---|---|---|
| S01 | 0–75 | 0.00–2.53s | "A single four-cent plastic washer" | EXTREME CLOSE-UP of ONE tiny washer alone on a pedestal, slowly rotating + gently bobbing. Camera slow push-in. Smallness is the point: washer fills frame only at the end; empty space around it. "four-cent" f23–43. |
| S02 | 76–186 | 2.53–6.23s | "once brought an entire high-speed rail line to a dead stop" | Top-down rail NETWORK map: 3 mini trains moving along tracks, all DECELERATING and grinding to a halt by f180; red halt dots pop up above each stopped train. Camera slow pull-back revealing the whole network. |
| S03 | 187–302 | 6.23–10.10s | "It started when an axle temperature sensor triggered a red alert" | Close-up: wheel SPINNING on its axle, sensor box mounted on the axle blinking. At f279–297 ("red alert") the dashboard RED LAMP flashes (scale pulse + emissive + red point light) — the alert is the event. Camera slow push-in. |
| S04 | 303–411 | 10.10–13.73s | "on an express locomotive moving at 180 miles an hour" | Express locomotive SPEEDING: train races along the track (camera tracks alongside), wheels spinning fast, poles/trees WHIPPING past, trackside speedometer needle climbing to 180 across the shot. |
| S05 | 412–542 | 13.73–18.10s | "Automated safety protocols immediately forced emergency braking" | Brake clamps SLAM onto the wheel disc (f496–508), SPARKS burst out (f508–539, "emergency braking"), wheel rotation DECELERATES to a dead stop by f539, train body lurches, camera shakes. |
| S06 | 543–600 | 18.10–20.03s | "stranding hundreds of passengers" | Carriage interior: 3 2D passengers JOLT forward (lean + slide, luggage sliding) at f543–560, then stand/sit WAITING, stranded — one checks the window, heads turn, idle sway. Outside the window the landscape is still: the train is stopped. |
| S07 | 601–684 | 20.03–22.83s | "Technicians tore apart the wheel assembly" | Two 2D technicians at the wheel assembly: parts FLY OUT into an EXPLODED VIEW (wheels, axle, bearings, sensor, seal, bolts separate along axes f618–680) while the technicians reach/point at the flying parts. |
| S08 | 685–759 | 22.83–25.33s | "expecting shattered bearings or melted metal" | The technicians' EXPECTATION, shown: a bearing with a jagged CRACK spreading across it + a metal blob GLOWING orange and DRIPPING molten drops — each inside a white "thought" ring. One technician points at the cracked bearing. Then cut to reality. |
| S09 | 760–836 | 25.33–27.90s | "Everything was pristine." | The real parts on a bench, GLEAMING: a magnifier sweeps over them (f770–830) finding nothing; sparkle glints FLASH across the parts in sequence. "pristine" f797–815. Camera slow drift. |
| S10 | 837–971 | 27.90–32.40s | "The culprit? A microscopic crack in a cheap nylon seal." | Camera ZOOMS INTO the tiny seal (dramatic push-in); at f870–907 ("microscopic crack") the hairline CRACK is revealed — jagged line scaling in + glowing red highlight pulse. Seal slowly rotating. "seal" f939–953. |
| S11 | 972–1069 | 32.40–35.67s | "It let tiny air pockets slip into the optical sensor" | Cutaway sensor housing: little AIR BUBBLES SLIP through the crack and travel along the channel INTO the optical sensor lens, staggered f980–1060; the sensor lens flickers as each bubble arrives. |
| S12 | 1070–1187 | 35.67–39.60s | "tricking the computer into thinking the axle was overheating" | THE LIE MADE VISIBLE, side by side: the computer gauge needle SPIKES INTO THE RED (f1142–1165, "overheating") with the red lamp flashing — while the axle beside it stays COOL BLUE, gently pulsing cool. Camera push-in on the gauge. |
| S13 | 1188–1286 | 39.60–42.90s | "One ten-cent seal caused millions in delays" | The tiny seal hero-centre on a pedestal; behind it a CLOCK's hands SPIN fast, a delay dial needle sweeps up, and a stack of COINS GROWS coin by coin. "ten-cent" f1198–1217. (Builds AS WRITTEN: "ten-cent" here vs "four-cent" in S01 — flagged to user.) |
| S14 | 1287–1409 | 42.90–47.00s | "proving modern mega-machines aren't brought down by massive engine failures" | A MASSIVE engine block, pistons PUMPING, flywheel SPINNING — running fine. One small red failure spark appears on it and FIZZLES OUT; the engine never falters. The giant is not the problem. |
| S15 | 1410–1505 | 47.00–50.18s | "they're held hostage by the smallest components" | The GIANT train looms over the ONE TINY seal: seal in sharp focus on its pedestal in the foreground, the huge locomotive looming behind it, a thin rope running from the train's nose to the seal — hostage. Camera slow push-in on the seal to the final frame. |

## Test frames (one per shot, for the Colab Eevee check + local stills)
40, 130, 245, 360, 480, 575, 645, 720, 800, 900, 1020, 1130, 1240, 1350, 1460.
Extra action frames: 290 (red alert flash), 525 (braking sparks), 800/815
(pristine glints), 890 (crack reveal), 1155 (gauge spike).

## Sets / cameras
- Set i centred at x = i*40 (i = 0..14), ground plane + backdrop per set.
- All shot cameras sit at +Y of their set centre, looking −Y; 2D humans
  use facing_deg=0 (+Y camera) with add_billboard re-pointed per shot.
- Global day lighting (sun + sky world); red point lights keyframed only
  in S03/S12 for the alert flashes.
- No text anywhere. No baked captions. Fade-in/out applied in ffmpeg
  assembly (fade-out from 49.684s), never in the scene.
