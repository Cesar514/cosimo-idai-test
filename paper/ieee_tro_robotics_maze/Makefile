MAIN=main

.PHONY: pdf clean

pdf:
	latexmk -pdf -interaction=nonstopmode -halt-on-error $(MAIN).tex

clean:
	latexmk -C
