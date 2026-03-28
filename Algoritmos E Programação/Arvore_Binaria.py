# Árvore Binária de Busca (Binary Search Tree)

class No:
    def __init__(self, valor):
        self.valor = valor
        self.filho_esquerda = None # nó inicia como nó folho (sem filhos)
        self.filho_direita = None # nó inicia como nó folho (sem filhos)

class ArvoreBinariaBusca: # BST - binary search tree
    def __init__(self):
        self.raiz = None # árvore inicia sem raiz
        
    def inserir(self, valor):
        if self.raiz is None: # se a árvore estiver vazia, o novo nó se torna a raiz
            self.raiz = No(valor)
        else:
            self._inserir_recursivo(self.raiz, valor) # caso contrário, insere recursivamente a partir da raiz
    def _inserir_recursivo(self, no_atual, valor):
        if valor < no_atual.valor: # se o valor for menor que o valor do nó atual, vá para a subárvore esquerda
            if no_atual.filho_esquerda is None: # se não houver filho à esquerda, insira o novo nó aqui
                no_atual.filho_esquerda = No(valor)
            else:
                self._inserir_recursivo(no_atual.filho_esquerda, valor) # caso contrário, continue recursivamente na subárvore esquerda
        else: # se o valor for maior ou igual ao valor do nó atual, vá para a subárvore direita
            if no_atual.filho_direita is None: # se não houver filho à direita, insira o novo nó aqui
                no_atual.filho_direita = No(valor)
            else:
                self._inserir_recursivo(no_atual.filho_direita, valor) # caso contrário, continue recursivamente na subárvore direita
    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor) # inicia a busca recursiva a partir da raiz
    def _buscar_recursivo(self, no_atual, valor):
        if no_atual is None: # se o nó atual for None, o valor não foi encontrado
            return False
        if valor == no_atual.valor: # se o valor for igual ao valor do nó atual, o valor foi encontrado
            return True
        elif valor < no_atual.valor: # se o valor for menor que o valor do nó atual, continue a busca na subárvore esquerda
            return self._buscar_recursivo(no_atual.filho_esquerda, valor)
        else: # se o valor for maior que o valor do nó atual, continue a busca na subárvore direita
            return self._buscar_recursivo(no_atual.filho_direita, valor)
    def percorrer_em_ordem(self):
        return self._percorrer_em_ordem_recursivo(self.raiz) # inicia o percurso em ordem recursivo a partir da raiz
    def _percorrer_em_ordem_recursivo(self, no_atual):
        if no_atual is None: # se o nó atual for None, retorne uma lista vazia
            return []
        # percorre a subárvore esquerda, depois o nó atual, e finalmente a subárvore direita
        return self._percorrer_em_ordem_recursivo(no_atual.filho_esquerda) + [no_atual.valor] + self._percorrer_em_ordem_recursivo(no_atual.filho_direita)
    def remover(self, valor):
        self.raiz = self._remover_recursivo(self.raiz, valor) # inicia a remoção recursiva a partir da raiz
    def _remover_recursivo(self, no_atual, valor):
        if no_atual is None: # se o nó atual for None, o valor não foi encontrado
            return None
        if valor < no_atual.valor: # se o valor for menor que o valor do nó atual, continue a remoção na subárvore esquerda
            no_atual.filho_esquerda = self._remover_recursivo(no_atual.filho_esquerda, valor)
        elif valor > no_atual.valor: # se o valor for maior que o valor do nó atual, continue a remoção na subárvore direita
            no_atual.filho_direita = self._remover_recursivo(no_atual.filho_direita, valor)
        else: # se o valor for igual ao valor do nó atual, este é o nó a ser removido
            if no_atual.filho_esquerda is None: # caso 1: nó com apenas um filho à direita ou sem filhos
                return no_atual.filho_direita
            elif no_atual.filho_direita is None: # caso 2: nó com apenas um filho à esquerda
                return no_atual.filho_esquerda
            else: # caso 3: nó com dois filhos
                # encontra o menor valor na subárvore direita (sucessor)
                sucessor = self._encontrar_minimo(no_atual.filho_direita)
                no_atual.valor = sucessor.valor # substitui o valor do nó atual pelo valor do sucessor
                # remove o sucessor da subárvore direita
                no_atual.filho_direita = self._remover_recursivo(no_atual.filho_direita, sucessor.valor)
        return no_atual
    def _encontrar_minimo(self, no_atual):
        while no_atual.filho_esquerda is not None: # o menor valor em uma subárvore é encontrado seguindo os filhos à esquerda até o final
            no_atual = no_atual.filho_esquerda
        return no_atual

# Exemplo de uso
if __name__ == "__main__":
    arvore = ArvoreBinariaBusca()
    arvore.inserir(5)
    arvore.inserir(3)
    arvore.inserir(7)
    arvore.inserir(2)
    arvore.inserir(4)
    arvore.inserir(6)
    arvore.inserir(8)
    arvore.remover(3) # Remove o nó com valor 3 (que tem dois filhos)

    print("Percurso em ordem:", arvore.percorrer_em_ordem()) # Deve imprimir os valores em ordem crescente
    print("Buscar 4:", arvore.buscar(4)) # Deve retornar True
    print("Buscar 10:", arvore.buscar(10)) # Deve retornar False
    
    