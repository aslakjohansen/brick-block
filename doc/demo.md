# Demonstration

## Group Generator

The [generate_group](https://github.com/aslakjohansen/brick-block/blob/master/src/generate_group) script produces the definitions needed for defining groups. The result is stored as `brick_group.ttl`. The In the following we will see a series of instantiations of such groups using [/src/group.py](https://github.com/aslakjohansen/brick-block/blob/master/src/group.py).

## Rotary Heat Exchanger

The [generate_rotary_heat_exchanger](https://github.com/aslakjohansen/brick-block/blob/master/src/generate_rotary_heat_exchanger) script uses the `brick_group.ttl` definitions to define a rotary heat exchanger:

![Rotary Heat Exchanger](figs/demo_rhx.png)

## Rotary Heat Exchanger Sequence

The [generate_seq_rotary_heat_exchanger](https://github.com/aslakjohansen/brick-block/blob/master/src/generate_seq_rotary_heat_exchanger) script builds on this to instantiate two rotary heat exchangers and connect them in sequence:

![Rotary Heat Exchanger Sequence](figs/demo_seq_rhx.png)

**Note:** The labeling of ports has been omitted due to space constraints.

## 2x2 Rotary Heat Exchanger Setup

The [generate_tbt_rotary_heat_exchanger](https://github.com/aslakjohansen/brick-block/blob/master/src/generate_tbt_rotary_heat_exchanger) script builds on this to instantiate two of these constructs and connect them in parallel:

![2x2 Rotary Heat Exchanger Setup](figs/demo_tbt_rhx.png)

**Note:** The labeling of ports has been omitted due to space constraints.

## Results



