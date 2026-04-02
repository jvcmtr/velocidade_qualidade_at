
from questao2 import insert
from questao2_utils import aleatorio
from utils import *
import random
import time
from collections import deque

def arvore_aleatoria(length):
    tree = {}
    arr_base = aleatorio(length)
    for n in arr_base:
        insert(tree, n, 0, 0)
    return tree



def atravessamento_amplitude_fila(root):
    if root is None:
        return []
    
    result = []
    q = deque()
    q.append(root)

    while q:
        item = q.popleft()
        result.append(item["val"])
        if item.get('l'):
            q.append(item['l'])
        if item.get('r'):
            q.append(item['r'])
    
    return result


def atravessamento_profundidade_pilha(root):
    if root is None:
        return []
    
    result = []
    pilha = [] 
    pilha.append(root)

    while pilha:
        item = pilha.pop()
        result.append(item['val'])
        
        if item.get('l'):
            pilha.append(item['l'])
        if item.get('r'):
            pilha.append(item['r'])
    
    return result




def test(SIZES, ALGORITHMS, ITERATIONS, verbose=True):
    cases = all_possible_combinations(SIZE=SIZES, FUNC=ALGORITHMS)
    
    # Gera arvores de teste.
    # Uma arvore diferente para cada iteração promove a convergencia da media para o caso medio do algoritimo
    # Utilizar as mesmas arvores para diferentes algoritimos auxilia a comparação entre eles 
    tree_sizes = {}
    total_trees = ITERATIONS * len(SIZES)    
    if verbose:
        print("Gerando arvores de teste...")

    for c in cases:
        for i in range(ITERATIONS):
            idx = (i, c["SIZE"])
            if not tree_sizes.get(idx):
                start = time.time()
                tree_sizes[idx] = arvore_aleatoria(c["SIZE"])
                delta = time.time() - start
                if verbose and i%100 ==0:
                    print(f"Arvore teste {len(tree_sizes.items())}/{total_trees} gerada em {(delta*1000):.2f} milisegundos \t\t SIZE:{c['SIZE']}", end="\r")
            c["DATA"] = tree_sizes[idx]
    # Preparando dados de output
    dt = []
    dt.append(["Tamanho", "Algoritimo", "Iterações", "Duração Media", "Tamanho do resultado"])

    # Rodando testes
    count = 0
    if verbose:
        print("Executando testes...")
    for c in cases:
        count+=1
        total = 0
        result = []

        for i in range(ITERATIONS):
            start = time.time()
            result = c["FUNC"](c["DATA"])
            total += time.time() - start

        avg = total / ITERATIONS
        size = c["SIZE"]
        name = c["FUNC"].__name__.replace("atravessamento_", "")
        dt.append([ size, name, ITERATIONS, f"{avg:.4f}s", len(result)])

        if verbose:
            print(f"Teste {count}/{len(cases)} executado em {total:.2f} segundos \tSize:{size} \tIterations:{ITERATIONS} \tAlgorithm:{name}", end="\r")
    
    print_table(dt)
    


if __name__ == "__main__":
    SIZES = [1000 , 10000, 25000]
    ALGORITHMS = [atravessamento_amplitude_fila, atravessamento_profundidade_pilha]
    ITERATIONS = 100
    dt = test(SIZES, ALGORITHMS, ITERATIONS)