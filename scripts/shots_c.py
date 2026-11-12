# shots_c.py — shots 11-15 (frames 972-1505) of the V3 train short.
import math

import bpy
from mathutils import Vector

import common as cm
import props as pr


def _face_camera(obj):
    """Rotate a dial/clock root (face = local XY, normal +Z) to face a +Y
    camera, dial-up staying world-up.

    Blender XYZ Euler composes as Rz @ Ry @ Rx, so (90, 0, 180) gives
    Rz(180) @ Rx(90): local +Z -> +Y (faces the camera) and local +Y ->
    +Z (dial-up stays up). The first build used (-90, 0, 180), which
    faces the dial AWAY (blank backs in the S12/S13 stills)."""
    obj.rotation_euler = (math.radians(90), 0, math.radians(180))


# ------------------------------------------------------------------ S11
def build_s11(ctx):
    """f972-1069 'It let tiny air pockets slip into the optical sensor' —
    cutaway housing: little AIR BUBBLES SLIP through the crack and travel
    along the channel INTO the optical sensor lens; the lens flickers as
    each bubble arrives."""
    cx = cm.set_x(11)
    cm.make_set(11, ground_hex="#c8ccd2", backdrop_hex="#b8d0e8")
    m_housing = cm.flat_mat("M_SensorHousing_S11", "#4a5a6a", 0.6)
    m_channel = cm.flat_mat("M_Channel_S11", "#9fc8e0", 0.3)
    m_lens = cm.emissive_mat("M_OpticalLens_S11", "#7fd4ff", 0.8)
    m_bubble = cm.emissive_mat("M_Bubble_S11", "#d8f0ff", 1.2)
    # cracked seal at the left (vertical: ring plane YZ, hole along X)
    cm.add_box("S11_SealPost", (0.3, 0.3, 1.3),
               cm.flat_mat("M_SealPost_S11", "#6a7078", 0.9),
               loc=(cx - 1.9, 0, 0.65))
    seal = pr.build_seal_hero("S11_Seal", (cx - 1.9, 0, 1.9), scale=0.8)
    seal["root"].rotation_euler = (0, math.radians(90), 0)
    seal["crack"].scale = (1.0, 1.0, 1.0)  # crack already there: the entry
    cm.key_emission(seal["glow_mat"], 972, 1.5)
    cm.key_emission(seal["glow_mat"], 1069, 1.5)
    # OPEN guide rail under the bubble path (the first build used a closed
    # channel box — the bubbles travelled INSIDE it and were invisible).
    cm.add_box("S11_Channel", (3.4, 0.08, 0.06), m_channel,
               loc=(cx + 0.2, 0, 1.70))
    # sensor housing + optical lens (lens faces -X, toward the channel)
    cm.add_box("S11_Housing", (1.7, 2.0, 2.0), m_housing,
               loc=(cx + 2.4, 0, 1.9))
    cm.add_box("S11_HousingBase", (1.4, 1.6, 0.9), m_housing,
               loc=(cx + 2.4, 0, 0.45))
    lens = cm.add_cylinder("S11_Lens", 0.55, 0.18, m_lens,
                           loc=(cx + 1.5, 0, 1.9),
                           rot=(0, math.radians(90), 0))
    # AIR BUBBLES slipping through the crack into the sensor, staggered
    starts = [980, 988, 996, 1004, 1012, 1020, 1028, 1036]
    for i, f0 in enumerate(starts):
        b = cm.add_sphere("S11_Bubble%02d" % i, 0.22, m_bubble,
                          loc=(cx - 1.6, 0, 1.9))
        dy = 0.12 if i % 2 == 0 else -0.12
        cm.scale_at(b, f0 - 1, cm.HIDDEN)
        cm.loc_key(b, f0, (cx - 1.6, 0, 1.9))
        cm.scale_at(b, f0, 1.0)
        cm.loc_key(b, f0 + 9, (cx + 0.2, dy, 1.9))
        cm.loc_key(b, f0 + 18, (cx + 1.45, 0, 1.9))
        cm.scale_at(b, f0 + 18, cm.HIDDEN)
        cm.set_linear_range(b, f0, f0 + 18)
    # lens flickers as each bubble arrives (arrivals ~f998, 1006, ...)
    for j, f in enumerate(range(998, 1062, 8)):
        cm.key_emission(m_lens, f, 3.0 if j % 2 == 0 else 0.7)
    cm.key_emission(m_lens, 1069, 2.0)
    cam, _ = cm.build_shot_camera(
        "Cam_S11",
        [(972, (cx + 0.5, 13.5, 3.0), 28), (1069, (cx + 0.5, 12.0, 2.7), 28)],
        [(972, (cx + 0.5, 0, 1.9)), (1069, (cx + 0.5, 0, 1.9))],
        972, 1069)
    return {"cameras": [(972, cam)]}


# ------------------------------------------------------------------ S12
def build_s12(ctx):
    """f1070-1187 'tricking the computer into thinking the axle was
    overheating' — THE LIE MADE VISIBLE: the computer gauge needle SPIKES
    INTO THE RED (f1142-1165) with the red lamp flashing — while the axle
    beside it stays COOL BLUE."""
    rig2d = ctx["rig2d"]
    cx = cm.set_x(12)
    cm.make_set(12, ground_hex="#b8bec4", backdrop_hex="#a8c0d8")
    m_axle = cm.flat_mat("M_CoolAxle_S12", "#3a7ac8", 0.35)
    m_cool = cm.emissive_mat("M_CoolPuff_S12", "#7fb8ff", 1.0)
    m_console = cm.flat_mat("M_Console_S12", "#33414e", 0.7)
    # cool blue axle (left) + gently pulsing cool puffs
    axle = cm.add_cylinder("S12_Axle", 0.5, 2.6, m_axle,
                           loc=(cx - 1.9, 0, 1.8),
                           rot=(0, math.radians(90), 0))
    cm.add_box("S12_AxleStand", (0.4, 0.4, 1.3),
               cm.flat_mat("M_AxleStand_S12", "#6a7078", 0.9),
               loc=(cx - 1.9, 0, 0.65))
    puffs = []
    for i, px in enumerate((-2.8, -1.9, -1.0)):
        p = cm.add_sphere("S12_CoolPuff%d" % i, 0.22, m_cool,
                          loc=(cx + px, 0.3, 2.5))
        puffs.append(p)
        for f, s in [(1070, 0.6), (1090, 1.15), (1110, 0.6), (1130, 1.15),
                     (1150, 0.6), (1170, 1.15), (1187, 0.6)]:
            cm.scale_at(p, f + i * 4, s)
    # computer console (right) + gauge facing the camera
    cm.add_box("S12_Console", (2.4, 1.3, 2.6), m_console,
               loc=(cx + 2.0, 0, 1.3))
    gauge = pr.build_gauge("S12_Gauge", (cx + 2.0, 0.75, 3.2), scale=0.9)
    _face_camera(gauge["root"])
    red_light = cm.add_point_light("S12_RedLight", (cx + 2.0, 2.0, 3.4),
                                   "#ff2010", 0)
    # cable from the axle to the console
    cm.add_box("S12_Cable", (2.0, 0.12, 0.12),
               cm.flat_mat("M_Cable_S12", "#1a1a1a", 0.8),
               loc=(cx + 0.1, 0.2, 2.25), rot=(0, 0, math.radians(25)))
    # NEEDLE SPIKES INTO THE RED f1142-1165 ("overheating")
    cm.rot_key(gauge["needle_pivot"], 1070, (0, 0, math.radians(-120)))
    cm.rot_key(gauge["needle_pivot"], 1142, (0, 0, math.radians(-115)))
    cm.rot_key(gauge["needle_pivot"], 1165, (0, 0, math.radians(55)))
    cm.rot_key(gauge["needle_pivot"], 1187, (0, 0, math.radians(55)))
    # red lamp flashes with the spike, then stays latched
    for f, v in [(1141, 0.0), (1146, 4.0), (1152, 0.5), (1158, 4.0),
                 (1164, 0.5), (1170, 4.0), (1187, 2.5)]:
        cm.key_emission(gauge["lamp_mat"], f, v)
    for f, e in [(1141, 0), (1146, 80), (1152, 5), (1158, 80),
                 (1164, 5), (1170, 80), (1187, 40)]:
        cm.key_light_energy(red_light, f, e)
    # technician watching the gauge, worried (closer to the camera so
    # they read at this shot's long camera distance)
    tech = rig2d.create_human(
        "S12_Tech", location=(cx + 0.1, 3.2, 0), height=1.76,
        skin=(0.85, 0.65, 0.50), shirt=(0.20, 0.45, 0.70),
        pants=(0.20, 0.24, 0.40), hair=(0.12, 0.08, 0.06),
        shoe=(0.30, 0.20, 0.14))
    cam, _ = cm.build_shot_camera(
        "Cam_S12",
        [(1070, (cx, 14.5, 3.6), 26), (1187, (cx, 13.0, 3.3), 26)],
        [(1070, (cx, 0, 2.3)), (1187, (cx + 0.4, 0, 2.4))], 1070, 1187)
    rig2d.add_billboard(tech, cam)
    rig2d.head_turn(tech, 1080, 1130, angle_deg=25)
    rig2d.point(tech, 1150, 1185, arm="R")  # gauge is screen-left of tech
    return {"cameras": [(1070, cam)]}


# ------------------------------------------------------------------ S13
def build_s13(ctx):
    """f1188-1286 'One ten-cent seal caused millions in delays' — the tiny
    seal hero-centre; behind it a CLOCK's hands SPIN fast, a delay-dial
    needle sweeps up, and a stack of COINS GROWS coin by coin."""
    cx = cm.set_x(13)
    cm.make_set(13, ground_hex="#cfd4d8", backdrop_hex="#b8d0e8")
    m_ped = cm.flat_mat("M_Pedestal_S13", "#8a94a0", 0.6)
    m_coin = cm.flat_mat("M_Coin_S13", "#e8c85a", 0.3)
    cm.add_cylinder("S13_Pedestal", 1.1, 1.0, m_ped, loc=(cx, 0, 0.5))
    seal = pr.build_seal_hero("S13_Seal", (cx, 0, 1.65), scale=1.2,
                              with_crack=False)
    cm.rot_key(seal["root"], 1188, (0, 0, 0))
    cm.rot_key(seal["root"], 1286, (0, 0, math.radians(40)))
    cm.set_linear_range(seal["root"], 1188, 1286)
    # big clock behind (hands spin fast = time/delays piling up)
    clock = pr.build_clock("S13_Clock", (cx, -2.2, 4.0), scale=1.2)
    _face_camera(clock["root"])
    cm.rot_key(clock["minute"], 1188, (0, 0, math.radians(90)))
    cm.rot_key(clock["minute"], 1286,
               (0, 0, math.radians(90 - 360 * 3)))
    cm.set_linear_range(clock["minute"], 1188, 1286)
    cm.rot_key(clock["hour"], 1188, (0, 0, math.radians(20)))
    cm.rot_key(clock["hour"], 1286, (0, 0, math.radians(20 - 180)))
    cm.set_linear_range(clock["hour"], 1188, 1286)
    # delay dial (left) sweeping up
    dial = pr.build_gauge("S13_Dial", (cx - 2.3, -1.2, 2.6), scale=0.8)
    _face_camera(dial["root"])
    cm.rot_key(dial["needle_pivot"], 1188, (0, 0, math.radians(-120)))
    cm.rot_key(dial["needle_pivot"], 1286, (0, 0, math.radians(55)))
    # coin stack (right) growing coin by coin
    for i in range(8):
        coin = cm.add_cylinder("S13_Coin%d" % i, 0.55, 0.13, m_coin,
                               loc=(cx + 2.3, 0.4, 0.07 + i * 0.14))
        f_in = 1196 + i * 10
        cm.scale_at(coin, f_in - 1, cm.HIDDEN)
        cm.scale_at(coin, f_in, 1.15)
        cm.scale_at(coin, f_in + 4, 1.0)
        cm.scale_at(coin, 1286, 1.0)
    cam, _ = cm.build_shot_camera(
        "Cam_S13",
        [(1188, (cx, 14.5, 3.4), 24), (1286, (cx, 13.0, 3.1), 24)],
        [(1188, (cx, -0.5, 2.5)), (1286, (cx, -0.5, 2.5))], 1188, 1286)
    return {"cameras": [(1188, cam)]}


# ------------------------------------------------------------------ S14
def build_s14(ctx):
    """f1287-1409 'proving modern mega-machines aren't brought down by
    massive engine failures' — a MASSIVE engine, pistons PUMPING, flywheel
    SPINNING, running fine; one small failure spark appears and FIZZLES
    OUT; the engine never falters."""
    cx = cm.set_x(14)
    cm.make_set(14, ground_hex="#b8bec4", backdrop_hex="#a8c0d8")
    eng = pr.build_engine("S14_Engine", (cx, 0, 0))
    # pistons pump up/down, staggered, the whole shot
    for i, p in enumerate(eng["pistons"]):
        px, py, _ = p.location
        f = 1287
        up = (i % 2 == 0)
        while f <= 1409:
            cm.loc_key(p, f, (px, py, 3.65 if up else 3.15))
            up = not up
            f += 8
        cm.set_linear_range(p, 1287, 1409)
    # flywheel spins fast
    cm.rot_key(eng["fly_spin"], 1287, (0, 0, 0))
    cm.rot_key(eng["fly_spin"], 1409, (0, math.radians(360 * 6), 0))
    cm.set_linear_range(eng["fly_spin"], 1287, 1409)
    # one small failure spark: appears, flickers, FIZZLES OUT
    m_spark = cm.emissive_mat("M_FailSpark_S14", "#ff3010", 3.0)
    spark = cm.add_sphere("S14_FailSpark", 0.22, m_spark,
                          loc=(cx + 1.6, 1.35, 2.3))
    cm.scale_at(spark, 1329, cm.HIDDEN)
    cm.scale_at(spark, 1334, 1.3)
    cm.scale_at(spark, 1344, 0.7)
    cm.scale_at(spark, 1354, 1.2)
    cm.scale_at(spark, 1366, 0.4)
    cm.scale_at(spark, 1372, cm.HIDDEN)
    cm.scale_at(spark, 1409, cm.HIDDEN)
    cam, _ = cm.build_shot_camera(
        "Cam_S14",
        [(1287, (cx, 14.0, 3.4), 30), (1409, (cx, 12.5, 3.1), 30)],
        [(1287, (cx, 0, 2.3)), (1409, (cx, 0, 2.3))], 1287, 1409)
    return {"cameras": [(1287, cam)]}


# ------------------------------------------------------------------ S15
def build_s15(ctx):
    """f1410-1505 'they're held hostage by the smallest components' — the
    GIANT train looms over the ONE TINY seal: seal in sharp focus on its
    pedestal in the foreground, the huge locomotive looming behind it, a
    thin rope running from the train's nose to the seal. Camera slow
    push-in on the seal to the final frame."""
    cx = cm.set_x(15)
    cm.make_set(15, ground_hex="#8ab868", backdrop_hex="#a8c8e8")
    pr.build_track("S15_Track", (cx, -4.5, 0), length=40.0)
    train = pr.build_train("S15_Train", (cx - 4.0, -4.5, 0.35), cars=0,
                           scale=1.5)
    # headlight dims: the giant brought low by the tiny seal
    cm.key_emission(train["headlight_mat"], 1410, 2.0)
    cm.key_emission(train["headlight_mat"], 1440, 0.4)
    cm.key_emission(train["headlight_mat"], 1505, 0.4)
    # tiny seal hero in the foreground
    m_ped = cm.flat_mat("M_Pedestal_S15", "#8a94a0", 0.6)
    cm.add_cylinder("S15_Pedestal", 0.6, 0.9, m_ped, loc=(cx, 1.5, 0.45))
    seal = pr.build_seal_hero("S15_Seal", (cx, 1.5, 1.3), scale=0.8,
                              with_crack=False)
    cm.rot_key(seal["root"], 1410, (0, 0, 0))
    cm.rot_key(seal["root"], 1505, (0, 0, math.radians(30)))
    cm.set_linear_range(seal["root"], 1410, 1505)
    # rope from the train's nose to the seal — the hostage line
    nose = Vector((cx + 1.43, -2.8, 3.2))
    seal_top = Vector((cx + 0.1, 1.5, 1.4))
    mid = (nose + seal_top) / 2
    direction = seal_top - nose
    rope = cm.add_cylinder("S15_Rope", 0.05, direction.length,
                           cm.flat_mat("M_Rope_S15", "#8a6a3a", 1.0),
                           loc=mid)
    rope.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    # glints on the seal: the smallest component holds the focus
    g1 = pr.build_glint("S15_Glint1", (cx - 0.5, 1.5, 1.75))
    pr.flash_glint(g1, 1440, 1448, 1456, peak_scale=1.0)
    g2 = pr.build_glint("S15_Glint2", (cx + 0.6, 1.5, 1.65))
    pr.flash_glint(g2, 1472, 1480, 1488, peak_scale=1.0)
    cam, _ = cm.build_shot_camera(
        "Cam_S15",
        [(1410, (cx, 12.0, 3.8), 38), (1505, (cx, 9.5, 3.2), 38)],
        [(1410, (cx, -0.5, 2.4)), (1505, (cx, 0.8, 1.9))], 1410, 1505)
    return {"cameras": [(1410, cam)]}
