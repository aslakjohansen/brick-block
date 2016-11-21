# Context

<!-- function block disclaimer: this is a group -->
Due to the foggy definition of a function block I have elected to call this a *group*. That name happens to mirror its functionality; it groups a subgraph. On the subgraph boundary a set of *ports* define its interface.

<!-- what is a group: subgraph, one entity to rule them all, interface through ports -->
The group can be derived by the following process:

1. Start with an RDF graph
2. Draw a circle encompassing the subgraph targeted for grouping
3. Create a group entity (aka node)
4. Make sure every entity within the circle has a within* path to the group entity
5. Ports are placed on the edge of the circle wherever en edge crosses it
6. Each edge crossing a port is split in two
7. Every port has a within edge to the group entity

**Note:** Ports may be reused to account for fanout or -in.

# Problem

The question then becomes, how can we create such a group instance from a group template?

# Approach

## Group Template

The group template should fundamentally be a Brick model. The set of ports belonging to a group which is not part of another group defines the interface. Ports are annotated with a label to allow us to name them.

## Group Instance


