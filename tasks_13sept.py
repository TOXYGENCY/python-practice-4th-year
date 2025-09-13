import math

# задача 3
def task3():
    n = int(input()) # ввод числа n
    results = [] # массив с результатами

    for number in range(1, n):
        digits = list(str(number))
        apply = True  # применяется ли условие задачи

        # если 0 - то сразу не подходит
        if "0" in digits:
            apply = False
            continue
        else:
            # проход деления по всем цифрам числа
            for d in digits:
                d = int(d)
                if number % d != 0:
                    apply = False
                    break
        # Проверка на условие
        if apply:
            results.append(number)
            print(f"{number} подходит.")

    print(results)

# Проверка на простое число
def is_simple(num):
    simple = True
    
    for i in range(2, num-1):
        if num % i == 0:
            simple = False
            continue
    
    return simple


# задача 4
def task4():
    n_min = 101
    n_max = 1000
    results = []

    for i in range(n_min, n_max, 2):
        if is_simple(i):
            results.append(i)
    print("Все трехзначные натуральные числа:", results)

# Определение является ли число числом армстронга
def is_armstrong(num):
    digits = list(str(num))
    n = len(digits)
    sum = 0

    for d in digits:
        sum += int(d)**n

    return sum == int(num)


# задача 6
def task6():
    k = int(input())
    results = []

    for i in range(1, k):
        if is_armstrong(i):
            results.append(i)

    print("Числа Армстронга: ", results)

# Проверка можно ли составить треугольник из трех отрезков с указанной длиной
def F(a,b,c):
    if a+b>=c and a+c>=b and b+c>=a:
        return True
    else:
        return False

# задача 7
def task7():
    a, b, c, d = int(input("a = ")), int(input("b = ")), int(input("c = ")), int(input("d = "))
    if F(a,b,c) or F(a,b,d) or F(a,d,c) or F(d,b,c):
        print("YES")
    else:
        print("NO")

# задача 8
def task8():
    a, b, c = int(input("a = ")), int(input("b = ")), int(input("c = "))
    if math.cos(a/b) < 0 or math.cos(b/c) < 0 or math.cos(a/c) < 0:
        print("Да, один из углов треугольника тупой.")
    else:
        print("Нет, не могут являться сторонами тупоугольного треугольника")
