from questao3_utils import *
from utils import *
import time

# Presume-se aqui que o processamento nescessario para computar o numero de operações e comparações será negligenciavel
# Por isso importamos as funções já definidas na questão 2 
from questao2 import binary_search_sort


def remove_duplicatas(arr):
    seen = {}
    result = []    
    for n in arr:
        if not seen.get(n):
            seen[n] = 1
            result.append(n)
            continue
    return result

def com_remove_duplicatas(func):
    result = lambda arr, k : func(remove_duplicatas(arr), k)
    result.__name__ = func.__name__
    return result

def k_smallest_A(arr, k):
    if len(arr) > k:
        return arr
    # Já que a fonte de dados é um array aleatorio, 
    # BST sort foi escolhido para ordenar o arrays grandes.
    binary_search_sort(arr)
    return arr[:k]

def partition(arr, idx):
    i = 0 # elemento sendo processado atualmente
    j = 0 # n_itens particionados (indice do primeiro elemento da segunda particao)

    # Move o pivot para o final do vetor
    troca(arr, idx, len(arr)-1)
    curr_idx = len(arr)-1
    
    # particiona os itens do array (coloca itens menores que o pivot na primeira particao)
    for i in range(len(arr)):
        if arr[i] < arr[curr_idx]:
            troca(arr, j, i)
            j+=1

    # coloca pivot entre as partições
    troca(arr, curr_idx, j)
    curr_idx = j
    return curr_idx

def k_smallest_B(arr, k):
    # Casos de saida
    if k < 1:
        return []

    if len(arr) < k:
        return arr

    idx = partition(arr, 0) # Poderia escolher um aleatorio, mas não traz benefício
    n_itens_encontrados = idx+1  # Declarado para manter a legibilidade do codigo e evitar erros de 'off by one'

    if n_itens_encontrados-1 == k:
        return arr[:idx]

    if n_itens_encontrados == k:
        return arr[:idx+1] # +1 para incluir o proprio idx 
    
    if n_itens_encontrados > k:
        return k_smallest_B( arr[:idx], k)

    if n_itens_encontrados < k:
        return [ 
            *arr[:idx + 1],  # +1 para incluir o proprio idx 
            *k_smallest_B( arr[idx + 1:], k - n_itens_encontrados )
        ]


def arr_equal(arr1, arr2):
    if not len(arr1) == len(arr2):
        return False

    binary_search_sort(arr1)
    binary_search_sort(arr2)
    for i in range(len(arr1)):
        if not arr1[i] == arr2[i]:
            return False
    return True


def test(algoritimos, tamanhos, duplicidades, relative_ks, verbose=False, print_output=True):

    # Inicializa variaveis    
    tempo_total = 0
    dt = []
    dt.append(["N_itens", "Duplicatas", "Seleções (k)", "Seleções relativas (%)", "Algoritmo", "Duração (ms)"])
    output_dt = []
    output_dt.append(["N_itens" , "Rate_duplicidade", "k", "Algoritmo", "Duração"])
    
    # Gera os arrays de teste
    cases = all_possible_combinations(TAMANHO=tamanhos, RELATIVE_K=relative_ks, ALGORITIMO=algoritimos, RATE_DUPLICIDADE=duplicidades)
    # cases = [ x for x in cases if x["K"] <= x["TAMANHO"] ] # remove casos de teste sem sentido
    case_data = {}
    for c in cases:
        idx = (c["TAMANHO"], c["RATE_DUPLICIDADE"])
        if not case_data.get(idx):
            case_data[idx] = aleatorio_com_duplicatas(c["TAMANHO"], c["RATE_DUPLICIDADE"])
        c["DATA"] = case_data[idx]
        c["K"] = int(c["TAMANHO"] * c["RELATIVE_K"])

    # Executa os testes
    for i in range(len(cases)):
        t = cases[i]
        size = t["TAMANHO"]
        rate_dup = f"{t["RATE_DUPLICIDADE"] * 100}%"
        fn = t["ALGORITIMO"]
        k = t["K"]
        rel_k = t["RELATIVE_K"]
        algotitimo = t["ALGORITIMO"].__name__.replace("k_smallest_", "Versao ")

        # Computa o resultado
        start = time.time()
        result = fn(t["DATA"], t["K"])
        delta = (time.time() - start) * 1000 
        tempo_total += delta

        # Formata/Salva o resultado
        output_dt.append([size, rate_dup, k, algotitimo, f"{delta:.8f}" ])
        if(print_output):
            dt.append([f"{size}", f"{t["RATE_DUPLICIDADE"] * 100}%", str(k), f"{rel_k*100}%" , algotitimo, f"{delta:.3f} ms" ])
        if(verbose):
            print(f"Caso de teste {i+1}/{len(cases)} executado em {delta:.3f} milisegundos. \t n_itens\"{size}\"; \t k\"{k}\"; \t  algotitimo:\"{algotitimo}\";")
    
    # Printa os resultados
    if print_output:
        print_table(dt)
    if verbose:  
        print(f"\nTempo total de computação: {(tempo_total/1000):.4f}s")

    return output_dt, tempo_total  



if __name__ == "__main__":
    ALGORITIMOS = [ com_remove_duplicatas(k_smallest_A), com_remove_duplicatas(k_smallest_B)]
    TAMANHOS=[1000, 10_000, 25_000, 50_000 ,100_000]
    RELATIVE_Ks = [0.1, 0.8]
    DUPLICIDADES=[0.2]

    # Teste 1
    dt, tempo_total = test(ALGORITIMOS, TAMANHOS, DUPLICIDADES, RELATIVE_Ks, verbose=True)
    
    # Teste 2 (mais completo, muito grande para tirar print)
    TAMANHOS=[1000, 10_000, 25_000, 50_000 ,100_000, 500_000]
    RELATIVE_Ks = [0.1, 0.5, 0.8]
    DUPLICIDADES=[0.2, 0.5, 0.8]
    dt, tempo_total = test(ALGORITIMOS, TAMANHOS, DUPLICIDADES, RELATIVE_Ks, verbose=True, print_output=False)
    save_table(dt, "questao3_output.csv")