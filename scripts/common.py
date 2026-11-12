# common.py — shared helpers for the V3 train short (Blender 4.2.23).
#
# Conventions (same as the chicken Blender short):
# - One scene, one 1506-frame timeline (frames 0-1505). Shots are HARD CUTS
#   at the marker frames in SHOTS (end is exclusive: shot N covers
#   [start, end-1]).
# - 15 shots, each its own set centred at x = (shot-1)*40, with its own
#   ground + backdrop. Cameras sit at +Y of their set centre.
# - Visibility is done by ROOT SCALE (0.001 = hidden), never hide_render.
#   Always key BOTH sides of a visibility change.
# - Humans are ALWAYS flat 2D Grease Pencil rigs from shared/2d_rig.py
#   (facing_deg=0 faces a +Y camera; do NOT "fix" the 180 deg base yaw).
#   Worlds/scenery/objects are own-built 3D meshes.
# - Timing comes from voice/words.json via SHOT_PLAN.md — never by feel.
import importlib.util
import math
import os

import bpy
from mathutils import Matrix, Vector

FRAME_END = 1506            # timeline is frames 0..1505
HIDDEN = 0.001              # root scale that reads as "not there"
SET_SPACING = 40.0          # metres between shot-set centres on X

# (shot number, start frame, end frame [exclusive])
SHOTS = [
    (1, 0, 76), (2, 76, 187), (3, 187, 303), (4, 303, 412),
    (5, 412, 543), (6, 543, 601), (7, 601, 685), (8, 685, 760),
    (9, 760, 837), (10, 837, 972), (11, 972, 1070), (12, 1070, 1188),
    (13, 1188, 1287), (14, 1287, 1410), (15, 1410, 1506),
]

# test frames: one per shot (mid-shot), for the Colab Eevee check
TEST_FRAMES = [40, 130, 245, 360, 480, 575, 645, 720, 800, 900,
               1020, 1130, 1240, 1350, 1460]


def set_x(shot_num):
    """World X of a shot set's centre."""
    return (shot_num - 1) * SET_SPACING


def load_rig2d():
    """Import shared/2d_rig.py via importlib (filename starts with a digit)."""
    here = os.path.dirname(os.path.abspath(__file__))
    shared = os.path.normpath(os.path.join(here, "..", "..", "shared"))
    spec = importlib.util.spec_from_file_location(
        "two_d_rig", os.path.join(shared, "2d_rig.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------- colour

def _srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hx(hexcol):
    """'#rrggbb' -> linear RGB tuple for Blender colour inputs."""
    h = hexcol.lstrip("#")
    return tuple(_srgb_to_linear(int(h[i:i + 2], 16) / 255.0)
                 for i in (0, 2, 4))


_mat_cache = {}


def flat_mat(name, hexcol, roughness=0.92):
    """Flat Principled material (Eevee + Cycles safe). Cached by name."""
    if name in _mat_cache:
        return _mat_cache[name]
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*hx(hexcol), 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Specular IOR Level"].default_value = 0.3
    mat.diffuse_color = (*hx(hexcol), 1.0)  # Workbench MATERIAL colour
    _mat_cache[name] = mat
    return mat


def emissive_mat(name, hexcol, strength=1.0, base_hexcol=None):
    """Principled material with an emission component (lamps, glints,
    sparks, screens). Keyframe strength with key_emission()."""
    if name in _mat_cache:
        return _mat_cache[name]
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (
        *hx(base_hexcol or hexcol), 1.0)
    bsdf.inputs["Emission Color"].default_value = (*hx(hexcol), 1.0)
    bsdf.inputs["Emission Strength"].default_value = strength
    bsdf.inputs["Roughness"].default_value = 0.6
    mat.diffuse_color = (*hx(hexcol), 1.0)
    _mat_cache[name] = mat
    return mat


def key_emission(mat, frame, strength):
    """Keyframe a Principled material's Emission Strength at one frame."""
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Emission Strength"].default_value = strength
    bsdf.inputs["Emission Strength"].keyframe_insert(
        data_path="default_value", frame=frame)


# ------------------------------------------------------------------- meshes

def _link(obj):
    bpy.context.collection.objects.link(obj)
    return obj


def _finish(obj, mat, parent, loc, rot):
    if parent is not None:
        obj.parent = parent
    obj.location = loc
    obj.rotation_euler = rot
    if mat is not None:
        obj.data.materials.append(mat)
    return obj


def _bake_scale(obj, sx, sy, sz):
    obj.data.transform(Matrix.Diagonal(Vector((sx, sy, sz, 1.0))))
    obj.data.update()


def _shade(obj, smooth=True):
    for p in obj.data.polygons:
        p.use_smooth = smooth


def new_empty(name, parent=None, loc=(0, 0, 0)):
    e = bpy.data.objects.new(name, None)
    e.empty_display_type = "PLAIN_AXES"
    e.empty_display_size = 0.08
    _link(e)
    if parent is not None:
        e.parent = parent
    e.location = loc
    return e


def add_box(name, dims, mat, parent=None, loc=(0, 0, 0), rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    _bake_scale(obj, dims[0], dims[1], dims[2])
    _shade(obj, False)
    return _finish(obj, mat, parent, loc, rot)


def add_sphere(name, r, mat, parent=None, loc=(0, 0, 0), rot=(0, 0, 0),
               scale=(1, 1, 1), seg=20, rings=14):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=seg, ring_count=rings, radius=r, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    _bake_scale(obj, *scale)
    _shade(obj, True)
    return _finish(obj, mat, parent, loc, rot)


def add_cylinder(name, r, depth, mat, parent=None, loc=(0, 0, 0),
                 rot=(0, 0, 0), verts=20):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=verts, radius=r, depth=depth, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    _shade(obj, True)
    return _finish(obj, mat, parent, loc, rot)


def add_cone(name, r1, r2, depth, mat, parent=None, loc=(0, 0, 0),
             rot=(0, 0, 0), verts=16):
    bpy.ops.mesh.primitive_cone_add(
        vertices=verts, radius1=r1, radius2=r2, depth=depth,
        location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    _shade(obj, True)
    return _finish(obj, mat, parent, loc, rot)


def add_torus(name, major_r, minor_r, mat, parent=None, loc=(0, 0, 0),
              rot=(0, 0, 0), scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_r, minor_radius=minor_r,
        major_segments=28, minor_segments=12, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    _bake_scale(obj, *scale)
    _shade(obj, True)
    return _finish(obj, mat, parent, loc, rot)


def add_plane(name, size, mat, parent=None, loc=(0, 0, 0), rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    return _finish(obj, mat, parent, loc, rot)


def add_point_light(name, loc, color_hex, energy):
    data = bpy.data.lights.new(name, type="POINT")
    data.color = hx(color_hex)
    data.energy = energy
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    return obj


def key_light_energy(light_obj, frame, energy):
    light_obj.data.energy = energy
    light_obj.data.keyframe_insert(data_path="energy", frame=frame)


# ---------------------------------------------------------------- keyframes

def kf(obj, frame, data_path="rotation_euler"):
    obj.keyframe_insert(data_path=data_path, frame=frame)


def set_linear(obj):
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"


def set_linear_range(obj, f_min, f_max):
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                if f_min <= kp.co.x <= f_max:
                    kp.interpolation = "LINEAR"


def set_bezier_range(obj, f_min, f_max):
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                if f_min <= kp.co.x <= f_max:
                    kp.interpolation = "BEZIER"


def loc_key(obj, frame, loc):
    obj.location = loc
    kf(obj, frame, "location")


def rot_key(obj, frame, rot):
    obj.rotation_euler = rot
    kf(obj, frame)


def scale_key(obj, frame, s):
    if isinstance(s, (int, float)):
        obj.scale = (s, s, s)
    else:
        obj.scale = s
    kf(obj, frame, "scale")


def scale_at(obj, frame, s):
    scale_key(obj, frame, s)


def visible_span(obj, f_start, f_end, base=1.0, fade_in=0, fade_out=0):
    """Object visible (scale=base) between f_start and f_end inclusive,
    hidden (scale 0.001) outside. Keys both sides of every transition."""
    if f_start > 0:
        scale_at(obj, f_start - 1, HIDDEN)
    if fade_in > 0:
        scale_at(obj, f_start, HIDDEN)
        scale_at(obj, f_start + fade_in, base)
    else:
        scale_at(obj, f_start, base)
    if fade_out > 0:
        scale_at(obj, f_end - fade_out, base)
        scale_at(obj, f_end, HIDDEN)
    else:
        scale_at(obj, f_end, base)
    if f_end < FRAME_END - 1:
        scale_at(obj, f_end + 1, HIDDEN)


def spin(obj, f_start, f_end, revolutions, axis="z", ease_out=False):
    """Spin an object about one local axis. Keys at both ends; LINEAR
    unless ease_out (decelerating spin — BEZIER with a flat end slope
    is approximated by an extra mid key)."""
    idx = {"x": 0, "y": 1, "z": 2}[axis]
    total = revolutions * 2 * math.pi
    obj.rotation_euler[idx] = 0.0
    kf(obj, f_start)
    if ease_out:
        mid = f_start + (f_end - f_start) * 2 // 3
        obj.rotation_euler[idx] = total * 0.85
        kf(obj, mid)
    obj.rotation_euler[idx] = total
    kf(obj, f_end)
    if not ease_out:
        set_linear_range(obj, f_start, f_end)


# -------------------------------------------------------------------- sets

def make_set(shot_num, ground_hex="#9db88a", backdrop_hex="#a8c8e8",
             ground_size=34.0):
    """Ground plane + sky backdrop for one shot set. Returns (ground,
    backdrop). The backdrop blocks the view behind the set so no
    neighbouring set is ever visible."""
    cx = set_x(shot_num)
    ground = add_plane("S%02d_Ground" % shot_num, ground_size,
                       flat_mat("M_Ground_S%02d" % shot_num, ground_hex),
                       loc=(cx, 0, 0))
    backdrop = add_plane("S%02d_Backdrop" % shot_num, 1.0,
                         flat_mat("M_Backdrop_S%02d" % shot_num,
                                  backdrop_hex),
                         loc=(cx, -16, 11),
                         rot=(math.radians(-90), 0, 0))
    backdrop.scale = (60.0, 26.0, 1.0)
    return ground, backdrop


# ------------------------------------------------------------------ camera

def _catmull_rom(p0, p1, p2, p3, u):
    return 0.5 * ((2 * p1) + (-p0 + p2) * u
                  + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u
                  + (-p0 + 3 * p1 - 3 * p2 + p3) * u * u * u)


def _sample_keys(pts, f):
    if f <= pts[0][0]:
        return pts[0][1], pts[0][2]
    if f >= pts[-1][0]:
        return pts[-1][1], pts[-1][2]
    i = next(i for i in range(len(pts) - 1)
             if pts[i][0] <= f < pts[i + 1][0])
    u = (f - pts[i][0]) / (pts[i + 1][0] - pts[i][0])
    p0 = pts[max(0, i - 1)][1]
    p1 = pts[i][1]
    p2 = pts[i + 1][1]
    p3 = pts[min(len(pts) - 1, i + 2)][1]
    loc = _catmull_rom(p0, p1, p2, p3, u)
    lens = pts[i][2] + (pts[i + 1][2] - pts[i][2]) * u
    return loc, lens


def build_shot_camera(name, cam_keys, focus_keys, f_start, f_end,
                      sample=3):
    """Build one marker-bound shot camera.

    cam_keys: [(frame, (x, y, z), lens_mm)] — Catmull-Rom path.
    focus_keys: [(frame, (x, y, z))] — Track-To focus path.
    f_end is INCLUSIVE (the shot's last rendered frame).
    Returns (camera object, focus empty).
    """
    cam_data = bpy.data.cameras.new(name)
    cam_data.lens = cam_keys[0][2]
    cam_data.sensor_fit = "VERTICAL"
    cam_data.sensor_width = 36
    cam_data.clip_start = 0.1
    cam_data.clip_end = 250
    cam = bpy.data.objects.new(name, cam_data)
    bpy.context.collection.objects.link(cam)
    focus = new_empty(name + "_Focus", loc=focus_keys[0][1])
    con = cam.constraints.new(type="TRACK_TO")
    con.target = focus
    con.track_axis = "TRACK_NEGATIVE_Z"
    con.up_axis = "UP_Y"

    pts = [(f, Vector(loc), lens) for f, loc, lens in cam_keys]
    fpts = [(f, Vector(loc), 0.0) for f, loc in focus_keys]
    frames = list(range(f_start, f_end + 1, sample))
    if frames[-1] != f_end:
        frames.append(f_end)
    for f in frames:
        loc, lens = _sample_keys(pts, f)
        cam.location = loc
        kf(cam, f, "location")
        cam_data.lens = lens
        cam_data.keyframe_insert(data_path="lens", frame=f)
        floc, _ = _sample_keys(fpts, f)
        focus.location = floc
        kf(focus, f, "location")
    set_linear(cam)
    set_linear(focus)
    if cam_data.animation_data and cam_data.animation_data.action:
        for fc in cam_data.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"
    return cam, focus
