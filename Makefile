# Makefile - Montador RISC-V CCF 252
# Grupo 18

PYTHON = python3
SRC = montador.py
ASM_FILE = entrada.asm
OUT_FILE = saida.bin

all:
	@echo "Montador em Python pronto para uso. Não requer compilação."
	@echo "Use 'make run' para um teste rápido ou 'make help' para comandos."
	@echo ""

run:
	$(PYTHON) $(SRC) $(ASM_FILE) -o $(OUT_FILE)
	@echo "Sucesso! Binário gerado em $(OUT_FILE)"
	@echo ""

terminal:
	$(PYTHON) $(SRC) $(ASM_FILE)

help:
	@echo "Comandos disponíveis:"
	@echo "  make all      - Exibe informações básicas e orientações de uso"
	@echo "  make run      - Executa o montador com entrada.asm e gera arquivo de saída"
	@echo "  make terminal - Executa o montador e exibe o binário na tela"
	@echo "  make clean    - Remove arquivos binários temporários"
	@echo ""

clean:
	rm -f $(OUT_FILE)
	@echo "Arquivos limpos."
	@echo ""