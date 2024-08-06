from abc import ABC, abstractmethod
import bpy


class Group_ABC(ABC):

    @classmethod
    def _check_group_exist(cls):
        if cls.name in bpy.data.node_groups.keys():
            return True
        
        return False
    

    @classmethod
    def get_group(cls, material:str, location:list=[0, 0]):
        group = bpy.data.materials[material].node_tree.nodes.new('ShaderNodeGroup')
        group.node_tree = bpy.data.node_groups[cls.name]
        group.location = location
        return group
    

    @classmethod
    @abstractmethod
    def set_group(cls):
        pass
