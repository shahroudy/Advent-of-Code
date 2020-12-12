from myutils.file_reader import read_str_list
import re


def get_seat_number1(board_code: str):
    return int(re.sub('B|R', '1', re.sub('F|L', '0', board_code)), 2)


def get_seat_number2(board_code):
    n = 0
    char_list = list(board_code)
    for c in char_list:
        if c.lower() in ['b', 'r']:
            n = n + 1
        elif c.lower() in ['f', 'l']:
            pass
        else:
            raise Exception('Invalid boarding code')
        n = n * 2
    n = n // 2
    return n


def test_answers():
    assert get_seat_number1('RRL') == 6
    assert get_seat_number1('BFRRL') == 22
    assert get_seat_number1('BFFFBBFRRR') == 567
    assert get_seat_number1('FFFBBBFRRR') == 119
    assert get_seat_number1('BBFFBBFRLL') == 820
    assert get_seat_number2('BFFFBBFRRR') == 567
    assert get_seat_number2('FFFBBBFRRR') == 119
    assert get_seat_number2('BBFFBBFRLL') == 820


if __name__ == '__main__':

    test_answers()

    passes = read_str_list('input.txt')

    minn = pow(2, 20)
    maxn = 0
    seats = set()

    for p in passes:
        n = get_seat_number2(p)
        maxn = max(maxn, n)
        minn = min(minn, n)
        seats.add(n)

    print(maxn, set(list(range(minn, maxn+1))) - seats)
