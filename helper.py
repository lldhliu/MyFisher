

def is_isbn_or_key(word):
    """
    判断传入参数word是关键字还是isbn
    :param word:
    :return:
    """
    # isbn:
    # isbn13 13个0-9的数字组成
    # isbn10 10个0-9的数字组成  里面含有一些 '-'
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'
    short_word = word.replace('-', '')
    if '-' in word and len(short_word) == 10 and short_word.isdigit():
        isbn_or_key = 'isbn'

    return isbn_or_key
