import bpy



class Logger:
    title_error = "ERROR"


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
    def task_done(cls):
        print("INFO: Successfully completed")


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
    def empty_path(cls, slot: str):
        cls._draw_message_error(f"Slot \"{slot}\" is empty")


    @classmethod
    def file_not_exist(cls, file: str, slot: str):
        cls._draw_message_error(f"File \"{file}\" in slot \"{slot}\" does not exist")


    @classmethod
    def file_empty(cls, file: str, slot: str):
        cls._draw_message_error(f"File \"{file}\" in slot \"{slot}\" is empty")


    @classmethod
    def file_not_image(cls, file: str, slot: str):
        cls._draw_message_error(f"File \"{file}\" in slot \"{slot}\" is not an image")
