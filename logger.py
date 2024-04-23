class Logger:
    @classmethod
    def task_done(cls):
        print("INFO: Success completed", end="\n\n")


    @classmethod
    def not_target_object(cls, obj: str, target_type: str):
        print(f"\033[33mWARNING: Object \"{obj}\" not a {target_type.lower()}\033[37m")


    @classmethod
    def uv_more_than_need(cls, obj: str, channels: int):
        print(f"\033[33mWARNING: Object \"{obj}\" has uv more than {channels}, need optimize\033[37m")


    @classmethod
    def uv_less_than_need(cls, obj: str, channels: int):
        print(f"\033[33mWARNING: Object \"{obj}\" has uv less than {channels}\033[37m")


    @classmethod
    def empty_sample(cls):
        print("\033[31mERROR: No correct object selected\033[37m")


    @classmethod
    def empty_path(cls, slot: str):
        print(f"\033[31mERROR: Empty path in slot \"{slot}\"\033[37m")
    
    @classmethod
    def file_not_exist(cls, file: str, slot: str):
        print(f"\033[31mERROR: File {file} not exist in slot \"{slot}\"\033[37m")


    @classmethod
    def file_empty(cls, file: str, slot: str):
        print(f"\033[31mERROR: File {file} is empty in slot \"{slot}\"\033[37m")


    @classmethod
    def file_not_texture(cls, file: str, slot: str):
        print(f"\033[31mERROR: File {file} not a texture in slot \"{slot}\"\033[37m")
