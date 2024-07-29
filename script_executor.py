import os
import sys



script_path = "/home/maxim/Projects/TileInjector"
script_name = "__init__.py"

sys.path.append(script_path)

script_filename = os.path.join(script_path, script_name)
with open(script_filename) as text:
    script = text.read()

exec(compile(
    source=script,
    filename=script_filename,
    mode='exec',
))
