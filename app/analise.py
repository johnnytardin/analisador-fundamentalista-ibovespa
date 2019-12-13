import db

print("stockCode", "crescimentoCincoAnos", "stockPrice", "valorIntriseco", "score", "desconto", "timestamp")
for row in db.select():
    print('{0:<7} {1:<7} {2:<10} {3:<7} {4:<10} {5:<7} {6:<10}'.format(
        row[0], row[1], row[2], row[3], row[4], row[5], row[6]
        ))