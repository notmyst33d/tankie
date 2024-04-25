import sys
import bpy
from math import radians

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=sys.argv[-1])

for model in bpy.data.objects["<3DSRoot>"].children:
    model.parent = None
    model.rotation_mode = "XYZ"
    model.rotation_euler.x = radians(-90)

    with bpy.context.temp_override(selected_editable_objects=[model]):
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

bpy.data.objects.remove(bpy.data.objects["<3DSRoot>"], do_unlink=True)

for image in bpy.data.images:
    path = image.filepath.split("/")
    path[-1] = path[-1].lower()
    image.filepath = "/".join(path)

bpy.ops.export_scene.gltf(filepath=sys.argv[-1])
