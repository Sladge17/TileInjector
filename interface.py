from bpy.types import Panel



class VIEW3D_PT_tile_injector(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MaterialHelpers'
    bl_label = 'Tile Injector'


    def draw(self, context):
        pass
