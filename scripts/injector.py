import os
import json
import shutil # Módulo usado para copiar o arquivo da ROM

# --- CONFIGURAÇÃO E CAMINHOS DINÂMICOS ---
# Esta parte encontra a pasta 'dados' de forma automática
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
dados_dir = os.path.join(project_root, 'dados')

# Caminhos para os arquivos de entrada e saída
original_rom_path = os.path.join(dados_dir, 'SMario.sfc')
modified_rom_path = os.path.join(dados_dir, 'SMario_modificado.sfc') # Arquivo que será criado/modificado
dicionario_path = os.path.join(dados_dir, 'dicionario.json')
json_input_path = os.path.join(dados_dir, 'texto_extraido.json') # Arquivo de entrada com a tradução

# --- 1. CARREGAR E PREPARAR DICIONÁRIOS ---
try:
    with open(dicionario_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # CORREÇÃO: Acessa o dicionário interno 'hex_to_char' antes de iterar
    hex_to_char = {int(key, 16): value for key, value in data['hex_to_char'].items()}
    
    # Cria o dicionário reverso (char -> hex) para converter o texto em bytes
    # Se uma letra tiver múltiplos códigos, este método simples pega o último mapeado
    char_to_hex = {value: key for key, value in hex_to_char.items()}
    print("Dicionários carregados com sucesso.")
except Exception as e:
    print(f"Erro ao carregar o dicionário: {e}")
    exit()

# --- 2. LER O ARQUIVO JSON COM A TRADUÇÃO E METADADOS ---
try:
    with open(json_input_path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

    start_offset = input_data['start_offset']
    original_size = input_data['original_size']
    translated_text = input_data['translated_text']

    if not translated_text:
        print(f"ERRO: O campo 'translated_text' no arquivo '{json_input_path}' está vazio.")
        exit()
    
    print(f"Texto a ser injetado lido de '{json_input_path}'")

except FileNotFoundError:
    print(f"ERRO: Arquivo '{json_input_path}' não encontrado. Execute o extractor.py primeiro.")
    exit()
except KeyError as e:
    print(f"ERRO: A chave '{e.args[0]}' não foi encontrada no arquivo JSON. Verifique o arquivo.")
    exit()


# --- 3. CONVERTER TEXTO PARA BYTES E VALIDAR TAMANHO ---
new_bytes = bytearray()
for char in translated_text:
    # Usa o dicionário para obter o byte. Se não encontrar, usa '?' (0x3F)
    byte_val = char_to_hex.get(char, 0x3F) 
    new_bytes.append(byte_val)

if len(new_bytes) > original_size:
    print(f"ERRO: O texto traduzido ({len(new_bytes)} bytes) é MAIOR que o original ({original_size} bytes)!")
    exit()
else:
    # Preenche o espaço restante com o código de espaço (0x1F) se a tradução for mais curta
    padding_size = original_size - len(new_bytes)
    new_bytes.extend([0x1F] * padding_size)
    print(f"Texto convertido para {len(new_bytes)} bytes (incluindo preenchimento).")

# --- 4. INJETAR OS BYTES NA ROM ---
try:
    # Cria uma cópia da ROM para não modificar o arquivo original
    shutil.copy(original_rom_path, modified_rom_path)

    # Abre a ROM copiada em modo 'leitura e escrita binária' ('r+b')
    with open(modified_rom_path, 'r+b') as f:
        # Move o "cursor" do arquivo para a posição exata onde a mensagem original começa
        f.seek(start_offset)
        # Sobrescreve os bytes antigos com os novos
        f.write(new_bytes)
    
    print(f"\nInjeção concluída com sucesso! Teste o arquivo '{modified_rom_path}' no emulador.")

except Exception as e:
    print(f"Ocorreu um erro ao escrever na ROM: {e}")

