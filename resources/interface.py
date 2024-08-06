import bpy
from bpy.types import Panel

from .inputs import Inputs



class VIEW3D_PT_tile_injector(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MaterialHelpers'
    bl_label = 'Tile Injector'
    
    icon_scale = 6


    def _draw_slot(self, layout, context, index:int) -> None:
        tile_box = layout.column().box()
        tile_box.label(text=getattr(Inputs, f'label_{index}').value)
        row_main = tile_box.row()
        row_main.prop(
            context.scene.tile_injector,
            getattr(Inputs, f'albedo_texture_{index}').name,
        )
        row_main.prop(
            context.scene.tile_injector,
            getattr(Inputs, f'is_preview_albedo_{index}').name,
        )
        if getattr(context.scene.tile_injector, f'albedo_texture_{index}') and\
            getattr(context.scene.tile_injector, f'is_preview_albedo_{index}') and\
            bpy.data.images.get(f'preview_albedo_{index}'):
            tile_box.row().template_icon(
                bpy.data.images[f'preview_albedo_{index}'].preview.icon_id,
                scale=self.icon_scale,
            )

        tile_box.prop(
            context.scene.tile_injector,
            getattr(Inputs, f'scale_albedo_{index}').name,
        )
        tile_box.prop(
            context.scene.tile_injector,
            getattr(Inputs, f'is_mask_texture_{index}').name,
        )
        if not getattr(context.scene.tile_injector, f'is_mask_texture_{index}'):
            tile_box.row().prop(
                context.scene.tile_injector,
                getattr(Inputs, f'mask_color_{index}').name,
            )
            return

        row_main = tile_box.row()
        row_main.prop(
            context.scene.tile_injector,
            getattr(Inputs, f'mask_texture_{index}').name,
        )
        row_main.prop(
            context.scene.tile_injector,
            getattr(Inputs, f'is_preview_mask_{index}').name,
        )
        if getattr(context.scene.tile_injector, f'mask_texture_{index}') and\
            getattr(context.scene.tile_injector, f'is_preview_mask_{index}') and\
            bpy.data.images.get(f'preview_mask_{index}'):
            tile_box.row().template_icon(
                bpy.data.images[f'preview_mask_{index}'].preview.icon_id,
                scale=self.icon_scale,
            )

        tile_box.prop(
            context.scene.tile_injector,
            getattr(Inputs, f'scale_mask_{index}').name,
        )


    def draw(self, context):
        layout = self.layout
        for index in range(4):
            self._draw_slot(layout, context, index)
        
        column_exec = layout.column()
        column_exec.scale_y = 1.4
        column_exec.operator(
            'material.tile_injector',
            text="Create tiled material",
        )
