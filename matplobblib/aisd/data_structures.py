#######################################################################################################################
# Базовые структуры данных
#######################################################################################################################

# Узел для односвязных списков (Стек, Очередь)
class Node:
    """Узел для односвязного списка."""
    def __init__(self, data):
        self.data = data
        self.next = None

# Стек через связный список
class Stack:
    """Реализация стека на основе односвязного списка."""
    def __init__(self):
        """Инициализирует пустой стек."""
        self.head = None

    def is_empty(self):
        """Проверяет, пуст ли стек.

        Returns:
            bool: True, если стек пуст, иначе False.
        """
        return self.head is None

    def push(self, item):
        """Добавляет элемент на вершину стека.

        Args:
            item: Элемент для добавления.
        """
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node

    def pop(self):
        """Удаляет и возвращает элемент с вершины стека.

        Returns:
            Элемент с вершины стека или None, если стек пуст.
        """
        if self.is_empty():
            return None
        else:
            popped_item = self.head.data
            self.head = self.head.next
            return popped_item

    def peek(self):
        """Возвращает элемент с вершины стека, не удаляя его.

        Returns:
            Элемент с вершины стека или None, если стек пуст.
        """
        if self.is_empty():
            return None
        else:
            return self.head.data

    def __str__(self):
        """Возвращает строковое представление стека."""
        current = self.head
        stack_str = ""
        while current:
            stack_str += str(current.data) + " → "
            current = current.next
        return stack_str.rstrip(" → ")

# Очередь через связный список
class Queue:
    """Реализация очереди на основе односвязного списка."""
    def __init__(self):
        """Инициализирует пустую очередь."""
        self.head = None
        self.tail = None

    def is_empty(self):
        """Проверяет, пуста ли очередь.

        Returns:
            bool: True, если очередь пуста, иначе False.
        """
        return not bool(self.head)

    def enqueue(self, data):
        """Добавляет элемент в конец очереди.

        Args:
            data: Элемент для добавления.
        """
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self):
        """Удаляет и возвращает элемент из начала очереди.

        Returns:
            Элемент из начала очереди.
        """
        data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return data

    def __len__(self):
        """Возвращает количество элементов в очереди."""
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        """Возвращает строковое представление очереди."""
        current = self.head
        queue_str = ""
        while current:
            queue_str += " → " + str(current.data)
            current = current.next
        return queue_str.lstrip(" → ")

# Узел для двусвязных списков
class DLLNode:
    """Узел для двусвязного списка."""
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

# Двусвязный список
class DoublyLinkedList:
    """Реализация двусвязного списка."""
    def __init__(self):
        """Инициализирует пустой двусвязный список."""
        self.head = None

    def add_node(self, data):
        """Добавляет узел в конец списка.

        Args:
            data: Данные для нового узла.
        """
        new_node = DLLNode(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
            new_node.prev = current

    def delete_node(self, data):
        """Удаляет узел с заданными данными.

        Args:
            data: Данные узла для удаления.
        """
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
        """Возвращает количество элементов в списке."""
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        """Возвращает строковое представление списка."""
        if self.head == None:
            return "Двусвязный список пустой"
        current = self.head
        dllist_str = ""
        while current:
            dllist_str += " ⇄ " + str(current.data)
            current = current.next
        return dllist_str.lstrip(" ⇄ ")

# Циклический двусвязный список
class CircularDoublyLinkedList:
    """Реализация циклического двусвязного списка."""
    def __init__(self):
        """Инициализирует пустой циклический двусвязный список."""
        self.head = None
        self.tail = None

    def append(self, data):
        """Добавляет элемент в конец списка.

        Args:
            data: Элемент для добавления.
        """
        new_node = DLLNode(data)
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
        """Добавляет элемент в начало списка.

        Args:
            data: Элемент для добавления.
        """
        new_node = DLLNode(data)
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
        """Удаляет узел по значению.

        Args:
            key: Значение узла для удаления.
        """
        if self.head is None:
            return

        current_node = self.head
        while True:
            if current_node.data == key:
                if self.head == self.tail:
                    self.head = None
                    self.tail = None
                elif current_node == self.head:
                    self.head = self.head.next
                    self.tail.next = self.head
                    self.head.prev = self.tail
                elif current_node == self.tail:
                    self.tail = self.tail.prev
                    self.head.prev = self.tail
                    self.tail.next = self.head
                else:
                    current_node.prev.next = current_node.next
                    current_node.next.prev = current_node.prev
                return
            current_node = current_node.next
            if current_node == self.head:
                break

    def __len__(self):
        """Возвращает количество элементов в списке."""
        if not self.head:
            return 0
        count = 0
        current_node = self.head
        while True:
            count += 1
            current_node = current_node.next
            if current_node == self.head:
                break
        return count

    def __str__(self):
        """Возвращает строковое представление списка."""
        if not self.head:
            return "⇄"
        cdllist_str = ""
        current_node = self.head
        while True:
            cdllist_str += str(current_node.data) + " ⇄ "
            current_node = current_node.next
            if current_node == self.head:
                break
        return "⇄ " + cdllist_str

# Узел для дерева
class TreeNode:
    """Узел для общего дерева."""
    def __init__(self, value):
        self.value = value
        self.children = []

# Дерево
class Tree:
    """Реализация общего дерева."""
    def __init__(self):
        """Инициализирует пустое дерево."""
        self.root = None

    def add_node(self, value, parent_value=None):
        """Добавляет узел в дерево.

        Args:
            value: Значение нового узла.
            parent_value (optional): Значение родительского узла. Defaults to None.
        
        Raises:
            ValueError: Если корень уже существует при добавлении нового корня.
            ValueError: Если родительский узел не найден.
        """
        node = TreeNode(value)
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
        """Находит узел по значению.

        Args:
            value: Значение для поиска.

        Returns:
            TreeNode: Найденный узел или None.
        """
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
        """Возвращает строковое представление дерева."""
        if self.root is None:
            return "Дерево пустое"
        return self._str_tree(self.root)

    def _str_tree(self, node, indent=0):
        result = "  " * indent + str(node.value) + "\n"
        for child in node.children:
            result += self._str_tree(child, indent + 2)
        return result

# Узел для бинарного дерева
class BinaryTreeNode:
    """Узел для бинарного дерева."""
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

# Бинарное дерево
class BinaryTree:
    """Реализация бинарного дерева поиска."""
    def __init__(self):
        """Инициализирует пустое бинарное дерево."""
        self.root = None

    def insert(self, data):
        """Вставляет элемент в дерево.

        Args:
            data: Элемент для вставки.
        """
        new_node = BinaryTreeNode(data)
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
        """Ищет элемент в дереве.

        Args:
            data: Элемент для поиска.

        Returns:
            bool: True, если элемент найден, иначе False.
        """
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
        """Удаляет элемент из дерева.

        Args:
            data: Элемент для удаления.
        """
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
        """Возвращает строковое представление дерева для вывода в консоль."""
        if self.root is None:
            return "Бинарное дерево пустое"
        return '\n'.join(self._display(self.root)[0])

    def _display(self, node):
        if node is None:
            return [], 0, 0, 0
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

# Хэш-таблица методом цепочек
class HashTableChaining:
    """Реализация хэш-таблицы методом цепочек."""
    def __init__(self, size):
        """Инициализирует хэш-таблицу.

        Args:
            size (int): Размер таблицы.
        """
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        """Вычисляет хэш для ключа.

        Args:
            key: Ключ.

        Returns:
            int: Хэш-значение.
        """
        return hash(key) % self.size

    def insert(self, key, value):
        """Вставляет пару ключ-значение.

        Args:
            key: Ключ.
            value: Значение.
        """
        slot = self.hash_function(key)
        for pair in self.table[slot]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[slot].append([key, value])

    def find(self, key):
        """Находит значение по ключу.

        Args:
            key: Ключ для поиска.

        Returns:
            Значение, связанное с ключом, или None, если ключ не найден.
        """
        slot = self.hash_function(key)
        for pair in self.table[slot]:
            if pair[0] == key:
                return pair[1]
        return None

# Хэш-таблица методом открытой адресации
class HashTableOpenAddressing:
    """Реализация хэш-таблицы методом открытой адресации (линейное пробирование)."""
    def __init__(self, size):
        """Инициализирует хэш-таблицу.

        Args:
            size (int): Размер таблицы.
        """
        self.size = size
        self.table = [None] * size

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        """Вставляет пару ключ-значение.

        Args:
            key: Ключ.
            value: Значение.
        """
        index = self.hash_function(key)
        while self.table[index] is not None:
            if self.table[index][0] == key:
                break
            index = (index + 1) % self.size
        self.table[index] = (key, value)

    def find(self, key):
        """Находит значение по ключу.

        Args:
            key: Ключ для поиска.

        Returns:
            Значение, связанное с ключом, или None, если ключ не найден.
        """
        index = self.hash_function(key)
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.size
        return None

# Двоичная куча
class BinaryHeap:
    """Реализация двоичной кучи (min-heap или max-heap)."""
    def __init__(self, type='max'):
        """Инициализирует кучу.

        Args:
            type (str, optional): Тип кучи ('max' или 'min'). Defaults to 'max'.
        """
        self.type = type
        self.data = []

    def buildHeap(self, arr):
        """Строит кучу из массива.

        Args:
            arr (list): Массив для построения кучи.
        """
        data = arr[:]
        n = len(data)
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(data, n, i)
        self.data = data

    def heapify(self, arr, n, i):
        """Поддерживает свойство кучи для поддерева с корнем в узле i.

        Args:
            arr (list): Массив.
            n (int): Размер кучи.
            i (int): Индекс корня поддерева.
        """
        f = True if self.type == 'max' else False
        extra = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and ((arr[i] < arr[l] and f) or (arr[i] > arr[l] and not f)):
            extra = l

        if r < n and ((arr[extra] < arr[r] and f) or (arr[extra] > arr[r] and not f)):
            extra = r

        if extra != i:
            arr[i], arr[extra] = arr[extra], arr[i]
            self.heapify(arr, n, extra)

    def insert(self, item):
        """Вставляет новый элемент в кучу.

        Args:
            item: Элемент для вставки.
        """
        self.data.append(item)
        i = len(self.data) - 1
        parent = (i - 1) // 2
        f = True if self.type == 'max' else False
        while i > 0 and ((self.data[parent] < self.data[i] and f) or (self.data[parent] > self.data[i] and not f)):
            self.data[parent], self.data[i] = self.data[i], self.data[parent]
            i = parent
            parent = (i - 1) // 2

    def sorted(self) -> list:
        """Возвращает отсортированный массив (Heapsort).

        Returns:
            list: Отсортированный список элементов.
        """
        temp_arr = self.data[:]
        n = len(temp_arr)
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(temp_arr, n, i)
        for i in range(n-1, 0, -1):
            temp_arr[i], temp_arr[0] = temp_arr[0], temp_arr[i]
            self.heapify(temp_arr, i, 0)
        if self.type == 'max':
            return temp_arr
        else:
            return temp_arr[::-1]

    def del_root(self):
        """Удаляет и возвращает корневой элемент.

        Returns:
            Корневой элемент.
        """
        if not self.data:
            return None
        root = self.data[0]
        last_val = self.data.pop()
        if self.data:
            self.data[0] = last_val
            self.heapify(self.data, len(self.data), 0)
        return root

# Базовый декоратор
def decorator_name(func, decorator_args=None):
    """Пример базового декоратора.

    Args:
        func (function): Функция для декорирования.
        decorator_args (optional): Аргументы для декоратора. Defaults to None.

    Returns:
        function: обернутая функция.
    """
    def wrapper(*args, **kwargs): # Параметры, которые хотите передать в функцию func
        print('BEFORE') # То, что выполнится ДО функции
        rez = func(*args, **kwargs)
        print('AFTER') # То, что выполнится ПОСЛЕ функции
        return rez
    return wrapper

# Очередь с приоритетом
class PriorityQueue:
    """Реализация очереди с приоритетом на основе двоичной кучи."""
    def __init__(self):
        """Инициализирует пустую очередь с приоритетом (min-priority)."""
        self.heap = BinaryHeap(type='min')

    def enqueue(self, item, priority):
        """Добавляет элемент с приоритетом в очередь.

        Args:
            item: Элемент.
            priority: Приоритет элемента (меньшее значение - выше приоритет).
        """
        self.heap.insert((priority, item))

    def dequeue(self):
        """Удаляет и возвращает элемент с наивысшим приоритетом.

        Returns:
            Элемент с наивысшим приоритетом.
        """
        priority, item = self.heap.del_root()
        return item

    def __str__(self):
        """Возвращает строковое представление очереди."""
        return str(self.heap.data)

#######################################################################################################################
# Список классов структур данных
#######################################################################################################################
AISD_DS = [
    Stack,
    Queue,
    DoublyLinkedList,
    CircularDoublyLinkedList,
    Tree,
    BinaryTree,
    HashTableChaining,
    HashTableOpenAddressing,
    BinaryHeap,
    PriorityQueue,
]
