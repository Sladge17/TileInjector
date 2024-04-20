import bpy
import os
import sys
sys.path.append(os.environ['SCRIPT_PATH'])

from sampler import Sampler
from logger import Logger



def main():
    sample = Sampler()
    sample.set_filter_by_type('MESH')
    if not sample.length:
        Logger.empty_sample()
        return
    
    for i in sample._objects_names:
        print(i)



if __name__ == "__main__":
    main()
    Logger.task_done()



# bpy.data.meshes['Cube.004'].uv_layers.values()