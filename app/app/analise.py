import db

for row in db.select():
    print(
        u"stockCode: {0:<7} \n"
        u"  setor: {1} \n"
        u"  score: {5:.2f} \n"
        u"  crescimentoCincoAnos: {2:.2f}% \n"
        u"  stockPrice: R$ {3:.2f} \n"
        u"  valorIntriseco: R$ {4:.2f} \n"
        u"  percentualDesconto: {6:.2f}% \n"
        u"  desconto: R$ {7:.2f} \n"
        u"  dividendos: {8:.2f}% \n"
        u"  timestamp: {9:<10}".format(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7],
            row[8],
            row[9],
        )
    )
