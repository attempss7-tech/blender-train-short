# shots_b.py — shots 6-10 (frames 543-971) of the V3 train short.
import math

import bpy

import common as cm
import props as pr


def _joint(obj, frame, z_deg=None, y_deg=None, x_deg=None):
    """Keyframe a 2D-rig joint rotation (degrees) at one frame."""
    if z_deg is not None:
        obj.rotation_euler[2] = math.radians(z_deg)
        obj.keyframe_insert(data_path="rotation_euler", index=2,
                            frame=frame)
    if y_deg is not None:
        obj.rotation_euler[1] = math.radians(y_deg)
        obj.keyframe_insert(data_path="rotation_euler", index=1,
                            frame=frame)
    if x_deg is not None:
        obj.rotation_euler[0] = math.radians(x_deg)
        obj.keyframe_insert(data_path="rotation_euler", index=0,
                            frame=frame)


def _place_key(rig, frame, loc):
    rig["placement"].location = loc
    rig["placement"].keyframe_insert(data_path="location", frame=frame)


# ------------------------------------------------------------------ S06
def build_s06(ctx):
    """f543-600 'stranding hundreds of passengers' — carriage interior:
    3 2D passengers JOLT forward as the train stops, luggage slides, then
    they wait, stranded (idle sway, heads turning to the still window)."""
    rig2d = ctx["rig2d"]
    cx = cm.set_x(6)
    cm.make_set(6, ground_hex="#b0a890", backdrop_hex="#a8c0d8")
    car = pr.build_carriage("S06_Car", (cx, 0, 0))
    specs = [
        ("S06_PaxA", (cx - 1.7, 0.3, 0.2), 1.75, (0.72, 0.48, 0.32),
         (0.75, 0.25, 0.25), None),
        ("S06_PaxB", (cx + 0.1, -0.1, 0.2), 1.68, (0.55, 0.38, 0.28),
         (0.20, 0.45, 0.70), "cap"),
        ("S06_PaxC", (cx + 1.9, 0.35, 0.2), 1.80, (0.85, 0.65, 0.50),
         (0.25, 0.60, 0.30), None),
    ]
    rigs = []
    for name, loc, h, skin, shirt, hat in specs:
        rig = rig2d.create_human(
            name, location=loc, height=h, skin=skin, shirt=shirt,
            pants=(0.20, 0.24, 0.40), hair=(0.12, 0.08, 0.06),
            shoe=(0.30, 0.20, 0.14), hat=hat,
            hat_color=(0.75, 0.20, 0.20))
        rigs.append(rig)
    cam, _ = cm.build_shot_camera(
        "Cam_S06",
        [(543, (cx, 13.5, 2.4), 30), (600, (cx, 12.5, 2.2), 30)],
        [(543, (cx, -0.5, 1.5)), (600, (cx, -0.5, 1.5))], 543, 600)
    for rig in rigs:
        rig2d.add_billboard(rig, cam)
    # JOLT f543-560: everyone lurches +X (braking throws them forward),
    # torsos tilt, then they settle; then idle waiting f560-600
    for rig, loc in zip(rigs, [s[1] for s in specs]):
        x, y, z = loc
        _place_key(rig, 543, (x, y, z))
        _place_key(rig, 552, (x + 0.35, y, z))
        _place_key(rig, 575, (x + 0.15, y, z))
        _place_key(rig, 600, (x + 0.15, y, z))
        _joint(rig["torso"], 543, z_deg=0)
        _joint(rig["torso"], 552, z_deg=-12)
        _joint(rig["torso"], 575, z_deg=0)
        _joint(rig["head_pivot"], 552, z_deg=-8)
        _joint(rig["head_pivot"], 575, z_deg=0)
        rig2d.idle(rig, 560, 600, cycles=1)
    # one passenger looks out of the window, puzzled
    rig2d.head_turn(rigs[1], 566, 596, angle_deg=30)
    # luggage slides forward with the jolt
    for bag in car["bags"]:
        bx, by, bz = bag.location
        cm.loc_key(bag, 543, (bx, by, bz))
        cm.loc_key(bag, 554, (bx + 0.55, by, bz))
        cm.loc_key(bag, 600, (bx + 0.55, by, bz))
    return {"cameras": [(543, cam)]}


# ------------------------------------------------------------------ S07
def build_s07(ctx):
    """f601-684 'Technicians tore apart the wheel assembly' — two 2D
    technicians at the wheel assembly; parts FLY OUT into an exploded
    view (f618-680) while the technicians reach and point."""
    rig2d = ctx["rig2d"]
    cx = cm.set_x(7)
    cm.make_set(7, ground_hex="#b8bec4", backdrop_hex="#a8c0d8")
    cm.add_box("S07_Platform", (5.0, 4.0, 0.3),
               cm.flat_mat("M_Platform_S07", "#6a7078", 0.9),
               loc=(cx, 0, 0.15))
    # stand posts under the bearing housings (the assembly floats 0.55 m
    # above the platform otherwise)
    for sy in (-1, 1):
        cm.add_box("S07_Stand_%+d" % sy, (0.3, 0.3, 1.15),
                   cm.flat_mat("M_Platform_S07", "#6a7078", 0.9),
                   loc=(cx, sy * 1.15, 0.875))
    asm = pr.build_wheel_assembly("S07_Asm", (cx, 0, 0.3), scale=1.0)
    tech_specs = [
        ("S07_TechA", (cx - 2.5, 0.8, 0.3), 1.80, (0.72, 0.48, 0.32),
         (0.95, 0.55, 0.10), "cap"),
        ("S07_TechB", (cx + 2.5, 0.8, 0.3), 1.74, (0.55, 0.38, 0.28),
         (0.95, 0.80, 0.10), None),
    ]
    rigs = []
    for name, loc, h, skin, shirt, hat in tech_specs:
        rig = rig2d.create_human(
            name, location=loc, height=h, skin=skin, shirt=shirt,
            pants=(0.20, 0.24, 0.40), hair=(0.12, 0.08, 0.06),
            shoe=(0.30, 0.20, 0.14), hat=hat,
            hat_color=(0.95, 0.80, 0.10))
        rigs.append(rig)
    # 3/4 view: face-on, the near wheel filled the frame and hid the
    # technicians and the exploding parts.
    cam, _ = cm.build_shot_camera(
        "Cam_S07",
        [(601, (cx + 5.0, 13.0, 3.4), 30), (684, (cx + 4.0, 12.0, 3.1), 30)],
        [(601, (cx, 0.3, 2.0)), (684, (cx, 0.3, 2.0))], 601, 684)
    for rig in rigs:
        rig2d.add_billboard(rig, cam)
    # exploded view: parts fly out along their axes f618-680.
    # The first pass exploded only along Y (the axle axis) — from a +Y
    # camera that reads as nothing moving, so the wheels/housings/seal
    # also spread in X and Z to separate visibly on screen.
    def explode(obj, f0, f1, assembled, exploded):
        cm.loc_key(obj, f0, assembled)
        cm.loc_key(obj, f1, exploded)
    explode(asm["wheels"][0], 618, 680, (0, -1.55, 0), (-0.8, -2.3, 0.3))
    explode(asm["wheels"][1], 618, 680, (0, 1.55, 0), (0.8, 2.3, 0.3))
    # hubs ride with their wheels (separate objects, same parent)
    for sy in (-1, 1):
        hub = bpy.data.objects["S07_Asm_hub_%+d" % sy]
        explode(hub, 618, 680, (0, sy * 1.55, 0),
                (sy * 0.8, sy * 2.3, 0.3))
    explode(asm["housings"][0], 618, 680, (0, -1.15, 1.6),
            (0.6, -1.9, 2.2))
    explode(asm["housings"][1], 618, 680, (0, 1.15, 1.6),
            (-0.6, 1.9, 2.2))
    explode(asm["sensor"], 618, 680, (0, 1.75, 2.6), (0, 1.75, 3.6))
    explode(asm["sensor_lens"], 618, 680, (0, 2.08, 2.6),
            (0, 2.08, 3.3))
    explode(asm["seal"], 618, 680, (0, 0.55, 1.6), (1.4, 1.2, 1.0))
    for i, bolt in enumerate(asm["bolts"]):
        bx, by, bz = bolt.location
        explode(bolt, 618 + i * 3, 680, (bx, by, bz),
                (bx * 2.2, by, bz + 1.1))
    # technicians: A points at the flying parts (screen-left of A -> arm R),
    # B works with both arms up
    rig2d.point(rigs[0], 615, 665, arm="R")
    for side, sgn in (("L", 1), ("R", -1)):
        _joint(rigs[1]["shoulder"][side], 601, z_deg=0)
        _joint(rigs[1]["shoulder"][side], 625, z_deg=sgn * 130)
        _joint(rigs[1]["shoulder"][side], 670, z_deg=sgn * 130)
        _joint(rigs[1]["shoulder"][side], 684, z_deg=0)
        _joint(rigs[1]["elbow"][side], 625, z_deg=sgn * -20)
        _joint(rigs[1]["elbow"][side], 684, z_deg=0)
    rig2d.head_turn(rigs[0], 665, 684, angle_deg=25)
    return {"cameras": [(601, cam)]}


# ------------------------------------------------------------------ S08
def build_s08(ctx):
    """f685-759 'expecting shattered bearings or melted metal' — the
    technicians' EXPECTATION: a bearing with a jagged crack SPREADING
    across it + a metal blob GLOWING orange and DRIPPING, each inside a
    white 'thought' ring. One technician points at the cracked bearing."""
    rig2d = ctx["rig2d"]
    cx = cm.set_x(8)
    cm.make_set(8, ground_hex="#b8bec4", backdrop_hex="#a8c0d8")
    m_ped = cm.flat_mat("M_Pedestal_S08", "#8a94a0", 0.6)
    m_ring = cm.flat_mat("M_ThoughtRing_S08", "#f5f5f5", 0.9)
    m_bearing = cm.flat_mat("M_Bearing_S08", "#9aa2ac", 0.35)
    m_crack = cm.flat_mat("M_BearingCrack_S08", "#1a1210", 1.0)
    m_melt = cm.emissive_mat("M_Melted_S08", "#ff7a20", 1.6,
                             base_hexcol="#c85a10")
    # --- left: cracked bearing on a pedestal, inside a thought ring
    cm.add_cylinder("S08_PedL", 0.7, 1.0, m_ped, loc=(cx - 1.7, 0, 0.5))
    bearing = cm.add_torus("S08_Bearing", 0.85, 0.28, m_bearing,
                           loc=(cx - 1.7, 0, 2.1),
                           rot=(math.radians(90), 0, 0))
    cm.add_torus("S08_RingL", 1.35, 0.05, m_ring, loc=(cx - 1.7, 0, 2.1),
                 rot=(math.radians(90), 0, 0))
    # jagged crack across the bearing face (front, +Y side), scales in
    crack = cm.new_empty("S08_Crack", loc=(cx - 1.7, 0.32, 2.1))
    for i, (dx, dz, ang) in enumerate(((-0.55, 0.35, 25), (-0.2, 0.15, -30),
                                       (0.15, -0.1, 35), (0.5, -0.3, -20))):
        cm.add_box("S08_Crack%d" % i, (0.5, 0.04, 0.07), m_crack,
                   parent=crack, loc=(dx, 0, dz),
                   rot=(0, math.radians(ang), 0))
    cm.scale_at(crack, 699, cm.HIDDEN)
    cm.scale_at(crack, 730, 1.0)
    cm.scale_at(crack, 759, 1.0)
    # bearing wobbles as if broken
    cm.rot_key(bearing, 685, (math.radians(90), 0, 0))
    cm.rot_key(bearing, 720, (math.radians(90), 0, math.radians(6)))
    cm.rot_key(bearing, 759, (math.radians(90), 0, math.radians(-4)))
    # --- right: glowing melted metal + drips, inside a thought ring
    cm.add_cylinder("S08_PedR", 0.7, 1.0, m_ped, loc=(cx + 1.7, 0, 0.5))
    blob = cm.add_sphere("S08_MeltBlob", 0.75, m_melt,
                         loc=(cx + 1.7, 0, 1.9), scale=(1.2, 0.85, 0.65))
    cm.add_torus("S08_RingR", 1.35, 0.05, m_ring, loc=(cx + 1.7, 0, 2.1),
                 rot=(math.radians(90), 0, 0))
    cm.key_emission(m_melt, 685, 1.2)
    cm.key_emission(m_melt, 720, 2.6)
    cm.key_emission(m_melt, 759, 2.0)
    # molten drips falling from the blob, staggered
    for i, f0 in enumerate((700, 718, 736)):
        drip = cm.add_sphere("S08_Drip%d" % i, 0.13, m_melt,
                             loc=(cx + 1.7 + (i - 1) * 0.3, 0, 1.55))
        cm.scale_at(drip, f0 - 1, cm.HIDDEN)
        cm.loc_key(drip, f0, (cx + 1.7 + (i - 1) * 0.3, 0, 1.55))
        cm.scale_at(drip, f0, 1.0)
        cm.loc_key(drip, f0 + 14,
                   (cx + 1.7 + (i - 1) * 0.3, 0, 0.55))
        cm.scale_at(drip, f0 + 14, cm.HIDDEN)
        cm.set_linear_range(drip, f0, f0 + 14)
    # blob sags slightly as it melts
    cm.scale_key(blob, 685, (1.2, 0.85, 0.65))
    cm.scale_key(blob, 759, (1.35, 0.95, 0.5))
    # --- technician pointing at the cracked bearing (screen-right side)
    tech = rig2d.create_human(
        "S08_Tech", location=(cx, 2.4, 0), height=1.78,
        skin=(0.72, 0.48, 0.32), shirt=(0.95, 0.55, 0.10),
        pants=(0.20, 0.24, 0.40), hair=(0.12, 0.08, 0.06),
        shoe=(0.30, 0.20, 0.14), hat="cap",
        hat_color=(0.95, 0.80, 0.10))
    cam, _ = cm.build_shot_camera(
        "Cam_S08",
        [(685, (cx, 13.5, 2.9), 26), (759, (cx, 12.0, 2.7), 26)],
        [(685, (cx, 0, 1.95)), (759, (cx, 0, 1.95))], 685, 759)
    rig2d.add_billboard(tech, cam)
    rig2d.point(tech, 695, 745, arm="L")
    return {"cameras": [(685, cam)]}


# ------------------------------------------------------------------ S09
def build_s09(ctx):
    """f760-836 'Everything was pristine.' — the real parts on a bench,
    GLEAMING: a magnifier sweeps over them finding nothing; sparkle glints
    flash across the parts in sequence ('pristine' f797-815)."""
    rig2d = ctx["rig2d"]
    cx = cm.set_x(9)
    cm.make_set(9, ground_hex="#c8c4b8", backdrop_hex="#b8d0e8")
    pr.build_bench("S09_Bench", (cx, 0, 0))
    m_shiny = cm.flat_mat("M_PrinstineSteel_S09", "#d8dde2", 0.15)
    m_shiny2 = cm.flat_mat("M_PrinstineBrass_S09", "#d8b060", 0.2)
    m_seal = cm.flat_mat("M_PrinstineSeal_S09", "#e8ddc0", 0.7)
    # parts laid out on the bench (bench top z = 1.09; the wheel stands
    # on it, centre at 1.09 + 0.62)
    wheel = cm.add_cylinder("S09_Wheel", 0.62, 0.22, m_shiny,
                            loc=(cx - 1.5, 0, 1.71),
                            rot=(math.radians(90), 0, 0))
    housing = cm.add_box("S09_Housing", (0.9, 0.6, 0.7), m_shiny2,
                         loc=(cx - 0.2, 0, 1.45))
    seal = cm.add_torus("S09_Seal", 0.4, 0.13, m_seal,
                        loc=(cx + 1.1, 0, 1.3))
    axle = cm.add_cylinder("S09_Axle", 0.18, 1.6, m_shiny,
                           loc=(cx + 0.4, 0, 1.32),
                           rot=(0, math.radians(90), 0))
    # magnifier sweeps left -> right over the parts
    mag = pr.build_magnifier("S09_Mag", (cx - 1.8, 1.1, 1.9))
    cm.loc_key(mag, 760, (cx - 1.8, 1.1, 1.9))
    cm.loc_key(mag, 798, (cx - 0.2, 1.1, 1.95))
    cm.loc_key(mag, 830, (cx + 1.5, 1.1, 1.9))
    cm.loc_key(mag, 836, (cx + 1.5, 1.1, 1.9))
    # glints flash across the parts in sequence as the magnifier passes
    glints = [
        (pr.build_glint("S09_GlintWheel", (cx - 1.5, 0.3, 1.7)), 772, 780),
        (pr.build_glint("S09_GlintHousing", (cx - 0.2, 0.35, 1.85)), 794,
         802),
        (pr.build_glint("S09_GlintSeal", (cx + 1.1, 0.3, 1.6)), 814, 822),
    ]
    for g, f_on, f_peak in glints:
        pr.flash_glint(g, f_on, f_peak, f_peak + 8, peak_scale=1.1)
    # technician watching, head turning with the magnifier
    tech = rig2d.create_human(
        "S09_Tech", location=(cx + 2.2, 1.4, 0), height=1.78,
        skin=(0.55, 0.38, 0.28), shirt=(0.95, 0.80, 0.10),
        pants=(0.20, 0.24, 0.40), hair=(0.12, 0.08, 0.06),
        shoe=(0.30, 0.20, 0.14), hat="cap",
        hat_color=(0.95, 0.80, 0.10))
    cam, _ = cm.build_shot_camera(
        "Cam_S09",
        [(760, (cx, 13.0, 2.7), 28), (836, (cx, 12.0, 2.5), 28)],
        [(760, (cx, 0, 1.5)), (836, (cx, 0, 1.5))], 760, 836)
    rig2d.add_billboard(tech, cam)
    rig2d.head_turn(tech, 770, 830, angle_deg=28)
    rig2d.idle(tech, 760, 836, cycles=1)
    return {"cameras": [(760, cam)]}


# ------------------------------------------------------------------ S10
def build_s10(ctx):
    """f837-971 'The culprit? A microscopic crack in a cheap nylon seal.'
    — camera ZOOMS INTO the tiny seal; at f870-907 the hairline CRACK is
    revealed, scaling in + glowing red."""
    cx = cm.set_x(10)
    cm.make_set(10, ground_hex="#cfd4d8", backdrop_hex="#b8d0e8")
    m_ped = cm.flat_mat("M_Pedestal_S10", "#8a94a0", 0.6)
    cm.add_cylinder("S10_Pedestal", 1.6, 1.0, m_ped, loc=(cx, 0, 0.5))
    cm.add_cylinder("S10_PedestalTop", 1.9, 0.15, m_ped, loc=(cx, 0, 1.05))
    seal = pr.build_seal_hero("S10_Seal", (cx, 0, 1.9), scale=1.4)
    # seal rotates slowly the whole shot
    cm.rot_key(seal["root"], 837, (0, 0, 0))
    cm.rot_key(seal["root"], 971, (0, 0, math.radians(45)))
    cm.set_linear_range(seal["root"], 837, 971)
    # CRACK REVEAL f870-907 ("microscopic crack"): scales in, then glows
    cm.scale_at(seal["crack"], 869, cm.HIDDEN)
    cm.scale_at(seal["crack"], 885, 1.0)
    cm.scale_at(seal["crack"], 971, 1.0)
    cm.key_emission(seal["glow_mat"], 869, 0.0)
    cm.key_emission(seal["glow_mat"], 890, 3.5)
    cm.key_emission(seal["glow_mat"], 900, 1.2)
    cm.key_emission(seal["glow_mat"], 907, 3.0)
    cm.key_emission(seal["glow_mat"], 971, 2.0)
    cam, _ = cm.build_shot_camera(
        "Cam_S10",
        [(837, (cx, 8.5, 4.8), 40), (971, (cx, 4.6, 3.3), 40)],
        [(837, (cx, 0, 1.9)), (971, (cx, 0, 1.9))], 837, 971)
    return {"cameras": [(837, cam)]}
