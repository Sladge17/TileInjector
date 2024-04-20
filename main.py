import bpy
import os
import sys
sys.path.append(os.environ['SCRIPT_PATH'])

from sampler import Sampler
from logger import Logger



def main():
    sample = Sampler()\
        .set_filter_by_type(target_type='MESH')\
        .check_uv(channels=2)
    if not sample.length:
        Logger.empty_sample()
        return




    material_name = "MatMixedTexture"
    try:
        bpy.data.materials.remove(bpy.data.materials.get(material_name))
        Logger.remove_material(material_name)
    except TypeError:
        pass
    mat = bpy.data.materials.new(material_name)

    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    for node in nodes:
        nodes.remove(node)

    node_rgb= nodes.new(type='ShaderNodeRGB')
    node_rgb.outputs[0].default_value = (1, 0, 0, 1)
    node_rgb.location = (-300, 0)



    node_BSDFprincipled = nodes.new(type='ShaderNodeBsdfPrincipled')
    links.new(node_rgb.outputs[0], node_BSDFprincipled.inputs[0])
    node_BSDFprincipled.location = (0, 0)


    node_output = nodes.new('ShaderNodeOutputMaterial')
    links.new(node_BSDFprincipled.outputs[0], node_output.inputs[0])
    node_output.location = (300, 0)


    for obj_name in sample._objects_names:
         bpy.data.meshes[obj_name].materials.clear()
         bpy.data.meshes[obj_name].materials.append(mat)




if __name__ == "__main__":
    main()
    Logger.task_done()
