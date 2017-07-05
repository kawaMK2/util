import bpy
import os

current_path = bpy.path.abspath("//")
node_tree = bpy.context.scene.node_tree
list = bpy.data.images.keys()
if not os.path.exists(current_path+"out"):
        os.mkdir(current_path+"out")

for filename in os.listdir(current_path):
    name, ext = os.path.splitext(filename)
    if ext == ".JPG" and filename not in list:
        bpy.ops.image.open(filepath="//"+filename)
        node_tree.nodes["InputImage"].image = bpy.data.images[filename]
        bpy.ops.render.render()
        bpy.data.images["Render Result"].save_render(filepath=current_path+"out/"+name+"G"+ext)
        