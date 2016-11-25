from rdflib import Graph, Namespace, URIRef, Literal
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
    
    # construct an entity in the target graph
    def compose (self, g, target_namespace, taget_prefix, namespace, name, source_prefix):
        ns = Namespace(target_namespace)
        
        # guard: make sure namepace is bound
        if not namespace in map(lambda pair: pair[1], g):
            g.bind(source_prefix, ns)
        
        # construct entity
        return ns['' % (target_namespace)]
    
    # copy an entity from one graph to another
    def copy_to_target (self, g, target_namespace, taget_prefix, entity):
        namespace, name, source_prefix = self.decompose(entity)
        print('%s %s %s' % (namespace, name, ns_prefix))
        target_entity = self.compose(g, target_namespace, taget_prefix, namespace, name, source_prefix)
        return target_entity
    
    def instantiate (self, target_namespace, target_prefix):
        g = Graph()
        
        # fetch list of entities
        entities = set()
        for sub, pred, obj in self.g:
            entities.add(sub)
            entities.add(obj)
        entities = sorted(entities)
        
        # find definitions
        q = 'SELECT DISTINCT ?entity WHERE { {?entity rdfs:subClassOf*/rdf:type owl:Class} union {?entity rdfs:subClassOf*/rdf:type owl:ObjectProperty} }'
        class_entities = sorted(set(self.g.query(q)))
        print('class instances:')
        for entity in class_entities:
            print(' - class entity: %s' % entity)
        
        # copy definitions
        for sub, pred, obj in self.g:
            if sub in class_entities or obj in class_entities:
                g.add( (sub, pred, obj) )
        
        
        
        return g
        
        ########################################################################
        
        # find ports
        q = 'SELECT ?port ?description WHERE { ?port rdf:type grp:Port . ?port grp:labeled ?description }'
        ports = set(self.g.query(q))
        print('ports:')
        for (port, description) in ports:
            print(' - %s "%s"' % (port, description))
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
        
        # find outer groups
        outer_groups = list(filter(lambda group: group not in entities, groups))
        print('outer groups:')
        for group in outer_groups:
            print(' - %s' % group)
        print('')
        
        # find outer entities
        outer_entities = list(filter(lambda entity: True in map(lambda group: (entity,group) in entitygroups,
                                                                outer_groups),
                                     entities))
        print('outer entities:')
        for entity in outer_entities:
            print(' - %s' % entity)
        print('')
        
        # find outer ports
        outer_ports = list(filter(lambda entity: entity in map(lambda port: port[0], ports), outer_entities))
        print('outer ports:')
        for port in outer_ports:
            print(' - %s' % port)
        print('')
        
        # create translation table
        outer_port = outer_ports[0]
        print(outer_port)
        print(type(outer_port))
        print(dir(outer_port))
#        print(help(outer_port.n3))
        print(self.g.namespaces)
        print(self.g.namespace_manager)
        print('')
        print('namespaces:')
        for (ns_prefix, path) in self.g.namespace_manager.namespaces():
            print(' - %9s %s' % (prefix, path))
        print('')
        print(dir(self.g.namespace_manager.store.prefix))
#        print(self.g.namespace_manager.store.prefix.__class__)
#        print(self.g.namespace_manager.store['http://www.w3.org/2001/XMLSchema#'])
        print('')
        
        # copy entities and create translation table
        print('copy and build:')
        for entity in entities:
            self.copy_to_target(g, target_namespace, taget_prefix, entity)
#            match = self.g.namespace_manager.store.prefix(entity)
#            print(match)
#            if not match:
#                sys.stderr.write('Error: Unable to lookup "%s"\n' % entity)
#                continue
#            
#            pfx, uri = match
#            print(' - %9s %s' % (pfx, uri))
        print('')
        
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

# target namespace
EX = Namespace('http://buildsys.org/ontologies/Example#')
g.bind('ex', EX)

################################################################################
###################################################################### main ####

group = Group('brick_rotary_heat_exchanger.ttl')
g2 = group.g

g += group.instantiate(EX, 'rhe1')

