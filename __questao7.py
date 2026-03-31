from utils import * 

#####################################################################
#                                       NOTA AO CORRETOR:
#       A notação `before` utilizada nos metodos da classe Node pode ser dificil de se acompanhar
#       em um primeiro contato. Eu recomendo a seguinte abstração (assumindo que before é sempre True):
#                                   
#              get_node(before)       -> retorna o node anterior, ou seja `self.next`
#              set_node(not before)   -> seta o node NÃO anterior, ou seja, `self.prev`
#
#####################################################################

class NullNode:
    def __init__(self):
        self.value = None
        self.next = None
        self.prev = None


    def __len__(self):
        return 0

    def _get_node(self, before=False):
        return self

    def _set_node(self, val, before=False):
        if before:
            self.prev = val
        else:
            self.next = val
    
    def _as_array(self, reverse=True):
        return []

    def __str__(self):
        return "[]"

    def find(self, key, depth=0):
        return -1

    def delete(self, key, reverse_direction=False):
        return self

    def insert(self, value, reverse_direction=False):
        print(f"insert({value}) : NULL")
        node = Node(value)

        return Node


NULL_NODE = NullNode()

class Node:
    def __init__(self, value, next_node=None, prev_node=None, before=False):
        self.value = value

        self.next = next_node if next_node else NULL_NODE
        self.prev = prev_node if prev_node else NULL_NODE

        if before:
            self.next, self.prev = self.prev, self.next

    def _get_node(self, before=False):
        """retorna o proximo node (next). Se BEFORE for True retorna o Node anterior (prev) """
        return self.prev if before else self.next
    
    def _set_node(self, node, before=False):
        """seta o valor do proximo node (next). Se BEFORE for True seta o Node anterior (prev) """
        if before:
            self.prev = node
        else:
            self.next = node

    def __len__(self):
        return 1 + len(self.next)

    def _as_array(self, forward=None):
        if forward == None:
            return [*self._get_node(True)._as_array(False) ,self.value, *self._get_node(False)._as_array(True)]
        if forward == True:

            # print(self.value, self.__class__)
            return [self.value, *self._get_node(False)._as_array(True)]
        if forward == False:
            return [*self._get_node(True)._as_array(False) ,self.value]

    def __str__(self):
        return str(self._as_array())

    def find(self, value, depth=0, before=False):
        if self.value == value:
            return depth if not before else -depth
        return self._get_node(before).find(value, depth=depth+1, )

    def delete(self, reverse_direction=False):
        before = reverse_direction

        nex = self._get_node(not before)
        prev = self._get_node(before)

        nex._set_node(prev, before)
        prev._set_node(nex, not before)

        return prev
    
    def insert(self, value, reverse_direction=False):
        print(f"insert({value}) : ", self.value)
        before = reverse_direction


        node = Node(value, prev_node=self._get_node(before), next_node=self, before=before)

        self._get_node(before)._set_node(node, not before)
        self._set_node(node, before)
        print(f"    {node.prev.value} - {node.value} -  {node.next.value}")
        print(f"    {self.prev.value} - {self.value} -  {self.next.value}")
        print(f"    {self.next.prev.value} - {self.next.value} -  {self.next.next.value}")
        return node

class DoublyLinkedList:
    def __init__(self):
        self.head = NULL_NODE 
        self.tail = NULL_NODE
        self._size = 0
    
    # Custo esperado: `O(1)``
    def __len__(self):
        return self._size

    # Custo esperado: `O(n)`
    def __str__(self):
        return str(self.head)

    # Custo esperado `O(1)`
    def insert_first(self, value):
        self.head = self.head.insert(value, reverse_direction=False)
        self._size += 1

    # Custo esperado `O(1)`
    def insert_last(self, value):
        self.tail = self.tail.insert(value, reverse_direction=True)
        self._size += 1
   
    # Custo esperado `O(1)`
    def delete_first(self):
        self.head = self.head.delete(reverse_direction=False)
        self._size -= 1

    # Custo esperado `O(1)`
    def delete_last(self):
        self.head = self.head.delete(reverse_direction=True)
        self._size -= 1

    # Custo esperado `O(n)`
    def search(self, value):
        return self.head.find(value)


if __name__ == "__main__":

    l = DoublyLinkedList()
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
    prt(f"insert_first(0)")
    l.insert_last(3)
    prt(f"insert_last(3)")
    l.insert_last(4)
    prt(f"insert_last(4)")

    l.delete_last()
    prt(f"delete_last()")
    l.delete_first()
    prt(f"delete_first()")

    prt(f"__len__()     ", output=len(l))
    prt(f"__str__()     ", output=str(l))

    print_table(dt)