from questao2_utils import *
import time
from utils import *
import sys
sys.setrecursionlimit(50000)


def bubble_sort(arr):
    comparacoes = 0
    operacoes = 0
    for i in range(1,len(arr)):
        for j in range(len(arr)-i):
            comparacoes+=1
            if arr[j] > arr[j+1]:
                operacoes+=3
                troca(arr, j, j+1)

    return comparacoes, operacoes

def selection_sort(arr): 
    comparacoes = 0
    operacoes = 0
    for i in range(len(arr)):
        operacoes+=1
        min_idx = i

        for j in range(i, len(arr)):
            comparacoes+=1
            if arr[i] < arr[min_idx]:
                operacoes+=1
                min_idx = i

        # Esta verificação adiciona uma comparação mas potencialmente evita uma troca.
        # Só se torna eficiente com vetores já ordenados ou semiordenados.
        comparacoes += 1 
        if min_idx != i: 
            operacoes+=3
            troca(arr, min_idx, i)
    
    return comparacoes, operacoes

def insertion_sort(arr):
    comparacoes = 0
    operacoes = 0
    for i in range(len(arr)):
        for j in range(i, 0, -1):
            comparacoes+=1
            if arr[i] < arr[i-1]:
                operacoes+=3
                troca(arr, i, i-1)

    return comparacoes, operacoes

def binary_search_sort(arr):
    # Neste metodo não foi implementado balanceamento da arvore, 
    # já que ele não traz nenhum valor para a ordenação dos elementos, 
    # O balanceamento de uma arvore binaria é importante para a seleção de itens, não para a ordenação
    tree = {}
    comparacoes = 0
    operacoes = 0

    for i in arr:
        comparacoes, operacoes = insert(tree, i, comparacoes, operacoes)

    s, comparacoes, operacoes = sort(tree, comparacoes, operacoes)
    
    # Para manter a mesma assinatura dos outros metodos de ordenação, 
    # Sobreescreve a instancia original
    arr.clear()
    arr.extend(s)

    return comparacoes, operacoes

def insert(el, valor, comparacoes, operacoes):
    comparacoes+= 1
    if not el:
        operacoes += 1
        # Altera a instancia original
        el.update({"val":valor, "l":{}, "r":{}})
        return comparacoes, operacoes

    comparacoes+= 1
    if valor >= el['val']:
        comparacoes, operacoes = insert(el['r'], valor, comparacoes, operacoes)
        return comparacoes, operacoes
    comparacoes+= 1
    if valor < el['val']:
        comparacoes, operacoes= insert(el['l'], valor,comparacoes, operacoes)
        return comparacoes, operacoes


def sort(el, comparacoes, operacoes):
    comparacoes+= 1
    if not el:
        return [], comparacoes, operacoes
        
    l, comp, op, = sort(el['l'], comparacoes, operacoes)
    r, comp2, op2 = sort(el['r'], 0, 0)
    return [
        *l, 
        el['val'], 
        *r
    ], comp+comp2 , op + op2


def test(algoritimos, tamanhos, geradores, verbose=False, print_output=True):

    tempo_total = 0
    cases = get_test_cases(tamanhos, geradores, algoritimos) 
    
    dt = []
    output_dt = []
    output_dt.append(["N_itens" , "Tipo de vetor" , "Algoritmo", "Comparacoes", "Comparacoes/N", "Operacoes", "Operacoes/N", "Duração (sec)"])
    dt.append(["N_itens" , "Tipo de vetor" , "Algoritmo", "Comparacoes (relativo)","Operacoes (relativo)", "Duração"])

    for i in range(len(cases)):
        t = cases[i]
        size = t["TAMANHO"]
        fn = t["ALGORITIMO"]
        algotitimo = t["ALGORITIMO"].__name__
        type = t["GERADORES"].__name__

        start = time.time()
        comparacoes, operacoes = fn(t["DATA"])
        delta = time.time() - start
        tempo_total += delta

        output_dt.append([size, type, algotitimo, comparacoes, f"{comparacoes/size:.4f}", operacoes, f"{operacoes/size:.4f}", f"{delta:.4f}" ])
        if(print_output):
            dt.append([f"{size}", type, algotitimo, f"{comparacoes} ({comparacoes/size:.2f})", f"{operacoes} ({operacoes/size:.2f})", f"{delta:.2f}s" ])
        if(verbose):
            print(f"Caso de teste {i+1}/{len(cases)} executado em {delta:.3f} segundos. \t n_itens\"{size}\"; \t tipo de vetor:\"{type}\"; \t  algotitimo:\"{algotitimo}\";")
    
    if print_output:
        print_table(dt)
    if verbose:  
        print(f"\nTempo total de computação: {(tempo_total/60):.2f}min")

    return output_dt, tempo_total  

if __name__ == "__main__":
    ALGORITIMOS = [bubble_sort, selection_sort, insertion_sort, binary_search_sort]
    TAMANHOS=[1000, 10_000, 25_000, 50_000 ,100_000]
    GERADORES=[ordenado, reverso, semiordenado, aleatorio]

    # Teste 1
    dt, tempo_total = test(ALGORITIMOS, TAMANHOS[:-2], GERADORES, verbose=True)
    
    relacao = ((25**2)+(10**2)+(1**2))/((100**2)+(50**2)) # Presume-se aqui que todos os algoritmos são O(n^2)
    estimativa = tempo_total / relacao
    print(f"Estimativa de tempo para o computar vetores com 100.000 e 50.000 items: {(estimativa/60/60):.2f} Horas") 
    
    save_table(dt, "questao2_output.csv")    