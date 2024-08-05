from bpy.path import abspath
from os import path as osp

from loger import Loger
from inputs import Inputs



class Validator:
    extensions = ("png", "tga", "jpg", "bmp")


    @classmethod
    def _get_extensions(cls) -> tuple:
        return cls.extensions
    
    
    @classmethod
    def _check_texture(cls, path: str, field: str, slot: int) -> bool:
        if not path:
            Loger.empty_path(field, slot)
            return False

        if not osp.isfile(path):
            Loger.file_not_exist(osp.basename(path), field, slot)
            return False
        
        if not osp.getsize(path):
            Loger.file_empty(osp.basename(path), field, slot)
            return False
        
        if not osp.basename(path).split('.')[1] in cls._get_extensions():
            Loger.file_not_image(osp.basename(path), field, slot)
            return False
        
        return True
    

    @classmethod
    def _get_path_normal(cls, path_albedo: str) -> str:
        base_name = osp.basename(path_albedo).split('.')
        base_name = f"{base_name[0][:-1]}n.{base_name[1]}"
        return osp.join(osp.split(path_albedo)[0], base_name)


    @classmethod
    def get_tiles(cls, context) -> list:
        tiles = [[None] * 2 for _ in range(4)]
        for slot in range(4):
            field = getattr(Inputs, f"albedo_texture_{slot}").value
            path_albedo = getattr(context.scene.tile_injector, f"albedo_texture_{slot}")
            if not cls._check_texture(
                abspath(path_albedo),
                field,
                slot,
            ) or not cls._check_texture(
                abspath(cls._get_path_normal(path_albedo)),
                field,
                slot,
            ):
                return None

            tiles[slot][0] = abspath(path_albedo)
            tiles[slot][1] = abspath(cls._get_path_normal(path_albedo))

        return tiles
    

    @classmethod
    def get_tiles_scale(cls, context) -> tuple:
        return (
            context.scene.tile_injector.scale_albedo_0,
            context.scene.tile_injector.scale_albedo_1,
            context.scene.tile_injector.scale_albedo_2,
            context.scene.tile_injector.scale_albedo_3,
        )
    

    @classmethod
    def get_is_masks_texture(cls, context) -> tuple:
        return (
            context.scene.tile_injector.is_mask_texture_0,
            context.scene.tile_injector.is_mask_texture_1,
            context.scene.tile_injector.is_mask_texture_2,
            context.scene.tile_injector.is_mask_texture_3,
        )
    

    @classmethod
    def get_masks(cls, context, is_masks_texture) -> list:
        masks = [None] * 4
        for slot in range(4):
            if not is_masks_texture[slot]:
                masks[slot] = [
                    *list(getattr(context.scene.tile_injector, f"mask_color_{slot}")),
                    1.0,
                ]
                continue

            path_mask =\
                abspath(getattr(context.scene.tile_injector, f"mask_texture_{slot}"))
            field = getattr(Inputs, f"mask_texture_{slot}").value
            if not cls._check_texture(path_mask, field, slot):
                return None
            
            masks[slot] = path_mask

        return masks
    

    @classmethod
    def get_masks_scale(cls, context) -> tuple:
        return (
            context.scene.tile_injector.scale_mask_0,
            context.scene.tile_injector.scale_mask_1,
            context.scene.tile_injector.scale_mask_2,
            context.scene.tile_injector.scale_mask_3,
        )
