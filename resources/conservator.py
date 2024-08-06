from bpy.types import PropertyGroup
from bpy.props import (
    StringProperty,
    FloatProperty,
    BoolProperty,
    FloatVectorProperty,
)

from .inputs import Inputs
from .properties_updater import PropertiesUpdater



class UI_Property(PropertyGroup):
    albedo_texture_0 : StringProperty(
        name=Inputs.albedo_texture_0.value,
        description="Path to tile albedo texture",
        subtype='FILE_PATH',
        update=PropertiesUpdater.update_albedo_texture_0,
    )
    is_preview_albedo_0 : BoolProperty(
        name=Inputs.is_preview_albedo_0.value,
        description="Flag for preview albedo texture",
        default=True,
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
        update=PropertiesUpdater.update_mask_texture_0,
    )
    is_preview_mask_0 : BoolProperty(
        name=Inputs.is_preview_mask_0.value,
        description="Flag for preview mask texture",
        default=False,
    )
    scale_mask_0 : FloatProperty(
        name=Inputs.scale_mask_0.value,
        description="Scale factor for tile mask texture",
        default=1.0,
        min=0.001,
        soft_max=2.0,
        subtype='FACTOR',
    )

    albedo_texture_1 : StringProperty(
        name=Inputs.albedo_texture_1.value,
        description="Path to tile albedo texture",
        subtype='FILE_PATH',
        update=PropertiesUpdater.update_albedo_texture_1,
    )
    is_preview_albedo_1 : BoolProperty(
        name=Inputs.is_preview_albedo_1.value,
        description="Flag for preview albedo texture",
        default=True,
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
        name=Inputs.mask_texture_1.value,
        description="Mixing textures texture",
        subtype='FILE_PATH',
        update=PropertiesUpdater.update_mask_texture_1,
    )
    is_preview_mask_1 : BoolProperty(
        name=Inputs.is_preview_mask_1.value,
        description="Flag for preview mask texture",
        default=False,
    )
    scale_mask_1 : FloatProperty(
        name=Inputs.scale_mask_1.value,
        description="Scale factor for tile mask texture",
        default=1.0,
        min=0.001,
        soft_max=2.0,
        subtype='FACTOR',
    )

    albedo_texture_2 : StringProperty(
        name=Inputs.albedo_texture_2.value,
        description="Path to tile albedo texture",
        subtype='FILE_PATH',
        update=PropertiesUpdater.update_albedo_texture_2,
    )
    is_preview_albedo_2 : BoolProperty(
        name=Inputs.is_preview_albedo_2.value,
        description="Flag for preview albedo texture",
        default=True,
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
        name=Inputs.mask_texture_2.value,
        description="Mixing textures texture",
        subtype='FILE_PATH',
        update=PropertiesUpdater.update_mask_texture_2,
    )
    is_preview_mask_2 : BoolProperty(
        name=Inputs.is_preview_mask_2.value,
        description="Flag for preview mask texture",
        default=False,
    )
    scale_mask_2 : FloatProperty(
        name=Inputs.scale_mask_2.value,
        description="Scale factor for tile mask texture",
        default=1.0,
        min=0.001,
        soft_max=2.0,
        subtype='FACTOR',
    )

    albedo_texture_3 : StringProperty(
        name=Inputs.albedo_texture_3.value,
        description="Path to tile albedo texture",
        subtype='FILE_PATH',
        update=PropertiesUpdater.update_albedo_texture_3,
    )
    is_preview_albedo_3 : BoolProperty(
        name=Inputs.is_preview_albedo_3.value,
        description="Flag for preview albedo texture",
        default=True,
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
        name=Inputs.mask_texture_3.value,
        description="Mixing textures texture",
        subtype='FILE_PATH',
        update=PropertiesUpdater.update_mask_texture_3,
    )
    is_preview_mask_3 : BoolProperty(
        name=Inputs.is_preview_mask_3.value,
        description="Flag for preview mask texture",
        default=False,
    )
    scale_mask_3 : FloatProperty(
        name=Inputs.scale_mask_3.value,
        description="Scale factor for tile mask texture",
        default=1.0,
        min=0.001,
        soft_max=2.0,
        subtype='FACTOR',
    )
