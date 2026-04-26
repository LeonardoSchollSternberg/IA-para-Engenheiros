import nbformat as nbf
from bs4 import BeautifulSoup
import re
import os

# --- CONFIGURAÇÃO ---
ARQUIVO_ENTRADA = 'Lab04BIAENGTarefa07.html'
# --- ---

def converter_notebook_completo():
    try:
        nome_base = os.path.splitext(ARQUIVO_ENTRADA)[0]
        arquivo_saida = f"{nome_base}.ipynb"

        with open(ARQUIVO_ENTRADA, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        nb = nbf.v4.new_notebook()
        cells = []
        textos_adicionados = set()  # Rastrear textos já adicionados para evitar duplicatas

        # Regex para limpar o "In [ ]:" dos blocos de código
        padrao_jupyter = re.compile(r'^In\s*\[.*?\]:\s*', re.MULTILINE)

        # Captura títulos (h1-h6), parágrafos (p), blocos de código <pre> e divs de destaque do Jupyter
        elementos = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre'])
        elementos += soup.find_all('div', class_='highlight')

        for elemento in elementos:
            # 1. Se for bloco de código (PRE ou div com classe 'highlight')
            if elemento.name == 'pre' or (elemento.name == 'div' and 'highlight' in elemento.get('class', [])):
                texto = elemento.get_text().strip()
                codigo_limpo = padrao_jupyter.sub('', texto).strip()
                if codigo_limpo and codigo_limpo not in textos_adicionados:
                    cells.append(nbf.v4.new_code_cell(codigo_limpo))
                    textos_adicionados.add(codigo_limpo)
            
            # 2. Se for Título (h1-h6) → Markdown
            elif elemento.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                texto_md = elemento.get_text().strip()
                if texto_md and texto_md not in textos_adicionados:
                    nivel = int(elemento.name[1])  # Extrai o número de h1-h6
                    texto_md = '#' * nivel + ' ' + texto_md
                    cells.append(nbf.v4.new_markdown_cell(texto_md))
                    textos_adicionados.add(texto_md)
            
            # 3. Se for Parágrafo (p) → Markdown
            elif elemento.name == 'p':
                texto_md = elemento.get_text().strip()
                if texto_md and not texto_md.startswith('In [') and texto_md not in textos_adicionados:
                    cells.append(nbf.v4.new_markdown_cell(texto_md))
                    textos_adicionados.add(texto_md)

        nb['cells'] = cells

        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)

        print(f"✅ Sucesso! Notebook completo (Texto + Código) gerado.")
        print(f"📂 Arquivo: {arquivo_saida}")

    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    converter_notebook_completo()