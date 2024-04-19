import os


script_path = "/home/maxim/Projects/LestaTest"
script_name = "main.py"

script_filename = os.path.join("/home/maxim/Projects/LestaTest", "main.py")
with open(script_filename) as text:
    script = text.read()

exec(compile(
    source=script,
    filename=script_filename,
    mode='exec',
))
