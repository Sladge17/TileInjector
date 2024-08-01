import bpy

from group_mix_by_color import Group_MixByColor



class Material:
    def __init__(self, name_suffix: str):
        self._material = self._get_material(name_suffix)
        self._set_nodespace()

    
    @staticmethod
    def _get_material(name_suffix: str):
        material_donor_name =\
            bpy.context.active_object.active_material.name
        if name_suffix in material_donor_name:
            material_donor_name = material_donor_name\
                [: material_donor_name.index(name_suffix) - 1]

        material = bpy.data.materials[material_donor_name].copy()
        material.name = f"{material_donor_name}_{name_suffix}"
        return material
    

    def _set_nodespace(self):
        self._material.use_nodes = True
        self._nodes = self._material.node_tree.nodes
        self._links = self._material.node_tree.links


    def _get_nodes_by_type(self, node_type: str):
        return [
            node for node in self._material.node_tree.nodes.values()\
            if node.type == node_type
        ]

    
    def fix_tex_uniq_color_space(self):
        nodes_tex = self._get_nodes_by_type('TEX_IMAGE')
        for node in nodes_tex:
            if "albedo" in node.image.name.lower():
                continue
            
            node.image.colorspace_settings.name = 'Non-Color'

        return self
    

    def _create_node_by_type(self, node_type: str, origin: tuple):
        node = self._nodes.new(type=node_type)
        node.location = origin
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

    
    def _set_uv_tex_uniq(self, nodes_tex_uniq: dict, origin: list):
        node_uv_map = self._create_node_by_type('ShaderNodeUVMap', origin)
        node_uv_map.uv_map = "UV1"
        self._links.new(
            node_uv_map.outputs['UV'],
            nodes_tex_uniq['Albedo'].inputs['Vector'],
        )
        self._links.new(
            node_uv_map.outputs['UV'],
            nodes_tex_uniq['Metallic'].inputs['Vector'],
        )
        self._links.new(
            node_uv_map.outputs['UV'],
            nodes_tex_uniq['Roughness'].inputs['Vector'],
        )
        self._links.new(
            node_uv_map.outputs['UV'],
            nodes_tex_uniq['Normal'].inputs['Vector'],
        )


    def _get_node_uv_tile(self, origin: list):
        node_uv_tile = self._create_node_by_type('ShaderNodeUVMap', origin)
        node_uv_tile.uv_map = "UV2"
        return node_uv_tile

    
    def _get_nodes_tile_scale(
            self,
            origin: list,
            tiles_scale: tuple,
            node_uv_tile
        ) -> list:
        nodes_math = [None] * 4
        for index in range(len(nodes_math)):
            node_math = self._create_node_by_type('ShaderNodeVectorMath', origin)
            node_math.operation = 'MULTIPLY'
            node_math.inputs[1].default_value = (tiles_scale[index],) * 3
            self._links.new(node_uv_tile.outputs['UV'], node_math.inputs['Vector'])
            nodes_math[index] = node_math
            origin = self._get_shifted_origin(origin, 0, -200)
        return nodes_math


    @staticmethod
    def _get_shifted_origin(origin: list, shift_x: int, shift_y: int) -> list:
        return [origin[0] + shift_x, origin[1] + shift_y]
    
    
    def _set_nodes_tex_uniq_tiled_by_block(
            self,
            tiles,
            origin: list,
            block_uv_tile,
            node_mask,
            nodes_tex_uniq: dict,
            is_normal: bool = False

        ):
        node_tex = self._create_node_by_type('ShaderNodeTexImage', origin)
        node_tex.image = bpy.data.images.load(tiles[int(is_normal)])
        node_mix_1 = Group_MixByColor.get_group(
            self._material.name,
            self._get_shifted_origin(origin, 300, 50),
        )
        node_mix_2 = Group_MixByColor.get_group(
            self._material.name,
            self._get_shifted_origin(origin, 300, -150),
        )

        self._links.new(
            block_uv_tile.outputs['Vector'],
            node_tex.inputs[0],
        )
        
        if not is_normal:
            self._links.new(
                node_mask.outputs['Color'],
                node_mix_1.inputs['Color'],
            )
            self._links.new(
                nodes_tex_uniq['Albedo'].outputs['Color'],
                node_mix_1.inputs['Color1'],
            )
            self._links.new(
                node_tex.outputs['Color'],
                node_mix_1.inputs['Color2'],
            )

            self._links.new(
                node_mask.outputs['Color'],
                node_mix_2.inputs['Color'],
            )
            self._links.new(
                nodes_tex_uniq['Metallic'].outputs['Color'],
                node_mix_2.inputs['Color1'],
            )
            self._links.new(
                node_tex.outputs['Alpha'],
                node_mix_2.inputs['Color2'],
            )

            nodes_tex_uniq['Albedo'] = node_mix_1
            nodes_tex_uniq['Metallic'] = node_mix_2
            return
        
        self._links.new(
            node_mask.outputs['Color'],
            node_mix_2.inputs['Color'],
        )
        self._links.new(
            nodes_tex_uniq['Normal'].outputs['Color'],
            node_mix_2.inputs['Color1'],
        )
        self._links.new(
            node_tex.outputs['Color'],
            node_mix_2.inputs['Color2'],
        )

        self._links.new(
            node_mask.outputs['Color'],
            node_mix_1.inputs['Color'],
        )
        self._links.new(
            nodes_tex_uniq['Roughness'].outputs['Color'],
            node_mix_1.inputs['Color1'],
        )
        self._links.new(
            node_tex.outputs['Alpha'],
            node_mix_1.inputs['Color2'],
        )

        nodes_tex_uniq['Roughness'] = node_mix_1
        nodes_tex_uniq['Normal'] = node_mix_2
        node_tex.image.colorspace_settings.name = 'Non-Color'

    
    def _get_node_mask(
            self,
            is_masks_texture: tuple,
            masks: list,
            masks_scale: tuple,
            index: int,
            origin: list,
            node_uv_tile,
        ):
        if not is_masks_texture[index]:
            node_mask = self._create_node_by_type('ShaderNodeRGB', origin)
            node_mask.outputs['Color'].default_value = masks[index]
            return node_mask
        
        node_mask = self._create_node_by_type('ShaderNodeTexImage', origin)
        node_mask.image = bpy.data.images.load(masks[index])
        node_mask.image.colorspace_settings.name = 'Non-Color'
        node_math = self._create_node_by_type(
            'ShaderNodeVectorMath',
            self._get_shifted_origin(origin, -200, 0),
        )
        node_math.operation = 'MULTIPLY'
        node_math.inputs[1].default_value = (masks_scale[index],) * 3
        self._links.new(node_uv_tile.outputs['UV'], node_math.inputs['Vector'])
        self._links.new(node_math.outputs['Vector'], node_mask.inputs['Vector'])
        return node_mask
    
    
    def _set_nodes_tex_uniq_tiled(
            self,
            tiles: list,
            is_masks_texture: tuple,
            masks: list,
            masks_scale: tuple,
            nodes_tex_uniq: dict,
            node_uv_tile,
            nodes_tile_scale: list,
        ):
        origin_node_mask = [-1600, 350]
        origin_block_a = [-900, 850]
        origin_block_n = [-900, -750]

        for index in range(4):
            node_mask = self._get_node_mask(
                is_masks_texture,
                masks,
                masks_scale,
                index,
                origin_node_mask,
                node_uv_tile,
            )

            self._set_nodes_tex_uniq_tiled_by_block(
                tiles[index],
                origin_block_a,
                nodes_tile_scale[index],
                node_mask,
                nodes_tex_uniq,
            )
            self._set_nodes_tex_uniq_tiled_by_block(
                tiles[index],
                origin_block_n,
                nodes_tile_scale[index],
                node_mask,
                nodes_tex_uniq,
                True,
            )
            
            origin_node_mask = self._get_shifted_origin(origin_node_mask, 0, -300)
            origin_block_a = self._get_shifted_origin(origin_block_a, 0, 400)
            origin_block_n = self._get_shifted_origin(origin_block_n, 0, -400)

        
    def _set_links_shader(self, nodes_outputs: dict):
        node_shader = self._get_nodes_by_type('BSDF_PRINCIPLED')[0]
        node_normal = self._get_nodes_by_type('NORMAL_MAP')[0]

        self._links.new(
            nodes_outputs['Albedo'].outputs['Color'],
            node_shader.inputs['Base Color'],
        )
        self._links.new(
            nodes_outputs['Metallic'].outputs['Color'],
            node_shader.inputs['Metallic']
        )
        self._links.new(
            nodes_outputs['Roughness'].outputs['Color'],
            node_shader.inputs['Roughness']
        )
        self._links.new(
            nodes_outputs['Normal'].outputs['Color'],
            node_normal.inputs['Color']
        )

    
    def set_tex_tile(
            self,
            tiles: list,
            tiles_scale: tuple,
            is_masks_texture: tuple,
            masks: list,
            masks_scale: tuple,
        ):
        nodes_tex_uniq = self._get_nodes_tex_uniq()
        self._unlink_nodes_tex_uniq(nodes_tex_uniq)
        self._set_uv_tex_uniq(nodes_tex_uniq, [-1200, 0])
        
        origin = [-2400, 0]
        node_uv_tile = self._get_node_uv_tile(origin)
        nodes_tile_scale = self._get_nodes_tile_scale(
            self._get_shifted_origin(origin, 300, 200),
            tiles_scale,
            node_uv_tile,
        )     
        self._set_nodes_tex_uniq_tiled(
            tiles,
            is_masks_texture,
            masks,
            masks_scale,
            nodes_tex_uniq,
            node_uv_tile,
            nodes_tile_scale,
        )

        self._set_links_shader(nodes_tex_uniq)
        return self
    

    @property
    def material(self):
        return self._material
    

    @property
    def material_name(self):
        return self._material.name
