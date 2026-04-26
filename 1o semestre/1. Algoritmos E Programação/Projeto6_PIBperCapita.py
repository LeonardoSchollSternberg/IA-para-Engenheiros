# Vamos cruzar duas bases de dados expressas em CSV para calcular o PIB per capita dos países do mundo e ordenar os países por essa métrica. São fornecidas duas listas: pib.csv (PIB dos Países (e territórios)) e pop.csv (População dos Países (e territórios) do mundo).

# 1. Processe os dois arquivos e crie uma estrutura em memória com indexação pelo nome do país e com todos os dadoos obtidos.
import pandas as pd

with open('pib.csv', 'r', encoding='utf-8') as f:
    pib_df = pd.read_csv(f)

with open('pop.csv', 'r', encoding='utf-8') as f:
    pop_df = pd.read_csv(f)

# Criar estrutura indexada por país
pib_df.set_index('Country/Territory', inplace=True)
pop_df.set_index('Location', inplace=True)

# Mesclar os dados por país (opções inner, leftm right, outer - todos os países)
dados = pib_df.join(pop_df, how='outer')

# 2. Processe essa strutura para gerar o PIB per capita (adotando apenas a primeira fonte de cada dado)
# Limpar dados (remover vírgulas, converter para float)
dados['IMF (2026)'] = pd.to_numeric(dados['IMF (2026)'].str.replace(',', ''), errors='coerce')
dados['Population'] = pd.to_numeric(dados['Population'].str.replace(',', ''), errors='coerce')

# Calcular PIB per capita
dados['PIB_per_Capita'] = dados['IMF (2026)'] / dados['Population']

# 3. Gere um CSV de saída com o nome do país e o PIB per capita correspondente, quando os dois dados existirem
dados_completos = dados.dropna(subset=['IMF (2026)', 'Population'])
dados_completos[['PIB_per_Capita']].to_csv('pib_per_capita.csv', encoding='utf-8')

# 4. Gere um segundo CSV com todos os países que não constam de uma das duas listas, indicando, na segunda coluna, a informação faltante
faltantes = []

# Países com PIB mas SEM População
pib_sem_pop = dados[dados['IMF (2026)'].notna() & dados['Population'].isna()]
for pais in pib_sem_pop.index:
    faltantes.append({'País': pais, 'Dado_Faltante': 'População'})

# Países com População mas SEM PIB
pop_sem_pib = dados[dados['Population'].notna() & dados['IMF (2026)'].isna()]
for pais in pop_sem_pib.index:
    faltantes.append({'País': pais, 'Dado_Faltante': 'PIB'})

faltantes_df = pd.DataFrame(faltantes)
faltantes_df.to_csv('paises_faltantes.csv', index=False, encoding='utf-8')

# 5. Gere um JSON de saída com todos os dados apresentados de forma estrutura.
dados.to_json('dados_completos.json', orient='index', force_ascii=False, indent=4)
