# calcular média e desvio padrão por disciplina

import numpy as np

rng = np.random.default_rng(seed=42)
notas = rng.normal(loc=65, scale = 15, size=(100,4))
notas = np.clip(notas, 0, 100) # garante [0, 100]
disciplinas = ['Matemática', 'Física', 'Química', 'Biologia']

medias = np.mean(notas, axis=0)
medias_2 = notas.mean(axis=0) # outra forma de calcular a média
desvios_padroes = np.std(notas, axis=0)

print(medias)
print(desvios_padroes)

# Adotando convenção de conceitos A (entre 90 a 100), B (entre 75 a 89), C (entre 60 a 74) e D (entre 0 a 59), determine o número de coneceitos em cada disciplina. NÃO USAR LOOPS NATIVOS DO PYTHON para operações sobre os arrays

conceitos_A = np.sum(notas >= 90, axis=0)
conceitos_B = np.sum((notas >= 75) & (notas < 90), axis=0)
conceitos_C = np.sum((notas >= 60) & (notas < 75), axis=0)
conceitos_D = np.sum(notas < 60, axis=0)
print(f"Conceitos A: {conceitos_A}")
print(f"Conceitos B: {conceitos_B}")
print(f"Conceitos C: {conceitos_C}")
print(f"Conceitos D: {conceitos_D}")

