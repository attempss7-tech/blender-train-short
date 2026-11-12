# props.py — own-built 3D props for the V3 train short.
# Every object is built from bpy primitives here; no downloaded models.
import math

import bpy

import common as cm


# ------------------------------------------------------------------- train

def build_train(name, loc, cars=2, scale=1.0, body_hex="#2e7ab8",
                stripe_hex="#e8e8e8"):
    """Express locomotive + `cars` cars, travelling along +X.
    Returns dict(root, wheels=[spinner empties], body, headlight_mat).
    Wheel spin: rotate each spinner about local Y."""
    root = cm.new_empty(name + "_root", loc=loc)
    root.scale = (scale, scale, scale)
    m_body = cm.flat_mat("M_TrainBody_" + name, body_hex, 0.7)
    m_dark = cm.flat_mat("M_TrainDark_" + name, "#1a2530", 0.6)
    m_win = cm.flat_mat("M_TrainWin_" + name, "#20384a", 0.3)
    m_stripe = cm.flat_mat("M_TrainStripe_" + name, stripe_hex, 0.7)
    m_wheel = cm.flat_mat("M_TrainWheel_" + name, "#2a2d33", 0.5)
    m_light = cm.emissive_mat("M_TrainLight_" + name, "#fff2b0", 2.0)

    # --- locomotive body: main box + sloped nose + cab windshield
    cm.add_box(name + "_body", (4.6, 2.4, 2.2), m_body, parent=root,
               loc=(0, 0, 2.0))
    nose = cm.add_box(name + "_nose", (1.6, 2.3, 1.9), m_body, parent=root,
                      loc=(2.9, 0, 1.85), rot=(0, math.radians(-18), 0))
    cm.add_box(name + "_windshield", (0.9, 2.0, 0.9), m_win, parent=root,
               loc=(3.15, 0, 2.75), rot=(0, math.radians(-32), 0))
    cm.add_box(name + "_stripe", (4.7, 2.45, 0.35), m_stripe, parent=root,
               loc=(0, 0, 1.55))
    cm.add_box(name + "_roof", (4.4, 2.2, 0.25), m_dark, parent=root,
               loc=(0, 0, 3.2))
    # headlight (front of nose, facing +X)
    cm.add_cylinder(name + "_headlight", 0.28, 0.15, m_light, parent=root,
                    loc=(3.62, 0, 1.9), rot=(0, math.radians(90), 0))
    # pantograph hint on the roof
    cm.add_box(name + "_panto_base", (0.9, 0.12, 0.12), m_dark,
               parent=root, loc=(-0.6, 0, 3.4))
    cm.add_box(name + "_panto_arm", (0.08, 0.08, 0.9), m_dark,
               parent=root, loc=(-0.6, 0, 3.8), rot=(0, 0.5, 0))

    # --- cars
    for i in range(cars):
        cx = -5.4 - i * 5.2
        cm.add_box("%s_car%d" % (name, i), (4.9, 2.4, 2.2), m_body,
                   parent=root, loc=(cx, 0, 2.0))
        cm.add_box("%s_car%d_win" % (name, i), (4.4, 2.45, 0.7), m_win,
                   parent=root, loc=(cx, 0, 2.55))
        cm.add_box("%s_car%d_stripe" % (name, i), (5.0, 2.45, 0.3),
                   m_stripe, parent=root, loc=(cx, 0, 1.55))
        cm.add_box("%s_car%d_roof" % (name, i), (4.7, 2.2, 0.2), m_dark,
                   parent=root, loc=(cx, 0, 3.2))

    # --- wheels (spinner empties so they can rotate about local Y)
    wheels = []
    n_bogies = 1 + cars
    for b in range(n_bogies):
        bx = -b * 5.2 if b > 0 else 0.0
        if b > 0:
            bx = -5.4 - (b - 1) * 5.2
        for dx in (-1.5, 1.5):
            for sy in (-1, 1):
                spin = cm.new_empty(
                    "%s_wheel_b%d_%+d_%+d" % (name, b, int(dx), sy),
                    parent=root, loc=(bx + dx, sy * 1.05, 0.55))
                cm.add_cylinder(
                    "%s_wheelmesh_b%d_%+d_%+d" % (name, b, int(dx), sy),
                    0.55, 0.25, m_wheel, parent=spin,
                    rot=(math.radians(90), 0, 0))
                hub = cm.add_cylinder(
                    "%s_hub_b%d_%+d_%+d" % (name, b, int(dx), sy),
                    0.22, 0.3, m_stripe, parent=spin,
                    rot=(math.radians(90), 0, 0))
                wheels.append(spin)
    return dict(root=root, wheels=wheels, headlight_mat=m_light)


def build_track(name, loc, length=60.0, parent=None):
    """Ballast + 2 rails + sleepers along X."""
    root = cm.new_empty(name + "_root", parent=parent, loc=loc)
    m_ballast = cm.flat_mat("M_Ballast_" + name, "#8a8378", 1.0)
    m_rail = cm.flat_mat("M_Rail_" + name, "#b8bcc2", 0.35)
    m_sleeper = cm.flat_mat("M_Sleeper_" + name, "#5a4632", 1.0)
    cm.add_box(name + "_ballast", (length, 3.6, 0.25), m_ballast,
               parent=root, loc=(0, 0, 0.12))
    for sy in (-0.75, 0.75):
        cm.add_box(name + "_rail_%+d" % int(sy), (length, 0.12, 0.18),
                   m_rail, parent=root, loc=(0, sy, 0.32))
    n = int(length // 1.2)
    for i in range(n):
        x = -length / 2 + 0.6 + i * 1.2
        cm.add_box("%s_sleeper%02d" % (name, i), (0.5, 2.4, 0.1),
                   m_sleeper, parent=root, loc=(x, 0, 0.28))
    return root


def build_pole(name, loc, parent=None):
    """Telegraph pole (for the speed shot's whipping background)."""
    root = cm.new_empty(name + "_root", parent=parent, loc=loc)
    m_wood = cm.flat_mat("M_PoleWood_" + name, "#6a5138", 1.0)
    cm.add_cylinder(name + "_post", 0.12, 5.0, m_wood, parent=root,
                    loc=(0, 0, 2.5))
    cm.add_box(name + "_arm", (0.12, 1.6, 0.12), m_wood, parent=root,
               loc=(0, 0, 4.6))
    return root


def build_tree(name, loc, parent=None, scale=1.0):
    root = cm.new_empty(name + "_root", parent=parent, loc=loc)
    root.scale = (scale, scale, scale)
    m_bark = cm.flat_mat("M_Bark_" + name, "#6a4a2e", 1.0)
    m_leaf = cm.flat_mat("M_Leaf_" + name, "#3e7a34", 1.0)
    cm.add_cylinder(name + "_trunk", 0.18, 2.0, m_bark, parent=root,
                    loc=(0, 0, 1.0))
    cm.add_sphere(name + "_leaves", 1.3, m_leaf, parent=root,
                  loc=(0, 0, 3.0), scale=(1, 1, 1.1))
    cm.add_sphere(name + "_leaves2", 0.85, m_leaf, parent=root,
                  loc=(0.6, 0.3, 3.8))
    return root


# ---------------------------------------------------------- wheel assembly

def build_wheel_assembly(name, loc, scale=1.0, parent=None):
    """Axle + 2 wheels + bearing housings + sensor + seal + bolts.
    Axle along Y. Returns dict of parts for the exploded view."""
    root = cm.new_empty(name + "_root", parent=parent, loc=loc)
    root.scale = (scale, scale, scale)
    m_steel = cm.flat_mat("M_Steel_" + name, "#9aa2ac", 0.35)
    m_dark = cm.flat_mat("M_DarkSteel_" + name, "#3a3f46", 0.5)
    m_house = cm.flat_mat("M_Housing_" + name, "#c86a2a", 0.7)
    m_sensor = cm.flat_mat("M_Sensor_" + name, "#2a4a7a", 0.6)
    m_lens = cm.emissive_mat("M_SensorLens_" + name, "#7fd4ff", 0.6)
    m_seal = cm.flat_mat("M_Seal_" + name, "#e8ddc0", 0.85)
    m_bolt = cm.flat_mat("M_Bolt_" + name, "#6a7078", 0.4)

    parts = {}
    # axle (spins: spinner empty about Y)
    spin = cm.new_empty(name + "_axle_spin", parent=root, loc=(0, 0, 1.6))
    cm.add_cylinder(name + "_axle", 0.28, 3.4, m_steel, parent=spin,
                    rot=(math.radians(90), 0, 0))
    parts["axle_spin"] = spin
    parts["axle"] = bpy.data.objects[name + "_axle"]
    # wheels (children of the axle spinner so they spin together)
    wheels = []
    for sy in (-1, 1):
        w = cm.add_cylinder(name + "_wheel_%+d" % sy, 1.05, 0.3, m_dark,
                            parent=spin, loc=(0, sy * 1.55, 0),
                            rot=(math.radians(90), 0, 0))
        cm.add_cylinder(name + "_hub_%+d" % sy, 0.35, 0.4, m_steel,
                        parent=spin, loc=(0, sy * 1.55, 0),
                        rot=(math.radians(90), 0, 0))
        wheels.append(w)
    parts["wheels"] = wheels
    # bearing housings (do NOT spin — parented to root)
    housings = []
    for sy in (-1, 1):
        h = cm.add_box(name + "_housing_%+d" % sy, (0.9, 0.5, 0.9),
                       m_house, parent=root, loc=(0, sy * 1.15, 1.6))
        housings.append(h)
    parts["housings"] = housings
    # sensor box on the NEAR bearing housing, pushed forward (+Y) and up
    # so it reads from a +Y camera: mounted between the wheels it was
    # hidden behind the near wheel; on the housing top it still peeked
    # only above the wheel rim. A mount arm ties it to the housing.
    sensor = cm.add_box(name + "_sensor", (0.7, 0.6, 0.5), m_sensor,
                        parent=root, loc=(0, 1.75, 2.6))
    lens = cm.add_cylinder(name + "_sensor_lens", 0.16, 0.1, m_lens,
                           parent=root, loc=(0, 2.08, 2.6),
                           rot=(math.radians(90), 0, 0))
    # Mount arm: sensor (0,1.75,2.6) to housing top (0,1.15,2.05);
    # direction (0,-0.6,-0.55) needs the cylinder's Z axis rotated 132
    # deg about X. Parented to the sensor so it flies with it in S07.
    mount = cm.add_cylinder(name + "_sensor_mount", 0.07, 0.95, m_sensor,
                            parent=sensor, loc=(0, -0.3, -0.28),
                            rot=(math.radians(132), 0, 0))
    parts["sensor"] = sensor
    parts["sensor_lens"] = lens
    parts["sensor_lens_mat"] = m_lens
    # nylon seal: small torus around the axle, near the sensor
    seal = cm.add_torus(name + "_seal", 0.34, 0.09, m_seal, parent=root,
                        loc=(0, 0.55, 1.6), rot=(math.radians(90), 0, 0))
    parts["seal"] = seal
    # bolts around the housings
    bolts = []
    for i, (dx, sy) in enumerate(((-0.3, -1), (0.3, -1), (-0.3, 1),
                                  (0.3, 1))):
        b = cm.add_cylinder(name + "_bolt%d" % i, 0.09, 0.25, m_bolt,
                            parent=root, loc=(dx, sy * 1.15, 2.15))
        bolts.append(b)
    parts["bolts"] = bolts
    parts["root"] = root
    return parts


def build_seal_hero(name, loc, scale=1.0, parent=None, with_crack=True):
    """One nylon seal (torus), large, for close-ups. Optional jagged crack
    (thin dark boxes + red glow slivers) hidden at scale 0.001 until the
    reveal keys scale it in."""
    root = cm.new_empty(name + "_root", parent=parent, loc=loc)
    root.scale = (scale, scale, scale)
    m_seal = cm.flat_mat("M_SealHero_" + name, "#e8ddc0", 0.8)
    m_crack = cm.flat_mat("M_Crack_" + name, "#1a1210", 1.0)
    m_glow = cm.emissive_mat("M_CrackGlow_" + name, "#ff2a1a", 0.0,
                             base_hexcol="#7a1a10")
    seal = cm.add_torus(name + "_torus", 1.0, 0.32, m_seal, parent=root)
    crack = cm.new_empty(name + "_crack", parent=root, loc=(0, 0, 0.28))
    # jagged crack: zig-zag thin boxes across the top of the torus ring
    segs = [(-0.55, 0.28, 18), (-0.28, 0.42, -24), (0.0, 0.30, 30),
            (0.28, 0.42, -18), (0.55, 0.30, 22)]
    crack_parts = []
    for i, (x, y, ang) in enumerate(segs):
        c = cm.add_box("%s_crack%d" % (name, i), (0.34, 0.045, 0.02),
                       m_crack, parent=crack, loc=(x, y, 0.01),
                       rot=(0, 0, math.radians(ang)))
        g = cm.add_box("%s_glow%d" % (name, i), (0.36, 0.075, 0.012),
                       m_glow, parent=crack, loc=(x, y, 0.0),
                       rot=(0, 0, math.radians(ang)))
        crack_parts.append((c, g))
    crack.scale = (cm.HIDDEN, cm.HIDDEN, cm.HIDDEN)
    return dict(root=root, seal=seal, crack=crack,
                crack_parts=crack_parts, glow_mat=m_glow)


# ------------------------------------------------------------------- gauge

def build_gauge(name, loc, scale=1.0, parent=None, red_zone=True):
    """Round dial + needle on a pivot + red zone arc + lamp.
    Returns dict(root, needle_pivot, lamp, lamp_mat). Needle rest angle
    points left (-120 deg); sweeping to +60 deg is full-scale red."""
    root = cm.new_empty(name + "_root", parent=parent, loc=loc)
    root.scale = (scale, scale, scale)
    m_face = cm.flat_mat("M_GaugeFace_" + name, "#f5f2e8", 0.9)
    m_rim = cm.flat_mat("M_GaugeRim_" + name, "#2a2d33", 0.5)
    m_red = cm.flat_mat("M_GaugeRed_" + name, "#d81a1a", 0.7)
    m_needle = cm.flat_mat("M_GaugeNeedle_" + name, "#c01a1a", 0.6)
    m_lamp = cm.emissive_mat("M_GaugeLamp_" + name, "#ff2010", 0.0,
                             base_hexcol="#5a1410")
    cm.add_cylinder(name + "_rim", 1.15, 0.18, m_rim, parent=root)
    cm.add_cylinder(name + "_face", 1.0, 0.2, m_face, parent=root)
    # tick marks around the dial
    for i in range(9):
        ang = math.radians(-120 + i * 30)
        x, y = 0.82 * math.cos(ang), 0.82 * math.sin(ang)
        cm.add_box("%s_tick%d" % (name, i), (0.16, 0.05, 0.03),
                   m_rim, parent=root, loc=(x, y, 0.11),
                   rot=(0, 0, ang))
    # red zone: 3 red blocks along the top-right arc
    if red_zone:
        for i, ang in enumerate((30, 55, 80)):
            a = math.radians(ang)
            x, y = 0.82 * math.cos(a), 0.82 * math.sin(a)
            cm.add_box("%s_red%d" % (name, i), (0.2, 0.14, 0.04), m_red,
                       parent=root, loc=(x, y, 0.11), rot=(0, 0, a))
    # needle on a pivot at the dial centre (face plane = local XY)
    pivot = cm.new_empty(name + "_needle_pivot", parent=root,
                         loc=(0, 0, 0.14))
    cm.add_box(name + "_needle", (0.85, 0.09, 0.03), m_needle,
               parent=pivot, loc=(0.36, 0, 0))
    cm.add_sphere(name + "_hub", 0.12, m_rim, parent=pivot, loc=(0, 0, 0))
    pivot.rotation_euler = (0, 0, math.radians(-120))
    lamp = cm.add_sphere(name + "_lamp", 0.22, m_lamp, parent=root,
                         loc=(1.45, 0.9, 0.1))
    return dict(root=root, needle_pivot=pivot, lamp=lamp, lamp_mat=m_lamp)


def build_dashboard(name, loc, parent=None):
    """Angled control panel with a dark screen + big red alert lamp."""
    root = cm.new_empty(name + "_root", parent=parent, loc=loc)
    m_panel = cm.flat_mat("M_DashPanel_" + name, "#33414e", 0.7)
    m_screen = cm.emissive_mat("M_DashScreen_" + name, "#1a3a2a", 0.8,
                               base_hexcol="#10241a")
    m_lamp = cm.emissive_mat("M_DashLamp_" + name, "#ff2010", 0.0,
                             base_hexcol="#5a1410")
    panel = cm.add_box(name + "_panel", (3.4, 0.3, 2.0), m_panel,
                       parent=root, rot=(math.radians(-18), 0, 0))
    cm.add_box(name + "_screen", (2.2, 0.1, 1.1), m_screen, parent=root,
               loc=(-0.4, 0.28, 0.35), rot=(math.radians(-18), 0, 0))
    lamp = cm.add_sphere(name + "_lamp", 0.34, m_lamp, parent=root,
                         loc=(1.25, 0.3, 0.55))
    # small buttons row
    for i, col in enumerate(("#2a9a4a", "#e8a020", "#2a6ab8")):
        cm.add_cylinder("%s_btn%d" % (name, i), 0.12, 0.12,
                        cm.flat_mat("M_DashBtn%d_" % i + name, col, 0.6),
                        parent=root, loc=(-1.1 + i * 0.55, 0.22, -0.55),
                        rot=(math.radians(72), 0, 0))
    return dict(root=root, lamp=lamp, lamp_mat=m_lamp,
                screen_mat=m_screen)


# ------------------------------------------------------------------ engine

def build_engine(name, loc, parent=None):
    """Massive engine block: pistons pumping, flywheel spinning."""
    root = cm.new_empty(name + "_root", parent=parent, loc=loc)
    m_block = cm.flat_mat("M_EngineBlock_" + name, "#4a5a6a", 0.6)
    m_dark = cm.flat_mat("M_EngineDark_" + name, "#2a3138", 0.5)
    m_piston = cm.flat_mat("M_EnginePiston_" + name, "#c8ccd2", 0.3)
    m_copper = cm.flat_mat("M_EngineCopper_" + name, "#b87333", 0.5)
    cm.add_box(name + "_block", (4.4, 2.6, 2.6), m_block, parent=root,
               loc=(0, 0, 1.3))
    cm.add_box(name + "_base", (5.0, 3.0, 0.4), m_dark, parent=root,
               loc=(0, 0, 0.2))
    cm.add_box(name + "_head", (4.0, 2.2, 0.5), m_dark, parent=root,
               loc=(0, 0, 2.85))
    # pistons on top, moving up/down
    pistons = []
    for i in range(4):
        p = cm.add_cylinder("%s_piston%d" % (name, i), 0.32, 1.1,
                            m_piston, parent=root,
                            loc=(-1.5 + i * 1.0, 0, 3.4))
        pistons.append(p)
    # flywheel on the front face (spins about Y)
    fly_spin = cm.new_empty(name + "_fly_spin", parent=root,
                            loc=(0, 1.45, 1.5))
    cm.add_cylinder(name + "_flywheel", 1.1, 0.3, m_dark, parent=fly_spin,
                    rot=(math.radians(90), 0, 0))
    cm.add_box(name + "_fly_spoke", (1.9, 0.34, 0.18), m_copper,
               parent=fly_spin, loc=(0, 0, 0))
    # exhaust stack + pipes
    cm.add_cylinder(name + "_stack", 0.35, 1.6, m_dark, parent=root,
                    loc=(1.8, -0.8, 3.8))
    cm.add_cylinder(name + "_pipe", 0.22, 3.2, m_copper, parent=root,
                    loc=(-1.8, 0, 2.2), rot=(0, 0, math.radians(90)))
    return dict(root=root, pistons=pistons, fly_spin=fly_spin)


# ------------------------------------------------------------------- clock

def build_clock(name, loc, scale=1.0, parent=None):
    """Wall clock with hour/minute hands on pivots (face = local XY)."""
    root = cm.new_empty(name + "_root", parent=parent, loc=loc)
    root.scale = (scale, scale, scale)
    m_face = cm.flat_mat("M_ClockFace_" + name, "#f5f2e8", 0.9)
    m_rim = cm.flat_mat("M_ClockRim_" + name, "#2a2d33", 0.5)
    m_hand = cm.flat_mat("M_ClockHand_" + name, "#1a1a1a", 0.6)
    cm.add_cylinder(name + "_rim", 1.15, 0.15, m_rim, parent=root)
    cm.add_cylinder(name + "_face", 1.0, 0.17, m_face, parent=root)
    for i in range(12):
        a = math.radians(i * 30)
        cm.add_box("%s_tick%d" % (name, i), (0.14, 0.05, 0.03), m_rim,
                   parent=root, loc=(0.85 * math.cos(a),
                                     0.85 * math.sin(a), 0.1),
                   rot=(0, 0, a))
    hour = cm.new_empty(name + "_hour_pivot", parent=root, loc=(0, 0, 0.12))
    cm.add_box(name + "_hour", (0.5, 0.08, 0.03), m_hand, parent=hour,
               loc=(0.22, 0, 0))
    minute = cm.new_empty(name + "_minute_pivot", parent=root,
                          loc=(0, 0, 0.14))
    cm.add_box(name + "_minute", (0.8, 0.06, 0.03), m_hand, parent=minute,
               loc=(0.36, 0, 0))
    cm.add_sphere(name + "_hub", 0.09, m_rim, parent=root, loc=(0, 0, 0.15))
    return dict(root=root, hour=hour, minute=minute)


# ------------------------------------------------------------------- misc

def build_bench(name, loc, parent=None):
    root = cm.new_empty(name + "_root", parent=parent, loc=loc)
    m_top = cm.flat_mat("M_BenchTop_" + name, "#7a6248", 0.9)
    m_leg = cm.flat_mat("M_BenchLeg_" + name, "#4a3a28", 0.9)
    cm.add_box(name + "_top", (4.6, 1.6, 0.18), m_top, parent=root,
               loc=(0, 0, 1.0))
    for dx, dy in ((-2.1, -0.6), (2.1, -0.6), (-2.1, 0.6), (2.1, 0.6)):
        cm.add_box("%s_leg_%+d_%+d" % (name, int(dx), int(dy)),
                   (0.18, 0.18, 1.0), m_leg, parent=root,
                   loc=(dx, dy, 0.5))
    return root


def build_magnifier(name, loc, parent=None):
    """Hand magnifier: torus ring + pale glass disc + handle."""
    root = cm.new_empty(name + "_root", parent=parent, loc=loc)
    # ring faces the camera (+Y): torus default lies in XY (normal +Z),
    # so rotate X 90 deg — the handle then points down.
    root.rotation_euler = (math.radians(90), 0, 0)
    m_ring = cm.flat_mat("M_MagRing_" + name, "#2a2d33", 0.5)
    m_glass = cm.flat_mat("M_MagGlass_" + name, "#bfe0f0", 0.15)
    m_handle = cm.flat_mat("M_MagHandle_" + name, "#7a4a20", 0.8)
    cm.add_torus(name + "_ring", 0.55, 0.07, m_ring, parent=root)
    cm.add_cylinder(name + "_glass", 0.5, 0.04, m_glass, parent=root)
    cm.add_cylinder(name + "_handle", 0.07, 0.8, m_handle, parent=root,
                    loc=(0, -0.95, 0), rot=(math.radians(90), 0, 0))
    return root


def build_glint(name, loc, parent=None):
    """4-point sparkle star (two crossed thin boxes, emissive white).
    Starts hidden; scale-key it in to flash."""
    root = cm.new_empty(name + "_root", parent=parent, loc=loc)
    m_glint = cm.emissive_mat("M_Glint_" + name, "#ffffff", 2.5)
    cm.add_box(name + "_h", (0.5, 0.08, 0.02), m_glint, parent=root)
    cm.add_box(name + "_v", (0.08, 0.5, 0.02), m_glint, parent=root)
    root.scale = (cm.HIDDEN, cm.HIDDEN, cm.HIDDEN)
    return root


def flash_glint(glint_root, f_on, f_peak, f_off, peak_scale=1.0):
    cm.scale_at(glint_root, f_on - 1, cm.HIDDEN)
    cm.scale_at(glint_root, f_on, cm.HIDDEN)
    cm.scale_at(glint_root, f_peak, peak_scale)
    cm.scale_at(glint_root, f_off, cm.HIDDEN)
    if f_off < cm.FRAME_END - 1:
        cm.scale_at(glint_root, f_off + 1, cm.HIDDEN)


def build_carriage(name, loc, parent=None):
    """Train carriage interior: floor, back wall, windows, seats."""
    root = cm.new_empty(name + "_root", parent=parent, loc=loc)
    m_floor = cm.flat_mat("M_CarFloor_" + name, "#8a7a5a", 0.9)
    m_wall = cm.flat_mat("M_CarWall_" + name, "#d8d2c0", 0.9)
    m_win = cm.flat_mat("M_CarWin_" + name, "#7ab8d8", 0.2)
    m_seat = cm.flat_mat("M_CarSeat_" + name, "#7a3a4a", 0.85)
    m_rack = cm.flat_mat("M_CarRack_" + name, "#5a5a5a", 0.7)
    cm.add_box(name + "_floor", (10.0, 4.0, 0.2), m_floor, parent=root,
               loc=(0, 0, 0.1))
    cm.add_box(name + "_backwall", (10.0, 0.25, 3.4), m_wall, parent=root,
               loc=(0, -1.9, 1.7))
    cm.add_box(name + "_ceiling", (10.0, 4.0, 0.2), m_wall, parent=root,
               loc=(0, 0, 3.5))
    # windows on the back wall (still landscape outside = stopped train)
    for i, wx in enumerate((-3.3, 0.0, 3.3)):
        cm.add_box("%s_win%d" % (name, i), (2.2, 0.1, 1.4), m_win,
                   parent=root, loc=(wx, -1.75, 2.1))
        # a still pole + tree silhouette outside each window
        cm.add_box("%s_outpole%d" % (name, i), (0.12, 0.06, 1.2),
                   cm.flat_mat("M_CarOutPole_" + name, "#4a6a3a", 1.0),
                   parent=root, loc=(wx + 0.6, -1.78, 2.0))
    # seats along the back wall
    for i, sx in enumerate((-4.0, -2.0, 2.0, 4.0)):
        cm.add_box("%s_seat%d" % (name, i), (1.4, 0.7, 0.5), m_seat,
                   parent=root, loc=(sx, -1.3, 0.55))
        cm.add_box("%s_seatback%d" % (name, i), (1.4, 0.2, 1.0), m_seat,
                   parent=root, loc=(sx, -1.7, 1.2))
    # luggage rack + bags
    cm.add_box(name + "_rack", (9.0, 0.5, 0.12), m_rack, parent=root,
               loc=(0, -1.6, 3.1))
    bags = []
    for i, (bx, col) in enumerate(((-1.2, "#a84838"), (0.4, "#2a6a8a"),
                                   (1.8, "#8a6a2a"))):
        b = cm.add_box("%s_bag%d" % (name, i), (0.7, 0.45, 0.45),
                       cm.flat_mat("M_CarBag%d_" % i + name, col, 0.85),
                       parent=root, loc=(bx, 0.4, 0.45))
        bags.append(b)
    return dict(root=root, bags=bags)
