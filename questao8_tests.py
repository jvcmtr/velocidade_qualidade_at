from questao3_utils import aleatorio_com_duplicatas


class Item:
    def __init__(self, valor, peso):
        self.v = valor
        self.w = peso

    def __str__(self):
        return f"Item({self.v},{self.w})"
    def __repr__(self):
        return self.__str__()

def ItemsValor1(weights):
    "Resultado com maior numero de items"
    arr = []
    for i in weights:
        arr.append( Item(1, i) )
    return arr

def ItemsValor0(weights):
    "Todos os possiveis resultados"
    arr = []
    for i in weights:
        arr.append( Item(0, i) )
    return arr

def ItemsValorIgualPeso(weights):
    "Resultados mais proximos do peso limite"
    arr = []
    for i in weights:
        arr.append( Item(i, i) )
    return arr

def ItemsValorDobroPeso(weights):
    "Prioriza itens mais leves"
    arr = []
    for i in weights:
        arr.append( Item(i, 2*i) )
    return arr

def ItemsValorInversoPeso(weights):
    "Prioriza itens mais pesados"
    arr = []
    for i in weights:
        arr.append( Item( 1/i, i ))
    return arr


def get_weight_list(size, dup=0):
    data = aleatorio_com_duplicatas(size, dup)
    return ItemsValor0(data)

def get_test_cases():
    TAMANHOS = [1,2,3,4,5,6,7,8,9,10] #[5, 10, 15]
    DUP = [0, 0.5, 1]
    cases = []
    for t in TAMANHOS:
        for d in DUP:
            weights = get_weight_list(t, d)
            target = t*t    # t^2 aqui permite que o limite de peso na mochila nunca seja atingido e todos os casos sejam calculados
            iteracoes = 1
            cases.append([d, target, weights, iteracoes])
    return cases