def balde2(x):
    n=x[0]
    for i in x:
        if i>n:
            n=i

    b =[0 for _ in range (n+1)]

    for i in range(len(x)):
        b[x[i]] = b[x[i]]+1

    x=[]


    for i in range(len(b)):
        if i>0:
            for j in range(b[i]):
                x.append(i)
    return x

print(balde2([2,5,8,1,4,9,2,3,7,8]))