from bpy.types import Panel



class VIEW3D_PT_tile_injector(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MaterialHelpers'
    bl_label = 'Tile Injector'


    def draw(self, context):
        layout = self.layout
        column_input = layout.column()
        column_input.prop(context.object.tile_injector, 'tile_albedo_0')
        column_input.prop(context.object.tile_injector, 'tile_albedo_1')
        column_input.prop(context.object.tile_injector, 'tile_albedo_2')
        column_input.prop(context.object.tile_injector, 'tile_albedo_3')
        column_input.prop(context.object.tile_injector, 'scale')
        
        column_exec = layout.column()
        column_exec.scale_y = 1.4
        column_exec.operator(
            'material.tile_injector',
            text="Create tiled material",
        )
