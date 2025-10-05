# Passo 1: Imports (nenhum import extra é necessário para este script básico)
import os
import json
# Arquivo da ROM que vamos analisar
diretory = os.path.dirname(os.getcwd())

rom_file = os.path.join(diretory, 'SMario.sfc')
dicionario_file = os.path.join(diretory,'dados','dicionario.json')

# A palavra que queremos encontrar. Você pode mudar esta variável.
search_word = input("Pesquise a expressão:")



# --- PREPARAÇÃO DOS DICIONÁRIOS ---

# Carrega o dicionário base (hex -> char) do arquivo JSON
hex_to_char = {}
try:
    with open(dicionario_file, 'r') as f:
        data = json.load(f)
    # Converte as chaves do JSON (que são texto) para números hexadecimais
    hex_to_char = {int(key, 16): value for key, value in data['hex_to_char'].items()}
    print("Dicionário (hex -> char) carregado do JSON.")

except Exception as e:
    print(f"Erro ao carregar o dicionário: {e}")
    exit()


# CORREÇÃO: Cria o dicionário invertido (char -> hex) necessário para o finder/injector
# Nota: Se uma letra tiver múltiplos códigos (como 's'), este método simples
# vai manter apenas o último que aparecer no dicionário original.
char_to_hex = {value: key for key, value in hex_to_char.items()}
print("Dicionário invertido (char -> hex) criado para a busca.")

# --- Lógica do programa ---

# Converte a string da palavra em uma sequência de bytes que podemos procurar
try:
    search_sequence = bytes([char_to_hex[char] for char in search_word])
except KeyError as e:
    # Se uma letra não estiver no dicionário, o programa avisa e para.
    print(f"Erro: O caractere '{e.args[0]}' não está no dicionário.")
    exit()

# Passo 3: Carregar a ROM
try:
    with open(rom_file, 'rb') as f:
        rom_data = f.read()
except FileNotFoundError:
    print(f"Erro: Arquivo '{rom_file}' não encontrado.")
    exit()

# Passo 4: Fazer a busca
# O método .find() procura a sequência e retorna a posição onde ela começa
position = rom_data.find(search_sequence)

# Passo 5: Retornar as posições
if position != -1:
    # O trabalho pede para retornar a posição e os valores hex.
    print(f"--- Ferramenta Finder ---")
    print(f"Palavra encontrada: '{search_word}'")
    print(f"Posição (offset): {hex(position)}")
    print(f"Valores Hex: {search_sequence.hex(' ').upper()}")
else:
    print(f"A palavra '{search_word}' não foi encontrada com o mapeamento atual.")