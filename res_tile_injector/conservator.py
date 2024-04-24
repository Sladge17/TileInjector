from bpy.types import PropertyGroup
from bpy.props import StringProperty, FloatProperty

from .inputs import Imputs



class UI_Property(PropertyGroup):
    tile_albedo_0 : StringProperty(
        name=Imputs.tile_albedo_0.value,
        description="Path to tile albedo texture",
        subtype='FILE_PATH',
    )
    tile_albedo_1 : StringProperty(
        name=Imputs.tile_albedo_1.value,
        description="Path to tile albedo texture",
        subtype='FILE_PATH',
    )
    tile_albedo_2 : StringProperty(
        name=Imputs.tile_albedo_2.value,
        description="Path to tile albedo texture",
        subtype='FILE_PATH',
    )
    tile_albedo_3 : StringProperty(
        name=Imputs.tile_albedo_3.value,
        description = "Path to tile albedo texture",
        subtype='FILE_PATH',
    )
    scale : FloatProperty(
        name=Imputs.scale.value,
        description="Scale factor for tile textures",
        default=1.0,
        min=0.001,
        soft_max=2.0,
        subtype='FACTOR',
    )
