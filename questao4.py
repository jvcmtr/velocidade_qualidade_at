class NullNode:
    def get(self, key):
        return None

    def find(self, key):
        return None

    def delete(self, key):
        return False

    def put_or_update(self, key, value):
        return Node(key, value), False 

    def as_array(self):
        return []

NULL_NODE = NullNode()

class Node:
    def __init__(self, key, value, next_node=None):
        self.key = key
        self.value = value
        self.next = next_node if next_node else NULL_NODE

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
        "Retorna verdadeiro se um Node foi atualizado"
        if self.key == key:
            self.value = value
            return self, True
        self.next, updated = self.next.put_or_update(key, value)
        return self, updated

    def as_array(self):
        return [self] + self.next.as_array()

class HashTableChained:
    def __init__(self, capacity=8, load_factor=0.75):
        self.size = 0
        self.capacity = capacity
        self.load_factor = load_factor
        self.buckets = [NULL_NODE] * self.capacity

    def _get_bucket_idx(self, key):
        return hash(key) % self.capacity
        
    def _get_bucket(self, key):
        return self.buckets[_get_bucket_id(key)]

    def put(self, key, value):
        b = self._get_bucket(key)
        node, updated = b.put_or_update(key, value)
        if updated:
            return
        
        self.size += 1
        self._try_rehash()

    def get(self, key):
        b = self._get_bucket(key)
        return b.get(key)

    def delete(self, key):
        idx = _get_bucket_idx(key)
        self.buckets[idx] = self.buckets[idx].delete(key)

    def __len__(self):
        return self.size

    def _try_rehash(self):
        if not self.size / self.capacity > self.load_factor:
            return

        nodes = [ x for bucket in self.buckets for x in bucket.as_array()]
        self.__init__(self.capacity*2, self.load_factor)

        for n in nodes:
            if n.key:
                self.put(n.key, n.value)

def teste_funcionalidade(verbose=False):
    INICIAL_LEN = 4
    dt = HashTableChained(initial_capacity=INICIAL_LEN)

    # Insere chaves para forçar rehash
    chaves_valores = { f"CHAVE_{i}":f"VALOR_{i}" for i in range( INICIAL_LEN+10 ) } 
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
    k = "CHAVE NOVA"
    dt.put(k, "VALOR")
    dt.put(k, "OUTRO VALOR")
    update = dt.get(k) == "OUTRO_VALOR"

    # Verifica se uma chave consegue ser devidamente removida
    k = "CHAVE REMOVER"
    dt.put(k, "VALOR_REMOVIDO")
    remove = dt.get(k) == None

    if verbose:
        print(f"             Sofreu rehash  : \t{ rehash }")
        print(f" Todas as chaves acessíveis : \t{ acessible } ")
        print(f"    Atualiza valor da chave : \t{ update } ")
        print(f"  Remove chave corretamente : \t{ remove } ")

    return rehash and acessible and update and remove


if __name__ == "__main__":
    if not teste_funcionalidade(verbose=True):
        return 
    

