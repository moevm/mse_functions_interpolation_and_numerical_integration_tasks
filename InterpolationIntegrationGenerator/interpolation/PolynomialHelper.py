from .Polynomial import Polynomial

class PolynomialHelper:
    @staticmethod
    def generatePolynomial(degree, seed=None):
        if type(degree) == int and 3 <= degree <= 6 \
                and ((type(seed) == int and 0 <= seed <= 2**32 - 1) or (seed is None)):
            return Polynomial(degree, seed)
        else:
            return None
