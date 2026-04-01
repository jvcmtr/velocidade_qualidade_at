
class Item:
    def __init__(self, valor, peso):
        self.v = valor
        self.w = peso

    def __str__(self):
        return str({"valor":self.v, "peso":self.w})

# Baseado na questão 6 do TP3
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

    max_val = 0
    best = []
    for comb in combinacoes:
        soma = sum([i.v for i in comb if i]) 
        print("Avaliando soma ", soma, comb, )
        if soma >= max_val:
            if soma > max_val:
                max_val = soma
                best = []
            best.append(comb)

    return best

def test(target, weights):
    arr = []
    for i in weights:
        arr.append( Item(1, i) )

    print([[x.w for x in sol] for sol in knapsack(target, arr)])

if __name__ == "__main__":
    test(3, [1, 1, 1, 2])
    # test(5, [1, 2, 2, 3])
    # test(11, [2, 2, 4, 5, 6, 7 ])
    # print(knapsack(19, [5, 5, 7, 8 ]))