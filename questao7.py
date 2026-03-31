from utils import *

class NullNode:
	def __init__(self):
		self.value = None

	def __len__(self):
		return 0

	def __str__(self):
		return "[]"

	def _as_array(self):
		return []

	def is_null(self):
		return True


NULL_NODE = NullNode()


class Node:
	def __init__(self, value, prev=None, next_node=None):
		self.value = value
		self.prev = prev if prev else NULL_NODE
		self.next = next_node if next_node else NULL_NODE

	def is_null(self):
		return False
	
	def __len__(self):
		return 1 + len(self.next)

	def _as_array(self):
		return [self.value, *self.next._as_array()]
	
	def __str__(self):
		return str(self._as_array())


class DoublyLinkedList:

	def __init__(self):
		self.head = NULL_NODE
		self.tail = NULL_NODE
		self._size = 0

    # O(1)
	def __len__(self):
		return self._size

    # O(1)
	def is_empty(self):
		return self._size == 0

    # O(n)
	def __str__(self):
		if self.is_empty():
			return str([])
		return str(self.head)

    # O(1)
	def insert_first(self, value):
		new_node = Node(value, NULL_NODE, self.head)

		if self.is_empty():
			self.tail = new_node
		else:
			self.head.prev = new_node

		self.head = new_node
		self._size += 1
	
    # O(1)
	def insert_last(self, value):
		new_node = Node(value, self.tail, NULL_NODE)

		if self.is_empty():
			self.head = new_node
		else:
			self.tail.next = new_node

		self.tail = new_node
		self._size += 1

    # O(1)
	def delete_first(self):
		if self.is_empty():
			return

		removed = self.head.value
		self.head = self.head.next

		if self.head != NULL_NODE:
			self.head.prev = NULL_NODE
		else:
			self.tail = NULL_NODE

		self._size -= 1
		return removed

    # O(1)
	def delete_last(self):
		if self.is_empty():
			return

		removed = self.tail.value
		self.tail = self.tail.prev

		if self.tail != NULL_NODE:
			self.tail.next = NULL_NODE
		else:
			self.head = NULL_NODE

		self._size -= 1
		return removed

    # O(n)
	def check_invariants(self):
		count = 0
		curr = self.head
		prev = NULL_NODE

		while curr != NULL_NODE:
			if curr.prev != prev:
				return "NODE", n

			prev = curr
			curr = curr.next
			count += 1

		if prev != self.tail and not self.is_empty():
			return "TAIL", prev

		if count != self._size:
			return "COUNT", count



class Deque:
	def __init__(self):
		self.lst = DoublyLinkedList()
    
    # O(1)
	def __len__(self):
		return len(self.lst)

    # O(1)
	def is_empty(self):
		return self.lst.is_empty()

    # O(1)
	def insert_left(self, value):
		self.lst.insert_first(value)

    # O(1)
	def insert_right(self, value):
		self.lst.insert_last(value)

    # O(1)
	def remove_left(self):
		return self.lst.delete_first()

    # O(1)
	def remove_right(self):
		return self.lst.delete_last()

    # O(1)
	def peek_left(self):
		return self.lst.head.value

    # O(1)
	def peek_right(self):
		return self.lst.tail.value

    # O(n)
	def __str__(self):
		return str(self.lst)




def test_list():
	print("Iniciando teste com DoublyLinkedList()")
	dt = [["Comando", "Lista (após comando)", "Output", "Inconsistencia"]]

	def prt(s, output=""):
		dt.append([s, str(l), output, l.check_invariants() or "nenhuma encontrada"])

	l = DoublyLinkedList()
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

	prt(f"__len__()", output=len(l))
	prt(f"__str__()", output=str(l))

	print_table(dt)


def test_deque():
	print("Iniciando teste com Deque()")
	dt = [["Comando", "Deque", "Output", "Inconsistencia"]]

	def prt(cmd, output=""):
		dt.append([cmd, str(q), output, q.lst.check_invariants() or "nenhuma encontrada"])

	q = Deque()
	prt("Deque criado")

	# Inserções alternadas
	q.insert_left(1)
	prt("insert_left(1)")
	q.insert_right(2)
	prt("insert_right(2)")
	q.insert_left(0)
	prt("insert_left(0)")
	q.insert_right(3)
	prt("insert_right(3)")

	# Remoções alternadas
	prt("remove_left()", q.remove_left())
	prt("remove_right()", q.remove_right())

	# Mais operações
	q.insert_left(-1)
	prt("insert_left(-1)")
	q.insert_right(4)
	prt("insert_right(4)")
	prt("peek_left()", q.peek_left())
	prt("peek_right()", q.peek_right())
	
	print_table(dt)

if __name__ == "__main__":
    test_list()
    test_deque()