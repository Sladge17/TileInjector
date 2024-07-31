from bpy.types import PropertyGroup
from bpy.props import StringProperty, FloatVectorProperty, BoolProperty, FloatProperty

from inputs import Inputs



class UI_Property(PropertyGroup):
    albedo_texture_0 : StringProperty(
        name=Inputs.albedo_texture_0.value,
        description="Path to tile albedo texture",
        subtype='FILE_PATH',
    )
    scale_albedo_0 : FloatProperty(
        name=Inputs.scale_albedo_0.value,
        description="Scale factor for tile albedo texture",
        default=1.0,
        min=0.001,
        soft_max=2.0,
        subtype='FACTOR',
    )    
    is_mask_texture_0 : BoolProperty(
        name=Inputs.is_mask_texture_0.value,
        description="Flag for usage texture",
        default=False,
    )
    mask_color_0 : FloatVectorProperty(
        name=Inputs.mask_color_0.value,
        description="Mixing textures color",
        default=(1.0, 0.1, 0.1),
        subtype='COLOR',
    )
    mask_texture_0 : StringProperty(
        name=Inputs.mask_texture_0.value,
        description="Mixing textures texture",
        subtype='FILE_PATH',
    )

    albedo_texture_1 : StringProperty(
        name=Inputs.albedo_texture_1.value,
        description="Path to tile albedo texture",
        subtype='FILE_PATH',
    )
    scale_albedo_1 : FloatProperty(
        name=Inputs.scale_albedo_1.value,
        description="Scale factor for tile albedo texture",
        default=1.0,
        min=0.001,
        soft_max=2.0,
        subtype='FACTOR',
    )    
    is_mask_texture_1 : BoolProperty(
        name=Inputs.is_mask_texture_1.value,
        description="Flag for usage texture",
        default=False,
    )
    mask_color_1 : FloatVectorProperty(
        name=Inputs.mask_color_1.value,
        description="Mixing textures color",
        default=(0.1, 1.0, 0.1),
        subtype='COLOR',
    )
    mask_texture_1 : StringProperty(
        name=Inputs.mask_texture_0.value,
        description="Mixing textures texture",
        subtype='FILE_PATH',
    )

    scale_albedo_2 : FloatProperty(
        name=Inputs.scale_albedo_2.value,
        description="Scale factor for tile albedo texture",
        default=1.0,
        min=0.001,
        soft_max=2.0,
        subtype='FACTOR',
    )    
    is_mask_texture_2 : BoolProperty(
        name=Inputs.is_mask_texture_2.value,
        description="Flag for usage texture",
        default=False,
    )
    mask_color_2 : FloatVectorProperty(
        name=Inputs.mask_color_2.value,
        description="Mixing textures color",
        default=(0.1, 0.1, 1.0),
        subtype='COLOR',
    )
    mask_texture_2 : StringProperty(
        name=Inputs.mask_texture_0.value,
        description="Mixing textures texture",
        subtype='FILE_PATH',
    )

    scale_albedo_3 : FloatProperty(
        name=Inputs.scale_albedo_3.value,
        description="Scale factor for tile albedo texture",
        default=1.0,
        min=0.001,
        soft_max=2.0,
        subtype='FACTOR',
    )    
    is_mask_texture_3 : BoolProperty(
        name=Inputs.is_mask_texture_3.value,
        description="Flag for usage texture",
        default=False,
    )
    mask_color_3 : FloatVectorProperty(
        name=Inputs.mask_color_3.value,
        description="Mixing textures color",
        default=(0.1, 0.1, 0.1),
        subtype='COLOR',
    )
    mask_texture_3 : StringProperty(
        name=Inputs.mask_texture_0.value,
        description="Mixing textures texture",
        subtype='FILE_PATH',
    )