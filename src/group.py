from rdflib import Graph, Namespace, URIRef, Literal, BNode
import sys

GROUP = Namespace('http://buildsys.org/ontologies/BrickGroup#')

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
#        print('~~~~~~~ types %s %s %s' % (str(type(entity)), str(type(namespace)), str(type(name))))
        return namespace, name, ns_prefix
    
    def instantiate (self, target_namespace, target_prefix):
        g = Graph()
        g.bind('grp', GROUP)
        
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
#        print('instance entities:')
#        for entity in instance_entities:
#            print(' - instance entity: %s /\n                    %s' % (entity, str(type(entity))))
        
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
            g.add( (mapping[sub], pred, mapping[obj]) )
        
        # find outer group
        group_tree = {}
        for sub, pred, obj in g:
            if pred==GROUP.within:
                group_tree[sub] = obj
        roots = list(set(filter(lambda val: val[1],
                                map(lambda key: (group_tree[key], not group_tree[key] in group_tree),
                                    group_tree.keys()))))
        if len(roots)!=1:
            print('Error: Group instantiation resulted in %u root(s), expected 1:' % len(roots))
            for i in range(len(roots)):
                print(' %u: %s' % (i, roots[i]))
            sys.exit()
        outer_group = roots[0][0]
        
        # locate ports
        q = '''
        SELECT DISTINCT ?portname ?port
        WHERE {
            ?port rdf:type grp:Port .
            ?port grp:labeled ?portname
        }
        '''
        r = g.query(q)
        ports = {}
        for portname, port in r:
            if (port, GROUP.within, outer_group) in g:
                ports[portname] = port
        
        return {
            'graph': g,
            'ports': ports,
        }
    

