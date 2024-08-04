import bpy

from group_mix_by_color import Group_MixByColor



class Environment:

    @classmethod
    def set_albedo_textures(cls):
        for index in range(4):
            bpy.data.textures.new(name=f"albedo_texture_{index}", type='IMAGE')


    @classmethod
    def set_mask_textures(cls):
        for index in range(4):
            bpy.data.textures.new(name=f"mask_texture_{index}", type='IMAGE')


    @classmethod
    def set_groups(cls):
        Group_MixByColor.set_group()
