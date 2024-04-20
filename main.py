import bpy
import os
import sys
sys.path.append(os.environ['SCRIPT_PATH'])

from logger import Logger



def check_empty_sample(selected_objects):
    if not len(selected_objects):
        return True
    return False


def get_selected_meshes():
    selected_objects = bpy.context.selected_objects
    if check_empty_sample(selected_objects):
        Logger.empty_sample()
        return None

    selected_meshes = []
    for obj in selected_objects:
        if not obj.type == 'MESH':
            Logger.not_mesh(obj)
            continue
        selected_meshes.append(obj)
   
    return selected_meshes


def main():
    selected_meshes = get_selected_meshes()
    if not selected_meshes:
        return
    
    for mesh in selected_meshes:
        print(mesh)



if __name__ == "__main__":
    main()
    Logger.task_done()
