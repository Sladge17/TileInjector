from bpy.types import Operator

from .sampler import Sampler
from .validator import Validator
from .loger import Loger
from .material import Material

from .node_groups import (
    Group_MixByColor,
    Group_MixByIntensity_N,
    Group_Color2MidFloat,
)



class MATERIAL_OT_tile_injector(Operator):
    bl_idname = 'material.tile_injector'
    bl_label = 'Tile Injector'


    @classmethod
    def poll(cls, context):
        if not context.object.mode == 'OBJECT':
            return False

        return True
    

    @classmethod
    def _set_environment(cls):
        Group_MixByColor.set_group()
        Group_MixByIntensity_N.set_group()
        Group_Color2MidFloat.set_group()


    def execute(self, context):
        self._set_environment()

        sample = Sampler()\
            .set_filter_by_type(target_type='MESH')\
            .check_uv(channels=2)
        if not sample.length:
            Loger.empty_sample()
            return {'CANCELLED'}
        
        if not context.active_object.type == 'MESH':
            Loger.invalid_active_object(target_type='MESH')
            return {'CANCELLED'}

        tiles = Validator.get_tiles(context)
        if not tiles:
            return {'CANCELLED'}
        
        is_masks_texture = Validator.get_is_masks_texture(context)
        masks = Validator.get_masks(context, is_masks_texture)
        if not masks:
            return {'CANCELLED'}
        
        material = Material(
            name_suffix="TILED",
        ).fix_tex_uniq_color_space().set_tex_tile(
            tiles=tiles,
            tiles_scale=Validator.get_tiles_scale(context),
            is_masks_texture=is_masks_texture,
            masks=masks,
            masks_scale=Validator.get_masks_scale(context),
        )
        Loger.created_material(material.material_name)
        sample.set_material(material=material.material)
        return {'FINISHED'}
    