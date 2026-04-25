import os

def compilar_arquivos(pasta_raiz, arquivo_saida, ignorar_pastas=None, ignorar_arquivos=None, ignorar_extensoes=None):
    """
    Compila arquivos ignorando pastas, nomes específicos e extensões.
    """
    if ignorar_pastas is None: ignorar_pastas = {'venv', '.git', '__pycache__'}
    if ignorar_arquivos is None: ignorar_arquivos = {'.env', 'conteudo_total.txt'}
    if ignorar_extensoes is None: ignorar_extensoes = {'.csv', '.pyc', '.exe'}

    with open(arquivo_saida, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(pasta_raiz):
            # Filtra pastas em tempo real
            dirs[:] = [d for d in dirs if d not in ignorar_pastas]
            
            for file in files:
                # 1. Ignorar nomes exatos
                if file in ignorar_arquivos:
                    continue
                
                # 2. Ignorar extensões específicas
                if any(file.endswith(ext) for ext in ignorar_extensoes):
                    continue
                
                caminho_completo = os.path.join(root, file)
                
                try:
                    with open(caminho_completo, 'r', encoding='utf-8') as infile:
                        outfile.write(f"\n--- ARQUIVO: {caminho_completo} ---\n")
                        outfile.write(infile.read())
                        outfile.write("\n")
                except Exception as e:
                    print(f"Ignorando {caminho_completo} (Erro de leitura: {e})")

if __name__ == "__main__":
    compilar_arquivos(
        pasta_raiz=".", 
        arquivo_saida="conteudo_total.txt"
    )
    print("Sucesso! Conteúdo compilado com segurança.")