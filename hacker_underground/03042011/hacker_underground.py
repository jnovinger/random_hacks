file = open('puzzle.txt')

while 1:
    line = file.readline()
    if not line:
        break
    lines = line.split(', ')
    lines.sort()
    prev_line = 0
    for line in lines:
        if line == prev_line:
            print line
            break
        else:
            prev_line = line
