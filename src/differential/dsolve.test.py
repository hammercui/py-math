import sympy as sy
x=sy.symbols('x')#约定变量x
y=x**3+10+sy.sin(x)#这个sin是sy的sin
dy_dx=sy.diff(y,x)#常微分，写成dy_dx=sy.diff(y)也可以
t=sy.symbols('t')
z=x*sy.ln(t)+t**4
dz_dt=sy.diff(z,t)#偏微分
print(dz_dt)
print(dy_dx)
print(dy_dx.subs({x:5}))#把x=5代入
print(dy_dx.subs({x:5}).n(10))#转浮点，总位数为10
