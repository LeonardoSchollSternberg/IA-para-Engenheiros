# Exemplo de leitura e escrita de arquivos em Python
with open('arquivo.txt', 'w',  encoding='utf-8') as arquivo:
    arquivo.write('Olá, este é um exemplo de escrita em um arquivo.\n')
    arquivo.write('Podemos escrever várias linhas usando o método write.\n')
    
with open('arquivo.txt', 'r', encoding='utf-8') as f:
    conteudo = f.read()
print(conteudo)
    
with open('arquivo.txt', 'r', encoding='utf-8') as f:
    for linha in f:
        print(linha.strip())  # strip() para remover a quebra de linha extra   

# Escrevendo e lendo arquivos CSV usando o módulo csv
import csv

with open('dados.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Nome', 'Idade', 'Cidade'])
    writer.writerow(['Alice', 30, 'São Paulo'])
    writer.writerow(['Bob', 25, 'Rio de Janeiro'])
    
with open('dados.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)

with open('dados.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['Nome'], row['Idade'], row['Cidade'])

# Escrevendo e lendo arquivos CSV usando o módulo pandas        
import pandas as pd

df = pd.DataFrame({
    'Nome': ['Alice', 'Bob', 'Charlie'],
    'Idade': [30, 25, 35],
    'Cidade': ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte']
})
df.to_csv('dados_pandas.csv', index=False, encoding='utf-8')

df_lido = pd.read_csv('dados_pandas.csv', encoding='utf-8')
print(df_lido)

# Escrevendo e lendo arquivos JSON usando o módulo json
import json
dados = {
    'nome': 'Alice',
    'idade': 30,
    'cidade': 'São Paulo'
}

with open('dados.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(dados, jsonfile, ensure_ascii=False, indent=4)
    
with open('dados.json', 'r', encoding='utf-8') as jsonfile:
    dados_lidos = json.load(jsonfile)
    
import os

# Apagar os arquivos
os.remove('arquivo.txt')
os.remove('dados.csv')
os.remove('dados_pandas.csv')
os.remove('dados.json')