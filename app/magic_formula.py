import db


def get_result():
    ev_ebit, roic, magic_formula = {}, {}, {}

    count = 0
    for row in db.select_ev_ebit():
        ev_ebit[row[0]] = count
        count += 1

    count = 0
    for row in db.select_roic():
        roic[row[0]] = count
        count += 1

    for code, score in ev_ebit.items():
        magic_formula[code] = score + roic[code]

    ordered = {
        k: v
        for k, v in sorted(
            magic_formula.items(), key=lambda item: item[1], reverse=True
        )
    }
    return ordered


def main():
    count = 0
    magic_result = get_result()
    for code, score in magic_result.items():
        print(f"{count} - {code} - {score}")
        count += 1

        if count == 30:
            break


if __name__ == "__main__":
    main()
