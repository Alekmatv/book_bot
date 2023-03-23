BOOK_PATH: str = 'books/tainstvennyy-ostrov.txt'
PAGE_SIZE: int = 700

book: dict = {}


def _get_part_text(text: str, start: int, page_size: int):
    """Функция делит текст на части
    Возвращает кортеж из текста и длины текста"""

    result = text[start: start + page_size + 1]

    if result[-2:] == '..':
        for i, c in enumerate(result[::-1]):
            if c not in ',.!:;?':
                result = result[:-i]
                break
    else:
        result = text[start: start + page_size]

    if result[-1] not in ',.!:;?':
        for i, c in enumerate(result[::-1]):
            if c in ',.!:;?':
                result = result[:-i]
                break

    return result, len(result)


def prepare_book(path: str) -> None:
    '''Функция формирует словарь со "страницами" книги, не возвращает ничего'''

    with open(path, encoding='utf-8') as file:
        data = file.read()

        start, key = 0, 1

        while True:
            if start < len(data):
                text, length = _get_part_text(data, start, PAGE_SIZE)
                book[key] = text.lstrip()
                key += 1
                start += length
            else:
                break


prepare_book(BOOK_PATH)
