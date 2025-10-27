from collections import Counter
from typing import Optional, Iterable, Sequence
from pathlib import Path
import re
import csv
def min_max (nums: list[float | int]) -> tuple[float | int, float | int]:
    if len(nums) == 0: return ValueError
    return (min(nums), max(nums))

def unique_sorted (nums: list[float | int]) -> list[float | int]:
    return sorted(list(set(nums)))

def flatten(mat: list[list | tuple]) -> list:
    st = set()
    for i in mat:
        if type(i) == list or type(i) == tuple:
            for j in i:
                if type(j) == int or type(j) == float:
                    st.add(j)
                else: return TypeError
        else: return TypeError
    return list(st)

def check_rectangular(mat: list[list[float | int]]) -> bool:
    if not mat:
        return True
    row_len = len(mat[0])
    for row in mat:
        if len(row) != row_len:
            return False
    return True

def transpose(mat: list[list[float | int]]) -> list | ValueError:
    if not mat:
        return []
    if check_rectangular(mat):
        return [list(col) for col in zip(*mat)]
    return ValueError("Матрица рваная (строки разной длины)")

def row_sums(mat: list[list[float | int]]) -> list[int] | list[float] | ValueError:
    if not mat:
        return []
    if check_rectangular(mat):
        return [sum(row) for row in mat]
    return ValueError("Матрица рваная (строки разной длины)")

def col_sums(mat: list[list[float | int]]) -> list[int] | list[float] | ValueError:
    if not mat:
        return []
    if check_rectangular(mat):
        return [sum(col) for col in zip(*mat)]
    return ValueError("Матрица рваная (строки разной длины)")

def format_record(rec: tuple[str, str, float]) -> str:

    if not isinstance(rec, tuple) or len(rec) != 3:
        raise TypeError("rec должен быть кортежем из 3 элементов (ФИО, группа, GPA)")
    if not isinstance(rec[0], str):
        raise TypeError("ФИО должно быть строкой")
    if not isinstance(rec[1], str):
        raise TypeError("Группа должна быть строкой")
    if not isinstance(rec[2], (int, float)):
        raise TypeError("GPA должно быть числом int или float")

    s = rec[0].split()
    
    if len(s) == 3:
        return f'{s[0].capitalize()} {s[1][0].upper()}.{s[2][0].upper()}., гр. {rec[1]}, GPA {rec[2]:.2f}'
    elif len(s) == 2:
        return f'{s[0].capitalize()} {s[1][0].upper()}., гр. {rec[1]}, GPA {rec[2]:.2f}'
    else:
        raise ValueError('Неверный формат ФИО')
    
def normalize (text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if yo2e == True:
        text = text.replace('Ё','Е').replace('ё','е')
    if casefold == True:
        text = text.casefold()
    for spaces in ['\t', '\r', '\n']:
        text = text.replace(spaces,' ')
    words = text.split()
    text = ' '.join(words)
    return text

def tokenize(text: str) -> list[str]:
    simv = r'\b[а-яёa-zA-Z0-9_]+(?:-[а-яёa-zA-Z0-9_]+)*\b'
    return re.findall(simv,text)

def count_freq(tokens: list[str], top_n: Optional[int] = None) -> dict[str, int]:
    counter = Counter(tokens)
    if top_n is not None:
        return dict(counter.most_common(top_n))
    return dict(counter)

def table(text: str, n: int = 5):
    print(f'Всего слов: {len(tokenize(normalize(text)))}')
    print(f'Уникальных слов: {len(set(tokenize(normalize(text))))}')
    print('Топ-5:')
    text = count_freq(tokenize(normalize(text)))
    item = dict(list(text.items())[:n])
    for keys, values in item.items():
        print(f"{keys}: {values}")
    print ('')
    print("слово        | частота")
    print("----------------------")
    for keys, values in item.items():
        print(f"{keys:<12} | {values}")


def write_csv(rows: Iterable[Sequence], path: str | Path,
              header: tuple[str, ...] | None = None) -> None:
    object = Path(path)
    rows = list(rows)
    for index in range(1, len(rows)):
        if len(rows[index-1]) != len(rows[index]):
            return ValueError
    if object.suffix == ".csv":
        p = Path(path)
        rows = list(rows)
        with p.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if header is not None:
                w.writerow(header)
            for r in rows:
                w.writerow(r)
        return "Успешная обработка"
    else:
        return "Неверный формат файла"

def write_any_text(rows: Iterable[Sequence], path: str | Path,
              header: tuple[str, ...] | None = None) -> None:
    p = Path(path)
    rows = list(rows)
    for index in range(1, len(rows)):
        if len(rows[index-1]) != len(rows[index]):
            return ValueError
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if header is not None:
            if len(header) == len(rows[0]):
                w.writerow(header)
            else:
                return "Ошибка"
        for r in rows:
            w.writerow(r)

def read_text (path : str|Path , encoding: str = 'utf-8') -> str:
    p = Path(path)
    try:
        return p.read_text(encoding=encoding)
    except FileNotFoundError:
        return 'Файл не найден'
    except UnicodeDecodeError:
        return 'Ошибка кодировки'