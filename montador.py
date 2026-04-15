# Montador RISC-V CCF 252
# Grupo 18

import sys

# registradores x0 a x31
REG = {}
for i in range(32):
    nome = "x" + str(i)
    numero = i
    binario = ""
    if numero == 0:
        binario = "0"
    else:
        while numero > 0:
            resto = numero % 2
            binario = str(resto) + binario
            numero = numero // 2
    while len(binario) < 5:
        binario = "0" + binario
    REG[nome] = binario

# opcodes por tipo
OPCODES = {
    'R': '0110011',
    'I': '0010011',
    'L': '0000011',
    'S': '0100011',
    'B': '1100011',
    'J': '1101111',
    'JR': '1100111',
    'U_LUI': '0110111',
    'U_AUIPC': '0010111'
}

# tipo de cada instrucao
TIPO = {
    'add': 'R',
    'sub': 'R',
    'and': 'R',
    'or': 'R',
    'xor': 'R',
    'sll': 'R',
    'srl': 'R',
    'sra': 'R',
    'slt': 'R',
    'sltu': 'R',
    'addi': 'I',
    'andi': 'I',
    'ori': 'I',
    'xori': 'I',
    'slti': 'I',
    'sltiu': 'I',
    'lw': 'L',
    'lb': 'L',
    'lh': 'L',
    'lbu': 'L',
    'lhu': 'L',
    'sw': 'S',
    'sb': 'S',
    'sh': 'S',
    'beq': 'B',
    'bne': 'B',
    'blt': 'B',
    'bge': 'B',
    'jal': 'J',
    'jalr': 'JR',
    'lui': 'U_LUI',
    'auipc': 'U_AUIPC'
}

FUNCT3 = {
    'add': '000',
    'sub': '000',
    'and': '111',
    'or': '110',
    'xor': '100',
    'sll': '001',
    'srl': '101',
    'sra': '101',
    'slt': '010',
    'sltu': '011',
    'addi': '000',
    'andi': '111',
    'ori': '110',
    'xori': '100',
    'slti': '010',
    'sltiu': '011',
    'lw': '010',
    'lb': '000',
    'lh': '001',
    'lbu': '100',
    'lhu': '101',
    'sw': '010',
    'sb': '000',
    'sh': '001',
    'beq': '000',
    'bne': '001',
    'blt': '100',
    'bge': '101',
    'jalr': '000'
}

FUNCT7 = {
    'add': '0000000',
    'sub': '0100000',
    'and': '0000000',
    'or': '0000000',
    'xor': '0000000',
    'sll': '0000000',
    'srl': '0000000',
    'sra': '0100000',
    'slt': '0000000',
    'sltu': '0000000'
}


def para_binario(valor_string, bits):
    valor = int(valor_string)
    if valor < 0:
        valor = valor + (2 ** bits)
    numero = valor
    binario = ""
    if numero == 0:
        binario = "0"
    else:
        while numero > 0:
            resto = numero % 2
            binario = str(resto) + binario
            numero = numero // 2
    while len(binario) < bits:
        binario = "0" + binario
    if len(binario) > bits:
        binario = binario[len(binario) - bits : len(binario)]
    return binario


def limpa_linha(linha):
    linha_limpa = ""
    for caractere in linha:
        if caractere == '#':
            break
        linha_limpa = linha_limpa + caractere
    linha_sem_sinais = ""
    for c in linha_limpa:
        if c == ',' or c == '(' or c == ')':
            linha_sem_sinais = linha_sem_sinais + " "
        else:
            linha_sem_sinais = linha_sem_sinais + c
    return linha_sem_sinais.strip()


def pre_processa(linhas):
    labels = {}
    pc = 0
    codigo_intermediario = []

    for linha in linhas:
        linha_limpa = limpa_linha(linha)

        if linha_limpa == "":
            continue

        tem_label = False
        for c in linha_limpa:
            if c == ':':
                tem_label = True
                break

        if tem_label:
            partes_label = linha_limpa.split(':')
            nome_do_label = partes_label[0].strip()
            labels[nome_do_label] = pc
            resto = ""
            for i in range(1, len(partes_label)):
                resto = resto + partes_label[i] + " "
            linha_limpa = resto.strip()
            if linha_limpa == "":
                continue

        partes = linha_limpa.split()
        if len(partes) == 0:
            continue

        op = partes[0].lower()

        # pseudo-instrucoes
        if op == "li":
            codigo_intermediario.append("addi " + partes[1] + " x0 " + partes[2])
        elif op == "mv":
            codigo_intermediario.append("addi " + partes[1] + " " + partes[2] + " 0")
        elif op == "j":
            codigo_intermediario.append("jal x0 " + partes[1])
        elif op == "ret":
            codigo_intermediario.append("jalr x0 x1 0")
        elif op == "nop":
            codigo_intermediario.append("addi x0 x0 0")
        else:
            linha_refeita = ""
            for p in partes:
                linha_refeita = linha_refeita + p + " "
            codigo_intermediario.append(linha_refeita.strip())

        pc = pc + 4

    return codigo_intermediario, labels


def montar(linhas):
    processado, labels = pre_processa(linhas)
    codigo_binario_final = []
    pc = 0

    for linha in processado:
        partes = linha.split()
        op = partes[0].lower()

        if op not in TIPO:
            print("Erro: instrução " + op + " não reconhecida.")
            sys.exit(1)

        t = TIPO[op]
        opc = OPCODES[t]

        if t == 'R':
            rd = partes[1].lower()
            rs1 = partes[2].lower()
            rs2 = partes[3].lower()
            f3 = FUNCT3[op]
            f7 = FUNCT7[op]
            resultado = f7 + REG[rs2] + REG[rs1] + f3 + REG[rd] + opc
            codigo_binario_final.append(resultado)

        elif t == 'I':
            rd = partes[1].lower()
            rs1 = partes[2].lower()
            imm = partes[3]
            f3 = FUNCT3[op]
            imm_bin = para_binario(imm, 12)
            resultado = imm_bin + REG[rs1] + f3 + REG[rd] + opc
            codigo_binario_final.append(resultado)

        elif t == 'L':
            rd = partes[1].lower()
            imm = partes[2]
            rs1 = partes[3].lower()
            f3 = FUNCT3[op]
            imm_bin = para_binario(imm, 12)
            resultado = imm_bin + REG[rs1] + f3 + REG[rd] + opc
            codigo_binario_final.append(resultado)

        elif t == 'S':
            rs2 = partes[1].lower()
            imm = partes[2]
            rs1 = partes[3].lower()
            f3 = FUNCT3[op]
            imm_bin = para_binario(imm, 12)
            parte_alta = imm_bin[0:7]
            parte_baixa = imm_bin[7:12]
            resultado = parte_alta + REG[rs2] + REG[rs1] + f3 + parte_baixa + opc
            codigo_binario_final.append(resultado)

        elif t == 'B':
            rs1 = partes[1].lower()
            rs2 = partes[2].lower()
            alvo = partes[3]
            f3 = FUNCT3[op]
            if alvo in labels:
                deslocamento = labels[alvo] - pc
            else:
                deslocamento = int(alvo)
            imm_bin = para_binario(str(deslocamento), 13)
            b12 = imm_bin[0]
            b11 = imm_bin[1]
            b10_5 = imm_bin[2:8]
            b4_1 = imm_bin[8:12]
            resultado = b12 + b10_5 + REG[rs2] + REG[rs1] + f3 + b4_1 + b11 + opc
            codigo_binario_final.append(resultado)

        elif t == 'J':
            rd = partes[1].lower()
            alvo = partes[2]
            if alvo in labels:
                deslocamento = labels[alvo] - pc
            else:
                deslocamento = int(alvo)
            imm_bin = para_binario(str(deslocamento), 21)
            b20 = imm_bin[0]
            b19_12 = imm_bin[1:9]
            b11 = imm_bin[9]
            b10_1 = imm_bin[10:20]
            resultado = b20 + b10_1 + b11 + b19_12 + REG[rd] + opc
            codigo_binario_final.append(resultado)

        elif t == 'JR':
            rd = partes[1].lower()
            rs1 = partes[2].lower()
            imm = partes[3]
            f3 = FUNCT3[op]
            imm_bin = para_binario(imm, 12)
            resultado = imm_bin + REG[rs1] + f3 + REG[rd] + opc
            codigo_binario_final.append(resultado)

        elif t == 'U_LUI' or t == 'U_AUIPC':
            rd = partes[1].lower()
            imm = partes[2]
            imm_bin = para_binario(imm, 20)
            resultado = imm_bin + REG[rd] + opc
            codigo_binario_final.append(resultado)

        pc = pc + 4

    return codigo_binario_final


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 montador.py <nome_arquivo.asm> -o <nome_arquivo_saida>")
        return

    arquivo_entrada = sys.argv[1]
    arquivo_saida = ""
    tem_saida = False

    for i in range(len(sys.argv)):
        if sys.argv[i] == "-o":
            if i + 1 < len(sys.argv):
                arquivo_saida = sys.argv[i + 1]
                tem_saida = True

    try:
        f = open(arquivo_entrada, 'r')
        linhas = []
        for linha in f:
            linhas.append(linha)
        f.close()

        resultado = montar(linhas)

        if tem_saida == True:
            f_out = open(arquivo_saida, 'w')
            for linha_binaria in resultado:
                f_out.write(linha_binaria + "\n")
            f_out.close()
        else:
            for linha_binaria in resultado:
                print(linha_binaria)

    except Exception as erro:
        print("Erro: " + str(erro))

if __name__ == "__main__":
    main()