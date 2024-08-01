import bpy

from loger import Loger



class Sampler:
    def __init__(self):
        self._objects_names = []


    def set_filter_by_type(self, target_type: str):
        selected_objects = bpy.context.selected_objects
        for obj in selected_objects:
            if not obj.type == target_type:
                Loger.not_target_object(obj.name, target_type)
                continue
            self._objects_names.append(obj.name)
        
        return self


    @property
    def length(self) -> int:
        return len(self._objects_names)
    

    @staticmethod
    def _rename_uv(obj_name):
        for index, value in enumerate(bpy.data.meshes[obj_name].uv_layers.values()[:2]):
            value.name = f"UV{index + 1}"


    def _remove_bad_objects(self, bad_objects):
        for obj_name in bad_objects:
            self._objects_names.remove(obj_name)
    
    
    def check_uv(self, channels: int):
        bad_objects = []
        for obj_name in self._objects_names:
            if len(bpy.data.meshes[obj_name].uv_layers.values()) < channels:
                Loger.uv_less_than_need(obj_name, channels)
                bad_objects.append(obj_name)
                continue

            if len(bpy.data.meshes[obj_name].uv_layers.values()) > channels:
                Loger.uv_more_than_need(obj_name, channels)
            
            self._rename_uv(obj_name)

        self._remove_bad_objects(bad_objects)
        return self
    

    def set_material(self, material):
        for obj_name in self._objects_names:
            bpy.data.meshes[obj_name].materials.clear()
            bpy.data.meshes[obj_name].materials.append(material)
        
        return self
