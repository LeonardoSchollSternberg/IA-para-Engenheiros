import nbformat as nbf
from bs4 import BeautifulSoup
import re
import os

# --- CONFIGURAÇÃO ---
ARQUIVO_ENTRADA = 'Lab04Tarefa04.html'
# --- ---

def converter_notebook_completo():
    try:
        nome_base = os.path.splitext(ARQUIVO_ENTRADA)[0]
        arquivo_saida = f"{nome_base}.ipynb"

        with open(ARQUIVO_ENTRADA, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        nb = nbf.v4.new_notebook()
        cells = []

        # Regex para limpar o "In [ ]:" dos blocos de código
        padrao_jupyter = re.compile(r'^In\s*\[.*?\]:\s*', re.MULTILINE)

        # Captura títulos (h1-h6), parágrafos (p) e blocos de código (pre)
        for elemento in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre', 'div']):
            
            # 1. Se for bloco de código (comumente dentro de 'pre' ou divs específicas)
            if elemento.name == 'pre' or 'highlight' in elemento.get('class', []):
                texto = elemento.get_text().strip()
                codigo_limpo = padrao_jupyter.sub('', texto).strip()
                if codigo_limpo:
                    cells.append(nbf.v4.new_code_cell(codigo_limpo))
            
            # 2. Se for Título ou Texto (Markdown)
            elif elemento.name in ['h1', 'h2', 'h3', 'p']:
                texto_md = elemento.get_text().strip()
                if texto_md and not texto_md.startswith('In ['): # Evita duplicar rótulos
                    # Se for título, adiciona os '#' do Markdown
                    if elemento.name == 'h1': texto_md = f"# {texto_md}"
                    elif elemento.name == 'h2': texto_md = f"## {texto_md}"
                    elif elemento.name == 'h3': texto_md = f"### {texto_md}"
                    
                    cells.append(nbf.v4.new_markdown_cell(texto_md))

        # Remove células duplicadas que podem surgir pela estrutura do HTML
        nb['cells'] = cells

        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)

        print(f"✅ Sucesso! Notebook completo (Texto + Código) gerado.")
        print(f"📂 Arquivo: {arquivo_saida}")

    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    converter_notebook_completo()