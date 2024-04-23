from bpy.types import Operator

from sampler import Sampler
from logger import Logger
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


    def execute(self, context):
        sample = Sampler()\
            .set_filter_by_type(target_type='MESH')\
            .check_uv(channels=2)
        if not sample.length:
            Logger.empty_sample()
            return {'CANCELLED'}
        
        tile_albedo_0 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile0_a.tga"
        tile_normal_0 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile0_n.tga"
        tile_albedo_1 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile1_a.tga"
        tile_normal_1 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile1_n.tga"
        tile_albedo_2 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile2_a.tga"
        tile_normal_2 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile2_n.tga"
        tile_albedo_3 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile3_a.tga"
        tile_normal_3 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile3_n.tga"

        tiles = (
            (tile_albedo_0, tile_normal_0),
            (tile_albedo_1, tile_normal_1),
            (tile_albedo_2, tile_normal_2),
            (tile_albedo_3, tile_normal_3),
        )
        
        material = Material(
            donor=sample.first_name,
            name="TILED_Material",
        ).fix_tex_normal().set_tex_tile(
            tiles=tiles,
            scale=context.object.tile_injector.scale,
        )
        sample.set_material(material=material)
        Logger.task_done()
        return {'FINISHED'}
    