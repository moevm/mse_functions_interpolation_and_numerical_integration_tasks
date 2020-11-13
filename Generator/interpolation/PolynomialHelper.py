from .Polynomial import Polynomial

class PolynomialHelper:
    @staticmethod
    def generatePolynomial(degree):
        if type(degree) == int and 3 <= degree <= 6:
            return Polynomial(degree)
        else:
            return None
