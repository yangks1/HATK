def divide(num):
    is_prime = 1
    for i in range(2, int(num**0.5+1)):
        if num%i == 0:
            is_prime = 0
            print(str(i),end=" ")
            divide(int(num/i))
            break
    if is_prime == 1:
        print(str(num), end=' ')
divide(180)
