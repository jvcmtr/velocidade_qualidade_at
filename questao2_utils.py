import random

def ordenado(n_elementos):
    return([*range(1, n_elementos+1)])

def reverso(n_elementos):
    return ordenado(n_elementos)[::-1]

def semiordenado(n_elementos, n_trocas=None ):
    if(n_trocas==None):
        n_trocas = int(0.05 * n_elementos)
    
    arr = ordenado(n_elementos)
    for i in range(n_trocas):
        pos1 = random.randrange(n_elementos)
        pos2 = random.randrange(n_elementos)
        troca(arr, pos1, pos2)
    return arr

def aleatorio(n_elementos):
    arr = []
    for i in range(n_elementos):
        arr.append(random.randrange(n_elementos*2))
    return arr

def all_possible_combinations(**kwargs):
    combinations = [{}]
    for k, v in kwargs.items():
        temp = []
        for c in combinations:
            for i in v:
                temp.append({**c, k : i})
        combinations = temp
    return combinations

def get_test_cases(tamanhos, geradores, algoritimos):
    cases = all_possible_combinations(TAMANHO=tamanhos, GERADORES=geradores, ALGORITIMO=algoritimos)  
    return [{**c, "DATA": c["GERADORES"](c["TAMANHO"])} for c in cases]