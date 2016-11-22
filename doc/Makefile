SVG_FIGS = $(wildcard figs/*.svg)
PNG_FIGS = $(SVG_FIGS:.svg=.png)

TARGETS = \
	${PNG_FIGS} \


all: ${TARGETS}

clean:
	touch ${TARGETS}
	rm ${TARGETS}

mrproper:
	touch dummy~ figs/dummy~
	rm *~ figs/*~


figs/%.png: figs/%.svg
	inkscape -z --export-png=$@ --export-area-page $<

