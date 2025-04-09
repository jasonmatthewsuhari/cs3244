PDF = main.pdf
TEX = main.tex

pdf:
	pdflatex $(TEX)
	-bibtex main || true
	pdflatex $(TEX)
	pdflatex $(TEX)
ifeq ($(OS),Windows_NT)
	explorer.exe $(PDF)
else
	open $(PDF) || xdg-open $(PDF)
endif

