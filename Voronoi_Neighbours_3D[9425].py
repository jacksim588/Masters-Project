import math
import numpy as np
from CGAL.CGAL_Kernel import Point_3
import CGAL.CGAL_Triangulation_3 as T

# Dimensions of a unit cell, as described in https://chem.libretexts.org/Courses/University_of_Arkansas_Little_Rock/Chem_1403%3A_General_Chemistry_2/Text/12%3A_Solids/12.01%3A_Crystal_Lattices_and_Unit_Cells

a, b, c = 1, 1, 1 # Lengths a, b, c.
al, be, ga = 90, 90, 90 # Angles alpha, beta, gamma in degrees.

#######################################

# Generation of lattice vectors u, v, w is derived from https://en.wikipedia.org/wiki/Fractional_coordinates

def Cell_Volume(a, b, c, al, be, ga):
    vol = a * b * c * np.sqrt( 1 - np.power(math.cos(al * math.pi / 180), 2) - np.power(math.cos(be * math.pi / 180), 2) - np.power(math.cos(ga * math.pi / 180), 2) + 2 * math.cos(al * math.pi / 180) * math.cos(be * math.pi / 180) * math.cos(ga * math.pi / 180))
    return vol

def Lattice_Vectors(a, b, c, al, be, ga):
    u = (a, 0, 0)
    v = (b * math.cos(ga * math.pi / 180), b * math.sin(ga * math.pi / 180), 0)

    x = c * math.cos(be * math.pi / 180)
    y = c * (math.cos(al * math.pi / 180 ) - math.cos(be * math.pi / 180) * math.cos(ga * math.pi / 180)) / math.sin(ga * math.pi / 180)
    z = Cell_Volume(a, b, c, al, be, ga) / (a * b * math.sin(ga * math.pi / 180))

    w = (x, y, z)

    return u, v, w

u, v, w = Lattice_Vectors(a, b, c, al, be, ga)

# A sufficiently large point cloud is generated.

points = []
dis = {}
k = 100

for counter_1 in range(-5, 6):
    for counter_2 in range(-5, 6):
        for counter_3 in range(-5, 6):
            points.append((u[0] * counter_1 + v[0] * counter_2 + w[0] * counter_3, u[1] * counter_1 + v[1] * counter_2 + w[1] * counter_3, u[2] * counter_1 + v[2] * counter_2 + w[2] * counter_3))

for elem in points:
    dis[elem] = np.sqrt(np.power(elem[0], 2) + np.power(elem[1], 2) + np.power(elem[2], 2))

dis = dict(sorted(dis.items(), key=lambda item: item[1]))
dis_items = dis.items()
points = list(dis_items)[:k]
points = [Point_3(column[0][0], column[0][1], column[0][2]) for column in points]

# Compute the Delaunay triangulation of the point cloud.

Del = T.Delaunay_triangulation_3(points)

# Write traingulation to file.

Del.write_to_file("output")

# Read triangulation and output any vertex that shares a cell with the origin in the Delaunay triangulation.

f = open("output", 'r')

f.readline()

num_vert = int(f.readline())

origin = -1
vertices = []

for counter in range(num_vert):
    fields = f.readline().split(' ')
    vertices.append((round(float(fields[0]), 2), round(float(fields[1]), 2), round(float(fields[2]), 2)))
    if float(fields[0]) == 0 and float(fields[1]) == 0 and float(fields[2]) == 0:
        origin = counter + 1

num_cells = int(f.readline())

voronoi_neighbours = set()

for counter in range(num_cells):
    fields = f.readline().split(' ')
    if int(fields[0]) == origin or int(fields[1]) == origin or int(fields[2]) == origin or int(fields[3]) == origin:
        voronoi_neighbours.update({int(fields[0]), int(fields[1]), int(fields[2]), int(fields[3])})

f.close()

voronoi_neighbours.discard(origin)

with open('Voronoi_Neighbours.txt', mode='w', encoding='utf-8') as output:
    for elem in voronoi_neighbours:
        print(vertices[elem - 1])
        output.write(str(vertices[elem - 1]))
        output.write('\n')
