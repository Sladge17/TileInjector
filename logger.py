class Logger:
    @classmethod
    def task_done(cls):
        print("INFO: Task done")


    @classmethod
    def empty_sample(cls):
        print("WARNING: No object selected")


    @classmethod
    def not_mesh(cls, obj):
        print(f"WARNING: Object \"{obj.name}\" not a mesh")
