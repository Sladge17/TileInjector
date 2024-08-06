from abc import ABC, abstractmethod
import bpy


class Group_ABC(ABC):

    @classmethod
    def _check_group_exist(cls):
        if cls.name in bpy.data.node_groups.keys():
            return True
        
        return False