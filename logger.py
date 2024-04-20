class Logger:
    @classmethod
    def task_done(cls):
        print("INFO: Task done", end="\n\n")


    @classmethod
    def empty_sample(cls):
        print("ERROR: No object selected")


    @classmethod
    def not_target_object(cls, obj, target_type: str):
        print(f"WARNING: Object \"{obj.name}\" not a {target_type.lower()}")
