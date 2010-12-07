all:
	pdflatex report.tex
	bibtex milestone.aux
	pdflatex report.tex
	pdflatex report.tex

clean:
	rm -f *.aux *.bbl *.blg *.log *.pdf
