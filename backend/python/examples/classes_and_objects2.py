class MyComplexNumber:
    # constructor method
    def __init__(self, real, imag):
        print('My Complex Number Constructor Executing...')
        self.real_part = real
        self.imag_part = imag
    
    def displayComplex(self):
        print('{0} + {1}j'.format(self.real_part, self.imag_part))

cmplx1 = MyComplexNumber(40, 50)
cmplx1.displayComplex()

cmplx2 = MyComplexNumber(10, 20)
cmplx2.my_property = 30
print(cmplx2, cmplx2.real_part, cmplx2.my_property)