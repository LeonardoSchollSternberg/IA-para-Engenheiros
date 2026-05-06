import tsplib95
import pandas as pd
import math
import random
import glob
import os

# Função padrão para calcular a distância total de um tour (incluindo o retorno ao início)
def calculate_total_distance(tsp_city, tour):
    total_distance = 0
    for i in range(len(tour)):
        # O operador % garante que o último nó se conecte ao primeiro (índice 0)
        total_distance += tsp_city.get_weight(tour[i], tour[(i + 1) % len(tour)])
    return total_distance

# Auxiliar para preencher o dataframe com base no tour calculado
def fill_df(tsp_city, tour, df, column_prefix):
    """Auxiliar para preencher o dataframe com base no tour calculado"""
    cumulative = 0
    for i in range(len(tour)):
        order = i + 1
        current_city = tour[i]
        next_city = tour[(i + 1) % len(tour)]
        dist = tsp_city.get_weight(current_city, next_city)
        cumulative += dist
        
        df.loc[df['Order'] == order, f'City_{column_prefix}'] = current_city
        df.loc[df['Order'] == order, f'Distance_{column_prefix}'] = dist
        df.loc[df['Order'] == order, f'Cumulative_Distance_{column_prefix}'] = cumulative

# Método que procura o nó mais próximo a cada passo, sem considerar futuras consequências
def greedy(tsp_city, initial_city):
    tour = [initial_city]
    unvisited = set(tsp_city.get_nodes()) - {initial_city}
    while unvisited:
        current_node = tour[-1]
        next_node = min(unvisited, key=lambda node: tsp_city.get_weight(current_node, node))
        tour.append(next_node)
        unvisited.remove(next_node)        
    return tour

# Método de otimização local que tenta melhorar a solução atual trocando duas arestas (2-opt)
def hillclimbing_2opt(tsp_city):
    tour = list(tsp_city.get_nodes())
    random.shuffle(tour)
    
    # Armazenamos a distância atual para não recalcular tudo
    current_dist = calculate_total_distance(tsp_city, tour)
    
    improved = True
    n = len(tour)
    
    while improved:
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                # Nodos envolvidos na troca
                a, b = tour[i-1], tour[i]
                c, d = tour[j], tour[(j + 1) % n]
                
                # Cálculo do delta (diferença na distância)
                # Remove as arestas (a,b) e (c,d) e adiciona (a,c) e (b,d)
                old_dist = tsp_city.get_weight(a, b) + tsp_city.get_weight(c, d)
                new_dist = tsp_city.get_weight(a, c) + tsp_city.get_weight(b, d)
                
                if new_dist < old_dist:
                    # Aplica a troca (inverte o segmento)
                    tour[i:j+1] = tour[i:j+1][::-1]
                    current_dist -= (old_dist - new_dist)
                    improved = True
                    # Opcional: remover o break aqui para ser "best improvement" 
                    # em vez de "first improvement", mas manter o break
                    # ajuda na velocidade para TSP.
                    break 
            if improved: break
            
    return tour
# Método auxiliar para gerar um vizinho aleatório trocando dois nós no tour
def get_random_neighbor(tour):
    new_tour = tour[:]
    i, j = random.sample(range(len(tour)), 2)
    new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
    return new_tour

# Método de otimização global que aceita soluções piores com uma probabilidade que diminui ao longo do tempo (Simulated Annealing)
def simulated_annealing(tsp_city, temperature=1000, alpha=0.995, T_min=0.01):
    tour = list(tsp_city.get_nodes())
    random.shuffle(tour)
    distance = calculate_total_distance(tsp_city, tour)
    best_tour, best_distance = tour[:], distance
    # Enquanto a temperatura for maior que o mínimo, continua explorando vizinhos
    while temperature > T_min:
        new_tour = get_random_neighbor(tour)
        new_distance = calculate_total_distance(tsp_city, new_tour)
        delta = new_distance - distance
        # Aceita a nova solução se for melhor ou com uma probabilidade que depende da temperatura
        if delta < 0 or random.random() < math.exp(-delta / temperature):
            tour, distance = new_tour, new_distance
            if distance < best_distance:
                best_tour, best_distance = tour[:], distance
        temperature *= alpha
    return best_tour

# Método que aceita soluções piores com uma probabilidade fixa, sem considerar a temperatura (Threaded Acceptor)
def threaded_acceptor(tsp_city, iterations=1000):
    tour = list(tsp_city.get_nodes())
    random.shuffle(tour)
    distance = calculate_total_distance(tsp_city, tour)
    best_tour, best_distance = tour[:], distance
    for _ in range(iterations):
        new_tour = get_random_neighbor(tour)
        new_distance = calculate_total_distance(tsp_city, new_tour)
        # Aceita a nova solução se for melhor ou com uma probabilidade fixa (exemplo: 0.1)
        if new_distance < distance or random.random() < 0.1:
            tour, distance = new_tour, new_distance
            if distance < best_distance:
                best_tour, best_distance = tour[:], distance
    return best_tour


# Supondo que suas funções (greedy, hillclimbing_2opt, simulated_annealing) já existam

def main():
    random.seed(42)
    directory_path = './tsplib/*.tsp'
    results = []
    
    # 1. Lista todos os arquivos .tsp na pasta
    files = glob.glob(directory_path)
    
    print(f"Encontrados {len(files)} arquivos. Iniciando processamento...")

    for file_path in files:
        try:
            # 2. Carrega o problema
            tsp_instance = tsplib95.load(file_path)
            dataset_name = tsp_instance.name
            print(f"Processando: {dataset_name}")
            
            # Inicialização
            nodes = list(tsp_instance.get_nodes())
            initial_city = nodes[0] # Arbitrário, poderia ser qualquer um

            # --- Execução dos Algoritmos ---
            
            # Execução Greedy
            print("  Executando Greedy...")
            greedy_tour = greedy(tsp_instance, initial_city)
            dist_greedy = calculate_total_distance(tsp_instance, greedy_tour)
            
            # Execução Hill Climbing 2-Opt
            print("  Executando Hill Climbing 2-Opt...")
            opt_tour = hillclimbing_2opt(tsp_instance)
            dist_hc_opt = calculate_total_distance(tsp_instance, opt_tour)
            
            # Execução Simulated Annealing
            print("  Executando Simulated Annealing...")
            sa_tour = simulated_annealing(tsp_instance)
            dist_sa = calculate_total_distance(tsp_instance, sa_tour)
            
            # Execução Threaded Acceptor
            print("  Executando Threaded Acceptor...")
            ta_tour = threaded_acceptor(tsp_instance)
            dist_ta = calculate_total_distance(tsp_instance, ta_tour)

            # 3. Adiciona resultados à lista
            results.append({
                'Dataset': dataset_name,
                'N_Cities': len(nodes),
                'Greedy_Dist': dist_greedy,
                'HC_2Opt_Dist': dist_hc_opt,
                'SA_Dist': dist_sa,
                'TA_Dist': dist_ta
            })
            
        except Exception as e:
            print(f"Erro ao processar {file_path}: {e}")
    
    # 4. Cria um DataFrame com os resultados e exibe
    df_results = pd.DataFrame(results)
    print("\n--- Resultados Finais ---")
    print(df_results)

if __name__ == "__main__":
    main()