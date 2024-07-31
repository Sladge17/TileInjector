from bpy.path import abspath
from os import path as osp

from logger import Logger
from inputs import Inputs



class Validator:
    extensions = ("png", "tga", "jpg", "bmp")


    @classmethod
    def _get_extensions(cls) -> tuple:
        return cls.extensions
    
    
    @classmethod
    def _check_tex(cls, path: str, slot: str) -> bool:
        if not path:
            Logger.empty_path(slot)
            return False

        if not osp.isfile(path):
            Logger.file_not_exist(osp.basename(path), slot)
            return False
        
        if not osp.getsize(path):
            Logger.file_empty(osp.basename(path), slot)
            return False
        
        if not osp.basename(path).split('.')[1] in cls._get_extensions():
            Logger.file_not_image(osp.basename(path), slot)
            return False
        
        return True
    

    @classmethod
    def _get_path_normal(cls, path_albedo: str) -> str:
        if not path_albedo:
            return path_albedo

        base_name = osp.basename(path_albedo).split('.')
        base_name = f"{base_name[0][:-1]}n.{base_name[1]}"
        return osp.join(osp.split(path_albedo)[0], base_name)


    @classmethod
    def get_tiles(cls, context) -> list:
        tiles = [[None] * 2] * 4
        for slot in range(4):
            path_albedo = getattr(context.scene.tile_injector, f"albedo_texture_{slot}")
            path_normal = abspath(cls._get_path_normal(path_albedo))
            path_albedo = abspath(path_albedo)
            if not cls._check_tex(path_albedo, slot) or\
                not cls._check_tex(path_normal, slot):
                return None
            
            tiles[slot][0] = path_albedo
            tiles[slot][1] = path_normal

        return tiles