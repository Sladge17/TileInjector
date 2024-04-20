import bpy
from logger import Logger



class Material:
    def __init__(self, shader: str, name: str):
        self._remove_material(name)
        self.material = bpy.data.materials.new(name)
        self._set_nodespace()
        self._set_base_shader(shader)


    @staticmethod
    def _remove_material(name: str):
        try:
            bpy.data.materials.remove(bpy.data.materials.get(name))
            Logger.remove_material(name)
        except TypeError:
            pass


    def _set_nodespace(self):
        self.material.use_nodes = True
        self._nodes = self.material.node_tree.nodes
        self._links = self.material.node_tree.links

        for node in self._nodes:
            self._nodes.remove(node)


    def _set_base_shader(self, shader: str):
        self._node_base = self._nodes.new(type=shader)
        self._node_base.location = (0, 0)

        node_output = self._nodes.new('ShaderNodeOutputMaterial')
        self._links.new(self._node_base.outputs[0], node_output.inputs[0])
        node_output.location = (300, 0)


    def set_target_shader(self):
        node_rgb= self._nodes.new(type='ShaderNodeRGB')
        node_rgb.outputs[0].default_value = (1, 0, 0, 1)
        self._links.new(node_rgb.outputs[0], self._node_base.inputs[0])
        node_rgb.location = (-300, 0)
        return self
