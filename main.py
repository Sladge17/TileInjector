import bpy
import os
import sys
sys.path.append(os.environ['SCRIPT_PATH'])

from sampler import Sampler
from logger import Logger
from material import Material, check_donor_soft



def main():
    sample = Sampler()\
        .set_filter_by_type(target_type='MESH')\
        .check_uv(channels=2)
    if not sample.length:
        Logger.empty_sample()
        return
    
    if not check_donor_soft(sample.first_name):
        return

    material = Material(
        donor=sample.first_name,
        name="MODE_Material",
    ).fix_tex_normal()
    sample.set_material(material=material)



if __name__ == "__main__":
    main()
    Logger.task_done()
