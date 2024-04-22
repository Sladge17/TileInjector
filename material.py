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

    
    def _get_nodes_tex_uniq(self) -> dict:
        nodes_tex_uniq = self._get_nodes_by_type('TEX_IMAGE')
        nodes_tex_uniq_sorted = {}
        for node in nodes_tex_uniq:
            if "albedo" in node.image.name.lower():
                nodes_tex_uniq_sorted['Albedo'] = node
                continue

            if "metallic" in node.image.name.lower():
                nodes_tex_uniq_sorted['Metallic'] = node
                continue            

            if "roughness" in node.image.name.lower():
                nodes_tex_uniq_sorted['Roughness'] = node
                continue

            nodes_tex_uniq_sorted['Normal'] = node
            return nodes_tex_uniq_sorted 


    def _unlink_nodes_tex_uniq(self, nodes_tex_uniq: dict):
        for node in nodes_tex_uniq.values():
            self._links.remove(node.outputs['Color'].links[0])

    
    def _set_uv_tex_uniq(self, nodes_tex_uniq: dict, location: list):
        node_uv_map = self._create_node_by_type('ShaderNodeUVMap', location)
        node_uv_map.uv_map = "UV1"
        self._links.new(node_uv_map.outputs['UV'], nodes_tex_uniq['Albedo'].inputs['Vector'])
        self._links.new(node_uv_map.outputs['UV'], nodes_tex_uniq['Metallic'].inputs['Vector'])
        self._links.new(node_uv_map.outputs['UV'], nodes_tex_uniq['Roughness'].inputs['Vector'])
        self._links.new(node_uv_map.outputs['UV'], nodes_tex_uniq['Normal'].inputs['Vector'])


    def _get_block_uv_tile(self, location: list, scale: float):
        node_uv_map = self._create_node_by_type('ShaderNodeUVMap', location)
        node_uv_map.uv_map = "UV2"
        location[0] += 300
        node_math = self._create_node_by_type('ShaderNodeVectorMath', location)
        node_math.operation = 'MULTIPLY'
        node_math.inputs[1].default_value = (1,) * 3
        self._links.new(node_uv_map.outputs['UV'], node_math.inputs['Vector'])
        return node_math
    
    
    @staticmethod
    def _get_shifted_origin(origin: list, shift_x: int, shift_y: int) -> list:
        return [origin[0] + shift_x, origin[1] + shift_y]
    
    
    def _set_nodes_tex_uniq_mixed_by_block(
            self,
            block: str,
            origin: list,
            block_uv_tile,
            node_rgb,
            nodes_tex_uniq,
            index: int,
        ):
        node_tex = self._create_node_by_type('ShaderNodeTexImage', origin)
        node_tex.image = bpy.data.images.load(osp.join(self._tex_tile_path, f"Tile{index}_{block}.tga"))            
        node_mix_1 = self._create_node_by_type(
            'ShaderNodeMixRGB', self._get_shifted_origin(origin, 300, 50)
        )
        node_mix_2 = self._create_node_by_type(
            'ShaderNodeMixRGB', self._get_shifted_origin(origin, 300, -150)
        )

        self._links.new(block_uv_tile.outputs['Vector'], node_tex.inputs[0])
        
        if block == 'a':
            self._links.new(node_rgb.outputs['Color'], node_mix_1.inputs['Fac'])
            self._links.new(nodes_tex_uniq['Albedo'].outputs['Color'], node_mix_1.inputs['Color1'])
            self._links.new(node_tex.outputs['Color'], node_mix_1.inputs['Color2'])

            self._links.new(node_rgb.outputs['Color'], node_mix_2.inputs['Fac'])
            self._links.new(nodes_tex_uniq['Metallic'].outputs['Color'], node_mix_2.inputs['Color1'])
            self._links.new(node_tex.outputs['Alpha'], node_mix_2.inputs['Color2'])

            nodes_tex_uniq['Albedo'] = node_mix_1
            nodes_tex_uniq['Metallic'] = node_mix_2
            return
        
        self._links.new(node_rgb.outputs['Color'], node_mix_2.inputs['Fac'])
        self._links.new(nodes_tex_uniq['Normal'].outputs['Color'], node_mix_2.inputs['Color1'])
        self._links.new(node_tex.outputs['Color'], node_mix_2.inputs['Color2'])

        self._links.new(node_rgb.outputs['Color'], node_mix_1.inputs['Fac'])
        self._links.new(nodes_tex_uniq['Roughness'].outputs['Color'], node_mix_1.inputs['Color1'])
        self._links.new(node_tex.outputs['Alpha'], node_mix_1.inputs['Color2'])

        nodes_tex_uniq['Roughness'] = node_mix_1
        nodes_tex_uniq['Normal'] = node_mix_2
        node_tex.image.colorspace_settings.name = 'Non-Color'

    
    def _set_nodes_tex_uniq_mixed(self, nodes_tex_uniq: dict, block_uv_tile) -> dict:
        mask_colors = (
            (1, 0, 0, 1), # color Red
            (0, 1, 0, 1), # color Green
            (0, 0, 1, 1), # color Blue
            (0, 0, 0, 1), # color Black
        )

        origin_node_rgb = [-1450, 200]
        origin_block_a = [-900, 850]
        origin_block_n = [-900, -750]

        for index in range(2):
            node_rgb = self._create_node_by_type('ShaderNodeRGB', origin_node_rgb)
            node_rgb.outputs['Color'].default_value = mask_colors[index]

            self._set_nodes_tex_uniq_mixed_by_block(
                'a', origin_block_a, block_uv_tile, node_rgb, nodes_tex_uniq, index
            )
            self._set_nodes_tex_uniq_mixed_by_block(
                'n', origin_block_n, block_uv_tile, node_rgb, nodes_tex_uniq, index
            )
            
            origin_node_rgb = self._get_shifted_origin(origin_node_rgb, 0, -200)
            origin_block_a = self._get_shifted_origin(origin_block_a, 0, 400)
            origin_block_n = self._get_shifted_origin(origin_block_n, 0, -400)

        
    def _set_links_shader(self, nodes_outputs: dict):
        node_shader = self._get_nodes_by_type('BSDF_PRINCIPLED')[0]
        node_normal = self._get_nodes_by_type('NORMAL_MAP')[0]

        self._links.new(nodes_outputs['Albedo'].outputs['Color'], node_shader.inputs['Base Color'])
        self._links.new(nodes_outputs['Metallic'].outputs['Color'], node_shader.inputs['Metallic'])
        self._links.new(nodes_outputs['Roughness'].outputs['Color'], node_shader.inputs['Roughness'])
        self._links.new(nodes_outputs['Normal'].outputs['Color'], node_normal.inputs['Color'])

    
    def set_tex_tile(self):
        nodes_tex_uniq = self._get_nodes_tex_uniq()
        self._unlink_nodes_tex_uniq(nodes_tex_uniq)
        self._set_uv_tex_uniq(nodes_tex_uniq, [-1200, 0])
        block_uv_tile = self._get_block_uv_tile([-2000, 0], self._scale_tile)        
        self._set_nodes_tex_uniq_mixed(nodes_tex_uniq, block_uv_tile)
        self._set_links_shader(nodes_tex_uniq)
        return self
