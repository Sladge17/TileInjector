import bpy



class Group_MixByColor:
    cursor = [0, 0]
    offset = (50, 100)
    channels = ('Red', 'Green', 'Blue')
    name = "MixByColor"


    @classmethod
    def _check_group_exist(cls):
        if cls.name in bpy.data.node_groups.keys():
            return True
        
        return False


    @classmethod
    def _set_input_node(cls):
        cls.input_node = cls.nodes.new('NodeGroupInput')
        cls.input_node.location = cls.cursor
        cls.cursor[0] += cls.input_node.width + cls.offset[0]


    @classmethod
    def _set_separate_node_mask(cls):
        cls.separate_node_mask = cls.nodes.new('ShaderNodeSeparateColor')
        cls.separate_node_mask.location = cls.cursor
        cls.cursor[0] += cls.separate_node_mask.width + cls.offset[0]


    @classmethod
    def _set_mix_nodes_block(cls):
        cls.mix_nodes = [None] * 3
        cls.separate_nodes = [None] * 3
        cls.cursor[1] += 200
        for index, channel in enumerate(cls.channels):
            cls.mix_nodes[index] = cls.nodes.new('ShaderNodeMixRGB')
            cls.mix_nodes[index].location = cls.cursor
            cls.links.new(
                cls.separate_node_mask.outputs[channel],
                cls.mix_nodes[index].inputs['Fac'],
            )
            
            cls.separate_nodes[index] = cls.nodes.new('ShaderNodeSeparateColor')
            cls.separate_nodes[index].location =\
                (cls.cursor[0] + cls.mix_nodes[index].width + cls.offset[0], cls.cursor[1])
            cls.links.new(
                cls.mix_nodes[index].outputs['Color'],
                cls.separate_nodes[index].inputs['Color'],
            )
            
            cls.cursor[1] -= cls.mix_nodes[index].height + cls.offset[1]

        cls.cursor[0] +=\
            cls.mix_nodes[index].width + cls.separate_nodes[index].width + 2 * cls.offset[0]
        cls.cursor[1] = 0


    @classmethod
    def _set_combine_node(cls):
        cls.combine_node = cls.nodes.new('ShaderNodeCombineColor')
        cls.combine_node.location = cls.cursor
        for index, channel in enumerate(cls.channels):
            cls.links.new(
                cls.separate_nodes[index].outputs[channel],
                cls.combine_node.inputs[channel],
            )

        cls.cursor[0] += cls.combine_node.width + cls.offset[0]


    @classmethod
    def _set_output_node(cls):
        cls.output_node = cls.nodes.new('NodeGroupOutput')
        cls.output_node.location = cls.cursor


    @classmethod
    def _link_input_node(cls):
        cls.input_node.outputs.new('NodeSocketColor', "Color1")
        for index in range(len(cls.mix_nodes)):
            cls.links.new(
                cls.input_node.outputs['Color1'],
                cls.mix_nodes[index].inputs['Color1'],
            )
            
        cls.input_node.outputs.new('NodeSocketColor', "Color2")
        for index in range(len(cls.mix_nodes)):
            cls.links.new(
                cls.input_node.outputs['Color2'],
                cls.mix_nodes[index].inputs['Color2'],
            )

        cls.input_node.outputs.new('NodeSocketColor', "Color")
        cls.links.new(
            cls.input_node.outputs['Color'],
            cls.separate_node_mask.inputs['Color'],
        )


    @classmethod
    def _link_output_node(cls):
        cls.output_node.inputs.new('NodeSocketColor', "Color")
        cls.links.new(
            cls.combine_node.outputs['Color'],
            cls.output_node.inputs['Color'],
        )
    
    
    @classmethod
    def set_group(cls):
        if cls._check_group_exist():
            return
        
        group = bpy.data.node_groups.new(
            name=cls.name,
            type='ShaderNodeTree',
        )
        cls.nodes = group.nodes
        cls.links = group.links

        cls._set_input_node()
        cls._set_separate_node_mask()
        cls._set_mix_nodes_block()
        cls._set_combine_node()
        cls._set_output_node()

        cls._link_input_node()
        cls._link_output_node()


    @classmethod
    def get_group(cls, material:str, location:list=[0, 0]):
        group = bpy.data.materials[material].node_tree.nodes.new('ShaderNodeGroup')
        group.node_tree = bpy.data.node_groups[cls.name]
        group.location = location
        return group
