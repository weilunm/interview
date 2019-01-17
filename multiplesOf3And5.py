def multiplesOf3And5(n):
    res = 0
    for num in range(1, n):
        if num % 3 == 0 or num % 5 == 0:
            res = res + num
    return res


print(multiplesOf3And5(1000))
