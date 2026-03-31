from utils import * 

class NullNode:
    def __len__(self):
        return 0
    
    def _as_array(self):
        return []

    def __str__(self):
        return "[]"

    def find(self, key, depth=0):
        return -1

    def delete(self, key):
        return self

    def insert(self, value):
        return Node(value)

    def delete_at(self, depth):
        raise IndexError("Index out of range")
    def insert_at(self, value, depth):
        raise IndexError("Index out of range")


NULL_NODE = NullNode()

class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node if next_node else NULL_NODE

    def __len__(self):
        return 1 + len(self.next)

    def _as_array(self):
        return [self.value, *self.next._as_array()]
    
    def __str__(self):
        return str(self._as_array())

    def find(self, value, depth=0):
        if self.value == value:
            return depth
        return self.next.find(value, depth=depth+1)

    def delete(self, value):
        if self.value == value:
            return self.next
        self.next = self.next.delete(value)
        return self

    def delete_at(self, depth):
        if depth == 0:
            return self.next
        self.next = self.next.delete_at(depth-1)
        return self

    def insert(self, value):
        self.next = self.next.insert(value)
        return self

    def insert_at(self, value, depth):
        if depth == 0:
            return Node(value, self)
        self.next = self.next.insert_at(value, depth-1)
        return self


class SinglyLinkedList:
    def __init__(self):
        self.head = NULL_NODE
        self._size = 0
    
    # Custo esperado: `O(1)``
    def __len__(self):
        return self._size

    # CUsto esperado: `O(n)`
    def __str__(self):
        return str(self.head)

    # Custo esperado `O(1)`
    def insert_first(self, value):
        self.head = Node(value, self.head)
        self._size += 1

    # Custo esperado `O(n)`
    def insert_last(self, value):
        self.head = self.head.insert(value)
        self._size += 1

    # Custo esperado `O(n)`
    def insert_at(self, index, value):
        self.head = self.head.insert_at(value, index)
       
    # Custo esperado `O(n)`
    def search(self, value):
        return self.head.find(value)

    # Custo esperado `O(n)`
    def delete(self, value):
        self.head = self.head.delete(value)

    # Custo esperado `O(n)`
    def delete_at(self, index):
        self.head = self.head.delete_at(index)

if __name__ == "__main__":

    l = SinglyLinkedList()
    dt = [["Comando", "Lista (após comando)", "Output"]]

    def prt(s, output=""):
        dt.append([s, str(l), output])
        out = f"output=> {output}" if output else "\t"
        # print(f"    {s}\t; \t{out}\t; \tList=> {l}")

    prt(f"Lista criada")

    #  Testando insert 
    l.insert_first(1)
    prt(f"insert_first(1)")
    l.insert_first(0)
    prt(f"insert_first(1)")
    l.insert_last(3)
    prt(f"insert_last(3)")
    l.insert_at(2, 2)
    prt(f"insert_at(2,3)")
    l.insert_at(2, 2)
    prt(f"insert_at(2,3)")
    l.insert_at(0, -1)
    prt(f"insert_at(0, -1)")

    # Testando erros no insert... ")
    try:
        l.insert_at(99, 0)
    except Exception as e:
        prt(f"insert_at(99,3)", e)
    try:
        l.insert_at(-1, 0)
    except Exception as e:
        prt(f"insert_at(-1,3)", e)
        
    # Testando deleção e erros 
    l.delete(-1)
    prt(f"delete(-1)     ")
    l.delete_at(2)
    prt(f"delete_at(2)    ")
    l.delete(999)
    prt(f"delete(999)    ")
    try:
        l.delete_at(10)
    except Exception as e:
        prt(f"delete_at(10)", e)
    try:
        l.delete_at(-1)
    except Exception as e:
        prt(f"delete_at(-1)", e)

    # Testando busca 
    prt(f"search(0)      ", output=l.search(0))
    prt(f"search(1)      ", output=l.search(1))
    prt(f"search(5)      ", output=l.search(5))
    prt(f"search(999)    ", output=l.search(999))

    # Testando outros 
    prt(f"__len__()     ", output=len(l))
    prt(f"__str__()     ", output=str(l))

    print_table(dt)