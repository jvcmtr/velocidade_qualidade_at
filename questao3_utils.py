import random

def aleatorio_com_duplicatas(length, dup_rate):
    if dup_rate > 1 or dup_rate < 0:
        raise Exception("Argumento 'dup_rate' (Duplication rate) deve ser um valor entre 0 e 1")
    
    n_duplicatas = int(length * dup_rate)
    
    if n_duplicatas == length:
        return [0] * length

    max_value = length - (n_duplicatas) 
    arr = [*range(max_value)]
    for i in range(n_duplicatas):
        arr.append(random.randrange(max_value))
    
    random.shuffle(arr)
    return arr