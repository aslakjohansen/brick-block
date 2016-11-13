from rdflib import Graph, Namespace, URIRef, Literal

class Group:
    def __init__ (self, filename):
        self.g = Graph()
        self.g.parse(filename, format='turtle')
    

group = Group('brick_rotary_heat_exchanger.ttl')
g = group.g

print('dir')
ds = sorted(dir(g))
for d in ds:
    print(' - %s' % (d))

print('nodes')
ns = g.all_nodes()
for n in ns:
    print(' - %s' % (n))

