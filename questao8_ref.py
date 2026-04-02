import time

class Item:
    def __init__(self, valor, peso):
        self.v = valor
        self.w = peso

    def __str__(self):
        return str( {"valor":self.v, "peso":self.w} )


# Baseado na questão 6 do TP3, atualizado para que weights seja uma lista de itens e não de numeros
# Leva em conta o valor de cada item, diferentemente da versão original
def knapsack(target, weights, depth=0):
    array = [*weights]
    combinacoes = [[]] # Representa "Não selecionar mais nenhum item" 

    if len(weights)==0:
        return [[]]

    for i in weights:
        if i.w <= target:
            # Alterar o array original aqui evita duplicatas
            array.remove(i) 
            combinacoes.extend([[i, *x] for x in knapsack(target-i.w, array, depth+1) if x is not None ])

    # FIltrar a cada recursão é ideal para reduzir o problema a cada iteração
    max_val = 0
    best = []
    for comb in combinacoes:
        soma = sum([i.v for i in comb if i]) 
        if soma >= max_val:
            if soma > max_val:
                max_val = soma
                best = []
            best.append(comb)

    return best




# Tentativa de otimizar a função original fazendo o loop para selecionar as combinações de mais valor somente no final
# Evidentemente não é bom, é melhor ir reduzindo o problema a cada iteração do que tentar computar tudo
def knapsack_1(target, weights, depth=0):

    def all_viable_combinations(target, weights, depth=0):
        array = [*weights]
        combinacoes = [[]] # Representa "Não selecionar mais nenhum item" 

        if len(weights)==0:
            return [[]]

        for i in weights:
            if i.w <= target:
                # Alterar o array original aqui evita duplicatas
                array.remove(i) 
                combinacoes.extend([[i, *x] for x in all_viable_combinations(target-i.w, array, depth+1) if x is not None ])
        return combinacoes

    
    combinacoes = all_viable_combinations(target, weights, depth)
    max_val = 0
    best = []
    for comb in combinacoes:
        soma = sum([i.v for i in comb if i]) 
        if soma >= max_val:
            if soma > max_val:
                max_val = soma
                best = []
            best.append(comb)

    return best




# Versão otimizada da primeira implementação, unifica o loop do 
# subproblema com o de calculo do valor. Alem de ser bem mais concisa e legivel.
def knapsack_2(target, items):

    best = 0         # Melhor soma de valor até agora
    combinacoes = [[]]    # [] Representa "Não selecionar mais nenhum item" 
    
    # if len(items)==0:  # Não nescessario, o loop vai ser pulado se não houver itens
    #     return 0, [[]]

    array = [*items]

    for i in items:
        if i.w <= target:
            array.remove(i) # Alterar o array aqui evita duplicatas
            
            # Solução do subproblema
            subproblema = knapsack_2(target-i.w, array)
            soma = i.v + subproblema[0]
            solucoes = [ [i, *x] for x in subproblema[1] ]

            # Atualiza melhores combinações se nescessario
            if soma == best: combinacoes.extend(solucoes)
            if soma > best: best, combinacoes = soma, solucoes

    return best, combinacoes


# ____________________________________________________________________________
# TESTES:

def timed(n, func):
    start = time.time()
    for i in range(n):
        print(f"Rodando caso ({i+1}/{n})", end="\r")
        func()
    print(f" "*60, end="\r")
    return time.time() - start


def test(target, weights):
    arr = []
    for i in weights:
        arr.append( Item(1, i) )

    print(f"Target: {target}")
    print("    Knapsack   : ", [[x.w for x in sol] for sol in knapsack(target, arr)])
    print("    Knapsack_1 : ", [[x.w for x in sol] for sol in knapsack_1(target, arr)])
    print("    Knapsack_2 : ", [[x.w for x in sol] for sol in knapsack_2(target, arr)[1]])



if __name__ == "__main__":

    print("Teste funcional")
    test(3, [1, 1, 1, 2])
    test(5, [1, 2, 2, 3])
    test(11, [2, 2, 4, 5, 6, 7 ])
    print()
    
    print("Teste de performance")
    N = 6
    TARGET = 50
    ITEMS = [ Item(i, i*1) for i in range(TARGET) ]

    t = timed(N, lambda: knapsack(TARGET, ITEMS))
    print(f"    Knapsack : {t:.2f}")
    t = timed(N, lambda: knapsack_1(TARGET, ITEMS))
    print(f"    Knapsack_1 : {t:.2f}")
    t = timed(N, lambda: knapsack_2(TARGET, ITEMS))
    print(f"    Knapsack_2 : {t:.2f}")


