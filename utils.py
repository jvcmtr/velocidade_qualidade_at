
def print_table(arr):
    BUFFER = 1
    col_width = {x:0 for x in range(len(arr[0]))}
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

def save_table(arr, path):
    data = "\n".join(
        [", ".join([str(a).strip() for a in x]) for x in arr]
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(data)

def troca(arr, a, b):
    val = arr[a]
    arr[a] = arr[b]
    arr[b] = val