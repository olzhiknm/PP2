#1
def squaregenerator(N):
    for i in range(N + 1):
        yield i ** 2

N = int(input())
for square in squaregenerator(N):
    print(square, end=" ")
  #2
def evennumbers(n):
    for i in range(0, n + 1, 2):
        yield i

n = int(input())
print(",".join(map(str, even_numbers(n))))
#3
def divby3and4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

n = int(input())
for num in divby3and4(n):
    print(num, end=" ")
#4
def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2
a, b = map(int, input("a and b: ").split())
for sq in squares(a, b):
    print(sq)
#5
def countdown(n):
    while n >= 0:
        yield n
        n -= 1
n = int(input())
for num in countdown(n):
    print(num, end=" ")



