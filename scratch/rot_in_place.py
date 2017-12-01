def rotate(s, x):
    i = 0
    c = 0
    l = len(s)
    tmp = s[0]
    while c < l:
        next = (i + x)
        tmp2 = s[next % l]
        s[next % l] = tmp
        tmp = tmp2

        i = next
        if i >= l:
            i = (i % l) + 1

        c += 1

    return s
