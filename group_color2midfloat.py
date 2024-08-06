import bpy



class Group_Color2MidFloat:
    cursor = [0, 0]
    offset = (50, 50)
    name = "Color2MidFloat"


    @classmethod
    def _check_group_exist(cls):
        if cls.name in bpy.data.node_groups.keys():
            return True
        
        return False


    @classmethod
    def _get_input_node(cls):
        input_node = cls.nodes.new('NodeGroupInput')
        input_node.location = cls.cursor
        cls.cursor[0] += input_node.width + cls.offset[0]
        return input_node


    @classmethod
    def _get_middle_float(cls, output_color):
        separate_node = cls.nodes.new('ShaderNodeSeparateColor')
        separate_node.location = cls.cursor
        cls.cursor[0] += separate_node.width + cls.offset[0]
        cls.links.new(
            output_color,
            separate_node.inputs['Color'],
        )

        add_node_1 = cls.nodes.new('ShaderNodeMath')
        add_node_1.operation = 'ADD'
        add_node_1.location = cls.cursor
        cls.cursor[0] += add_node_1.width + cls.offset[0]
        cls.links.new(
            separate_node.outputs['Red'],
            add_node_1.inputs[0],
        )
        cls.links.new(
            separate_node.outputs['Green'],
            add_node_1.inputs[1],
        )

        add_node_2 = cls.nodes.new('ShaderNodeMath')
        add_node_2.operation = 'ADD'
        add_node_2.location = cls.cursor
        cls.cursor[0] += add_node_2.width + cls.offset[0]
        cls.links.new(
            add_node_1.outputs['Value'],
            add_node_2.inputs[0],
        )
        cls.links.new(
            separate_node.outputs['Blue'],
            add_node_2.inputs[1],
        )

        divide_node = cls.nodes.new('ShaderNodeMath')
        divide_node.operation = 'DIVIDE'
        divide_node.location = cls.cursor
        cls.cursor[0] += divide_node.width + cls.offset[0]
        cls.links.new(
            add_node_2.outputs['Value'],
            divide_node.inputs[0],
        )
        divide_node.inputs[1].default_value = 3
        return divide_node.outputs[0]
    

    @classmethod
    def _set_output_node(cls, middle_float):
        output_node = cls.nodes.new('NodeGroupOutput')
        output_node.location = cls.cursor
        cls.links.new(
            middle_float,
            output_node.inputs.new('NodeSocketFloat', "Value"),
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

        input_node = cls._get_input_node()
        middle_float = cls._get_middle_float(
            input_node.outputs.new('NodeSocketColor', "Color")
        )
        cls._set_output_node(middle_float)


    @classmethod
    def get_group(cls, material:str, location:list=[0, 0]):
        group = bpy.data.materials[material].node_tree.nodes.new('ShaderNodeGroup')
        group.node_tree = bpy.data.node_groups[cls.name]
        group.location = location
        return group
