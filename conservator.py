from bpy.types import PropertyGroup
from bpy.props import StringProperty, FloatVectorProperty, FloatProperty

from inputs import Inputs



class UI_Property(PropertyGroup):
    tile_albedo_0 : StringProperty(
        name=Inputs.tile_albedo_0.value,
        description="Path to tile albedo texture",
        subtype='FILE_PATH',
    )
    mix_color_0 :FloatVectorProperty(
        name=Inputs.mix_color_0.value,
        description="Mixing textures color",
        default=(1.0, 0.1, 0.1),
        subtype='COLOR',
    )

    tile_albedo_1 : StringProperty(
        name=Inputs.tile_albedo_1.value,
        description="Path to tile albedo texture",
        subtype='FILE_PATH',
    )
    mix_color_1 :FloatVectorProperty(
        name=Inputs.mix_color_1.value,
        description="Mixing textures color",
        default=(0.1, 1.0, 0.1),
        subtype='COLOR',
    )

    tile_albedo_2 : StringProperty(
        name=Inputs.tile_albedo_2.value,
        description="Path to tile albedo texture",
        subtype='FILE_PATH',
    )
    mix_color_2 :FloatVectorProperty(
        name=Inputs.mix_color_2.value,
        description="Mixing textures color",
        default=(0.1, 0.1, 1.0),
        subtype='COLOR',
    )

    tile_albedo_3 : StringProperty(
        name=Inputs.tile_albedo_3.value,
        description = "Path to tile albedo texture",
        subtype='FILE_PATH',
    )
    mix_color_3 :FloatVectorProperty(
        name=Inputs.mix_color_3.value,
        description="Mixing textures color",
        default=(0.1, 0.1, 0.1),
        subtype='COLOR',
    )

    scale : FloatProperty(
        name=Inputs.scale.value,
        description="Scale factor for tile textures",
        default=1.0,
        min=0.001,
        soft_max=2.0,
        subtype='FACTOR',
    )
