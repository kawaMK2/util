import bpy
import math
import bmesh

file_path = "./mesh_all_3_color.xyzrgb"

def read_xyzrgb(file_path):
    xyz = []
    rgb = []
    with open(file_path) as myfile:
        for line in myfile:
            xyz.append([float(x) / 10 for x in line.split()[0:3]])
            rgb.append([float(r) / 255 for r in line.split()[3:6]])
    return xyz, rgb

def create_faces(num_wid, num_heigh):
    faces = []
    j = 0
    for i in range(0, num_heigh * (num_wid - 1)):
        if j < num_heigh - 1:
            face = (i, i + 1,  i + num_heigh + 1, i + num_heigh)
            faces.append(face)
            j = j + 1
        else:
            j = 0
    return faces

verts, rgb = read_xyzrgb(file_path) 
num_width = int(math.sqrt(len(verts)))
faces = create_faces(num_width, num_width)

# mesh
mesh = bpy.data.meshes.new("terrain")
mesh.from_pydata(verts,[],faces)
mesh.update(calc_edges=True)

# object
object = bpy.data.objects.new("terrain",mesh)
object.location = (-10, -10, 0)
bpy.context.scene.objects.link(object)
bpy.context.scene.objects.active = object
object.select = True

col = object.data.vertex_colors.new(name="Col")

for i, color in enumerate(rgb):
    col.data[i].color = color
