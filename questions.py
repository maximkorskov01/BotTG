import json


quiz_data = [
    {
        'question': 'Что такое Python?',
        'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
        'correct_option': 0
    },
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'natural'],
        'correct_option': 0
    },
    {
        'question': 'Как создать пустой список в Python?',
        'options': ['list()', '[]', 'new list', 'create list()'],
        'correct_option': 1
    },
    {
        'question': 'Какой оператор используется для деления без остатка?',
        'options': ['/', '//', '%', 'div'],
        'correct_option': 1
    },
    {
        'question': 'Что такое декоратор в Python?',
        'options': ['Специальный синтаксис для изменения поведения функций', 'Тип данных', 'Метод класса', 'Ключевое слово'],
        'correct_option': 0
    },
    {
        'question': 'Какой метод используется для добавления элемента в конец списка?',
        'options': ['add()', 'append()', 'push()', 'insert()'],
        'correct_option': 1
    },
    {
        'question': 'Что такое None в Python?',
        'options': ['Специальное значение, обозначающее отсутствие значения', 'Тип данных', 'Ключевое слово', 'Функция'],
        'correct_option': 0
    },
    {
        'question': 'Какой оператор используется для проверки принадлежности элемента множеству?',
        'options': ['in', 'contains', 'is', 'has'],
        'correct_option': 0
    },
    {
        'question': 'Что такое генератор в Python?',
        'options': ['Специальный тип функции, создающий последовательность значений', 'Тип данных', 'Метод', 'Ключевое слово'],
        'correct_option': 0
    },
    {
        'question': 'Какой метод используется для удаления элемента из множества?',
        'options': ['remove()', 'delete()', 'pop()', 'clear()'],
        'correct_option': 0
    },
    {
        'question': 'Что такое кортеж в Python?',
        'options': ['Неизменяемая последовательность элементов', 'Изменяемый список', 'Тип данных для хранения ключей', 'Функция'],
        'correct_option': 0
    },
    {
        'question': 'Какой оператор используется для возведения в степень?',
        'options': ['^', '**', '@', 'pow()'],
        'correct_option': 1
    },
    {
        'question': 'Что такое словарь в Python?',
        'options': ['Структура данных для хранения пар ключ-значение', 'Тип данных для хранения чисел', 'Метод', 'Функция'],
        'correct_option': 0
    },
    {
        'question': 'Какой метод используется для получения длины последовательности?',
        'options': ['length()', 'size()', 'len()', 'count()'],
        'correct_option': 2
    },
    {
        'question': 'Что такое исключение в Python?',
        'options': ['Ошибка, возникающая во время выполнения программы', 'Тип данных', 'Метод', 'Ключевое слово'],
        'correct_option': 0
    }
]




with open('C:\\Users\\MSI Note\\BotTG\\BotTG\\questions.json', 'w', encoding='utf-8') as f:
    json.dump(quiz_data, f, ensure_ascii=False, indent=4)

