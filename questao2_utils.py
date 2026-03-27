import random

def troca(arr, a, b):
    val = arr[a]
    arr[a] = arr[b]
    arr[b] = val

def ordenado(n_elementos):
    return([*range(1, n_elementos+1)])

def reverso(n_elementos):
    return ordenado(n_elementos)[::-1]

def semiordenado(n_elementos, n_trocas=None ):
    if(n_trocas==None):
        n_trocas = int(0.05 * n_elementos)
    
    arr = ordenado(n_elementos)
    for i in range(n_trocas):
        pos1 = random.randrange(n_elementos)
        pos2 = random.randrange(n_elementos)
        troca(arr, pos1, pos2)
    return arr

def aleatorio(n_elementos):
    arr = []
    for i in range(n_elementos):
        arr.append(random.randrange(n_elementos*2))
    return arr


def get_test_cases(algoritimos):
    TAMANHOS=[100]#0, 10_000 25_000, 50_000, 100_000]
    GERADORES=[ordenado, reverso, semiordenado, aleatorio]
    
    cases = []
    for t in TAMANHOS:
        for a in algoritimos:
            for g in GERADORES:
                cases.append({"size":t, "type":g.__name__, "data":g(t), "algorithm" : a})
    return cases


def print_table(arr):
    BUFFER = 1
    col_width = {x:0 for x in range(len(arr))}
    columns = range(len(arr[0]))

    for row in arr:
        for col_id in columns:
            if col_width[col_id] < len(row[col_id]):
                col_width[col_id] = len(row[col_id])

    def print_line(columns, start, fill, dividers, end, contents=None):
        buff = fill * BUFFER
         
        cells = []
        for col in columns:
            s = contents[col] if contents else ""
            offset = fill * (col_width[col] - len(s))
            cells.append(s + offset)
    
        separators = buff + dividers + buff
        columns = separators.join(cells)

        print(start + buff + columns + buff + end)

    print_line(columns,"┌", "─", "┬", "┐") 
    for ln in arr:
        print_line(columns, "│", " ", "│", "│",  ln)
        if ln != arr[-1]:
            print_line(columns,"├", "─", "┼", "┤" )
    print_line(columns, "└", "─", "┴", "┘")

