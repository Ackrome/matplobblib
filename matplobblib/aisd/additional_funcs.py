from ..forall import *
from random import shuffle
from .data_structures import *
#######################################################################################################################
# Дополнительные функции для структур данных
#######################################################################################################################
def AISD_ADD_1(self, key):
    """Функция двойного хэширования"""
    return 1 + (hash(key) % (self.size-2))
#######################################################################################################################
def AISD_ADD_2(stack):
    """Функция для нахождения первого четного элемента в стеке"""
    current = stack.head
    while current:
        if current.data % 2 == 0:
            return current.data
        current = current.next
    return None
#######################################################################################################################
def AISD_ADD_3(stack):
    """Альтернативная функция для нахождения первого четного элемента в стеке"""
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
    """Функция для добавления нового элемента в стек после первого нечетного элемента"""
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
    """Функция для проверки сбалансированности скобок в математическом выражении"""
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
    """Функция для вычисления математических выражений в обратной польской нотации"""
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
    """Функция для нахождения первого нечетного элемента очереди"""
    current = queue.head
    while current:
        if current.data % 2 != 0:
            return current.data
        current = current.next
    return None
#######################################################################################################################
def AISD_ADD_8(queue, item):
    """Функция для добавления нового элемента в очередь перед первым четным элементом"""
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
    """Альтернативная функция для добавления нового элемента в очередь перед первым четным элементом"""
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
    """Функция для удвоения каждого четного элемента двусвязного списка"""
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
    """Функция для удаления всех отрицательных элементов из двусвязного списка"""
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
    """Функция, возводящая в квадрат все отрицательные элементы в циклическом двусвязном списке"""
    current_node = cdllist.head
    while current_node:
        if current_node.data < 0:
            current_node.data = current_node.data ** 2
        current_node = current_node.next
        if current_node == cdllist.head:
            break
#######################################################################################################################
def AISD_ADD_13(cdllist):
    """Функция для удаления всех элементов из циклического двусвязного списка, кратных 5"""
    current_node = cdllist.head
    while current_node:
        if current_node.data % 5 == 0:
            cdllist.delete(current_node.data)
        current_node = current_node.next
        if current_node == cdllist.head:
            break
#######################################################################################################################
def AISD_ADD_14(levels):
    """Функция для создания случайного дерева заданной глубины (каждый узел имеет два дочерних узла)"""
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
    """Функция для замены каждого числа в дереве на сумму чисел всех его потомков"""
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
    """Функция, удваивающая каждое нечетное число в дереве"""
    if node is None:
        node = tree.root
    if node.value % 2 == 1:
        node.value *= 2
    for child in node.children:
        AISD_ADD_16(tree, child)
    return tree
#######################################################################################################################
def AISD_ADD_17(tree, node=None, leaves=None):
    """Функция для определения листьев дерева"""
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
    """Функция для нахождения количества узлов в бинарном дереве"""
    if node is None:
        return 0
    return 1 + AISD_ADD_18(node.left) + AISD_ADD_18(node.right)
#######################################################################################################################
def AISD_ADD_19(node, target_node):
    """Функция для нахождения всех узлов, которые являются родительскими для заданного узла в бинарном дереве"""
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
    """Функция для нахождения всех узлов, которые имеют значение больше или равно заданному значению в бинарном дереве"""
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
    """Функция для нахождения наиболее часто встречающегося значения в хеш-таблице (по полю species)"""
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
