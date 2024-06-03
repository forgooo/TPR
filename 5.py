from fractions import Fraction
from dataclasses import dataclass
from itertools import chain

# Класс для представления переменной в линейном программировании
@dataclass(frozen=True)
class Variable:
    a: Fraction  # Коэффициент переменной
    name: str     # Имя переменной

    def __str__(self):  # Метод для строкового представления переменной
        return self.name

# Класс для представления таблицы в линейном программировании
@dataclass(frozen=True)
class Table:
    body: tuple[tuple[Fraction, ...], ...]  # Тело таблицы (матрица значений)
    cols: tuple[Variable, ...]              # Переменные-столбцы таблицы
    rows: tuple[Variable, ...]              # Переменные-строки таблицы

    # Метод для вывода таблицы
    def out(self):
        print('\nTable:')  # Заголовок таблицы
        print('', '', *(col.a for col in self.cols), sep='\t')  # Значения переменных-столбцов
        print('', '', *(col.name for col in self.cols), sep='\t')  # Имена переменных-столбцов
        for rw, row in zip(chain(self.rows, (None,)), self.body):
            print(('' if rw is None else rw.a), ('' if rw is None else rw.name), *row, sep='\t')  # Строки таблицы
        print()  # Пустая строка для разделения таблиц

# Функция для вычисления последнего элемента строки таблицы
def last_row_el(table: Table, i, ia: Fraction):
    ans = ia  # Начальное значение
    for (row, rw) in zip(table.body, table.rows):
        ans += row[i] * rw.a  # Вычисление значения
    return ans  # Возврат значения

# Функция для вычисления последней строки таблицы
def last_row(table: Table) -> tuple[Fraction, ...]:
    return tuple((last_row_el(table, i, -cw.a) for (i, cw) in enumerate(table.cols)))  # Возврат последней строки

# Функция для получения ключевой переменной и значения для строки таблицы
def get_krv(row, key_col) -> (Fraction, Fraction):
    key_val = row[key_col]  # Значение ключевой переменной
    last_val = row[-1]      # Последнее значение строки
    return (Fraction(last_val, key_val) if key_val > 0 else float('inf')), key_val  # Возврат кортежа (значение, ключ)

# Функция для вычисления значения элемента таблицы
def get_num(table: Table, key_col: int, key_row: int, i: int, j: int) -> Fraction:
    if i == key_row:  # Если строка является ключевой
        if j == key_col:  # Если столбец является ключевым
            return Fraction(1)  # Возвращаем 1
        return table.body[i][j]  # Возвращаем значение элемента таблицы
    if j == key_col:  # Если столбец является ключевым
        return -table.body[i][j]  # Возвращаем отрицательное значение элемента таблицы
    # Возвращаем результат операции над элементами таблицы для вычисления нового значения
    return table.body[i][j] * table.body[key_row][key_col] - table.body[i][key_col] * table.body[key_row][j]

# Функция для решения внутренней задачи линейного программирования
def solve_inner(prob: Table):
    assert len(prob.body) == len(prob.rows)  # Проверка соответствия размеров тела и строк таблицы
    table = Table(prob.body + (last_row(prob),), prob.cols, prob.rows)  # Добавление последней строки к таблице
    table.out()  # Вывод начальной таблицы
    while True:  # Цикл решения
        assert last_row(table) == table.body[-1]  # Проверка соответствия последней строки и последнего элемента тела
        # Поиск ключевой переменной и столбца
        key_cv, key_col = min(((val, col) for (col, val) in enumerate(table.body[-1][:-1])))
        if key_cv >= 0:  # Если значение ключевой переменной неотрицательно
            break  # Выход из цикла
        # Поиск ключевой строки и значения
        (_, key_val), key_row = min(((get_krv(row, key_col), i) for (i, row) in enumerate(table.body[:-1])))
        # Построение новой таблицы на основе найденных значений
        table = Table(
            tuple((
                tuple((
                    Fraction(get_num(table, key_col, key_row, i, j), key_val)  # Вычисление нового значения элемента
                    for j in range(len(table.cols))  # Проход по столбцам
                ))
                for i in range(len(table.rows) + 1)  # Проход по строкам
            )),
            tuple((
                cv if col != key_col else table.rows[key_row] for (col, cv) in enumerate(table.cols)
            )),
            tuple((
                rv if row != key_row else table.cols[key_col] for (row, rv) in enumerate(table.rows)
            ))
        )
        print(key_val)
        table.out()  # Вывод промежуточной таблицы

    ans = {}  # Словарь для хранения ответа
    # Заполнение словаря ответа
    for rv, row in zip(table.rows, table.body):
        if rv.name != "-1":  # Исключение переменной "-1" из вывода
            ans[rv] = row[-1]
    for cv in table.cols:  # Заполнение нулями значений для колонок
        ans[cv] = Fraction(0)
    return ans  # Возвращение ответа

# Функция для решения внешней задачи линейного программирования
def solve_outer(a1m: tuple[tuple[Fraction, ...], ...], a0: tuple[Fraction, ...], c: tuple[Fraction, ...]):
    # Вызов функции решения внутренней задачи с формированием внутренней таблицы
    ans = solve_inner(Table(
        tuple((ai + (a0i,) for (ai, a0i) in zip(a1m, a0))),
        tuple((Variable(ci, f"X{i + 1}") for (i, ci) in enumerate(c))) +
        (Variable(Fraction(0), "X7"),),
        tuple((Variable(Fraction(0), f"X{i + len(a1m) + 1}") for i in range(len(a0))))
    ))
    print("\nSolution:")  # Вывод заголовка для решения
    # Вывод решения
    k=0
    for var, val in sorted(ans.items(), key=lambda x: x[0].name):
        if var.name == "X4" and k<1:
            k+=1
            print(f"{var} = {val}")
        if var.name != "-1" and var.name != "X4":  # Исключение переменной "-1" из вывода
            print(f"{var} = {val}")

def main():
    solve_outer(  # Вызов функции решения внешней задачи
        (
            (Fraction(5), Fraction(20)),  # Матрица A1m
            (Fraction(10), Fraction(15)),  # Матрица A1m
            (Fraction(1, 2), Fraction(3, 10)),  # Применение точных дробей
            (Fraction(1), Fraction(2))   # Матрица A1m
        ),
        (Fraction(400), Fraction(450), Fraction(25), Fraction(300)),  # Вектор a0
        (Fraction(20), Fraction(50))  # Вектор c
    )

if __name__ == '__main__':
    main()
