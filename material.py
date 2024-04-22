import bpy
from os import path as osp
from logger import Logger



class Material:
    def __init__(self, donor: str, name: str):
        self._remove_material(name)
        self.material = self._get_material(donor, name)
        self._set_nodespace()
        self._tex_tile_path = "/home/maxim/Projects/LestaTest/Textures/Tile_textures"
        self._scale_tile = 1.0

        
        # self.material = bpy.data.materials.new(name)
        # self._set_nodespace()
        # self._set_base_shader(shader)
        # self._tex_unic_path = "/home/maxim/Projects/LestaTest/Textures/Object_Textures"
        # self._tex_unic_name = ("Albedo", "Metallic", "Roughness", "Normal")


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


    def _get_nodes_by_type(self, node_type: str):
        return [node for node in self.material.node_tree.nodes.values() if node.type == node_type]

    
    def fix_tex_normal(self):
        nodes = self._get_nodes_by_type('TEX_IMAGE')
        for node in nodes:
            if "normal" in node.image.name.lower():
                node.image.colorspace_settings.name = 'Non-Color'
                break

        return self
    

    def _create_node_by_type(self, node_type: str, location: tuple):
        node = self._nodes.new(type=node_type)
        node.location = location
        return node
    

    # def _link_nodes(self, links: list):
    #     for link in links:
    #         self._links.new(link[0], link[1])

    
    def _get_nodes_tex_uniq_sorted(self) -> list:
        nodes_tex_uniq = self._get_nodes_by_type('TEX_IMAGE')
        nodes_tex_uniq_sorted = [None] * 4
        for node in nodes_tex_uniq:
            if "albedo" in node.image.name.lower():
                nodes_tex_uniq_sorted[0] = node
                continue

            if "metallic" in node.image.name.lower():
                nodes_tex_uniq_sorted[1] = node
                continue            

            if "roughness" in node.image.name.lower():
                nodes_tex_uniq_sorted[2] = node
                continue

            nodes_tex_uniq_sorted[3] = node
            return nodes_tex_uniq_sorted 


    def _unlink_nodes_tex_uniq(self, nodes_tex_uniq: list):
        for node in nodes_tex_uniq:
            self._links.remove(node.outputs['Color'].links[0])

    
    
    def _set_uv_tex_uniq(self, nodes_tex_uniq: list, location: list):
        node_uv_map = self._create_node_by_type('ShaderNodeUVMap', location)
        node_uv_map.uv_map = "UV1"
        self._links.new(node_uv_map.outputs['UV'], nodes_tex_uniq[0].inputs['Vector'])
        self._links.new(node_uv_map.outputs['UV'], nodes_tex_uniq[1].inputs['Vector'])
        self._links.new(node_uv_map.outputs['UV'], nodes_tex_uniq[2].inputs['Vector'])
        self._links.new(node_uv_map.outputs['UV'], nodes_tex_uniq[3].inputs['Vector'])


    def _get_block_uv_tile(self, location: list, scale: float):
        node_uv_map = self._create_node_by_type('ShaderNodeUVMap', location)
        node_uv_map.uv_map = "UV2"
        location[0] += 300
        node_math = self._create_node_by_type('ShaderNodeVectorMath', location)
        node_math.operation = 'MULTIPLY'
        node_math.inputs[1].default_value = (1,) * 3
        self._links.new(node_uv_map.outputs['UV'], node_math.inputs['Vector'])
        return node_math
    

    
    def _get_blocks_mixed_tex(self, nodes_tex_uniq_sorted: list, block_uv_tile) -> list:
        albedo_active = nodes_tex_uniq_sorted[0]
        metallic_active = nodes_tex_uniq_sorted[1]
        roughness_acctive = nodes_tex_uniq_sorted[2]
        normal_active = nodes_tex_uniq_sorted[3]
        mask_colors = (
            (1, 0, 0, 1),
            (0, 1, 0, 1),
            (0, 0, 1, 1),
            (0, 0, 0, 1),
        )

        for index in range(1):
            node_rgb = self._create_node_by_type('ShaderNodeRGB', [-1450, 200])
            node_rgb.outputs['Color'].default_value = mask_colors[index]
        
            node_tex = self._create_node_by_type('ShaderNodeTexImage', [-900, 850])
            node_tex.image = bpy.data.images.load(osp.join(self._tex_tile_path, f"Tile{index}_a.tga"))
            
            node_mix_1 = self._create_node_by_type('ShaderNodeMixRGB', [-600, 900])
            node_mix_2 = self._create_node_by_type('ShaderNodeMixRGB', [-600, 700])

            self._links.new(block_uv_tile.outputs['Vector'], node_tex.inputs[0])
        
            self._links.new(node_rgb.outputs['Color'], node_mix_1.inputs['Fac'])
            self._links.new(albedo_active.outputs['Color'], node_mix_1.inputs['Color1'])
            self._links.new(node_tex.outputs['Color'], node_mix_1.inputs['Color2'])

            self._links.new(node_rgb.outputs['Color'], node_mix_2.inputs['Fac'])
            self._links.new(metallic_active.outputs['Color'], node_mix_2.inputs['Color1'])
            self._links.new(node_tex.outputs['Alpha'], node_mix_2.inputs['Color2'])


            node_tex = self._create_node_by_type('ShaderNodeTexImage', [-900, -750])
            node_tex.image = bpy.data.images.load(osp.join(self._tex_tile_path, f"Tile{index}_n.tga"))
            node_tex.image.colorspace_settings.name = 'Non-Color'
            
            node_mix_3 = self._create_node_by_type('ShaderNodeMixRGB', [-600, -700])
            node_mix_4 = self._create_node_by_type('ShaderNodeMixRGB', [-600, -900])

            self._links.new(block_uv_tile.outputs['Vector'], node_tex.inputs[0])
            
            self._links.new(node_rgb.outputs['Color'], node_mix_4.inputs['Fac'])
            self._links.new(normal_active.outputs['Color'], node_mix_4.inputs['Color1'])
            self._links.new(node_tex.outputs['Color'], node_mix_4.inputs['Color2'])

            self._links.new(node_rgb.outputs['Color'], node_mix_3.inputs['Fac'])
            self._links.new(roughness_acctive.outputs['Color'], node_mix_3.inputs['Color1'])
            self._links.new(node_tex.outputs['Alpha'], node_mix_3.inputs['Color2'])

        
        return [node_mix_1, node_mix_2, node_mix_3, node_mix_4]
    
    
    
    
   
    
    
    def _set_links_shader(self, nodes_outputs: list):
        node_shader = self._get_nodes_by_type('BSDF_PRINCIPLED')[0]
        node_normal = self._get_nodes_by_type('NORMAL_MAP')[0]

        self._links.new(nodes_outputs[0].outputs['Color'], node_shader.inputs['Base Color'])
        self._links.new(nodes_outputs[1].outputs['Color'], node_shader.inputs['Metallic'])
        self._links.new(nodes_outputs[2].outputs['Color'], node_shader.inputs['Roughness'])
        self._links.new(nodes_outputs[3].outputs['Color'], node_normal.inputs['Color'])

    
    def set_tex_tile(self):
        nodes_tex_uniq_sorted = self._get_nodes_tex_uniq_sorted() # sort nodes TexImages like: [Albedo, Metallic, Roughness, Normal]
        self._unlink_nodes_tex_uniq(nodes_tex_uniq_sorted)
        self._set_uv_tex_uniq(nodes_tex_uniq_sorted, [-1200, 0])
        block_uv_tile = self._get_block_uv_tile([-2000, 0], self._scale_tile)

        
        nodes_outputs = self._get_blocks_mixed_tex(nodes_tex_uniq_sorted, block_uv_tile)
        self._set_links_shader(nodes_outputs)

        return self















    
    


    # def _set_nodespace(self):
    #     self.material.use_nodes = True
    #     self._nodes = self.material.node_tree.nodes
    #     self._links = self.material.node_tree.links
    #     for node in self._nodes:
    #         self._nodes.remove(node)


    # def _set_base_shader(self, shader: str):
    #     self._node_base = self._nodes.new(type=shader)
    #     self._node_base.location = (0, 0)

    #     node_output = self._nodes.new('ShaderNodeOutputMaterial')
    #     self._links.new(self._node_base.outputs[0], node_output.inputs[0])
    #     node_output.location = (300, 0)


    # def _set_node_teximg(self, name: str, input: int, position: list):
    #     node_teximg_unique = self._nodes.new(type='ShaderNodeTexImage')
    #     node_teximg_unique.image = bpy.data.images.load(osp.join(self._tex_unic_path, f"{name}.tga"))
    #     self._links.new(node_teximg_unique.outputs[0], input)
    #     node_teximg_unique.location = position

    
    # def _set_unic_shader_part(self):
    #     input_index = iter([0, 6, 9, 22])
    #     position_2d = [-800, 200]
    #     for name in self._tex_unic_name[:-1]:
    #         self._set_node_teximg(
    #             name, self._node_base.inputs[next(input_index)], position_2d
    #         )
    #         position_2d[1] -= 300

    #     node_teximg_unique = self._nodes.new(type='ShaderNodeTexImage')
    #     node_teximg_unique.image = bpy.data.images.load(osp.join(self._tex_unic_path, f"{self._tex_unic_name[-1]}.tga"))
    #     node_teximg_unique.image.colorspace_settings.name = 'Non-Color'
    #     node_teximg_unique.location = position_2d

    #     position_2d[0] += 500
    #     node_normal_map = self._nodes.new(type='ShaderNodeNormalMap')
    #     node_normal_map.location = position_2d

    #     self._links.new(node_teximg_unique.outputs[0], node_normal_map.inputs[1])
    #     self._links.new(node_normal_map.outputs[0], self._node_base.inputs[next(input_index)])
    
    
    
    
    # def set_target_shader(self):
    #     self._set_unic_shader_part()
    #     return self