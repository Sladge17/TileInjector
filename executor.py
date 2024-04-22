from bpy.types import Operator
from bpy.props import StringProperty, FloatProperty



class MESH_OT_tile_injector(Operator):
    bl_idname = 'mesh.tile_injector'
    bl_label = 'Tile Injector'
    bl_options = {'REGISTER', 'UNDO'}

    texture_albedo_1 : StringProperty(
        name = "albedo_1",
        description = "Path to texture",
    )
    texture_albedo_2 : StringProperty(
        name = "albedo_2",
        description = "Path to texture",
    )
    texture_albedo_3 : StringProperty(
        name = "albedo_3",
        description = "Path to texture",
    )
    texture_albedo_4 : StringProperty(
        name = "albedo_4",
        description = "Path to texture",
    )
    scale : FloatProperty(
        name = "scale",
        description = "Scale factor for tile textures",
        default = 1.0,
    )


    def execute(self, context):
        return {'FINISHED'}
