# pub = 03ca5606a1e820e7a2f6bb3ab090e8ade7b04a7e0b5909a68dda2744ae3b8ecbfa
# priv = 23D4A09295BE678B21A5F1DCEAE1F634A69C1B41775F680EBF8165266471401B

pub = '65540419151317157747671900246361345335112119010416684680126380557251106866307'
priv = '535057393045998874059714060903434364160149232400'

# publist = len(pub)
# print(publist)
# pubsplit = pub.split()
# print(pubsplit)


# pub = '91519190036866233587583752863966343541024156557754641198598352460350806215674'

result = 0
for i in pub:
    res = int(i)
    result += res  # Update the result by adding the current digit

print(result)  # Print the final result after the loop


resultpriv = 0
for i in priv:
    res = int(i)
    resultpriv += res

print(resultpriv)