from rdflib import Graph, Namespace, URIRef, Literal, BNode
import sys

GROUP = Namespace('http://buildsys.org/ontologies/BrickGroup#')

cache = {}

# pull apart an entity from the source graph
def decompose (def_g, entity):
    '''
    Extracts from an entity a tuple containing the rdflib namespace
    holding the entity, the relative name of the entity within this
    namespace, and the active abbreviation for this namespace.
    
    Arguments:
    def_g -- definition graph context
    entity -- the entity to decompose
    '''
    
    paths = []
    for (ns_prefix, path) in def_g.namespace_manager.namespaces():
        if entity.startswith(path): paths.append((ns_prefix, path))
    if len(paths)!=1:
        sys.stderr.write('Error: "%s" decomposes into %u paths, not 1: %s\n' % (entity, len(paths), str(paths)))
    ns_prefix = paths[0][0]
    namespace = paths[0][1]
    name = entity[len(namespace):]
    return namespace, name, ns_prefix

def instantiate (filename, target_namespace, target_prefix):
    '''
    Construct a graph containing an instance of group.
    
    Arguments:
    filename -- which turtle file (ttl-extension) to load the definition from
    target_namespace -- which namespace to place the instance entities in
    target_prefix -- what the prefix the instance entities with
    
    It will return a dictionary with three entries:
    graph -- the resulting graph
    ports -- a dictionary mapping port names to port entities
    group -- the encapsulating group entity
    '''
    
    if not filename in cache:
        cache[filename] = Graph()
        cache[filename].parse(filename, format='turtle')
    def_g = cache[filename]
    
    g = Graph()
    g.bind('grp', GROUP)
    
    # clone namespace bindings
    for (ns_prefix, path) in def_g.namespace_manager.namespaces():
        g.bind(ns_prefix, Namespace(path))
    
    # fetch list of entities
    entities = set()
    for sub, pred, obj in def_g:
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
    class_entities = set(map(lambda row: row[0], def_g.query(q)))
    
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
    
    # process
    mapping = {}
    for sub, pred, obj in def_g:
        for entity in [sub, obj]:
            if not entity in mapping:
                if entity in definition_entities:
                    newentity = entity
                else:
                    namespace, name, source_prefix = decompose(def_g, entity)
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
    SELECT DISTINCT ?port ?type
    WHERE {
        ?port rdf:type/rdfs:subClassOf+ grp:Port .
        ?port rdf:type ?type
    }
    '''
    r = g.query(q)
    ports = {}
    for port, ptype in r:
        if (port, GROUP.within, outer_group) in g:
            portname = decompose(g, ptype)[1]
            ports[portname] = port
    
    return {
        'graph': g,
        'ports': ports,
        'group': outer_group,
    }


