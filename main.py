import bpy
import os
import sys
sys.path.append(os.environ['SCRIPT_PATH'])

from sampler import Sampler
from logger import Logger



def main():
    # sample = Sampler()\
    #     .set_filter_by_type(target_type='MESH')\
    #     .check_uv(channels=2)
    # if not sample.length:
    #     Logger.empty_sample()
    #     return
    
    # for i in sample._objects_names:
    #     print(i)



    material_name = "MatMixedTexture"
    try:
        bpy.data.materials.remove(bpy.data.materials.get(material_name))
        Logger.remove_material(material_name)
    except TypeError:
        pass
    mat = bpy.data.materials.new(material_name)





if __name__ == "__main__":
    main()
    Logger.task_done()
