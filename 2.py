a = [[8, 7, 9, 8],
     [9, 6, 8, 5],
     [7, 8, 7, 7],
     [6, 5, 7, 6],
     [8, 6, 8, 7],
     [7, 6, 8, 9],
     [7, 6, 8, 9]]
size = 7
b = [' x '] * size

c = [3, 4, 4, 3]

for i in range(size):
    b[i] = [' x '] * size

countdominant = 0
countdominanted = 0

res = []
for i in range(size):
    for m in range(i + 1, size):
        for j in range(4):
            if j == 0 or j == 1:
                if a[i][j] < a[m][j]:
                    countdominant += c[j]
                elif a[i][j] > a[m][j]:
                    countdominanted += c[j]
            else:
                if a[i][j] > a[m][j]:
                    countdominant += c[j]
                elif a[i][j] < a[m][j]:
                    countdominanted += c[j]
        if countdominant != 0 and countdominanted == 0:
            b[i][m] = 'inf'
            b[m][i] = ' - '
        elif countdominant == 0 and countdominanted != 0:
            b[m][i] = 'inf'
            b[i][m] = ' - '
        else:
            if countdominanted == 0:
                b[i][m] = ' - '
                b[m][i] = ' - '
            elif countdominant / countdominanted == 1:
                b[i][m] = ' - '
                b[m][i] = ' - '
            elif countdominant / countdominanted < 1:
                b[i][m] = ' - '
                b[m][i] = str(round(countdominanted / countdominant, 2))
            else:
                b[i][m] = str(round(countdominant / countdominanted, 2))
                b[m][i] = ' - '
        countdominant = 0
        countdominanted = 0

# Выравнивание
max_length = max(len(str(x)) for row in b for x in row)

# Вывод
for row in b:
    print(" ".join(str(x).rjust(max_length) for x in row))

# Определяем, сколько раз каждая альтернатива входит в другие альтернативы
alternative_counts = [0] * size

for i in range(size):
    for j in range(size):
        if b[i][j] == ' - ':
            alternative_counts[i] += 1

# Сортировка по количеству вхождений
sorted_alternatives = sorted(range(len(alternative_counts)), key=lambda k: alternative_counts[k])

print("\nBest alternatives:")
for i in range(size):
    if i == 0:
        print(f"Alternative {sorted_alternatives[i] + 1}", end="")
    else:
        print(f" -> Alternative {sorted_alternatives[i] + 1}", end="")
print()
