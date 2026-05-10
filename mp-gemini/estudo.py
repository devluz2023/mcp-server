import pathlib

def consolidar_arquivos(diretorio_raiz, arquivo_saida):
    # Lista de arquivos e extensões para ignorar
    ignore_list = {
        'requirements.txt', '.env', '.gitignore', 'consolidado.txt',
        'package-lock.json', 'poetry.lock', '.DS_Store'
    }
    ignore_extensions = {'.pyc', '.exe', '.bin', '.png', '.jpg', '.pdf'}
    ignore_dirs = {'.git', '__pycache__', '.venv', 'venv', 'node_modules'}

    path_raiz = pathlib.Path(diretorio_raiz)
    
    with open(arquivo_saida, 'w', encoding='utf-8') as outfile:
        # rglob('*') varre pastas e subpastas
        for path in path_raiz.rglob('*'):
            
            # Pula se for diretório ou se estiver em uma pasta ignorada
            if path.is_dir() or any(part in ignore_dirs for part in path.parts):
                continue
            
            # Pula se o arquivo estiver na lista de ignorados ou tiver extensão irrelevante
            if path.name in ignore_list or path.suffix in ignore_extensions:
                continue

            try:
                # Escreve o cabeçalho do arquivo para você saber de onde veio o texto
                outfile.write(f"\n{'='*50}\n")
                outfile.write(f"ARQUIVO: {path.relative_to(path_raiz)}\n")
                outfile.write(f"{'='*50}\n\n")
                
                # Lê o conteúdo e grava no TXT
                content = path.read_text(encoding='utf-8')
                outfile.write(content)
                outfile.write("\n")
                
            except Exception as e:
                outfile.write(f"\n[ERRO AO LER {path.name}]: {e}\n")

if __name__ == "__main__":
    # '.' indica a pasta atual onde o script está
    consolidar_arquivos('.', 'projeto_completo.txt')
    print("Documento gerado com sucesso: projeto_completo.txt")