import time
import random
from utils import all_possible_combinations, print_table
from questao4 import HashTableChained 
from questao8_tests import *


# Implementação padrão baseada em `knapsack_2()` disponivel em `questao8_ref.py`. 
# possui algumas alterações para poder usar memoization
def _knapsack(target, items, _recursive_self=None, **kwargs):
    if not _recursive_self: _recursive_self = _knapsack

    # Variaveis de retorno. 
    # Também servem como caso base para sair da recussão 
    best = 0
    combinacoes = [[]]  # [] Representa os itens selecionados, ou seja, nenhum. 
    
    
    # Duplica o array que será usado no subproblema 
    # para não alterar a instancia original 
    array = [*items] 

    for i in items:
        array.remove(i) # Alterar diretamente o array aqui evita duplicatas
        if i.w <= target:
            
            # Solução do subproblema
            subproblema, meta = _recursive_self(target-i.w, array, _recursive_self, **kwargs).values()
            soma = i.v + subproblema[0]
            solucoes = [ [i, *x] for x in subproblema[1] ]
            kwargs.update(meta)

            # Atualiza melhores combinações se nescessario
            if soma == best: combinacoes.extend(solucoes)
            if soma > best: best, combinacoes = soma, solucoes

    return {"result": (best, combinacoes), "meta":kwargs}



# Wrapper que conta o numero de chamadas
def _knapsack_count_calls(target, items, _recursive_self=None, **__META):
    # Valores default
    _recursive_self = _recursive_self or _knapsack_count_calls
    __META = {"CALLS":0 , **__META}

    __META["CALLS"] += 1
    return _knapsack(target, items, _recursive_self=_recursive_self, **__META)



# Wrapper que aplica memoization
def _knapsack_memo(target, items, _recursive_self=None, **__META):
    # Valores default
    _recursive_self = _recursive_self or _knapsack_memo
    __META = {"CACHE":HashTableChained(), "CACHED_CALLS":0, **__META}
    
    # Busca no cache
    key = f"{target}:{items}" 
    result = __META["CACHE"].get( key )

    # Chama knapsack se não encontrou
    if not result:
        result, __META = _knapsack_count_calls(target, items, _recursive_self=_knapsack_memo, **__META).values()
        __META["CACHE"].put(key, result)
    else:
        __META["CACHED_CALLS"] +=1

    # Retorna
    return {"result": result, "meta":__META}



# Delega para _knapsack_memo ou para __knapsack. Potencialmente trata o retorno
def knapsack(target, items, usememo=True, include_meta=False):
    fn = _knapsack_memo if usememo else _knapsack_count_calls
    result = fn(target, items)
    return result if include_meta else result["result"]








def test_cases(CASOS, ALGORITIMOS):
    dt = []
    # dt.append(["N_Itens", "Duplicatas (%)", "Iterações", "Algoritimo", "Duração", "Duração media", "Duração maxima", "Duração minima", "Chamadas", "Chamadas relativas"])
    
    dt.append(["N_Itens", "Duplicatas (%)", "Algoritimo", "Duração", "Chamadas", "Chamadas / N_itens"])

    tests = all_possible_combinations(CASO=CASOS, ALGORITIMO=ALGORITIMOS)
    
    for j in range(len(tests)):
        t = tests[j]
        dup, target, weights, iteracoes = t["CASO"]
        algoritimo, func = t["ALGORITIMO"]
        total=0
        result = None
        calls=0
        calls_t=0
        max_time=0
        min_time=999999
        for i in range(iteracoes):
            start = time.time()
            result, meta = func(target, weights).values()
            delta = time.time() - start
            total += delta
            calls = meta["CALLS"]
            calls_t += calls
            if delta > max_time: max_time = delta 
            if delta < min_time: min_time = delta

            print(f"[{j+1}/{len(tests)}] [{i+1}/{iteracoes}] Teste executado com sucesso: \t SIZE:{len(weights)} \t ALGORITIMO:{algoritimo} \t DURAÇÃO:{delta:.4f} (decorrido:{total:.2f}s)", end="\r")
        
        avg = total/iteracoes 
        call_rel = calls/len(weights)
        # dt.append([len(weights), f"{(dup*100):.2f}%", iteracoes, algoritimo, f"{(avg*1000):.2f}ms", f"{(max_time*1000):.2f}ms", f"{(min_time*1000):.2f}ms", calls, f"{call_rel:.2f}"])
        dt.append([len(weights), f"{(dup*100):.2f}%", algoritimo, f"{(avg*1000):.2f}ms", calls, f"{call_rel:.2f}"])

    print()
    print_table(dt)


def test(target, weights):
    def str_list(dt):
        if len(dt) == 0: return "[]"
        return  "".join([ '\n   - '+str(x) for x in dt ])

    print("___________________")
    print(f"Target: {target}")
    print(f"Items: { str_list(weights) }")
    result = knapsack(target, weights, True)
    print(f"Valor da combinação: { knapsack(target, weights)[0]  }")
    print(f"Combinações: { str_list( knapsack(target, weights)[1] )  }")

if __name__ == "__main__":

    # Teste de funcionalidade
    # test(3, ItemsValor1([1, 1, 1, 2]))
    # test(2, ItemsValor0([1, 2, 3]))
    # test(3, ItemsValorIgualPeso([1, 1, 1]))

    # Provando que é 2^n
    print("______________________________________")
    print("Teste: Itens na mochila são todos iguais")
    N = 10
    weights = get_weight_list(N, 1)
    result = knapsack( N**N , weights, False, True) # N^N para evitar que o limite da mochila seja atingido
    result2 = knapsack( N**N , weights, True, True)
    print("N = ", N)
    print("N solucoes : ", len(result["result"][1]))
    print("N Chamadas (sem memoization)  : ", result["meta"]["CALLS"], f" 2^N")
    print("N Chamadas (com memoization)  : ", result2["meta"]["CALLS"], f" 1+N")


    # Teste de performance
    algoritimos = [
        ("Com Memoization",_knapsack_memo),
        # ("Sem Memoization", _knapsack_count_calls)
    ]
    casos = get_test_cases()
    test_cases(casos, algoritimos)



