import bpy
from logger import Logger



class Sampler:
    def __init__(self):
        self._objects_names = []


    @staticmethod
    def _check_empty_sample(selected_objects: list) -> bool:
        if not len(selected_objects):
            return True
        return False


    def set_filter_by_type(self, target_type: str):
        selected_objects = bpy.context.selected_objects
        if self._check_empty_sample(selected_objects):
            return
        
        for obj in selected_objects:
            if not obj.type == target_type:
                Logger.not_target_object(obj, target_type)
                continue
            self._objects_names.append(obj.name)


    @property
    def length(self) -> int:
        return len(self._objects_names)
