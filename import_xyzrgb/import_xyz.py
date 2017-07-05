import bpy
import math
import bmesh

file_path = "./mesh_all_1.xyz"

def read_verts(file_path):
    verts = [] 
    with open(file_path) as myfile:
        for line in myfile:
            verts.append([float(x) / 10 for x in line.split()])
    return verts

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



verts = read_verts(file_path) 
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