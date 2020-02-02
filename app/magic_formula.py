import db

ev_ebit = {}
roic = {}

magic_formula = {}

count = 1
for row in db.select_ev_ebit():
    ev_ebit[row[0]] = count
    count += 1


count = 1
for row in db.select_roic():
    roic[row[0]] = count
    count += 1

for code, score in ev_ebit.items():
    magic_formula[code] = score + roic[code]


ordered = {
    k: v
    for k, v in sorted(magic_formula.items(), key=lambda item: item[1], reverse=True)
}

count = 1
for code, score in ordered.items():
    print(f"{count} - {code} - {score}")
    count += 1

    if count == 31:
        break
