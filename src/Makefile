TARGETS = \
	demo.txt \
	demo_replaced.txt \


all: ${TARGETS}

clean:
	touch ${TARGETS} dummy.ttl
	rm    ${TARGETS}     *.ttl

mrproper: clean
	touch dummy~
	rm        *~


brick_group.ttl: generate_group
	./generate_group

brick_rotary_heat_exchanger.ttl: generate_rotary_heat_exchanger brick_group.ttl group.py
	./generate_rotary_heat_exchanger ../../GroundTruth/Brick

brick_seq_rotary_heat_exchanger.ttl: generate_seq_rotary_heat_exchanger brick_rotary_heat_exchanger.ttl group.py
	./generate_seq_rotary_heat_exchanger ../../GroundTruth/Brick

brick_tbt_rotary_heat_exchanger.ttl: generate_tbt_rotary_heat_exchanger brick_seq_rotary_heat_exchanger.ttl group.py
	./generate_tbt_rotary_heat_exchanger ../../GroundTruth/Brick

demo.ttl: generate_demo_setup brick_tbt_rotary_heat_exchanger.ttl group.py
	./generate_demo_setup ../../GroundTruth/Brick

demo.txt: demo demo.ttl
	./demo ../../GroundTruth/Brick demo.ttl > demo.txt

demo_replaced.ttl: generate_demo_replaced_setup demo.ttl passthrough.ttl group.py
	./generate_demo_replaced_setup ../../GroundTruth/Brick

demo_replaced.txt: demo demo_replaced.ttl
	./demo ../../GroundTruth/Brick demo_replaced.ttl > demo_replaced.txt

passthrough.ttl: generate_passthrough
	./generate_passthrough ../../GroundTruth/Brick

