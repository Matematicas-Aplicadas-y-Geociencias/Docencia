# Nombre del archivo principal (sin extensión .tex)
MAIN = main

# Comando base de latexmk
LATEXMK = latexmk -pdf -bibtex

# Compilación estándar
all:
	$(LATEXMK) $(MAIN).tex

# Modo continuo (vigila cambios y recompila automáticamente)
watch:
	$(LATEXMK) -pvc -pdf -bibtex $(MAIN).tex

# Limpiar archivos auxiliares (mantiene el PDF)
clean:
	$(LATEXMK) -c $(MAIN).tex

# Limpiar TODO (incluye el PDF)
cleanall:
	$(LATEXMK) -C $(MAIN).tex

# Abrir el PDF generado
view:
	xdg-open $(MAIN).pdf 2>/dev/null || open $(MAIN).pdf 2>/dev/null || evince $(MAIN).pdf &

# Ayuda
help:
	@echo "Uso:"
	@echo "  make          - Compilar el documento"
	@echo "  make watch    - Compilación continua (vigila cambios)"
	@echo "  make clean    - Limpiar archivos auxiliares"
	@echo "  make cleanall - Limpiar todo (incluye PDF)"
	@echo "  make view     - Abrir el PDF"
	@echo "  make help     - Mostrar esta ayuda"

.PHONY: all watch clean cleanall view help
