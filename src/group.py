from rdflib import Graph, Namespace, URIRef, Literal
import sys

class Group:
    def __init__ (self, filename):
        self.g = Graph()
        self.g.parse(filename, format='turtle')
    
    def instantiate (self, g):
        print('diff')
        for s,p,o in self.g:
            if not (s,p,o) in g:
                print(' * %s    %s    %s' % (s,p,o))
    

################################################################################
##################################################################### intro ####

# parts of brick to load
brick = {
    'BRICK': {
        'file': 'Brick.ttl',
        'namespace': Namespace('http://buildsys.org/ontologies/Brick#'),
        'prefix': 'brick',
    },
    'BRICKFRAME': {
        'file': 'BrickFrame.ttl',
        'namespace': Namespace('http://buildsys.org/ontologies/BrickFrame#'),
        'prefix': 'bf',
    },
    'BRICKTAG': {
        'file': 'BrickTag.ttl',
        'namespace': Namespace('http://buildsys.org/ontologies/BrickTag#'),
        'prefix': 'btag',
    },
}

# guard: command line arguments
if len(sys.argv)!=2:
    print('Syntax: %s PATH_TO_BRICK' % sys.argv[0])
    print('        %s ../../GroundTruth/Brick' % sys.argv[0])
    exit(1)
brickpath = sys.argv[1]

# get started on the graph
g = Graph()

# general namespaces
RDF   = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
OWL   = Namespace('http://www.w3.org/2002/07/owl#')
GROUP = Namespace('http://buildsys.org/ontologies/BrickGroup#')
g.parse('brick_group.ttl', format='turtle')
g.bind('rdf', RDF)
g.bind('owl', OWL)
g.bind('grp', GROUP)

# brick namespace
for name in brick:
    g.parse('%s/%s' % (brickpath, brick[name]['file']), format='turtle')
    g.bind(brick[name]['prefix'], brick[name]['namespace'])
    globals()[name] = brick[name]['namespace']

################################################################################
###################################################################### main ####

group = Group('brick_rotary_heat_exchanger.ttl')
g2 = group.g

print('dir')
ds = sorted(dir(g2))
for d in ds:
    print(' - %s' % (d))

print('nodes')
ns = g2.all_nodes()
for n in ns:
    print(' - %s' % (n))

print('graph')
for s,p,o in g2:
    print(' - %s    %s    %s' % (s,p,o))

group.instantiate(g)
