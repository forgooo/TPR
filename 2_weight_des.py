data = [[8, 7, 9, 8],
        [9, 6, 8, 5],
        [7, 8, 7, 7],
        [6, 5, 7, 6],
        [8, 6, 8, 7],
        [7, 6, 8, 9],
        [7, 6, 8, 9]]
weights = [3, 4, 4, 3]  # Веса
ambition = [1, 0, 1, 0]  # Стремление


def compare(a, b):
    p = [weights[i] if data[a][i] > data[b][i] and ambition[i] else
         weights[i] if data[a][i] < data[b][i] and not(ambition[i]) else 0 for i in range(len(weights))]
    n = [weights[i] if p[i] == 0 else 0 for i in range(len(p))]
    print('P{}{}= {} = {};'.format(a + 1, b + 1, " + ".join(str(x) for x in p), sum(p)))
    print('N{}{}= {} = {};'.format(a + 1, b + 1, " + ".join(str(x) for x in n), sum(n)))
    print('D{}{}= P{}{}/N{}{} = {}/{}'
          ' - {}'.format(a + 1, b + 1, a + 1, b + 1,
                         a + 1, b + 1, sum(p), sum(n),'принимаем' if sum(p) >= sum(n) else 'отбрасываем'))
    return None if a > b else compare(b, a)


def main():
    for i in range(len(data)):
        for j in range(i + 1, len(data), 1):
            compare(i, j)


main()
