from math import sqrt


def valor_intriseco(lpa, vpa):
    if lpa >= 0 and vpa >= 0:
        return sqrt(22.5 * lpa * vpa)
    return 0
