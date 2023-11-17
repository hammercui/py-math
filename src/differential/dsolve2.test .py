import sympy as sy
t = sy.Symbol('t')
x = sy.Symbol('x')
m = sy.integrate(sy.sin(t)/(sy.pi-t),(t,0,x))
n = sy.integrate(m,(x,0,sy.pi))
print(n)


