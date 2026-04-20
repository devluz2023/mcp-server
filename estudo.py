import os

def compilar_arquivos(pasta_raiz, arquivo_saida, pasta_excluir="venv"):
    """
    Lê todos os arquivos de forma recursiva, ignorando a pasta especificada.
    """
    with open(arquivo_saida, 'w', encoding='utf-8') as outfile:
        # Percorre a estrutura de diretórios
        for root, dirs, files in os.walk(pasta_raiz):
            # Exclui a pasta venv da busca
            if pasta_excluir in dirs:
                dirs.remove(pasta_excluir)
            
            for file in files:
                # Evita ler o próprio arquivo de saída
                if file == arquivo_saida:
                    continue
                
                caminho_completo = os.path.join(root, file)
                
                try:
                    with open(caminho_completo, 'r', encoding='utf-8') as infile:
                        outfile.write(f"\n--- ARQUIVO: {caminho_completo} ---\n")
                        outfile.write(infile.read())
                        outfile.write("\n")
                except Exception as e:
                    print(f"Não foi possível ler {caminho_completo}: {e}")

if __name__ == "__main__":
    # Configurações
    PASTA_ATUAL = "."
    SAIDA = "conteudo_total.txt"
    
    compilar_arquivos(PASTA_ATUAL, SAIDA)
    print(f"Sucesso! Todo o conteúdo foi compilado em: {SAIDA}")