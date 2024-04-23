from bpy.types import Operator
from bpy.path import abspath
from os import path as osp

from sampler import Sampler
from logger import Logger
from material import Material
from inputs import Imputs



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
    
    
    def _check_tex(self, path: str, slot: str) -> bool:
        if not path:
            Logger.empty_path(slot)
            return False

        if not osp.isfile(path):
            Logger.file_not_exist(osp.basename(path), slot)
            return False
        
        if not osp.getsize(path):
            Logger.file_empty(osp.basename(path), slot)
            return False
        
        if not osp.basename(path).split('.')[1] in self._get_extensions():
            Logger.file_not_texture(osp.basename(path), slot)
            return False
        
        return True


    @staticmethod
    def _get_path_normal(path_albedo: str) -> str:
        base_name = osp.basename(path_albedo).split('.')
        base_name = f"{base_name[0][:-1]}n.{base_name[1]}"
        return osp.join(osp.split(path_albedo)[0], base_name)


    def _check_texs(self, context):
        # tile_albedo_0 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile0_a.tga"
        # tile_albedo_1 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile1_a.tga"
        # tile_albedo_2 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile2_a.tga"
        # tile_albedo_3 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile3_a.tga"


        # /home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile0_a.tga

        # print(abspath(context.object.tile_injector.tile_albedo_0))

        if not self._check_tex(
            abspath(context.object.tile_injector.tile_albedo_0),
            Imputs.tile_albedo_0.value,
        ):
            return False
        
        if not self._check_tex(
            abspath(context.object.tile_injector.tile_albedo_1),
            Imputs.tile_albedo_1.value,
        ):
            return False
        
        if not self._check_tex(
            abspath(context.object.tile_injector.tile_albedo_2),
            Imputs.tile_albedo_2.value,
        ):
            return False
        
        if not self._check_tex(
            abspath(context.object.tile_injector.tile_albedo_3),
            Imputs.tile_albedo_3.value,
        ):
            return False
        
        if not self._check_tex(
            abspath(self._get_path_normal(context.object.tile_injector.tile_albedo_0)),
            Imputs.tile_albedo_0.value,
        ):
            return False
        
        if not self._check_tex(
            abspath(self._get_path_normal(context.object.tile_injector.tile_albedo_1)),
            Imputs.tile_albedo_1.value,
        ):
            return False
        
        if not self._check_tex(
            abspath(self._get_path_normal(context.object.tile_injector.tile_albedo_2)),
            Imputs.tile_albedo_2.value,
        ):
            return False
        
        if not self._check_tex(
            abspath(self._get_path_normal(context.object.tile_injector.tile_albedo_3)),
            Imputs.tile_albedo_3.value,
        ):
            return False

        return True    
    
    
    def execute(self, context):
        sample = Sampler()\
            .set_filter_by_type(target_type='MESH')\
            .check_uv(channels=2)
        if not sample.length:
            Logger.empty_sample()
            return {'CANCELLED'}
        
        if not self._check_texs(context):
            return {'CANCELLED'}
        
        
        # tile_albedo_0 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile0_a.tga"
        # tile_albedo_1 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile1_a.tga"
        # tile_albedo_2 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile2_a.tga"
        # tile_albedo_3 = "/home/maxim/Projects/LestaTest/Textures/Tile_textures/Tile3_a.tga"

        # //Textures/Tile_textures/Tile0_a.tga

        tiles = (
            (
                abspath(context.object.tile_injector.tile_albedo_0),
                abspath(self._get_path_normal(context.object.tile_injector.tile_albedo_0)),
            ),
            (
                abspath(context.object.tile_injector.tile_albedo_1),
                abspath(self._get_path_normal(context.object.tile_injector.tile_albedo_1)),
            ),
            (
                abspath(context.object.tile_injector.tile_albedo_2),
                abspath(self._get_path_normal(context.object.tile_injector.tile_albedo_2)),
            ),
            (
                abspath(context.object.tile_injector.tile_albedo_3),
                abspath(self._get_path_normal(context.object.tile_injector.tile_albedo_3)),
            ),
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
    