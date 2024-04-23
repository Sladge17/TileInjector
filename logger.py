class Logger:
    @classmethod
    def task_done(cls):
        print("INFO: Task done", end="\n\n")


    @classmethod
    def not_target_object(cls, obj: str, target_type: str):
        print(f"WARNING: Object \"{obj}\" not a {target_type.lower()}")


    @classmethod
    def uv_more_than_need(cls, obj: str, channels: int):
        print(f"WARNING: Object \"{obj}\" has uv more than {channels}, need optimize")


    @classmethod
    def uv_less_than_need(cls, obj: str, channels: int):
        print(f"WARNING: Object \"{obj}\" has uv less than {channels}")


    @classmethod
    def empty_sample(cls):
        print("ERROR: No correct object selected")


    @classmethod
    def empty_path(cls, slot: str):
        print(f"ERROR: Empty path in slot \"{slot}\"")
    
    @classmethod
    def file_not_exist(cls, file: str, slot: str):
        print(f"ERROR: File {file} not exist in slot \"{slot}\"")


    @classmethod
    def file_empty(cls, file: str, slot: str):
        print(f"ERROR: File {file} is empty in slot \"{slot}\"")


    @classmethod
    def file_not_texture(cls, file: str, slot: str):
        print(f"ERROR: File {file} not a texture in slot \"{slot}\"")
