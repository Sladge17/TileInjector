import bpy

from .group_abc import Group_ABC



class Group_MixByIntensity_N(Group_ABC):
    cursor = [0, 0]
    offset = (50, 50)
    name = "MixByIntensity_N"


    @classmethod
    def _get_input_node(cls):
        input_node = cls.nodes.new('NodeGroupInput')
        input_node.location = cls.cursor
        cls.cursor[0] += input_node.width + cls.offset[0]
        return input_node


    @classmethod
    def _get_spherical_angles(cls, output_vector, cursor: list):
        separate_node = cls.nodes.new('ShaderNodeSeparateXYZ')
        separate_node.location = cursor
        cursor[0] += separate_node.width + cls.offset[0]
        cls.links.new(
            output_vector,
            separate_node.inputs['Vector'],
        )

        math_node_1 = cls.nodes.new('ShaderNodeMath')
        math_node_1.operation = 'ARCTAN2'
        math_node_1.location = cursor
        cursor[1] += math_node_1.height + cls.offset[1]
        cls.links.new(
            separate_node.outputs['X'],
            math_node_1.inputs[1],
        )
        cls.links.new(
            separate_node.outputs['Y'],
            math_node_1.inputs[0],
        )

        combine_node = cls.nodes.new('ShaderNodeCombineXYZ')
        combine_node.location = cursor
        cursor[0] += combine_node.width + cls.offset[0]
        cls.links.new(
            separate_node.outputs['X'],
            combine_node.inputs['X'],
        )
        cls.links.new(
            separate_node.outputs['Y'],
            combine_node.inputs['Y'],
        )
        combine_node.inputs['Z'].default_value = 0

        vector_math_node = cls.nodes.new('ShaderNodeVectorMath')
        vector_math_node.operation = 'LENGTH'
        vector_math_node.location = cursor
        cursor[0] += vector_math_node.width + cls.offset[0]
        cls.links.new(
            combine_node.outputs['Vector'],
            vector_math_node.inputs['Vector'],
        )

        math_node_2 = cls.nodes.new('ShaderNodeMath')
        math_node_2.operation = 'ARCTAN2'
        math_node_2.location = cursor
        cls.links.new(
            vector_math_node.outputs['Value'],
            math_node_2.inputs[0],
        )
        cls.links.new(
            separate_node.outputs['Z'],
            math_node_2.inputs[1],
        )
        return math_node_1.outputs[0], math_node_2.outputs[0]
    

    @classmethod
    def _get_intensity_mask(cls, output_color, cursor: list):
        separate_node = cls.nodes.new('ShaderNodeSeparateColor')
        separate_node.location = cursor
        cursor[0] += separate_node.width + cls.offset[0]
        cls.links.new(
            output_color,
            separate_node.inputs['Color'],
        )

        add_node_1 = cls.nodes.new('ShaderNodeMath')
        add_node_1.operation = 'ADD'
        add_node_1.location = cursor
        cursor[0] += add_node_1.width + cls.offset[0]
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
        add_node_2.location = cursor
        cursor[0] += add_node_2.width + cls.offset[0]
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
        divide_node.location = cursor
        cls.links.new(
            add_node_2.outputs['Value'],
            divide_node.inputs[0],
        )
        divide_node.inputs[1].default_value = 3
        return divide_node.outputs[0]

    
    @classmethod
    def _get_mixin_normal_rotation(
        cls,
        mixin_phi_vector,
        mixin_theta_vector,
        intensity_mask_color,
    ):
        math_node = cls.nodes.new('ShaderNodeMath')
        math_node.operation = 'MULTIPLY'
        math_node.location = cls.cursor
        cls.cursor[0] += math_node.width + cls.offset[0]
        cls.links.new(
            mixin_theta_vector,
            math_node.inputs[0],
        )
        cls.links.new(
            intensity_mask_color,
            math_node.inputs[1],
        )

        vector_rotation_node_1 = cls.nodes.new('ShaderNodeVectorRotate')
        vector_rotation_node_1.rotation_type = 'Y_AXIS'
        vector_rotation_node_1.location = cls.cursor
        cls.cursor[0] += vector_rotation_node_1.width + cls.offset[0]
        vector_rotation_node_1.inputs['Vector'].default_value = (0.0, 0.0, 1.0)
        cls.links.new(
            math_node.outputs[0],
            vector_rotation_node_1.inputs['Angle'],
        )

        vector_rotation_node_2 = cls.nodes.new('ShaderNodeVectorRotate')
        vector_rotation_node_2.rotation_type = 'Z_AXIS'
        vector_rotation_node_2.location = cls.cursor
        cls.cursor[0] += vector_rotation_node_2.width + cls.offset[0]
        cls.links.new(
            vector_rotation_node_1.outputs['Vector'],
            vector_rotation_node_2.inputs['Vector'],
        )
        cls.links.new(
            mixin_phi_vector,
            vector_rotation_node_2.inputs['Angle'],
        )
        return vector_rotation_node_2.outputs['Vector']
    

    @classmethod
    def _get_base_normal_rotation(
        cls,
        base_phi_vector,
        base_theta_vector,
        mixin_normal_rotaion_vector,
    ):
        vector_rotation_node_1 = cls.nodes.new('ShaderNodeVectorRotate')
        vector_rotation_node_1.rotation_type = 'Z_AXIS'
        vector_rotation_node_1.invert = True
        vector_rotation_node_1.location = cls.cursor
        cls.cursor[0] += vector_rotation_node_1.width + cls.offset[0]
        cls.links.new(
            mixin_normal_rotaion_vector,
            vector_rotation_node_1.inputs['Vector'],
        )
        cls.links.new(
            base_phi_vector,
            vector_rotation_node_1.inputs['Angle'],
        )

        vector_rotation_node_2 = cls.nodes.new('ShaderNodeVectorRotate')
        vector_rotation_node_2.rotation_type = 'Y_AXIS'
        vector_rotation_node_2.location = cls.cursor
        cls.cursor[0] += vector_rotation_node_2.width + cls.offset[0]
        cls.links.new(
            vector_rotation_node_1.outputs['Vector'],
            vector_rotation_node_2.inputs['Vector'],
        )
        cls.links.new(
            base_theta_vector,
            vector_rotation_node_2.inputs['Angle'],
        )

        vector_rotation_node_3 = cls.nodes.new('ShaderNodeVectorRotate')
        vector_rotation_node_3.rotation_type = 'Z_AXIS'
        vector_rotation_node_3.location = cls.cursor
        cls.cursor[0] += vector_rotation_node_3.width + cls.offset[0]
        cls.links.new(
            vector_rotation_node_2.outputs['Vector'],
            vector_rotation_node_3.inputs['Vector'],
        )
        cls.links.new(
            base_phi_vector,
            vector_rotation_node_3.inputs['Angle'],
        )
        return vector_rotation_node_3.outputs['Vector']
    

    @classmethod
    def _get_fixed_base_normal_rotation(cls, base_normal_rotation_vector):
        separate_node = cls.nodes.new('ShaderNodeSeparateXYZ')
        separate_node.location = cls.cursor
        cls.cursor[0] += separate_node.width + cls.offset[0]
        cls.links.new(
            base_normal_rotation_vector,
            separate_node.inputs['Vector'],
        )

        clamp_node = cls.nodes.new('ShaderNodeClamp')
        clamp_node.location = (cls.cursor[0], cls.cursor[1] - 100)
        cls.cursor[0] += clamp_node.width + cls.offset[0]
        cls.links.new(
            separate_node.outputs['Z'],
            clamp_node.inputs['Value'],
        )
        clamp_node.inputs['Min'].default_value = 0.0
        clamp_node.inputs['Max'].default_value = 1.0

        combine_node = cls.nodes.new('ShaderNodeCombineXYZ')
        combine_node.location = cls.cursor
        cls.cursor[0] += combine_node.width + cls.offset[0]
        cls.links.new(
            separate_node.outputs['X'],
            combine_node.inputs['X'],
        )
        cls.links.new(
            separate_node.outputs['Y'],
            combine_node.inputs['Y'],
        )
        cls.links.new(
            clamp_node.outputs['Result'],
            combine_node.inputs['Z'],
        )

        vector_math_node = cls.nodes.new('ShaderNodeVectorMath')
        vector_math_node.operation = 'NORMALIZE'
        vector_math_node.location = cls.cursor
        cls.cursor[0] += vector_math_node.width + cls.offset[0]
        cls.links.new(
            combine_node.outputs['Vector'],
            vector_math_node.inputs['Vector'],
        )
        return vector_math_node.outputs['Vector']
    

    @classmethod
    def _set_output_node(cls, base_normal_rotation_vector):
        output_node = cls.nodes.new('NodeGroupOutput')
        output_node.location = cls.cursor
        cls.links.new(
            base_normal_rotation_vector,
            output_node.inputs.new('NodeSocketVector', "Vector"),
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
        base_phi, base_theta = cls._get_spherical_angles(
            input_node.outputs.new('NodeSocketVector', "Vector"),
            [cls.cursor[0], cls.cursor[1] + 400],
        )
        mixin_phi, mixin_theta = cls._get_spherical_angles(
            input_node.outputs.new('NodeSocketVector', "Vector"),
            cls.cursor[:],
        )
        intensity_mask = cls._get_intensity_mask(
            input_node.outputs.new('NodeSocketColor', "Color"),
            [cls.cursor[0], cls.cursor[1] - 300],
        )

        cls.cursor[0] += 800
        mixin_normal_rotaion = cls._get_mixin_normal_rotation(
            mixin_phi, mixin_theta, intensity_mask
        )
        base_normal_rotation = cls._get_base_normal_rotation(
            base_phi, base_theta, mixin_normal_rotaion
        )
        base_normal_rotation = cls._get_fixed_base_normal_rotation(
            base_normal_rotation
        )

        cls._set_output_node(base_normal_rotation)
