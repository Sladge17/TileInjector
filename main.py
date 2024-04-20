import bpy
import os
import sys
sys.path.append(os.environ['SCRIPT_PATH'])

from sampler import Sampler
from logger import Logger
from material import Material



def main():
    sample = Sampler()\
        .set_filter_by_type(target_type='MESH')\
        .check_uv(channels=2)
    if not sample.length:
        Logger.empty_sample()
        return

    mat = Material(
        shader='ShaderNodeBsdfPrincipled',
        name="MatMixedTexture",
    ).set_target_shader()
    for obj_name in sample._objects_names:
         bpy.data.meshes[obj_name].materials.clear()
         bpy.data.meshes[obj_name].materials.append(mat.material)



if __name__ == "__main__":
    main()
    Logger.task_done()
