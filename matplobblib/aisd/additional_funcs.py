from ..forall import *
from random import shuffle
from .data_structures import *
#######################################################################################################################
# Дополнительные функции для структур данных
#######################################################################################################################
def AISD_ADD_1(self, key):
    """
    Функция двойного хэширования для использования в хэш-таблицах с открытой адресацией.

    Args:
        self: Экземпляр класса хэш-таблицы, содержащий атрибут `size`.
        key: Ключ, для которого вычисляется вторичный хэш.

    Returns:
        int: Значение шага для пробирования, не равное нулю.
    """
    return 1 + (hash(key) % (self.size-2))
#######################################################################################################################
def AISD_ADD_2(stack):
    """
    Находит первый четный элемент в стеке, не изменяя его.

    Args:
        stack (Stack): Экземпляр класса `Stack`.

    Returns:
        int or None: Первый найденный четный элемент или None, если четных элементов нет.
    """
    current = stack.head
    while current:
        if current.data % 2 == 0:
            return current.data
        current = current.next
    return None
#######################################################################################################################
def AISD_ADD_3(stack):
    """
    Альтернативная функция для нахождения первого четного элемента в стеке.

    Эта функция изменяет стек, извлекая элементы, а затем восстанавливает его.

    Args:
        stack (Stack): Экземпляр класса `Stack`.

    Returns:
        int or None: Первый найденный четный элемент или None, если четных элементов нет.
    """
    temp_stack = Stack()
    even = None

    while not stack.is_empty():
        item = stack.pop()
        temp_stack.push(item)
        if item % 2 == 0:
            even = item
            break

    while not temp_stack.is_empty():
        stack.push(temp_stack.pop())

    return even
#######################################################################################################################
def AISD_ADD_4(stack, item):
    """
    Добавляет новый элемент в стек после первого нечетного элемента.

    Args:
        stack (Stack): Экземпляр класса `Stack`.
        item: Элемент для добавления.
    """
    current = stack.head
    while current:
        if current.data % 2 != 0:
            new_node = Node(item)
            new_node.next = current.next
            current.next = new_node
            return
        current = current.next
    stack.push(item)
#######################################################################################################################
def AISD_ADD_5(expr):
    """
    Проверяет сбалансированность скобок в математическом выражении.

    Args:
        expr (str): Строка с математическим выражением.

    Returns:
        bool: True, если скобки сбалансированы, иначе False.
    """
    stack = Stack()
    for char in expr:
        if char in "({[":
            stack.push(char)
        elif char in ")}]":
            if stack.is_empty():
                return False
            elif char == ")" and stack.peek() == "(":
                stack.pop()
            elif char == "}" and stack.peek() == "{":
                stack.pop()
            elif char == "]" and stack.peek() == "[":
                stack.pop()
            else:
                return False
    return stack.is_empty()
#######################################################################################################################
def AISD_ADD_6(expression):
    """
    Вычисляет математическое выражение в обратной польской нотации (RPN).

    Args:
        expression (list): Список токенов (числа и операторы) в RPN.

    Returns:
        float: Результат вычисления.
    """
    stack = Stack()
    for token in expression:
        if token.isdigit():
            stack.push(int(token))
        else:
            operand_2 = stack.pop()
            operand_1 = stack.pop()
            if token == '+':
                result = operand_1 + operand_2
            elif token == '-':
                result = operand_1 - operand_2
            elif token == '*':
                result = operand_1 * operand_2
            elif token == '/':
                result = operand_1 / operand_2
            stack.push(result)
    return stack.pop()
#######################################################################################################################
def AISD_ADD_7(queue):
    """
    Находит первый нечетный элемент в очереди, не изменяя ее.

    Args:
        queue (Queue): Экземпляр класса `Queue`.

    Returns:
        int or None: Первый найденный нечетный элемент или None, если таких нет.
    """
    current = queue.head
    while current:
        if current.data % 2 != 0:
            return current.data
        current = current.next
    return None
#######################################################################################################################
def AISD_ADD_8(queue, item):
    """
    Добавляет новый элемент в очередь перед первым четным элементом.

    Args:
        queue (Queue): Экземпляр класса `Queue`.
        item: Элемент для добавления.
    """
    new_node = Node(item)
    if not queue.head:
        queue.head = new_node
        queue.tail = new_node
    elif queue.head.data % 2 == 0:
        new_node.next = queue.head
        queue.head = new_node
    else:
        prev_node = queue.head
        current = prev_node.next
        while current:
            if current.data % 2 == 0:
                prev_node.next = new_node
                new_node.next = current
                return
            prev_node = current
            current = current.next
        queue.tail.next = new_node
        queue.tail = new_node
#######################################################################################################################
def AISD_ADD_9(queue, data):
    """
    Альтернативная функция для добавления нового элемента в очередь перед первым четным элементом.

    Args:
        queue (Queue): Экземпляр класса `Queue`.
        data: Элемент для добавления.
    """
    temp_queue = Queue()
    even_found = False

    while not queue.is_empty():
        item = queue.dequeue()
        if item % 2 == 0 and not even_found:
            temp_queue.enqueue(data)
            even_found = True
        temp_queue.enqueue(item)

    while not temp_queue.is_empty():
        queue.enqueue(temp_queue.dequeue())
#######################################################################################################################
def AISD_ADD_10(dllist):
    """
    Удваивает каждый четный элемент в двусвязном списке, добавляя его копию после него.

    Args:
        dllist (DoublyLinkedList): Экземпляр двусвязного списка.
    """
    current_node = dllist.head
    while current_node:
        if current_node.data % 2 == 0:
            new_node = Node(current_node.data)
            new_node.next = current_node.next
            new_node.prev = current_node
            if current_node.next:
                current_node.next.prev = new_node
            current_node.next = new_node
            current_node = new_node.next
        else:
            current_node = current_node.next
#######################################################################################################################
def AISD_ADD_11(dllist):
    """
    Удаляет все отрицательные элементы из двусвязного списка.

    Args:
        dllist (DoublyLinkedList): Экземпляр двусвязного списка.
    """
    current_node = dllist.head
    while current_node:
        if current_node.data < 0:
            if current_node.prev:
                current_node.prev.next = current_node.next
            else:
                dllist.head = current_node.next
            if current_node.next:
                current_node.next.prev = current_node.prev
        current_node = current_node.next
#######################################################################################################################
def AISD_ADD_12(cdllist):
    """
    Возводит в квадрат все отрицательные элементы в циклическом двусвязном списке.

    Args:
        cdllist (CircularDoublyLinkedList): Экземпляр циклического двусвязного списка.
    """
    current_node = cdllist.head
    while current_node:
        if current_node.data < 0:
            current_node.data = current_node.data ** 2
        current_node = current_node.next
        if current_node == cdllist.head:
            break
#######################################################################################################################
def AISD_ADD_13(cdllist):
    """
    Удаляет все элементы, кратные 5, из циклического двусвязного списка.

    Args:
        cdllist (CircularDoublyLinkedList): Экземпляр циклического двусвязного списка.
    """
    current_node = cdllist.head
    while current_node:
        if current_node.data % 5 == 0:
            cdllist.delete(current_node.data)
        current_node = current_node.next
        if current_node == cdllist.head:
            break
#######################################################################################################################
def AISD_ADD_14(levels):
    """
    Создает случайное бинарное дерево заданной глубины.

    Args:
        levels (int): Глубина создаваемого дерева.

    Returns:
        Tree: Экземпляр класса `Tree` со случайными значениями.
    """
    tree = Tree()
    nodes = 2**(levels+1) - 1
    values = list(range(1,nodes+1))
    shuffle(values)

    for i in range(nodes):
        value = values[i]
        if i == 0:
            tree.add_node(value)
        else:
            parent_index = (i-1)//2
            parent_value = values[parent_index]
            tree.add_node(value, parent_value)

    return tree
#######################################################################################################################
def AISD_ADD_15(tree, node=None):
    """
    Заменяет значение каждого узла в дереве на сумму значений всех его потомков.

    Args:
        tree (Tree): Экземпляр дерева.
        node (TreeNode, optional): Текущий узел для обработки. Defaults to `tree.root`.

    Returns:
        int: Сумма значений потомков для текущего узла.
    """
    if node is None:
        node = tree.root
    if not node.children:
        return node.value
    else:
        sum_of_children = 0
        for child in node.children:
            sum_of_children += AISD_ADD_15(tree, child)
        node.value = sum_of_children
        return sum_of_children
#######################################################################################################################
def AISD_ADD_16(tree, node=None):
    """
    Удваивает значение каждого нечетного узла в дереве.

    Args:
        tree (Tree): Экземпляр дерева.
        node (TreeNode, optional): Текущий узел для обработки. Defaults to `tree.root`.

    Returns:
        Tree: Модифицированное дерево.
    """
    if node is None:
        node = tree.root
    if node.value % 2 == 1:
        node.value *= 2
    for child in node.children:
        AISD_ADD_16(tree, child)
    return tree
#######################################################################################################################
def AISD_ADD_17(tree, node=None, leaves=None):
    """
    Находит все листья (конечные узлы) в дереве.

    Args:
        tree (Tree): Экземпляр дерева.
        node (TreeNode, optional): Текущий узел для обработки. Defaults to `tree.root`.
        leaves (list, optional): Список для сбора листьев. Defaults to None.

    Returns:
        list: Список значений всех листьев дерева.
    """
    if leaves is None:
        leaves = []
    if node is None:
        node = tree.root
    if len(node.children) == 0:
        leaves.append(node.value)
    else:
        for child in node.children:
            AISD_ADD_17(tree, child, leaves)
    return leaves
#######################################################################################################################
def AISD_ADD_18(node):
    """
    Рекурсивно находит количество узлов в бинарном дереве.

    Args:
        node (BinaryTreeNode): Корневой узел дерева или поддерева.

    Returns:
        int: Общее количество узлов.
    """
    if node is None:
        return 0
    return 1 + AISD_ADD_18(node.left) + AISD_ADD_18(node.right)
#######################################################################################################################
def AISD_ADD_19(node, target_node):
    """
    Находит путь от корня до заданного узла в бинарном дереве.

    Args:
        node (BinaryTreeNode): Текущий узел для поиска.
        target_node (BinaryTreeNode): Целевой узел.

    Returns:
        list: Список значений узлов на пути от корня до целевого узла.
    """
    if node is None:
        return []
    if node.left == target_node or node.right == target_node:
        return [node.data]
    left = AISD_ADD_19(node.left, target_node)
    right = AISD_ADD_19(node.right, target_node)
    if left:
        return [node.data] + left
    elif right:
        return [node.data] + right
    else:
        return []
#######################################################################################################################
def AISD_ADD_20(node, value):
    """
    Находит все узлы в бинарном дереве, значение которых больше или равно заданному.

    Args:
        node (BinaryTreeNode): Текущий узел для поиска.
        value: Значение для сравнения.

    Returns:
        list: Список значений узлов, удовлетворяющих условию.
    """
    if node is None:
        return []
    result = []
    if node.data >= value:
        result.append(node.data)
    result += AISD_ADD_20(node.left, value)
    result += AISD_ADD_20(node.right, value)
    return result
#######################################################################################################################
def AISD_ADD_21(hash_table):
    """
    Находит наиболее часто встречающееся значение в хэш-таблице по полю `species`.

    Args:
        hash_table (HashTableChaining): Экземпляр хэш-таблицы, где значениями являются объекты с атрибутом `species`.

    Returns:
        object: Наиболее часто встречающееся значение `species`.
    """
    species_count = {}
    for slot in hash_table.table:
        for _, animal in slot:
            if animal.species in species_count:
                species_count[animal.species] += 1
            else:
                species_count[animal.species] = 1
    return max(species_count, key=species_count.get)
#######################################################################################################################
AISD_ADD = [
    AISD_ADD_1,
    AISD_ADD_2,
    AISD_ADD_3,
    AISD_ADD_4,
    AISD_ADD_5,
    AISD_ADD_6,
    AISD_ADD_7,
    AISD_ADD_8,
    AISD_ADD_9,
    AISD_ADD_10,
    AISD_ADD_11,
    AISD_ADD_12,
    AISD_ADD_13,
    AISD_ADD_14,
    AISD_ADD_15,
    AISD_ADD_16,
    AISD_ADD_17,
    AISD_ADD_18,
    AISD_ADD_19,
    AISD_ADD_20,
    AISD_ADD_21,
]
