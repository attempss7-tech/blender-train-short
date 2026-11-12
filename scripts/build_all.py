# build_all.py — master build for the V3 train short (Blender 4.2.23).
#
# Builds all 15 shots in ONE scene on ONE 1506-frame timeline (frames
# 0-1505), each shot its own set at x = (shot-1)*40 with its own
# marker-bound camera. 2D flat humans via shared/2d_rig.py; all 3D
# objects own-built in bpy. Saves scenes/train.blend (BLENDER_EEVEE_NEXT,
# 1080x1920, 30 fps).
#
# Run from ~/workspace/blender_shorts_4/v3_train:
#   ~/workspace/blender_chicken/tools/blender-4.2.23-linux-x64/blender \
#       --background --python scripts/build_all.py
import os
import sys
import time

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import common as cm  # noqa: E402
import shots_a  # noqa: E402
import shots_b  # noqa: E402
import shots_c  # noqa: E402

SHOTS = [
    shots_a.build_s01, shots_a.build_s02, shots_a.build_s03,
    shots_a.build_s04, shots_a.build_s05, shots_b.build_s06,
    shots_b.build_s07, shots_b.build_s08, shots_b.build_s09,
    shots_b.build_s10, shots_c.build_s11, shots_c.build_s12,
    shots_c.build_s13, shots_c.build_s14, shots_c.build_s15,
]


def build_lights():
    """One sun + sky world for the whole timeline. Shadows OFF: the sets
    span 560 m on X (a sun shadow frustum cannot cover them all) and the
    flat cartoon look does not need them."""
    world = bpy.data.worlds.new("Sky")
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (*cm.hx("#a8c8e8"), 1.0)
    bg.inputs["Strength"].default_value = 1.0
    bpy.context.scene.world = world

    bpy.ops.object.light_add(type="SUN", location=(280, 30, 40))
    sun = bpy.context.active_object
    sun.name = "Sun"
    sun.data.energy = 3.0
    sun.data.color = (1.0, 0.96, 0.88)
    sun.data.use_shadow = False
    # light the camera-facing (+Y) sides: direction (0,-1,-1)
    sun.rotation_euler = (Vector((0, -1, -1))
                          .to_track_quat("-Z", "Y").to_euler())
    return sun


def main():
    t0 = time.time()
    bpy.ops.wm.read_factory_settings(use_empty=True)

    build_lights()
    rig2d = cm.load_rig2d()
    ctx = dict(rig2d=rig2d)

    cameras = []  # (marker frame, camera object)
    for i, fn in enumerate(SHOTS, start=1):
        ts = time.time()
        info = fn(ctx)
        cameras.extend(info["cameras"])
        print("  shot %02d built in %.1fs" % (i, time.time() - ts))

    # ---- markers + camera binding (hard cuts)
    scene = bpy.context.scene
    for frame, cam in sorted(cameras):
        m = scene.timeline_markers.new(name="Shot_%04d" % frame,
                                       frame=frame)
        m.camera = cam
    scene.camera = sorted(cameras)[0][1]

    # ---- scene settings (final: 1080x1920, 30 fps, Eevee on Colab GPU)
    scene.frame_start = 0
    scene.frame_end = 1505
    scene.render.fps = 30
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1920
    scene.render.resolution_percentage = 100
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.image_settings.file_format = "PNG"

    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.normpath(os.path.join(here, "..", "scenes",
                                        "train.blend"))
    bpy.ops.wm.save_as_mainfile(filepath=out)

    n_mesh = sum(1 for o in scene.objects if o.type == "MESH")
    n_gp = sum(1 for o in scene.objects if o.type == "GPENCIL")
    n_all = len(scene.objects)
    n_poly = sum(len(o.data.polygons) for o in scene.objects
                 if o.type == "MESH")
    n_actions = len(bpy.data.actions)
    print("BUILD ALL OK in %.1fs: %d objects (%d meshes, %d GP), "
          "%d polys, %d actions, %d cameras, frames 0-1505"
          % (time.time() - t0, n_all, n_mesh, n_gp, n_poly, n_actions,
             len(cameras)))
    print("saved:", out)


if __name__ == "__main__":
    main()
