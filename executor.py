from bpy.types import Operator

from sampler import Sampler
from validator import Validator
from loger import Loger
from group_mix_by_color import Group_MixByColor
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
        
        scales = Validator.get_scales(context)
        is_masks_texture = Validator.get_is_masks_texture(context)
        masks = Validator.get_masks(context, is_masks_texture)
        if not masks:
            return {'CANCELLED'}

        Group_MixByColor.init_group()
        material = Material(
            name_suffix="TILED",
        ).fix_tex_normal().set_tex_tile(
            tiles=tiles,
            scales=scales,
            is_masks_texture=is_masks_texture,
            masks=masks,
        )
        Loger.created_material(material.material_name)
        sample.set_material(material=material.material)
        return {'FINISHED'}
    