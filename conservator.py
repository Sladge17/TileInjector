from bpy.types import PropertyGroup
from bpy.props import StringProperty, FloatProperty



class UI_Property(PropertyGroup):
    tile_albedo_0 : StringProperty(
        name = "tile_albedo",
        description = "Path to tile albedo texture",
    )
    tile_albedo_1 : StringProperty(
        name = "tile_albedo",
        description = "Path to tile albedo texture",
    )
    tile_albedo_2 : StringProperty(
        name = "tile_albedo",
        description = "Path to tile albedo texture",
    )
    tile_albedo_3 : StringProperty(
        name = "tile_albedo",
        description = "Path to tile albedo texture",
    )
    scale : FloatProperty(
        name = "scale",
        description = "Scale factor for tile textures",
        default = 1.0,
        min = 0.001,
        soft_max = 2.0,
        subtype = 'FACTOR',
    )
