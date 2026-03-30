from questao3_utils import *
from utils import *

# Presume-se aqui que o processamento nescessario para computar o numero de operações e comparações será negligenciavel
# Por isso importamos as funções já definidas na questão 2 
from questao2 import binary_search_sort


def remove_duplicatas(arr):
    seen = {}
    result = []    
    for n in arr:
        if not seen[n]:
            seen[n] = 1
            result.append(n)
            continue
    return result

def k_smallest_v1(arr, k):
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

def quick_select_sort(arr):
    # Casos de saida 
    l = len(arr) 
    if l <= 1:
        return
    # Otimização para vetores de 2 elementos
    if l == 2 and arr[0] > arr[1]:
        troca(arr, 0, 1)
        return
    if l == 2:
        return
    
    idx = 0 # Poderia escolher um aleatorio, mas não traz benefício
    
    pivot = partition(arr, idx)
    quick_select_sort(arr[:pivot])
    quick_select_sort(arr[pivot:])


def quick_select_smallest(arr, k):
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
        return quick_select_smallest( arr[:idx], k)

    if n_itens_encontrados < k:
        return [ 
            *arr[:idx + 1],  # +1 para incluir o proprio idx 
            *quick_select_smallest( arr[idx + 1:], k - n_itens_encontrados )
        ]


def k_smallest_v2(arr, k):
    items_found = []
    to_be_found = k
    search_area = [*arr]
    
    while to_be_found > 0:
        if len(search_area) < to_be_found:
            items_found.extend(search_area)
            break

        pivot_idx = partition(search_area, 1)
        
        if pivot_idx > to_be_found:
            search_area = [*search_area[:pivot_idx]]
            continue

        if pivot_idx <= to_be_found:
            items_found.extend( search_area[:pivot_idx] )
            to_be_found -= pivot_idx

def arr_equal(arr1, arr2):
    if not len(arr1) == len(arr2):
        return False

    binary_search_sort(arr1)
    binary_search_sort(arr2)
    for i in range(len(arr1)):
        if not arr1[i] == arr2[i]:
            return False
    return True

def test(tamanho, dup_rate, k):
    arr = aleatorio_com_duplicatas(tamanho, dup_rate)
    
    correct = k_smallest_v1([*arr], k)
    print(f"Resultado esperado : {correct}")
    rec = quick_select_smallest([*arr], k)
    print(f"Recursivo : {rec}")
    print(f"OK : {arr_equal(correct, rec)}")
    #wil = k_smallest_v2([*arr], k)
    #print(f"While Loop : {wil}")
    
    print("________________________________-")

test(100, 1, 5)
test(100, 0.2, 10)
test(10, 0.2, 8 )
test(5, 0, 5)
test(5, 0, 6)

if __name__ == "__main__":
    # ALGORITIMOS = [bubble_sort, selection_sort, insertion_sort, binary_search_sort]
    TAMANHOS=[1000, 10_000, 25_000, 50_000 ,100_000]
    # GERADORES=[ordenado, reverso, semiordenado, aleatorio]

    # # Teste 1
    # dt, tempo_total = test(ALGORITIMOS, TAMANHOS[:-3], GERADORES, verbose=True)
    