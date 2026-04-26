# Árvore Binária de Busca (Binary Search Tree)

class Node:
    def __init__(self, value):
        self.value = value
        self.left_child = None
        self.right_child = None

class BinarySearchTree: # BST - binary search tree
    def __init__(self):
        self.root = None
        
    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)
    def _insert_recursive(self, current_node, value):
        if value < current_node.value:
            if current_node.left_child is None:
                current_node.left_child = Node(value)
            else:
                self._insert_recursive(current_node.left_child, value)
        elif value > current_node.value:
            if current_node.right_child is None:
                current_node.right_child = Node(value)
            else:
                self._insert_recursive(current_node.right_child, value)
        # se o value for igual, não insira (não faz nada)

    def dfs_preorder(self):
        # DFS pré-ordem: nó -> esquerda -> direita
        # Usado para copiar/serializar árvores (visita a raiz antes dos filhos)
        return self._dfs_preorder(self.root, '')
    def _dfs_preorder(self, current_node, path):
        if current_node is None:
            return []
        return (
            [(current_node.value, path)]
            + self._dfs_preorder(current_node.left_child, path + 'L')
            + self._dfs_preorder(current_node.right_child, path + 'R')
        )

    def dfs_inorder(self):
        # DFS em-ordem: esquerda -> nó -> direita
        # Gera valores ordenados para BST e mostra posição relativa dos nós
        return self._inorder_traversal(self.root, '')
    def _inorder_traversal(self, current_node, path):
        if current_node is None:
            return []
        return (
            self._inorder_traversal(current_node.left_child, path + 'L')
            + [(current_node.value, path)]
            + self._inorder_traversal(current_node.right_child, path + 'R')
        )

    def dfs_postorder(self):
        # DFS pós-ordem: esquerda -> direita -> nó
        # Útil para remoção ou liberação de recursos bottom-up
        return self._dfs_postorder(self.root, '')
    def _dfs_postorder(self, current_node, path):
        if current_node is None:
            return []
        return (
            self._dfs_postorder(current_node.left_child, path + 'L')
            + self._dfs_postorder(current_node.right_child, path + 'R')
            + [(current_node.value, path)]
        )

    def bfs(self):
        # BFS (amplitude): visita a árvore nível a nível
        # Retorna valor + posição do nó (caminho) para cada nó visitado
        if self.root is None:
            return []
        queue = [(self.root, '')]
        result = []
        while queue:
            node, path = queue.pop(0)
            result.append((node.value, path))
            if node.left_child is not None:
                queue.append((node.left_child, path + 'L'))
            if node.right_child is not None:
                queue.append((node.right_child, path + 'R'))
        return result

    def remove(self, value):
        self.root = self._remove_recursive(self.root, value)
    def _remove_recursive(self, current_node, value):
        if current_node is None:
            return None
        if value < current_node.value:
            current_node.left_child = self._remove_recursive(current_node.left_child, value)
        elif value > current_node.value:
            current_node.right_child = self._remove_recursive(current_node.right_child, value)
        else:
            if current_node.left_child is None:
                return current_node.right_child
            elif current_node.right_child is None:
                return current_node.left_child
            else:
                successor = self._find_minimum(current_node.right_child)
                current_node.value = successor.value
                current_node.right_child = self._remove_recursive(current_node.right_child, successor.value)
        return current_node
    def _find_minimum(self, current_node):
        while current_node.left_child is not None:
            current_node = current_node.left_child
        return current_node

if __name__ == "__main__":
    tree = BinarySearchTree()
    values = [5, 3, 7, 2, 4, 6, 8, 9]
    for value in values:
        tree.insert(value)
    tree.remove(9)

    print("DFS pré-ordem:", tree.dfs_preorder())
    print("DFS em-ordem:", tree.dfs_inorder())
    print("DFS pós-ordem:", tree.dfs_postorder())
    print("BFS:", tree.bfs())