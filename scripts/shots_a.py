# shots_a.py — shots 1-5 (frames 0-542) of the V3 train short.
import math

import bpy

import common as cm
import props as pr


def _face_camera(obj):
    """Rotate a dial/clock root (face = local XY, normal +Z) to face a +Y
    camera, dial-up staying world-up. Blender XYZ Euler composes as
    Rz @ Ry @ Rx, so (90, 0, 180) gives local +Z -> +Y, +Y -> +Z."""
    obj.rotation_euler = (math.radians(90), 0, math.radians(180))


# ------------------------------------------------------------------ S01
def build_s01(ctx):
    """f0-75 'A single four-cent plastic washer' — ONE tiny washer alone,
    slowly rotating + bobbing on a pedestal; camera push-in."""
    cx = cm.set_x(1)
    cm.make_set(1, ground_hex="#cfd4d8", backdrop_hex="#b8d0e8")
    m_ped = cm.flat_mat("M_Pedestal_S01", "#8a94a0", 0.6)
    cm.add_cylinder("S01_Pedestal", 0.7, 1.0, m_ped, loc=(cx, 0, 0.5))
    cm.add_cylinder("S01_PedestalTop", 0.85, 0.15, m_ped, loc=(cx, 0, 1.05))
    seal = pr.build_seal_hero("S01_Washer", (cx, 0, 1.5), scale=0.75,
                              with_crack=False)
    # slow rotation + gentle bob
    cm.rot_key(seal["root"], 0, (0, 0, 0))
    cm.rot_key(seal["root"], 75, (0, 0, math.radians(55)))
    cm.set_linear_range(seal["root"], 0, 75)
    cm.loc_key(seal["root"], 0, (cx, 0, 1.5))
    cm.loc_key(seal["root"], 38, (cx, 0, 1.62))
    cm.loc_key(seal["root"], 75, (cx, 0, 1.5))
    cam, _ = cm.build_shot_camera(
        "Cam_S01",
        [(0, (cx, 11.5, 4.0), 32), (75, (cx, 9.0, 3.3), 32)],
        [(0, (cx, 0, 1.5)), (75, (cx, 0, 1.5))], 0, 75)
    return {"cameras": [(0, cam)]}


# ------------------------------------------------------------------ S02
def build_s02(ctx):
    """f76-186 'once brought an entire high-speed rail line to a dead
    stop' — top-down rail network map; 3 mini trains decelerate and grind
    to a halt; red halt dots pop up above each stopped train."""
    cx = cm.set_x(2)
    ground, _ = cm.make_set(2, ground_hex="#d8e0c8",
                            backdrop_hex="#b8d0e8", ground_size=60.0)
    ground.location = (cx, 0, 0.03)  # lift: avoids z-fighting with the
    # neighbouring sets' ground planes where the wider map overlaps them
    m_track = cm.flat_mat("M_MapTrack_S02", "#5a5f6a", 0.9)
    m_station = cm.flat_mat("M_MapStation_S02", "#c86a2a", 0.8)
    # track strips (flat, on the ground)
    cm.add_box("S02_TrackH1", (22, 0.55, 0.08), m_track, loc=(cx, 2.5, 0.07))
    cm.add_box("S02_TrackH2", (22, 0.55, 0.08), m_track, loc=(cx, -2.5, 0.07))
    cm.add_box("S02_TrackV", (0.55, 14, 0.08), m_track, loc=(cx + 5, 0, 0.07))
    # stations
    for sx, sy in ((-7, 2.5), (2, -2.5), (5, 5.0)):
        cm.add_box("S02_Station_%+d_%+d" % (int(sx), int(sy)),
                   (1.4, 1.4, 0.3), m_station, loc=(cx + sx, sy, 0.18))
    # three mini trains, decelerating to a halt (BEZIER keys: fast, then
    # ever-smaller steps = grinding to a stop)
    trains = []
    specs = [
        # (name, start pos, end pos, yaw, keys: (frame, fraction))
        ("S02_TrainA", (cx - 8, 2.5, 0.1), (cx - 2, 2.5, 0.1), 0),
        ("S02_TrainB", (cx + 8, -2.5, 0.1), (cx + 2, -2.5, 0.1), 180),
        ("S02_TrainC", (cx + 5, 6, 0.1), (cx + 5, 1.5, 0.1), -90),
    ]
    stops = [(76, 0.0), (105, 0.45), (130, 0.72), (155, 0.90), (180, 1.0)]
    for name, start, end, yaw in specs:
        t = pr.build_train(name, start, cars=1, scale=0.35)
        t["root"].rotation_euler = (0, 0, math.radians(yaw))
        for f, frac in stops:
            pos = tuple(start[i] + (end[i] - start[i]) * frac
                        for i in range(3))
            cm.loc_key(t["root"], f, pos)
        # wheels spin fast, then stop with the train
        for w in t["wheels"]:
            cm.rot_key(w, 76, (0, 0, 0))
            cm.rot_key(w, 130, (0, math.radians(360 * 5), 0))
            cm.rot_key(w, 180, (0, math.radians(360 * 6.2), 0))
        trains.append((name, end))
    # red halt dots pop up above each stopped train
    m_halt = cm.emissive_mat("M_HaltDot_S02", "#ff2010", 2.0)
    for name, end in trains:
        dot = cm.add_sphere(name + "_halt", 0.8, m_halt,
                            loc=(end[0], end[1], 2.5))
        cm.scale_at(dot, 168, cm.HIDDEN)
        cm.scale_at(dot, 176, 1.3)
        cm.scale_at(dot, 186, 1.0)
    cam, _ = cm.build_shot_camera(
        "Cam_S02",
        [(76, (cx, 14, 46), 28), (186, (cx, 16, 52), 28)],
        [(76, (cx, 0, 0)), (186, (cx, 0, 0))], 76, 186)
    return {"cameras": [(76, cam)]}


# ------------------------------------------------------------------ S03
def build_s03(ctx):
    """f187-302 'axle temperature sensor triggered a red alert' — wheel
    spinning, sensor blinking; at f279-297 the RED ALERT flashes on the
    dashboard (lamp pulse + emissive + red point light)."""
    cx = cm.set_x(3)
    cm.make_set(3, ground_hex="#b8bec4", backdrop_hex="#a8c0d8")
    asm = pr.build_wheel_assembly("S03_Asm", (cx, 0, 0), scale=1.1)
    dash = pr.build_dashboard("S03_Dash", (cx + 2.6, 0.9, 1.05))
    red_light = cm.add_point_light("S03_RedLight", (cx + 2.6, 2.2, 1.8),
                                   "#ff2010", 0)
    # wheel spins fast the whole shot (train still moving)
    cm.rot_key(asm["axle_spin"], 187, (0, 0, 0))
    cm.rot_key(asm["axle_spin"], 302, (0, math.radians(360 * 3), 0))
    cm.set_linear_range(asm["axle_spin"], 187, 302)
    # sensor lens blinks gently until the alert
    lens_mat = asm["sensor_lens_mat"]
    for f, v in [(187, 0.6), (210, 2.2), (233, 0.6), (256, 2.2),
                 (278, 0.6)]:
        cm.key_emission(lens_mat, f, v)
    # RED ALERT flash f279-297 (words "red alert" f279-297)
    lamp_mat = dash["lamp_mat"]
    for f, v in [(278, 0.0), (281, 4.0), (286, 0.5), (290, 4.0),
                 (294, 0.5), (297, 4.0), (302, 2.5)]:
        cm.key_emission(lamp_mat, f, v)
    for f, s in [(278, 1.0), (281, 1.3), (286, 1.0), (290, 1.3),
                 (294, 1.0), (297, 1.3), (302, 1.15)]:
        cm.scale_at(dash["lamp"], f, s)
    for f, e in [(278, 0), (281, 80), (286, 5), (290, 80), (294, 5),
                 (297, 80), (302, 40)]:
        cm.key_light_energy(red_light, f, e)
    cm.key_emission(dash["screen_mat"], 187, 0.8)
    cm.key_emission(dash["screen_mat"], 281, 2.0)
    cm.key_emission(dash["screen_mat"], 302, 1.6)
    cam, _ = cm.build_shot_camera(
        "Cam_S03",
        [(187, (cx + 1.6, 12.5, 3.4), 24), (302, (cx + 1.6, 11.5, 3.1), 24)],
        [(187, (cx + 1.6, 0.3, 1.9)), (302, (cx + 1.6, 0.3, 1.9))],
        187, 302)
    return {"cameras": [(187, cam)]}


# ------------------------------------------------------------------ S04
def build_s04(ctx):
    """f303-411 'express locomotive moving at 180 miles an hour' — train
    races along the track, camera tracking alongside; poles/trees whip
    past; HUD speedometer needle climbs to 180."""
    cx = cm.set_x(4)
    ground, _ = cm.make_set(4, ground_hex="#8ab868",
                            backdrop_hex="#a8c8e8", ground_size=60.0)
    ground.location = (cx, 0, 0.05)  # lift: avoids z-fighting where the
    # wider ground overlaps the neighbouring sets' planes
    pr.build_track("S04_Track", (cx + 5, 0, 0), length=60.0)
    # background poles + trees (camera motion makes them whip past).
    # Kept clear of x < cx-25: a pole at cx-32 intruded into the S03
    # frame's left edge in the first stills pass.
    for i, px in enumerate(range(-25, 36, 7)):
        pr.build_pole("S04_Pole%d" % i, (cx + px, -4.5, 0))
    for i, (tx, tz) in enumerate(((-20, -7), (-12, -8), (2, -7), (16, -8),
                                  (28, -7))):
        pr.build_tree("S04_Tree%d" % i, (cx + tx, tz, 0), scale=1.4)
    train = pr.build_train("S04_Train", (cx - 8, 0, 0.35), cars=2)
    # train races +X; wheels spin fast
    cm.loc_key(train["root"], 303, (cx - 8, 0, 0.35))
    cm.loc_key(train["root"], 411, (cx + 8, 0, 0.35))
    cm.set_linear_range(train["root"], 303, 411)
    for w in train["wheels"]:
        cm.rot_key(w, 303, (0, 0, 0))
        cm.rot_key(w, 411, (0, math.radians(360 * 7), 0))
        cm.set_linear_range(w, 303, 411)
    # camera tracks the train (same +X motion, slightly ahead of it)
    cam, _ = cm.build_shot_camera(
        "Cam_S04",
        [(303, (cx - 6, 11.5, 3.6), 35), (411, (cx + 10, 11.5, 3.6), 35)],
        [(303, (cx - 6, 0, 2.2)), (411, (cx + 10, 0, 2.2))], 303, 411)
    # HUD speedometer, parented to the camera (bottom-right of frame):
    # needle climbs from 0 to 180 across the shot. True half-FOV at 7 m,
    # lens 35: half-width 1.35 m, half-height 2.4 m — the dial must sit
    # inside that box.
    gauge = pr.build_gauge("S04_Speedo", (0, 0, 0), scale=0.55,
                           parent=cam)
    gauge["root"].location = (0.45, -1.6, -7.0)
    cm.rot_key(gauge["needle_pivot"], 303, (0, 0, math.radians(-120)))
    cm.rot_key(gauge["needle_pivot"], 411, (0, 0, math.radians(55)))
    cm.set_linear_range(gauge["needle_pivot"], 303, 411)
    return {"cameras": [(303, cam)]}


# ------------------------------------------------------------------ S05
def build_s05(ctx):
    """f412-542 'automated safety protocols immediately forced emergency
    braking' — brake pads SLAM onto the wheel (f496-508), SPARKS burst
    (f508-539), wheel decelerates to a dead stop, train lurches, camera
    shakes."""
    cx = cm.set_x(5)
    cm.make_set(5, ground_hex="#b8bec4", backdrop_hex="#a8c0d8")
    asm = pr.build_wheel_assembly("S05_Asm", (cx, 0, 0), scale=1.3)
    m_pad = cm.flat_mat("M_BrakePad_S05", "#c8a020", 0.6)
    # brake pads hover beside the near wheel, then SLAM onto its rim.
    # Pads sit at y=2.5, IN FRONT of the wheel's front face (y=2.2) —
    # at y=2.05 they were embedded inside the wheel and invisible.
    pad_l = cm.add_box("S05_PadL", (0.5, 0.3, 1.0), m_pad,
                       loc=(cx - 2.6, 2.5, 2.1))
    pad_r = cm.add_box("S05_PadR", (0.5, 0.3, 1.0), m_pad,
                       loc=(cx + 2.6, 2.5, 2.1))
    for pad, side in ((pad_l, -1), (pad_r, 1)):
        cm.loc_key(pad, 412, (cx + side * 2.6, 2.5, 2.1))
        cm.loc_key(pad, 496, (cx + side * 2.6, 2.5, 2.1))
        cm.loc_key(pad, 508, (cx + side * 1.45, 2.5, 2.1))
        cm.loc_key(pad, 542, (cx + side * 1.45, 2.5, 2.1))
    # wheel spin: fast, then decelerating to a dead stop by f539
    spin_keys = [(412, 0.0), (460, 2.5), (496, 3.6), (520, 4.0),
                 (539, 4.08), (542, 4.08)]
    for f, rev in spin_keys:
        cm.rot_key(asm["axle_spin"], f, (0, math.radians(360 * rev), 0))
    # train lurch at brake bite
    cm.loc_key(asm["root"], 412, (cx, 0, 0))
    cm.loc_key(asm["root"], 508, (cx, 0, 0))
    cm.loc_key(asm["root"], 516, (cx + 0.3, 0, 0))
    cm.loc_key(asm["root"], 542, (cx + 0.3, 0, 0))
    cm.rot_key(asm["root"], 412, (0, 0, 0))
    cm.rot_key(asm["root"], 508, (0, 0, 0))
    cm.rot_key(asm["root"], 516, (0, 0, math.radians(2.5)))
    cm.rot_key(asm["root"], 542, (0, 0, math.radians(2.5)))
    # SPARKS: 12 emissive sparks arcing out from the two contact points
    m_spark = cm.emissive_mat("M_Spark_S05", "#ffb020", 3.0)
    contacts = [(cx - 1.45, 2.5, 2.1), (cx + 1.45, 2.5, 2.1)]
    for i in range(12):
        c = contacts[i % 2]
        side = -1 if i % 2 == 0 else 1
        f0 = 508 + (i // 2) * 3
        spark = cm.add_sphere("S05_Spark%02d" % i, 0.11, m_spark, loc=c)
        up = 1.5 + (i % 3) * 0.6
        out = side * (1.0 + (i % 4) * 0.45)
        cm.scale_at(spark, f0 - 1, cm.HIDDEN)
        cm.loc_key(spark, f0, c)
        cm.scale_at(spark, f0, 1.0)
        cm.loc_key(spark, f0 + 8, (c[0] + out * 0.6, c[1] + 0.4,
                                   c[2] + up))
        cm.loc_key(spark, f0 + 16, (c[0] + out, c[1] + 0.7,
                                    c[2] + up - 1.6))
        cm.scale_at(spark, f0 + 16, cm.HIDDEN)
        cm.set_linear_range(spark, f0, f0 + 16)
    # 3/4 view: face-on, the near wheel filled the frame and hid the
    # pads/sparks; from the side-front the rim, pads and sparks all read.
    cam, _ = cm.build_shot_camera(
        "Cam_S05",
        [(412, (cx + 4.0, 12.0, 3.3), 36), (542, (cx + 3.5, 11.5, 3.1), 36)],
        [(412, (cx, 0.8, 2.0)), (542, (cx, 0.8, 2.0))], 412, 542)
    # camera shake during the screech (f508-539): shake the parent empty
    shake = cm.new_empty("Cam_S05_Shake", loc=(0, 0, 0))
    cam.parent = shake
    import random
    random.seed(5)
    cm.loc_key(shake, 507, (0, 0, 0))
    for f in range(508, 540, 3):
        cm.loc_key(shake, f, (random.uniform(-0.07, 0.07),
                              random.uniform(-0.05, 0.05),
                              random.uniform(-0.07, 0.07)))
    cm.loc_key(shake, 542, (0, 0, 0))
    cm.set_linear_range(shake, 507, 542)
    return {"cameras": [(412, cam)]}
