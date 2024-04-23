import os
import sys
sys.path.append(os.environ['SCRIPT_PATH'])


from bpy.types import Scene
from bpy.props import PointerProperty
from bpy.utils import register_class, unregister_class

from conservator import UI_Property
from executor import MATERIAL_OT_tile_injector
from interface import VIEW3D_PT_tile_injector



def register():
    register_class(UI_Property)
    register_class(MATERIAL_OT_tile_injector)
    register_class(VIEW3D_PT_tile_injector)
    Scene.tile_injector = PointerProperty(type=UI_Property)


def unregister():
    del Scene.tile_injector
    unregister_class(VIEW3D_PT_tile_injector)
    unregister_class(MATERIAL_OT_tile_injector)
    unregister_class(UI_Property)



if __name__ == "__main__":
    register()
