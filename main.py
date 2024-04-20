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
    
    for i in sample._objects_names:
        print(i)



if __name__ == "__main__":
    main()
    Logger.task_done()
