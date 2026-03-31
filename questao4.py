import random
from utils import *

class NullNode:
    def __len__(self):
        return 0
    
    def __str__(self):
        return str(None)

    def get(self, key):
        return None

    def find(self, key):
        return None

    def delete(self, key):
        return self

    def put_or_update(self, key, value):
        return Node(key, value), False, 1

    def as_array(self):
        return []

NULL_NODE = NullNode()

class Node:
    def __init__(self, key, value, next_node=None):
        self.key = key
        self.value = value
        self.next = next_node if next_node else NULL_NODE

    def __len__(self):
        return 1 + len(self.next)
    
    def __str__(self):
        return [ f"{self.key}:{self.value}" ] + str(self.next)

    def get(self, key):
        if self.key == key:
            return self.value
        return self.next.get(key)

    def find(self, key):
        if self.key == key:
            return self
        return self.next.find(key)

    def delete(self, key):
        if self.key == key:
            return self.next
        
        self.next = self.next.delete(key)
        return self

    def put_or_update(self, key, value):
        "Retorna (n, true, comparacoes) se um Node foi atualizado"
        if self.key == key:
            self.value = value
            return self, True, 1

        self.next, updated, comp = self.next.put_or_update(key, value)
        return self, updated, 1+comp

    def as_array(self):
        return [self, *self.next.as_array()]

class HashTableChained:
    def __init__(self, capacity=8, load_factor=0.75):
        self.size = 0
        self.capacity = capacity
        self.load_factor = load_factor
        self.buckets = [NULL_NODE] * self.capacity

    def __len__(self):
        return self.size

    def _current_load_factor(self):
        return self.size / self.capacity

    def _try_rehash(self):
        if not self._current_load_factor() > self.load_factor:
            return

        nodes = [ x for b in self.buckets for x in b.as_array()]
        self.__init__(self.capacity*2, self.load_factor)
        for n in nodes:
            self.put(n.key, n.value)

    def _get_bucket_idx(self, key):
        return hash(key) % self.capacity
        
    def _get_bucket(self, key):
        return self.buckets[self._get_bucket_idx(key)]

    def put(self, key, value):
        idx = self._get_bucket_idx(key)
        
        self.buckets[idx], updated, comparacoes = self.buckets[idx].put_or_update(key, value)
        if updated:
            return comparacoes
        
        self.size += 1
        self._try_rehash()
        return comparacoes

    def get(self, key):
        b = self._get_bucket(key)
        return b.get(key)

    def delete(self, key):
        idx = self._get_bucket_idx(key)
        self.buckets[idx] = self.buckets[idx].delete(key)

def teste_funcionalidade(verbose=False):
    INICIAL_LEN = 4
    dt = HashTableChained(capacity=INICIAL_LEN)

    # Insere chaves para forçar rehash
    chaves_valores = { f"CHAVE_{i}":f"VALOR_{i}" for i in range( INICIAL_LEN+20 ) } 
    for k, v in chaves_valores.items():
        dt.put(k, v)
    rehash = len(dt) > INICIAL_LEN
        
    # Verifica se todas as chaves permanecem acessíveis após rehash
    acessible = True
    for k,v in chaves_valores.items():
        val = dt.get(k)
        if not val == v:
            all_accessible = False
            break

    # Verifica se valor da chave é atualizado quando a chave já existe:
    k = "CHAVE_NOVA"
    dt.put(k, "VALOR")
    dt.put(k, "OUTRO_VALOR")
    update = dt.get(k) == "OUTRO_VALOR"

    # Verifica se uma chave consegue ser devidamente removida
    k = "CHAVE REMOVER"
    dt.put(k, "VALOR_REMOVIDO")
    dt.delete(k)
    remove = dt.get(k) == None

    if verbose:
        print(f"             Sofreu rehash  : \t{ rehash }")
        print(f" Todas as chaves acessíveis : \t{ acessible } ")
        print(f"    Atualiza valor da chave : \t{ update } ")
        print(f"  Remove chave corretamente : \t{ remove } ")

    return rehash and acessible and update and remove


def teste(FATORES_CARGA, N_ELEMENTOS, ITERACOES ):
    dt = []
    dt.append(["fator_carga", "n_elementos", "n_testes", "custo_esperado", "comparações (media)", " Diferença (%)"])
    
    # Gera os arrays de teste
    cases = all_possible_combinations(FATOR_ALVO=FATORES_CARGA, N=N_ELEMENTOS, I=ITERACOES)
    for c in cases:
        # Inicializa array
        capacity = int(c["N"] / c["FATOR_ALVO"])+1 
        t = HashTableChained(capacity, load_factor=c["FATOR_ALVO"])
        for i in range( c["N"] ):
            t.put(f"k{i}", f"val{i}")

        # Realiza inserções    
        total = 0
        for i in range(c["I"]):
            k = "NOVA_CHAVE" + f"{random.randrange(c['I'])}"
            total += t.put(k, "VALOR")
            t.delete(k)

        esperado = 1+ t._current_load_factor() /2
        avg = total / c["I"] 
        dif = esperado - avg
        dt.append([f"{t._current_load_factor():.2f}", str(c["N"]), str(c["I"]), f"{esperado:.2f}", f"~{avg:.2f}", f"{(dif*100):.2f}%" ])
    
    print_table(dt)


if __name__ == "__main__":
    teste_funcionalidade(verbose=True)

    FATORES_ALVO = [0.1, 0.25, 0.5, 0.75, 0.9]
    N_ELEMENTOS = [10000]
    ITERACOES = [9999]
    teste(FATORES_ALVO, N_ELEMENTOS, ITERACOES )
    

