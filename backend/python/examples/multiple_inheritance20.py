# Multiple Inheritance

class Base1:
    def fun1(self):
        print('Fun1 is executing...')

class Base2:
    def fun2(self):
        print('Fun2 in executing...')

class Base3:
    def fun3(self):
        print('Fun3 is executing...')

class MultiDerived(Base1, Base2, Base3):
    def multiDerived(self):
        print('multiDerived function is executing...')

md1 = MultiDerived()
md1.multiDerived()
md1.fun1()
md1.fun2()
md1.fun3()

