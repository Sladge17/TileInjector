from bpy.types import Operator

from sampler import Sampler
from validator import Validator
from loger import Loger
from material import Material



class MATERIAL_OT_tile_injector(Operator):
    bl_idname = 'material.tile_injector'
    bl_label = 'Tile Injector'


    @classmethod
    def poll(cls, context):
        if not context.object.mode == 'OBJECT':
            return False
        
        if not context.active_object.type == 'MESH':
            return False
        
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                return True
            
        return False


    def execute(self, context):
        sample = Sampler()\
            .set_filter_by_type(target_type='MESH')\
            .check_uv(channels=2)
        if not sample.length:
            Loger.empty_sample()
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
    