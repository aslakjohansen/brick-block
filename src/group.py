from rdflib import Graph, Namespace, URIRef, Literal
import sys

class Group:
    def __init__ (self, filename):
        self.g = Graph()
        self.g.parse(filename, format='turtle')
    
    def instantiate (self, g):
        # find ports
        q = 'SELECT ?port WHERE { ?port rdf:type grp:Port }'
        ports = set(self.g.query(q))
        print('ports:')
        for port in ports:
            print(' - %s' % port)
        print('')
        
        # find entities
        q = 'SELECT ?entity ?group WHERE { ?group rdf:type grp:Group . ?entity grp:within ?group }'
        entitygroups = set(self.g.query(q))
        entities = set(map(lambda entry: entry[0], entitygroups))
        print('entities:')
        for entity, group in entitygroups:
            print(' - %s of %s' % (entity, group))
        print('')
        
        # find groups
        groups = set(map(lambda entry: entry[1], entitygroups))
        print('groups:')
        for group in groups:
            print(' - %s' % group)
        print('')
        
        # find outer group
        outer_groups = filter(lambda group: group not in entities, groups)
        print('outer groups:')
        for group in outer_groups:
            print(' - %s' % group)
        print('')
        
        # find outer ports
        
        # create translation table
        
        # copy entities
        
        # copy relations
        
        # create and return portmap
    

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

group.instantiate(g)

