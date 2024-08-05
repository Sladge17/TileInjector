import bpy
from bpy.path import abspath



class PropertiesUpdater:

    @staticmethod
    def update_albedo_texture_0(self, context):
        if bpy.data.images.get('preview_albedo_0'):
            bpy.data.images.remove(bpy.data.images['preview_albedo_0'])

        try:
            image = bpy.data.images.load(
                abspath(context.scene.tile_injector.albedo_texture_0),
                check_existing=True,
            )
        except RuntimeError:
            return
        
        image.name = 'preview_albedo_0'
        image.preview_ensure()


    @staticmethod
    def update_albedo_texture_1(self, context):
        if bpy.data.images.get('preview_albedo_1'):
            bpy.data.images.remove(bpy.data.images['preview_albedo_1'])

        try:
            image = bpy.data.images.load(
                abspath(context.scene.tile_injector.albedo_texture_1),
                check_existing=True,
            )
        except RuntimeError:
            return
        
        image.name = 'preview_albedo_1'
        image.preview_ensure()


    @staticmethod
    def update_albedo_texture_2(self, context):
        if bpy.data.images.get('preview_albedo_2'):
            bpy.data.images.remove(bpy.data.images['preview_albedo_2'])

        try:
            image = bpy.data.images.load(
                abspath(context.scene.tile_injector.albedo_texture_2),
                check_existing=True,
            )
        except RuntimeError:
            return
        
        image.name = 'preview_albedo_2'
        image.preview_ensure()


    @staticmethod
    def update_albedo_texture_3(self, context):
        if bpy.data.images.get('preview_albedo_3'):
            bpy.data.images.remove(bpy.data.images['preview_albedo_3'])

        try:
            image = bpy.data.images.load(
                abspath(context.scene.tile_injector.albedo_texture_3),
                check_existing=True,
            )
        except RuntimeError:
            return
        
        image.name = 'preview_albedo_3'
        image.preview_ensure()
            

    @staticmethod
    def update_mask_texture_0(self, context):
        if bpy.data.images.get('preview_mask_0'):
            bpy.data.images.remove(bpy.data.images['preview_mask_0'])

        try:
            image = bpy.data.images.load(
                abspath(context.scene.tile_injector.mask_texture_0),
                check_existing=True,
            )
        except RuntimeError:
            return
        
        image.name = 'preview_mask_0'
        image.preview_ensure()


    @staticmethod
    def update_mask_texture_1(self, context):
        if bpy.data.images.get('preview_mask_1'):
            bpy.data.images.remove(bpy.data.images['preview_mask_1'])

        try:
            image = bpy.data.images.load(
                abspath(context.scene.tile_injector.mask_texture_1),
                check_existing=True,
            )
        except RuntimeError:
            return
        
        image.name = 'preview_mask_1'
        image.preview_ensure()


    @staticmethod
    def update_mask_texture_2(self, context):
        if bpy.data.images.get('preview_mask_2'):
            bpy.data.images.remove(bpy.data.images['preview_mask_2'])

        try:
            image = bpy.data.images.load(
                abspath(context.scene.tile_injector.mask_texture_2),
                check_existing=True,
            )
        except RuntimeError:
            return
        
        image.name = 'preview_mask_2'
        image.preview_ensure()


    @staticmethod
    def update_mask_texture_3(self, context):
        if bpy.data.images.get('preview_mask_3'):
            bpy.data.images.remove(bpy.data.images['preview_mask_3'])

        try:
            image = bpy.data.images.load(
                abspath(context.scene.tile_injector.mask_texture_3),
                check_existing=True,
            )
        except RuntimeError:
            return
        
        image.name = 'preview_mask_3'
        image.preview_ensure()
