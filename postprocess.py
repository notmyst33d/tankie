import os
import sys
import bpy
import bmesh
from math import radians

texture = os.environ.get("TEXTURE", "")
normal_map = os.environ.get("NORMAL_MAP", "")

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=sys.argv[-1])

for image in bpy.data.images:
    path = image.filepath.split("/")
    path[-1] = path[-1].lower()
    if os.path.isfile(texture):
        print(f"Using texture: {texture}")
        path = texture.split("/")
    image.filepath = "/".join(path)

for model in bpy.data.objects["<3DSRoot>"].children:
    model.parent = None
    model.rotation_mode = "XYZ"
    model.rotation_euler.x = radians(-90)

    with bpy.context.temp_override(selected_editable_objects=[model]):
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        bpy.ops.object.shade_smooth()

    bm = bmesh.new()
    bm.from_mesh(model.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.01)
    bm.to_mesh(model.data)
    model.data.update()
    bm.clear()

    if os.path.isfile(normal_map):
        print(f"Using normal map: {normal_map}")
        bpy.data.images.load(normal_map)

        node_tree = model.material_slots[0].material.node_tree
        normal_map = node_tree.nodes.new("ShaderNodeNormalMap")
        normal_map_texture = node_tree.nodes.new("ShaderNodeTexImage")
        principled_bsdf = node_tree.nodes["Principled BSDF"]

        normal_map_texture.image = bpy.data.images[normal_map.split("/")[-1]]
        node_tree.links.new(normal_map_texture.outputs["Color"], normal_map.inputs["Color"])
        node_tree.links.new(normal_map.outputs["Normal"], principled_bsdf.inputs["Normal"])

bpy.data.objects.remove(bpy.data.objects["<3DSRoot>"], do_unlink=True)

bpy.ops.export_scene.gltf(filepath=sys.argv[-1])
