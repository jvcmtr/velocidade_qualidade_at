from questao2_utils import *
import sys 
sys.setrecursionlimit(100_100) 
import time

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
  

if __name__ == "__main__":
    ALGORITIMOS = [bubble_sort, selection_sort, insertion_sort]

    dt = []
    dt.append(["Tipo de vetor" , "Algoritmo", "N_itens" , "Comparacoes (relativo)","Operacoes (relativo)", "Duração"])
    tempo_total = 0
    cases = get_test_cases(ALGORITIMOS)
    for i in range(len(cases)):
        t = cases[i]
        type = t["type"]
        size = t["size"]
        fn = t["algorithm"]
        algotitimo = t["algorithm"].__name__
        start = time.time()
        comparacoes, operacoes = fn(t["data"])
        delta = time.time() - start
        tempo_total += delta
        dt.append([type, algotitimo, f"{size}", f"{comparacoes} ({comparacoes/size:.2f})", f"{operacoes} ({operacoes/size:.2f})", f"{delta:.2f}s" ])
        print(f"Caso de teste {i}/{len(cases)} executado em {delta:.4f} segundos . \t tipo de vetor:\"{type}\"; \t  algotitimo:\"{algotitimo}\";  \t n_itens\"{size}\";")
    print_table(dt)  
    print(f"\nTempo total de computação: {(tempo_total/60):.2f}min")

    relacao = ((25**2)+(10**2)+(1**2))/((100**2)+(50**2))
    estimativa = tempo_total / relacao
    print(f"Estimativa de tempo para o computar vetores com 100.000 e 50.000 items: {(estimativa/60/60):.2f} Horas")      