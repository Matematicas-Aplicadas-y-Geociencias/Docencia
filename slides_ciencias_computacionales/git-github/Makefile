NAME = slides-git-github
all:
	latexmk -pdf $(NAME).tex

clean:
	latexmk -c $(NAME).tex
	rm -f $(NAME).nav $(NAME).snm $(NAME).vrb

cleanAll: clean
	rm -f $(NAME).pdf

.PHONY: all clean cleanAll
