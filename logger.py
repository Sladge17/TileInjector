import bpy



class Logger:
    title_error = "ERROR"
    title_info = "INFO"


    @classmethod
    def _draw_message_info(cls, message):
        print(f"{cls.title_info}: {message}")
        def draw_message(self, context):
            self.layout.label(text=message)
        
        bpy.context.window_manager.popup_menu(
            draw_message,
            title=cls.title_info,
            icon='INFO'
        )

    
    @classmethod
    def _draw_message_error(cls, message):
        print(f"\033[31m{cls.title_error}: {message}\033[37m")
        def draw_message(self, context):
            self.layout.label(text=message)
        
        bpy.context.window_manager.popup_menu(
            draw_message,
            title=cls.title_error,
            icon='ERROR'
        )


    @classmethod
    def created_material(cls, material_name: str):
        cls._draw_message_info(f"Created tiled material: {material_name}")


    @classmethod
    def not_target_object(cls, obj: str, target_type: str):
        print(f"\033[33mWARNING: Object \"{obj}\" is not a {target_type.lower()}\033[37m")


    @classmethod
    def uv_more_than_need(cls, obj: str, channels: int):
        print(f"\033[33mWARNING: Object \"{obj}\" has UV channels more than {channels}, need optimize\033[37m")


    @classmethod
    def uv_less_than_need(cls, obj: str, channels: int):
        print(f"\033[33mWARNING: Object \"{obj}\" has UV channels less than {channels}\033[37m")


    @classmethod
    def empty_sample(cls):
        cls._draw_message_error("Not selected mesh objects with two UV channels")


    @classmethod
    def empty_path(cls, field: str, slot: int):
        cls._draw_message_error(f"Field \"{field}\" of slot \"Tile_{slot}\" is empty")


    @classmethod
    def file_not_exist(cls, file: str, field: str, slot: int):
        cls._draw_message_error(
            f"File \"{file}\" in field \"{field}\" of slot \"Tile_{slot}\" does not exist"
        )


    @classmethod
    def file_empty(cls, file: str, field: str, slot: int):
        cls._draw_message_error(
            f"File \"{file}\" in field \"{field}\" of slot \"Tile_{slot}\" is empty"
        )


    @classmethod
    def file_not_image(cls, file: str, field: str, slot: int):
        cls._draw_message_error(
            f"File \"{file}\" in field \"{field}\" of slot \"Tile_{slot}\" is not an image"
        )
