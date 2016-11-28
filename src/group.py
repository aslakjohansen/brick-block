from rdflib import Graph, Namespace, URIRef, Literal, BNode
import sys

class Group:
    def __init__ (self, filename):
        self.g = Graph()
        self.g.parse(filename, format='turtle')
    
    # pull apart an entity from the source graph
    def decompose (self, entity):
        paths = []
        for (ns_prefix, path) in self.g.namespace_manager.namespaces():
            if entity.startswith(path): paths.append((ns_prefix, path))
        if len(paths)!=1:
            sys.stderr.write('Error: "%s" decomposes into %u paths, not 1: %s\n' % (entity, len(paths), str(paths)))
        namespace = paths[0][0]
        ns_prefix = paths[0][1]
        name = entity[len(namespace):]
        print('~~~~~~~ types %s %s %s' % (str(type(entity)), str(type(namespace)), str(type(name))))
        return namespace, name, ns_prefix
    
    def instantiate (self, target_namespace, target_prefix):
        g = Graph()
        
        # fetch list of entities
        entities = set()
        for sub, pred, obj in self.g:
            entities.add(sub)
            entities.add(obj)
        entities = sorted(entities)
        
        # find classes
        q = '''
        SELECT DISTINCT ?entity
        WHERE {
            {?entity rdfs:subClassOf*/rdf:type owl:Class} union
            {?entity rdfs:subClassOf*/rdf:type owl:ObjectProperty} union
            {?entity rdfs:subClassOf*/rdf:type owl:AnnotationProperty}
        }
        '''
        class_entities = set(map(lambda row: row[0], self.g.query(q)))
        
        # find literals
        literal_entities = set(filter(lambda entity: type(entity)==Literal, entities))
        
        # find bnodes
        bnode_entities = set(filter(lambda entity: type(entity)==BNode, entities))
        
        # find owls
        owl_entities = set(filter(lambda entity: str(entity).startswith('http://www.w3.org/2002/07/owl#'), entities))
        
        # find brickroots
        brickroot_entities = set(filter(lambda entity: str(entity) in ['http://buildsys.org/ontologies/Brick', 'http://buildsys.org/ontologies/BrickFrame', 'http://buildsys.org/ontologies/BrickTag'], entities))
        
        # define definitions
        definition_entities = sorted(class_entities|literal_entities|bnode_entities|owl_entities|brickroot_entities)
        
        # find instances
        instance_entities = list(set(entities) - set(definition_entities))
        print('instance entities:')
        for entity in instance_entities:
            print(' - instance entity: %s /\n                    %s' % (entity, str(type(entity))))
        
        # process
        mapping = {}
        for sub, pred, obj in self.g:
            for entity in [sub, obj]:
                if not entity in mapping:
                    if entity in definition_entities:
                        newentity = entity
                    else:
                        namespace, name, source_prefix = self.decompose(entity)
                        newentity = target_namespace['%s/%s' % (target_prefix , name)]
                    mapping[entity] = newentity
            if sub in definition_entities or obj in definition_entities:
                g.add( (mapping[sub], pred, mapping[obj]) )
        
        return g
    

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
RDFS  = Namespace('http://www.w3.org/2000/01/rdf-schema#')
OWL   = Namespace('http://www.w3.org/2002/07/owl#')
GROUP = Namespace('http://buildsys.org/ontologies/BrickGroup#')
g.parse('brick_group.ttl', format='turtle')
g.bind('rdf' , RDF)
g.bind('rdfs', RDFS)
g.bind('owl' , OWL)
g.bind('grp' , GROUP)

# brick namespace
for name in brick:
    g.parse('%s/%s' % (brickpath, brick[name]['file']), format='turtle')
    g.bind(brick[name]['prefix'], brick[name]['namespace'])
    globals()[name] = brick[name]['namespace']

# target namespace
EX = Namespace('http://buildsys.org/ontologies/Example#')
g.bind('ex', EX)

################################################################################
###################################################################### main ####

group = Group('brick_rotary_heat_exchanger.ttl')
g2 = group.g

g += group.instantiate(EX, 'rhe1')

