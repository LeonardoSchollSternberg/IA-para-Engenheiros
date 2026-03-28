# Algoritmo de Monte Carlo para estimar o valor de pi. O algoritmo gera pontos aleatórios dentro de um quadrado de lado 1 e conta quantos pontos caem dentro de um círculo inscrito nesse quadrado. A razão entre os pontos dentro do círculo e o total de pontos é igual à razão entre a área do círculo e a área do quadrado, que é pi/4. Multiplicando por 4, obtemos a estimativa de pi.
import random
import numpy as np

def monte_carlo(num_points):
    counter_in_circle = 0
    counter_out_circle = 0  
    for _ in range(num_points):
        x, y = random.random(), random.random()
        if x**2 + y**2 <= 1:
            counter_in_circle += 1
        else:
            counter_out_circle += 1
    pi_estimate = (counter_in_circle / (counter_in_circle + counter_out_circle)) * 4
    return pi_estimate

random.seed(666)
num_points = 10000
num_iterations = 1000
pi_real = 3.141592653589793
pi_estimate = []

for i in range(num_iterations):
    print(f'Estimativa de pi na iteração {i + 1}: {monte_carlo(num_points)}')
    pi_estimate.append(monte_carlo(num_points))

print(f'Estimativa final de pi após {num_iterations} iterações: {np.mean(pi_estimate)}')
print(f'Valor real de pi: {pi_real}')
print(f'Erro percentual: {abs(np.mean(pi_estimate) - pi_real) / pi_real * 100:.2f}%')