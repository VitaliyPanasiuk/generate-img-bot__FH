a = ['0','1','2','3','4','5','6','7','8','9','10']

for i in range(len(a[2:])):
    if i % 3 == 0:
        print(a[2:][i])
        print(a[2:][i+1])
        print(a[2:][i+2])