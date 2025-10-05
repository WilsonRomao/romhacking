import json
import os

# --- CORREÇÃO 1: Caminhos Dinâmicos ---
# Esta parte agora encontra a pasta 'dados' de forma automática,
# não importa onde você salve a pasta do seu projeto.

# Pega o caminho do diretório onde o script está (a pasta 'script')
script_dir = os.path.dirname(os.path.abspath(__file__))
# "Sobe" um nível para a pasta raiz do projeto
project_root = os.path.dirname(script_dir)
# Monta o caminho para a pasta 'dados'
dados_dir = os.path.join(project_root,'dados')

# Agora, definimos os caminhos dos arquivos de forma segura
rom_file = os.path.join(dados_dir, 'SMario.sfc')
dicionario_file = os.path.join(dados_dir, 'dicionario.json')
output_filename = os.path.join(dados_dir, 'texto_extraido.json') # O arquivo de saída será um JSON

# Posição de início da mensagem (encontrada pelo finder)
start_offset = 0x2a5d9

# Byte que marca o fim da mensagem
terminator = 0x1C

# --- CARREGAR DICIONÁRIO ---
hex_to_char = {}
try:
    # CORREÇÃO 2: Simplificado para usar a variável de caminho correta
    with open(dicionario_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    hex_to_char = {int(key, 16): value for key, value in data['hex_to_char'].items()}
    print("Dicionário (hex -> char) carregado do JSON.")
except Exception as e:
    print(f"Erro ao carregar o dicionário: {e}")
    exit()

# --- EXTRAIR BYTES DA ROM ---
extracted_bytes = []
try:
    with open(rom_file, 'rb') as f:
        rom_data = f.read()

    current_offset = start_offset
    while rom_data[current_offset] != terminator:
        extracted_bytes.append(rom_data[current_offset])
        current_offset += 1
        if current_offset >= len(rom_data):
            print("Aviso: Fim do arquivo atingido sem encontrar o byte terminador.")
            break
            
    print(f"Foram extraídos {len(extracted_bytes)} bytes da mensagem.")

except FileNotFoundError:
    print(f"Erro: Arquivo '{rom_file}' não encontrado.")
    exit()
        
# --- CONVERTER BYTES PARA TEXTO ---
extracted_text = ""
for byte_value in extracted_bytes:
    character = hex_to_char.get(byte_value, f'[?{hex(byte_value)}]')
    extracted_text += character
    
# --- CORREÇÃO 3: SALVAR DADOS EM FORMATO JSON COM METADADOS ---
# Cria um dicionário que contém todas as informações necessárias
output_data = {
    "start_offset": start_offset,
    "original_size": len(extracted_bytes),
    "original_text": extracted_text,
    "translated_text": ""  # Deixe este campo vazio para você preencher depois
}

# Salva o dicionário como um arquivo JSON bem formatado
with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"\nDados extraídos e salvos em '{output_filename}'.")
print("---")
print("Texto original extraído:")
print(extracted_text)
print("---")
print(f"Tamanho original: {len(extracted_bytes)} bytes.")
print("\nPróximo passo: Edite o arquivo 'texto_extraido.json' e preencha o campo 'translated_text' com sua tradução.")
