# fibachi code 

def code_fib(x):
    x = int(x)
    seq = []
    res = []
    seq.append(1)
    seq_i = 1
    while seq_i <= x:
        seq.append(seq_i)
        seq_i = seq[-1] + seq[-2]
    seq.reverse()
    res = [0] * len(seq)
    for i in range(len(seq)-1):
        if x >= seq[i]:
            x -= seq[i]
            res[i] = 1
        else:
            res[i] = 0
    print(res)
    
    print(seq)



code_fib(input("Введите число: "))