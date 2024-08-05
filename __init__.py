from bpy.types import Scene
from bpy.props import PointerProperty
from bpy.utils import register_class, unregister_class

from conservator import UI_Property
from executor import MATERIAL_OT_tile_injector
from interface import VIEW3D_PT_tile_injector

from group_mix_by_color import Group_MixByColor



def set_environment():
    Group_MixByColor.set_group()


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



bl_info = {
    "name": "Tile Injector",
    "author": "Sosov Maxim",
    "version": (1, 0),
    "blender": (3, 3, 0),
    "category": "Material",
    "location": "View3D > UI > MaterialHelpers",
    "description": "Inject tile patterns to selected meshes materials from selected textures",
    "warning": "",
    "wiki_url": "https://github.com/Sladge17/TileInjector",
}



if __name__ == "__main__":
    set_environment()
    register()
