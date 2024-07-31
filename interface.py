from bpy.types import Panel

from inputs import Inputs



class VIEW3D_PT_tile_injector(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MaterialHelpers'
    bl_label = 'Tile Injector'


    def _draw_tile_box(self, layout, context, index:int) -> None:
        tile_box = layout.column().box()
        tile_box.label(text=getattr(Inputs, f"label_{index}").value)
        tile_box.prop(
            context.scene.tile_injector,
            getattr(Inputs, f"albedo_texture_{index}").name,
        )
        tile_box.prop(
            context.scene.tile_injector,
            getattr(Inputs, f"scale_albedo_{index}").name,
        )
        tile_box.prop(
            context.scene.tile_injector,
            getattr(Inputs, f"is_mask_texture_{index}").name,
        )
        if getattr(context.scene.tile_injector, f"is_mask_texture_{index}"):
            tile_box.prop(
                context.scene.tile_injector,
                getattr(Inputs, f"mask_texture_{index}").name,
            )
            return
        
        tile_box.row().prop(
            context.scene.tile_injector,
            getattr(Inputs, f"mask_color_{index}").name,
        )


    def draw(self, context):
        layout = self.layout        
        for index in range(4):
            self._draw_tile_box(layout, context, index)        
        
        column_exec = layout.column()
        column_exec.scale_y = 1.4
        column_exec.operator(
            'material.tile_injector',
            text="Create tiled material",
        )
