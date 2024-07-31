from bpy.types import Operator

from sampler import Sampler
from validator import Validator
from logger import Logger
from group_mix_by_color import Group_MixByColor
from material import Material



class MATERIAL_OT_tile_injector(Operator):
    bl_idname = 'material.tile_injector'
    bl_label = 'Tile Injector'


    @classmethod
    def poll(cls, context):
        if not context.object.mode == 'OBJECT':
            return False
        
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                return True
            
        return False


    def _get_mix_colors(self, context) -> tuple:
        return (
            list(context.scene.tile_injector.mix_color_0) + [1.0],
            list(context.scene.tile_injector.mix_color_1) + [1.0],
            list(context.scene.tile_injector.mix_color_2) + [1.0],
            list(context.scene.tile_injector.mix_color_3) + [1.0],        
        )


    def _get_is_mask_texture(self, context):
        return (
            context.scene.tile_injector.is_mask_texture_0,
            context.scene.tile_injector.is_mask_texture_1,
            context.scene.tile_injector.is_mask_texture_2,
            context.scene.tile_injector.is_mask_texture_3,
            
        )
    
    
    def execute(self, context):
        sample = Sampler()\
            .set_filter_by_type(target_type='MESH')\
            .check_uv(channels=2)
        if not sample.length:
            Logger.empty_sample()
            return {'CANCELLED'}
        

        # is_mask_texture = self._get_is_mask_texture(context)
        # print(is_mask_texture)
        # return {'FINISHED'}


        tiles = Validator.get_tiles(context)
        if not tiles:
            return {'CANCELLED'}  


        
        Group_MixByColor.init_group()
        material = Material(
            donor=sample.first_name,
            name="TILED_Material",
        ).fix_tex_normal().set_tex_tile(
            tiles=tiles,
            mix_colors=self._get_mix_colors(context),
            scale=context.scene.tile_injector.scale,
        )
        sample.set_material(material=material)
        Logger.task_done()
        return {'FINISHED'}
    