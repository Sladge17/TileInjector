from bpy.types import Operator

from sampler import Sampler
from logger import Logger
from material import Material



class MATERIAL_OT_tile_injector(Operator):
    bl_idname = 'material.tile_injector'
    bl_label = 'Tile Injector'
    tiled = False


    @classmethod
    def poll(cls, context):
        if not context.object.mode == 'OBJECT':
            return False
        
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                return True
            
        return False


    def execute(self, context):
        sample = Sampler()\
            .set_filter_by_type(target_type='MESH')\
            .check_uv(channels=2)
        if not sample.length:
            Logger.empty_sample()
            return {'CANCELLED'}
        
        material = Material(
            donor=sample.first_name,
            name="MODE_Material",
        ).fix_tex_normal().set_tex_tile(
            tiled=self.tiled,
            scale=context.object.tile_injector.scale,
        )
        MATERIAL_OT_tile_injector.tiled = True
        sample.set_material(material=material)
        Logger.task_done()
        return {'FINISHED'}
    