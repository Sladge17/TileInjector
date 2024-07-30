from bpy.types import Panel

from inputs import Inputs



class VIEW3D_PT_tile_injector(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MaterialHelpers'
    bl_label = 'Tile Injector'


    def draw(self, context):
        layout = self.layout
        raw_input = layout.row()
        raw_input.prop(context.scene.tile_injector, Inputs.tile_albedo_0.name)
        raw_input.prop(context.scene.tile_injector, Inputs.mix_color_0.name)

        raw_input = layout.row()
        raw_input.prop(context.scene.tile_injector, Inputs.tile_albedo_1.name)
        raw_input.prop(context.scene.tile_injector, Inputs.mix_color_1.name)

        raw_input = layout.row()
        raw_input.prop(context.scene.tile_injector, Inputs.tile_albedo_2.name)
        raw_input.prop(context.scene.tile_injector, Inputs.mix_color_2.name)

        raw_input = layout.row()
        raw_input.prop(context.scene.tile_injector, Inputs.tile_albedo_3.name)
        raw_input.prop(context.scene.tile_injector, Inputs.mix_color_3.name)

        raw_input = layout.row()
        raw_input.prop(context.scene.tile_injector, Inputs.scale.name)
        
        raw_input = layout.row()
        column_exec = layout.column()
        column_exec.scale_y = 1.4
        column_exec.operator(
            'material.tile_injector',
            text="Create tiled material",
        )
