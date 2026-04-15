# TP01_OC-I
Trabalho pratico de Organização de Computadores I

## Como Executar

Você pode rodar o montador de forma simplificada através do `Makefile` ou usando comandos no próprio terminal.

### Usando o Makefile

Certifique-se de que o arquivo de entrada desejado esteja nomeado como `entrada.asm`.
No terminal, utilize um dos comandos a seguir:

* `make all`: Exibe informações básicas e orientações de uso.
* `make run`: Executa o montador utilizando o `entrada.asm` e gera o resultado em um arquivo chamado `saida.bin`.
* `make terminal`: Executa o montador utilizando o `entrada.asm` e exibe os binários diretamente na tela do terminal.
* `make clean`: Limpa o diretório do projeto, apagando o arquivo gerado (`saida.bin`).
* `make help`: Exibe no terminal a lista de comandos do Makefile disponíveis.

### Usando o Terminal (Manualmente)

Você também pode utilizar o script em Python diretamente, o que possibilita passar qualquer arquivo `.asm` e customizar a saída.

Para rodar e imprimir o resultado diretamente pelo terminal:
```bash
python3 montador.py <nome_arquivo.asm>
```

Para rodar e salvar o resultado em um novo arquivo (ex: `.bin` ou `.txt`):
```bash
python3 montador.py <nome_arquivo.asm> -o <nome_arquivo_saida>
```

Exemplo:
```bash
python3 montador.py entrada.asm -o saida.bin
```
