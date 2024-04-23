from bpy.types import Operator
from os import path as osp

from sampler import Sampler
from logger import Logger
from material import Material



class MATERIAL_OT_tile_injector(Operator):
    bl_idname = 'material.tile_injector'
    bl_label = 'Tile Injector'
    extensions = ("png", "tga", "jpg", "bmp")


    @classmethod
    def poll(cls, context):
        if not context.object.mode == 'OBJECT':
            return False
        
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                return True
            
        return False


    @classmethod
    def _get_extensions(cls) -> tuple:
        return cls.extensions
    
    
    def _check_tex(self, path: str) -> bool:
        if not osp.isfile(path):
            print(f"ERROR: File {osp.basename(path)} not exist")
            return False
        
        if not osp.getsize(path):
            print(f"ERROR: File {osp.basename(path)} is empty")
            return False
        
        if not osp.basename(path).split('.')[1] in self._get_extensions():
            print(f"ERROR: File {osp.basename(path)} not a texture")
            return False
        
        return True


    @staticmethod
    def _get_path_normal(path_albedo: str) -> str:
        base_name = osp.basename(path_albedo).split('.')
        base_name = f"{base_name[0][:-1]}n.{base_name[1]}"
        return osp.join(osp.split(path_albedo)[0], base_name)


    def _check_texs(self):
        tile_albedo_0 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile0_a.tga"
        tile_albedo_1 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile1_a.tga"
        tile_albedo_2 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile2_a.tga"
        tile_albedo_3 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile3_a.tga"

        if not self._check_tex(tile_albedo_0):
            return False
        
        if not self._check_tex(tile_albedo_1):
            return False
        
        if not self._check_tex(tile_albedo_2):
            return False
        
        if not self._check_tex(tile_albedo_3):
            return False
        
        if not self._check_tex(self._get_path_normal(tile_albedo_0)):
            return False
        
        if not self._check_tex(self._get_path_normal(tile_albedo_1)):
            return False
        
        if not self._check_tex(self._get_path_normal(tile_albedo_2)):
            return False
        
        if not self._check_tex(self._get_path_normal(tile_albedo_3)):
            return False

        return True    
    
    
    def execute(self, context):
        sample = Sampler()\
            .set_filter_by_type(target_type='MESH')\
            .check_uv(channels=2)
        if not sample.length:
            Logger.empty_sample()
            return {'CANCELLED'}
        
        if not self._check_texs():
            return {'CANCELLED'}
        
        
        tile_albedo_0 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile0_a.tga"
        tile_albedo_1 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile1_a.tga"
        tile_albedo_2 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile2_a.tga"
        tile_albedo_3 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile3_a.tga"

        tiles = (
            (tile_albedo_0, self._get_path_normal(tile_albedo_0)),
            (tile_albedo_1, self._get_path_normal(tile_albedo_1)),
            (tile_albedo_2, self._get_path_normal(tile_albedo_2)),
            (tile_albedo_3, self._get_path_normal(tile_albedo_3)),
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
    