class Logger:
    @classmethod
    def task_done(cls):
        print("INFO: Task done", end="\n\n")


    @classmethod
    def empty_sample(cls):
        print("ERROR: No object selected")


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
    def remove_material(cls, name: str):
        print(f"WARNING: Material \"{name}\" was removed")


    @classmethod
    def tex_wrong_name(cls, tex_name: str):
        print(f"ERROR: Texture {tex_name} has wrong name")
