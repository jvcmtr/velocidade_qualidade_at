from questao2_utils import *
import sys 
sys.setrecursionlimit(100_100) 
import time

def _bubble_sort(arr, end=None, comparacoes=0, operacoes=0):
    if end == None:
        raise Exception("_bubble_sort nescessita de um end. você quis usar 'bubble_sort(arr)' ?")

    if end == 0:
        return comparacoes, operacoes

    for i in range(end):
        comparacoes+=1
        if arr[i] > arr[i+1]:
            operacoes+=3
            troca(arr, i, i+1)
    
    return _bubble_sort(arr, end-1, comparacoes, operacoes)

def _selection_sort(arr, start=0, comparacoes=0, operacoes=0):
    min_idx = start
    
    if start == len(arr):
        return comparacoes, operacoes

    for i in range(start, len(arr)):
        comparacoes+=1
        if arr[i] < arr[min_idx]:
            min_idx = i

    # Esta verificação adiciona uma comparação mas potencialmente evita uma troca.
    # Só se torna eficiente com vetores já ordenados ou semiordenados.
    comparacoes += 1 
    if min_idx != start: 
        operacoes+=3
        troca(arr, min_idx, start)
    
    return _selection_sort(arr, start+1, comparacoes, operacoes)

def _insertion_sort(arr, end=1, comparacoes=0, operacoes=0):
    if end == len(arr):
        return comparacoes, operacoes

    for i in range(end, 0, -1):
        comparacoes+=1
        if arr[i] < arr[i-1]:
            operacoes+=3
            troca(arr, i, i-1)
    return _insertion_sort(arr, end+1, comparacoes, operacoes) 

def bubble_sort(arr):
    return _bubble_sort(arr, len(arr)-1)

def selection_sort(arr):
    return _selection_sort(arr)

def insertion_sort(arr):
    return _insertion_sort(arr)

if __name__ == "__main__":
    ALGORITIMOS = [bubble_sort, selection_sort, insertion_sort]
    dt = []
    dt.append(["Tipo de vetor" , "Algoritmo", "N_itens" , "Comparacoes (relativo)","Operacoes (relativo)"])
    cases = get_test_cases(ALGORITIMOS)
    for i in range(len(cases)):
        t = cases[i]
        type = t["type"]
        size = t["size"]
        fn = t["algorithm"]
        algotitimo = t["algorithm"].__name__
        comparacoes, operacoes = fn(t["data"])
        dt.append([type, algotitimo, f"{size}", f"{comparacoes} ({comparacoes/size:.2f})", f"{operacoes} ({operacoes/size:.2f})" ])
        print(f"Executando caso de teste {i}/{len(t)}. \t tipo de vetor:\"{type}\"; \t  algotitimo:\"{algotitimo}\";  \t n_itens\"{size}\";")
        # print(f"│ {type}\t| {algotitimo}\t| {size}\t|{comparacoes} ({comparacoes/size:.2f})\t|{operacoes} ({operacoes*100/size:.2f})\t) |")
    print_table(dt)        