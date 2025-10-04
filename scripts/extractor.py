import json
import os

# --- CONFIGURAÇÃO ---
rom_filename = 'SMario.sfc'
dict_filename = 'dicionario.json'
output_filename = 'texto_extraido.txt'

# Posição de início da mensagem (encontrada pelo finder)
# Este é o offset para "Welcome" que confirmamos ser 0x2a5d9 no seu arquivo
start_offset = 0x2a5d9 

# Byte que marca o fim da mensagem
terminator = 0x1C

# --- 1. CARREGAR DICIONÁRIO ---
hex_to_char = {}
try:
    with open(dict_filename, 'r') as f:
        data = json.load(f)
    # Converte as chaves do JSON (que são texto, como "1a") para números (como 0x1a)
    hex_to_char = {int(key, 16): value for key, value in data['hex_to_char'].items()}
    print("Dicionário (hex -> char) carregado do JSON.")
except Exception as e:
    print(f"Erro ao carregar o dicionário: {e}")
    exit()

# --- 2. EXTRAIR BYTES DA ROM ---
extracted_bytes = []
try:
    with open(rom_filename, 'rb') as f:
        rom_data = f.read()

    current_offset = start_offset
    # Loop para ler os bytes até encontrar o terminador
    while rom_data[current_offset] != terminator:
        extracted_bytes.append(rom_data[current_offset])
        current_offset += 1
        # Medida de segurança para não entrar em loop infinito
        if current_offset >= len(rom_data):
            print("Aviso: Fim do arquivo atingido sem encontrar o byte terminador.")
            break
            
    print(f"Foram extraídos {len(extracted_bytes)} bytes da mensagem.")

except FileNotFoundError:
    print(f"Erro: Arquivo '{rom_filename}' não encontrado.")
    exit()
        
# --- 3. CONVERTER BYTES PARA TEXTO ---
extracted_text = ""
for byte_value in extracted_bytes:
    # Usa o dicionário para encontrar a letra. Se não achar, mostra o código hex.
    character = hex_to_char.get(byte_value, f'[?{hex(byte_value)}]')
    extracted_text += character
    
# --- 4. SALVAR TEXTO EM ARQUIVO ---
with open(output_filename, 'w', encoding='utf-8') as f:
    f.write(extracted_text)

print(f"\nTexto extraído e salvo em '{output_filename}':")
print("---")
print(extracted_text)
print("---")