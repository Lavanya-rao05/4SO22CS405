import http.client
import random

URL = "http://20.244.56.144/test/numbers/{numberid}"

#prime numbers
def is_prime(n):
    if n == 1:
        print("nor prime nor composite")
    elif n > 1:
        for i in range(2, n):
            if n % i == 0:
                print("not prime")
                break
        else:
            print("prime")
    else:
        print("not prime")

# fibonacci series
def fibanocci(n):
    count = 0
    a,b = 0,1
    while n > count:
        print(a, end=" ")
        a,b = b,a+b
        count += 1
n = int(input())
print(fibanocci(10))
    
# even or odd
def even_numbers(n):
    return n % 2 == 0
even_numbers(n)
        
def random_number(window_size, l, u):
    for i in range(window_size):
        return [random.randint(l, u)]

        
window_size = 10

qualified_numbers = (URL, window_size)

for number, qualifications in qualified_numbers:
    print(f"Number: {number}, Qualifications: {qualifications}")
