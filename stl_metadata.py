
from collections import defaultdict, namedtuple
import sys

Point = namedtuple('Point', 'x y z')
class Facet():
    ''' facet implementation '''

    def __init__(self, n: tuple, v: list) -> None:
        ''' init facet object '''
        self.N = n
        self.A = Point(*v[0])
        self.B = Point(*v[1])
        self.C = Point(*v[2])
        self.area = self.find_area()

    def __repr__(self) -> str:
        ''' string repr for facet '''
        return f"N: {self.N}, A: {self.A} B: {self.B} C: {self.C}"

    def find_area(self) -> float:
        ''' Heron's formula for triangle area '''
        a, b, c = self.A, self.B, self.C

        def _distance(p1: Point, p2: Point) -> float:
            return ((p2.x-p1.x)**2 +
                    (p2.y-p1.y)**2 +
                    (p2.z-p1.z)**2)**.5

        ab = _distance(a, b)
        bc = _distance(b, c)
        ca = _distance(c, a)
        s = 0.5 * (ab + bc + ca)  # semi-perimeter
        return (s * (s - ab) * (s - bc) * (s - ca))**.5

    def get_normal(self) -> tuple:
        ''' get facet normal '''
        return self.N

    def get_vertices(self) -> tuple:
        ''' get facet vertices '''
        return (self.A, self.B, self.C)

    def get_area(self) -> float:
        ''' get facet area '''
        return self.area


class Surface():
    ''' surface implementation '''

    def __init__(self) -> None:
        ''' init surface object '''
        self.name = None
        self.area = 0
        self.facets = []
        self.vertices = defaultdict(list)
        self.min_x = self.max_x = \
            self.min_y = self.max_y = \
            self.min_z = self.max_z = 0

    def set_name(self, name: str) -> None:
        ''' set surface name '''
        self.name = name

    def load(self, filename: str) -> None:
        ''' parse/load stl file '''

        """ format
        solid Moon
        facet normal -0.785875 0 -0.618385
        outer loop
            vertex 0.360463 0 2.525
            vertex 0 0 2.98309
            vertex 0.360463 0.2 2.525
        endloop
        endfacet
        """

        def _parse_line(l):
            key_val = l.split()
            return (key_val[0], key_val[1:])

        with open(filename) as fp:
            normal, vertices = None, []
            for line in fp:
                key, value = _parse_line(line)
                if key == 'solid':
                    self.set_name(value)
                elif key == 'facet':
                    normal = tuple(map(float, value[1:]))
                elif key == 'vertex':
                    v = tuple(map(float, value))
                    vertices.append(v)
                elif key == 'endfacet':
                    self.add_facet(normal, vertices)
                    normal, vertices = None, []
                else:
                    pass

    def add_facet(self, n: list, verts: list) -> None:
        ''' add facet to surface '''
        f = Facet(n, verts)
        self.set_area(f)
        self.set_min_max(f)
        self.facets.append(f)
        for v in verts:
            self.vertices[v].append(f)

    def get_facets(self) -> list:
        ''' get facet list '''
        return self.facets

    def find_facets(self, vert: tuple) -> list:
        ''' find facets for a particular vertex '''
        return self.vertices[vert]

    def set_area(self, f: Facet) -> None:
        self.area += f.get_area()

    def get_area(self) -> str:
        ''' get total surface area '''
        return ("%.6f" % self.area)

    def set_min_max(self, f: Facet) -> None:
        ''' find min/max values '''
        A = f.get_vertices()[0]
        self.min_x = min(self.min_x, A.x)
        self.max_x = max(self.max_x, A.x)
        self.min_y = min(self.min_y, A.y)
        self.max_y = max(self.max_y, A.y)
        self.min_z = min(self.min_z, A.z)
        self.max_z = max(self.max_z, A.z)

    def find_dims(self) -> tuple:
        ''' find the max-min dimensions '''
        return (self.max_x - self.min_x,
                self.max_y - self.min_y,
                self.max_z - self.min_z)

    def find_bounds(self) -> tuple:
        ''' find vertices of bounding box '''
        X, Y, Z = self.find_dims()
        return ((0, 0, 0), (0, 0, Z), (0, Y, 0), (0, Y, Z),
                (X, 0, 0), (X, 0, Z), (X, Y, 0), (X, Y, Z))
    def get_bounding_box_volume(self):
        X,Y,Z = self.find_dims()
        return X*Y*Z

if __name__ == "__main__":

    # if len(sys.argv) == 2 and sys.argv[1][-4:] == ".stl":
    #     file_ = sys.argv[1]
    # else:
    #     print("format: stl_data <filename.stl>")
    #     sys.exit()
    file_ = "C:\\Users\\COE\\Desktop\\stl_1000\\123597_310-711du_prt.stl"
    surface = Surface()
    surface.load(file_)

    print(f"Number of Triangles: {len(surface.get_facets())}")
    print(f"Surface Area: {surface.get_area()}")
    bounds = surface.find_bounds()
    print(f"Bounding Box:")
    for vertex in bounds:
        print(f"{vertex}")
    
    vol = surface.get_bounding_box_volume()
    print(f"Bounding box volume:{vol}")