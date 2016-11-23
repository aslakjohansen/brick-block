# Context

<!-- what do we hope to accomplish with this? -->

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

The group template should fundamentally be a Brick model. The set of ports belonging to an outer group (a group which is not part of another group) defines the interface. Ports are annotated with a label to allow us to name them individually.

## Group Instance

Given a graph template, generating a corresponding graph instance is the matter of:

* 
* Exposing the outer ports for composition

# Example

A rotary heat exchanger is a device which transfers heat (but not matter) between two flows of air. It does so by sending both through a rotating barrel with a large surface and and a high heat conductivity (think of a barrel filled up with copper pipes). How do we model this is Brick?

![Single-entity representation](figs/rhx_single.png)

In order to differentiate the two flows we would have to subclass these flow relations. This (i) moves the problem to the relations, (ii) exposes the complexities of the solution to the users, and (iii) makes it harder to write queries (having to differentiate between `feedsReturn` and `feedsSupply`). What happens if we use a two-node setup where each node represents a distinct flow and a relation between them specifies how one affects the other?

![Simple two-entity representation](figs/rhx.png)

This relation integrates significantly better with SparQL (and similar querying languages) as one can find anything being thermically affected by `?heater` by the triplet pattern `?heater (feeds|affectsHeat)+ ?thing`. However, device is now represented by two entities and one relation; there is no single entity for referencing the device.

In addition to solving this, the group also allows us to operate at a higher level of abstraction.

![Complex eleven-entity representation](figs/rhx_complex.png)

At first this seems like a lot of complexity. The entity count goes from two to eleven. What do we gain from increasing this complexity? It allows us to name a port of a group:

```sparql
SELECT ?port ?group
WHERE {
    ?port rdf:type grp:Port .
    ?port grp:within ?group .
    ?port grp:labeled "Source Input" .
}

```

This in turn provides us with the fundamentals for reasoning about subgraphs and their interactions.

![Becoming a block](figs/becoming.png)

At this point the subgraph can be seen as a block with an interface separating use from implementation. In short, it allows us to compose our graph (or subgraph) at block-level granularity.
