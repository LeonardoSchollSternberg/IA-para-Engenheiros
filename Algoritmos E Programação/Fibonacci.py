def fibonacci_recursive(n):
    if n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        fib_sequence = fibonacci_recursive(n - 1)
        next_term = fib_sequence[-1] + fib_sequence[-2]
        fib_sequence.append(next_term)
        return fib_sequence

def fibonacci_iterative(n):
    if n == 1:
        return [0]
    else:
        fib_sequence = [0, 1]
        for i in range(2, n):
            next_term = fib_sequence[i - 1] + fib_sequence[i - 2]
            fib_sequence.append(next_term)
        return fib_sequence

num_termos = 10
print("Fibonacci (Recursivo):", fibonacci_recursive(num_termos))
print("Fibonacci (Iterativo):", fibonacci_iterative(num_termos))