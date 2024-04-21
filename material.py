import bpy
from os import path as osp
from logger import Logger



class Material:
    def __init__(self, donor: str, name: str):
        self._remove_material(name)
        self.material = self._get_material(donor, name)
        self._tex_tile_path = "/home/maxim/Projects/LestaTest/Textures/Tile_textures"

        
        # self.material = bpy.data.materials.new(name)
        # self._set_nodespace()
        # self._set_base_shader(shader)
        # self._tex_unic_path = "/home/maxim/Projects/LestaTest/Textures/Object_Textures"
        # self._tex_unic_name = ("Albedo", "Metallic", "Roughness", "Normal")


    def fix_tex_normal(self):
        nodes = self._get_nodes_by_type('TEX_IMAGE')
        for node in nodes:
            if "normal" in node.image.name.split('.')[0].lower():
                node.image.colorspace_settings.name = 'Non-Color'
                break

        return self

        
    def _get_nodes_by_type(self, node_type: str):
        return [node for node in self.material.node_tree.nodes.values() if node.type == node_type]
    
    
    @staticmethod
    def _remove_material(name: str):
        try:
            bpy.data.materials.remove(bpy.data.materials.get(name))
            Logger.remove_material(name)
        except TypeError:
            pass


    @staticmethod
    def _get_material(donor: str, name: str):
        donor_material_name = bpy.data.meshes[donor].materials.values()[0].name
        material = bpy.data.meshes[donor].materials[donor_material_name].copy()
        material.name = name
        return material       


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


    def _set_node_teximg(self, name: str, input: int, position: list):
        node_teximg_unique = self._nodes.new(type='ShaderNodeTexImage')
        node_teximg_unique.image = bpy.data.images.load(osp.join(self._tex_unic_path, f"{name}.tga"))
        self._links.new(node_teximg_unique.outputs[0], input)
        node_teximg_unique.location = position

    
    def _set_unic_shader_part(self):
        input_index = iter([0, 6, 9, 22])
        position_2d = [-800, 200]
        for name in self._tex_unic_name[:-1]:
            self._set_node_teximg(
                name, self._node_base.inputs[next(input_index)], position_2d
            )
            position_2d[1] -= 300

        node_teximg_unique = self._nodes.new(type='ShaderNodeTexImage')
        node_teximg_unique.image = bpy.data.images.load(osp.join(self._tex_unic_path, f"{self._tex_unic_name[-1]}.tga"))
        node_teximg_unique.image.colorspace_settings.name = 'Non-Color'
        node_teximg_unique.location = position_2d

        position_2d[0] += 500
        node_normal_map = self._nodes.new(type='ShaderNodeNormalMap')
        node_normal_map.location = position_2d

        self._links.new(node_teximg_unique.outputs[0], node_normal_map.inputs[1])
        self._links.new(node_normal_map.outputs[0], self._node_base.inputs[next(input_index)])
    
    
    
    
    def set_target_shader(self):
        self._set_unic_shader_part()
        return self
