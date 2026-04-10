# RPM Calculator usando árvore de expressão (RPN)
# Ler as expressões a partir de um arquivo CSV. Criar os métodos para "dumpar" a árvore para um arquivo JSON e reconstruir a árvore a partir deste arquivo.

class ExpressionNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class RPMCalculator:
    operators = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b if b != 0 else float('inf'),
        '^': lambda a, b: a ** b
    }

    def __init__(self, rpn_string):
        self.rpn = rpn_string.strip()
        self.root = self._build_tree_from_rpn(self.rpn)

    def _build_tree_from_rpn(self, rpn_str):
        tokens = rpn_str.split()
        stack = []

        for token in tokens:
            if token in self.operators:
                if len(stack) < 2:
                    raise ValueError('Expressão RPN inválida: operador sem operandos')
                right = stack.pop()
                left = stack.pop()
                node = ExpressionNode(token)
                node.left = left
                node.right = right
                stack.append(node)
            else:
                try:
                    value = float(token) if '.' in token else int(token)
                except ValueError:
                    raise ValueError(f'Token inválido: {token}')
                stack.append(ExpressionNode(value))

        if len(stack) != 1:
            raise ValueError('Expressão RPN inválida: resto na pilha')
        return stack[0]

    def evaluate(self):
        return self._evaluate_node(self.root)

    def _evaluate_node(self, node):
        if node is None:
            raise ValueError('Nó vazio em avaliação')
        if isinstance(node.value, (int, float)):
            return node.value
        op = node.value
        if op not in self.operators:
            raise ValueError(f'Operador desconhecido: {op}')
        left_val = self._evaluate_node(node.left)
        right_val = self._evaluate_node(node.right)
        return self.operators[op](left_val, right_val)

    def inorder(self):
        return self._inorder(self.root)
    def _inorder(self, node):
        if node is None:
            return []
        return self._inorder(node.left) + [(node.value, self._path(node, self.root))] + self._inorder(node.right)

    def preorder(self):
        return self._preorder(self.root)
    def _preorder(self, node):
        if node is None:
            return []
        return [(node.value, self._path(node, self.root))] + self._preorder(node.left) + self._preorder(node.right)

    def postorder(self):
        return self._postorder(self.root)
    def _postorder(self, node):
        if node is None:
            return []
        return self._postorder(node.left) + self._postorder(node.right) + [(node.value, self._path(node, self.root))]

    def _path(self, target, current, prefix=''):
        if current is None:
            return None
        if current is target:
            return prefix
        left = self._path(target, current.left, prefix + 'L')
        if left is not None:
            return left
        right = self._path(target, current.right, prefix + 'R')
        return right

    def bfs_with_pos(self):
        if self.root is None:
            return []
        q = [(self.root, '')]
        out = []
        while q:
            node, path = q.pop(0)
            out.append((node.value, path))
            if node.left is not None:
                q.append((node.left, path + 'L'))
            if node.right is not None:
                q.append((node.right, path + 'R'))
        return out

if __name__ == '__main__':
    import json
    try:
        with open('expression_RPM_Calculator.txt', 'r', encoding='utf-8') as f:
            expression=f.read().strip()
    except FileNotFoundError:
        print("Arquivo de expressão não encontrado.")
        exit(1)

    calc = RPMCalculator(expression)
    result = calc.evaluate()  # Avaliar a expressão para garantir que a árvore foi construída corretamente
    print('Expressão RPN:', expression)
    print('Avaliação:', result)
    print('DFS pré-ordem (valor, posição):', calc.preorder())
    print('DFS em-ordem (valor, posição):', calc.inorder())
    print('DFS pós-ordem (valor, posição):', calc.postorder())
    print('BFS (valor, posição):', calc.bfs_with_pos())
    
    with open('result_RPM_Calculator.json', 'w', encoding='utf-8') as f:
        def node_to_dict(node, path=''):
            if node is None:
                return None
            return {
                'value': node.value,
                'path': path if path else 'raiz',
                'left': node_to_dict(node.left, path + 'L'),
                'right': node_to_dict(node.right, path + 'R')
            }
        json.dump(node_to_dict(calc.root), f, ensure_ascii=False, indent=4)