import random

def linear_search(arr, target):
    comparacoes = 0
    for i in range(len(arr)):
        comparacoes+=1
        if arr[i] == target:
            return i, comparacoes
    return -1, comparacoes

def _binary_search(arr, target, comparacoes=0, offset=0):
    "Implementação interna para manter o offset inalteravel"
    
    i = len(arr)//2
    n = arr[i]

    comparacoes+=1 # Caso array não ordenado
    if arr[0] > n or n > arr[-1]:
        raise Exception("Busca binaria não pode ser efetuada pois o array não está ordenado")
    
    comparacoes+=1 # Caso target encontrado
    if target == n:
        return i + offset, comparacoes
    
    comparacoes+=1 # Caso não restam mais buscas a serem feitas
    if i == 0:
        return -1, comparacoes
    
    comparacoes+=1 # Caso buscar na metade superior
    if target > n:
        return _binary_search(arr[i:], target, comparacoes, i+offset)
    
    comparacoes+=1 # Caso buscar na metade inferior
    if target < n:
        return _binary_search(arr[:i], target, comparacoes, offset)

def binary_search(arr, target):
    return _binary_search(arr, target, offset=0)


def teste_performance(n_elementos, n_testes=1):
    arr = range(n_elementos)

    print(f"Executando {n_testes} testes com Arrays de {n_elementos} elementos")
    print(f"| Metodo  \t| comparações (avg)\t| % do array")

    comparacoes = 0
    bcomparacoes = 0
    for i in range(n_testes):
        target = random.randrange(n_elementos)
        result, c = linear_search(arr, target)
        bresult, bc = binary_search(arr, target)
        comparacoes += c
        bcomparacoes += bc
    
    print(f"| Linear search\t| {comparacoes/n_testes:.3f} \t\t| {(comparacoes/n_testes)*100/n_elementos:.2f}%\t")        
    print(f"| Binary search\t| {bcomparacoes/n_testes:.3f} \t\t| {(bcomparacoes/n_testes)*100/n_elementos:.2f}%") 
    print(f"________________________________________________\n")       

def teste_funcionalidade(search_fn, n_elementos, n_testes):
    printed_negativo = False
    printed = False

    for i in range(n_testes):
        target = random.randint(-n_elementos//3, n_elementos-1)
        result, c = search_fn(range(n_elementos), target )
        if not result == target and target >= 0:
            raise Exception(f"Erro de funcionalidade. a posição de {target} no range({n_elementos}) não é igual a {target}. O resultado da busca retornou {result}")
        if not result == -1 and target < 0:
            raise Exception(f"Erro de funcionalidade. {target} não deveria ser encontrado em range({n_elementos}). O valor experado era -1, mas a função retornou {result}")
        
        if result<0 and not printed_negativo:
            printed_negativo = True
            print(f"{search_fn.__name__} : a posição de {target} em range({n_elementos}) é {result} como o esperado")
        
        if result>=0 and not printed:
            printed = True
            print(f"{search_fn.__name__} : a posição de {target} em range({n_elementos}) é {result} como o esperado")


if __name__ == "__main__":
    # Teste de funcionalidade
    teste_funcionalidade(linear_search, 1000, 100)
    teste_funcionalidade(binary_search, 1000, 100)
    print()
    print()

    # Teste de performance
    teste_performance(10, 1000)
    teste_performance(100, 1000)
    teste_performance(1000, 1000)
    teste_performance(10000, 1000)
    teste_performance(100000, 1000)