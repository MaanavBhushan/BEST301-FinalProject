from quote import quote

for i in range(100):
    res = quote('Greta Thunberg')
    print(str(i) + " " + res[i]['quote'])

