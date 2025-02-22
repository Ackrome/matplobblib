text1 = '''
# Стек через связный список
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def push(self, item):
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node

    def pop(self):
        if self.is_empty():
            return None
        else:
            popped_item = self.head.data
            self.head = self.head.next
            return popped_item

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.head.data

    def __str__(self):
        current = self.head
        stack_str = ""
        while current:
            stack_str += str(current.data) + " → "
            current = current.next
        return stack_str.rstrip(" → ")

# Очередь через связный список
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return not bool(self.head)

    def enqueue(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self):
        data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return data

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        current = self.head
        queue_str = ""
        while current:
            queue_str += " → " + str(current.data)
            current = current.next
        return queue_str.lstrip(" → ")
'''+'abracadabrabibidi' +'''
# Двусвязнйы список
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
            new_node.prev = current

    def delete_node(self, data):
        if self.head is None:
            return
        elif self.head.data == data:
            if self.head.next is not None:
                self.head = self.head.next
                self.head.prev = None
            else:
                self.head = None
        else:
            current = self.head
            while current.next is not None and current.next.data != data:
                current = current.next
            if current.next is None:
                return
            else:
                current.next = current.next.next
                if current.next is not None:
                    current.next.prev = current

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        if self.head == None:
            return f"Двусвязный список пустой"
        current = self.head
        dllist_str = ""
        while current:
            dllist_str += " ⇄ " + str(current.data)
            current = current.next
        return dllist_str.lstrip(" ⇄ ")
'''+'abracadabrabibidi' +'''
# Цикличный двусвязный список
class Node:
    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None

class CircularDoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            new_node.prev = self.tail
            new_node.next = self.head
        else:
            new_node.prev = self.tail
            new_node.next = self.head
            self.tail.next = new_node
            self.head.prev = new_node
            self.tail = new_node

    def prepend(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            new_node.prev = self.tail
            new_node.next = self.head
        else:
            new_node.prev = self.tail
            new_node.next = self.head
            self.head.prev = new_node
            self.tail.next = new_node
            self.head = new_node

    def delete(self, key):
        current_node = self.head
        while current_node:
            if current_node.data == key:
                if current_node == self.head:
                    self.head = current_node.next
                    self.tail.next = self.head
                    self.head.prev = self.tail
                elif current_node == self.tail:
                    self.tail = current_node.prev
                    self.head.prev = self.tail
                    self.tail.next = self.head
                else:
                    current_node.prev.next = current_node.next
                    current_node.next.prev = current_node.prev
                return
            current_node = current_node.next

    def __len__(self):
        count = 0
        current_node = self.head
        while current_node:
            count += 1
            current_node = current_node.next
            if current_node == self.head:
                break
        return count

    def __str__(self):
        cdllist_str = ""
        current_node = self.head
        while current_node:
            cdllist_str += str(current_node.data) + " ⇄ "
            current_node = current_node.next
            if current_node == self.head:
                break
        return " ⇄ " + cdllist_str
'''+'abracadabrabibidi' +'''
# Дерево
class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

class Tree:
    def __init__(self):
        self.root = None

    def add_node(self, value, parent_value=None):
        node = Node(value)
        if parent_value is None:
            if self.root is not None:
                raise ValueError("У дерева уже есть корень")
            self.root = node
        else:
            parent_node = self.find_node(parent_value)
            if parent_node is None:
                raise ValueError("Родительский узел не найден")
            parent_node.children.append(node)

    def find_node(self, value):
        return self._find_node(value, self.root)

    def _find_node(self, value, node):
        if node is None:
            return None
        if node.value == value:
            return node
        for child in node.children:
            found = self._find_node(value, child)
            if found is not None:
                return found
        return None

    def __str__(self):
        return self._str_tree(self.root)

    def _str_tree(self, node, indent=0):
        result = "  " * indent + str(node.value) + "\n"
        for child in node.children:
            result += self._str_tree(child, indent + 2)
        return result
'''+'abracadabrabibidi' +'''
# Бинарное дерево
class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        new_node = Node(data)
        if self.root is None:
            self.root = new_node
        else:
            current = self.root
            while True:
                if data < current.data:
                    if current.left is None:
                        current.left = new_node
                        break
                    else:
                        current = current.left
                else:
                    if current.right is None:
                        current.right = new_node
                        break
                    else:
                        current = current.right

    def search(self, data):
        current = self.root
        while current is not None:
            if data == current.data:
                return True
            elif data < current.data:
                current = current.left
            else:
                current = current.right
        return False

    def delete(self, data):
        if self.root is not None:
            self.root = self._delete(data, self.root)

    def _delete(self, data, node):
        if node is None:
            return node

        if data < node.data:
            node.left = self._delete(data, node.left)
        elif data > node.data:
            node.right = self._delete(data, node.right)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self._find_min_node(node.right)
            node.data = temp.data
            node.right = self._delete(temp.data, node.right)

        return node

    def _find_min_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def __str__(self):
        return '\n'.join(self._display(self.root)[0])

    def _display(self, node):
        if node.right is None and node.left is None:
            line = str(node.data)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        if node.right is None:
            lines, n, p, x = self._display(node.left)
            s = str(node.data)
            u = len(s)
            first_line = (x + 1)*' ' + (n - x - 1)*'_' + s
            second_line = x*' ' + '/' + (n - x - 1 + u)*' '
            shifted_lines = [line + u*' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        if node.left is None:
            lines, n, p, x = self._display(node.right)
            s = str(node.data)
            u = len(s)
            first_line = s + x*'_' + (n - x)*' '
            second_line = (u + x)*' ' + '\\' + (n - x - 1)*' '
            shifted_lines = [u*' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        left, n, p, x = self._display(node.left)
        right, m, q, y = self._display(node.right)
        s = str(node.data)
        u = len(s)
        first_line = (x + 1)*' ' + (n - x - 1)*'_' + s + y*'_' + (m - y)*' '
        second_line = x*' ' + '/' + (n - x - 1 + u + y)*' ' + '\\' + (m - y - 1)*' '
        if p < q:
            left += [n*' ']*(q - p)
        elif q < p:
            right += [m*' ']*(p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u*' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2
'''+'abracadabrabibidi' +'''
# Хэш-таблица методом цеполк (когда данные с одинаковыми ключами хранятся в виде списка)
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        slot = self.hash_function(key)
        for pair in self.table[slot]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[slot].append([key, value])

    def find(self, key):
        slot = self.hash_function(key)
        for pair in self.table[slot]:
            if pair[0] == key:
                return pair[1]
        return None
'''+'abracadabrabibidi' +'''
# Хэш-таблица методом открытой адресации
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        while self.table[index]:
            if self.table[index][0] == key:
                break
            index = (index + 1) % self.size
        self.table[index] = (key, value)

    def find(self, key):
        index = self.hash_function(key)
        while self.table[index]:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.size
        return None
'''+'abracadabrabibidi' +'''
# Двоичная куча
class BinaryHeap():

    def __init__(self, type='max'):
        #type can be 'max' or 'min'
        
        self.type = type
        self.data = []
    
    
    def buildHeap(self, arr):
        data = arr[::]
        n = len(data)
        for i in range(n, -1, -1):
            data = self.heapify(data, n, i)
        
        self.data = data

    
    def heapify(self, arr, n, i):
        f = True if self.type=='max' else False
        extra = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and ((arr[i] < arr[l] and f) or (arr[i] > arr[l] and not f)):
            extra = l

        if r < n and ((arr[extra] < arr[r] and f) or (arr[extra] > arr[r] and not f)):
            extra = r

        if extra != i:
            arr[i], arr[extra] = arr[extra], arr[i]

            return self.heapify(arr, n, extra)
        else:
            return arr
    
    
    def insert(self, data):
        self.data.append(data)
        self.buildHeap(self.data)
        
    
    def sorted(self) -> list:
        data = self.data[::]
        n = len(data)

        for i in range(n-1, 0, -1):
            data[i], data[0] = data[0], data[i]
            data = self.heapify(data, i, 0)
            
        return data

    
    def del_root(self):
        root = self.data.pop(0)
        return root
''' + 'abracadabrabibidi' + '''
# Базовый декоратор
def decorator_name(func, decorator_args=None):
    def wrapper(*args, **kwargs): # Параметры, которые хотите передать в функцию func
        
        print('BEFORE') # То, что выполнится ДО функции
        rez = func(*args, **kwargs)
        print('AFTER') # То, что выполнится ПОСЛЕ функции
        
        return rez
        
    return wrapper
''' + 'abracadabrabibidi' + '''
# Очередь с приоритетом
class PriorityQueue:
    def __init__(self):
        self.heap = BinaryHeap()

    def enqueue(self, item, priority):
        self.heap.insert((priority, item))

    def dequeue(self):
        return self.heap.delMin()[1]

    def __str__(self):
        return self.heap.__str__()
''' + 'abracadabrabibidi' + '''
# Очередь через двусвязный список
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return not bool(self.head)

    def enqueue(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self):
        data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return data

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        current = self.head
        queue_str = ""
        while current:
            queue_str += " → " + str(current.data)
            current = current.next
        return queue_str.lstrip(" → ")
'''
