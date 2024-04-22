import os
import sys
sys.path.append(os.environ['SCRIPT_PATH'])

import bpy
from bpy.utils import register_class, unregister_class

from sampler import Sampler
from logger import Logger
from material import Material
from interface import VIEW3D_PT_tile_injector
from executor import MESH_OT_tile_injector



def register():
    register_class(VIEW3D_PT_tile_injector)


def unregister():
    unregister_class(VIEW3D_PT_tile_injector)





def main():
    sample = Sampler()\
        .set_filter_by_type(target_type='MESH')\
        .check_uv(channels=2)
    if not sample.length:
        Logger.empty_sample()
        return
    
    material = Material(
        donor=sample.first_name,
        name="MODE_Material",
    ).fix_tex_normal().set_tex_tile()
    sample.set_material(material=material)



if __name__ == "__main__":
    register()
    # main()
    Logger.task_done()
