import os
import sys
sys.path.append(os.environ['SCRIPT_PATH'])


from bpy.types import Object
from bpy.props import PointerProperty
from bpy.utils import register_class, unregister_class

from executor import Property, MATERIAL_OT_tile_injector
from interface import VIEW3D_PT_tile_injector



def register():
    register_class(Property)
    register_class(MATERIAL_OT_tile_injector)
    register_class(VIEW3D_PT_tile_injector)
    Object.tile_injector = PointerProperty(type=Property)


def unregister():
    unregister_class(Property)
    unregister_class(MATERIAL_OT_tile_injector)
    unregister_class(VIEW3D_PT_tile_injector)



if __name__ == "__main__":
    register()
