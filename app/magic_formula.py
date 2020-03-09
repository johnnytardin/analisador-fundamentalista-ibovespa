from tabulate import tabulate

import magic

def output():
    magic.set_log()
    estrategia, small_caps, numero_empresas, setor = magic.parse_param()
    magic.pl_bolsa()
    rank = magic.rank(estrategia, small_caps, numero_empresas, setor)

    print(
        tabulate(
        rank["data"],
            headers=rank["collumns"],
            tablefmt="orgtbl",
        )
    )


def main():
    print(chr(27) + "[2J")

    output()



if __name__ == "__main__":
    main()
