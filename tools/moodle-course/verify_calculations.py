"""Independent exact-arithmetic checks of selected source problems and model optima.
Run with Python 3 and SymPy. This checks economics separately from the renderer.
"""
from fractions import Fraction as F
import sympy as s
Q=s.symbols('Q', real=True)
checks=[]
def check(name,actual,expected):
    assert s.simplify(actual-expected)==0,(name,actual,expected)
    checks.append(name)
def optimum(name,price,cost,expected_q,expected_profit):
    profit=s.expand(price*Q-cost)
    check(name+' stationary',s.diff(profit,Q).subs(Q,expected_q),0)
    assert s.diff(profit,Q,2).subs(Q,expected_q)<0
    check(name+' profit',profit.subs(Q,expected_q),expected_profit)
# Consumer choice: enumerate all feasible integer baskets instead of relying on a tangent.
a=[0,10,18,25,30,34,37,38];b=[0,6,11,15,18,20,21,21]
for budget,expected in [(70,(33,2,3)),(150,(54,5,5))]:
    baskets=[(a[x]+b[y],x,y) for x in range(8) for y in range(8) if 20*x+10*y<=budget]
    assert max(baskets)==expected,(budget,max(baskets))
    checks.append('S4 pizza budget '+str(budget))
check('S4 Cobb-Douglas budget',6*s.Rational(100,9)+8*s.Rational(50,3),200)
check('S4 marginal utility ratios',2/s.Rational(100,9)/6,4/s.Rational(50,3)/8)
check('S5 AP',F(3000,125),24)
check('S5 labor required',F(6000,30),200)
check('S5 power function',30*27**s.Rational(1,3)*25**s.Rational(1,2),450)
check('S6 TC',(50+4*50)**2,62500)
check('S6 marginal cost',s.diff((50+4*Q)**2,Q).subs(Q,50),2000)
check('S6 finite cost',(50+4*51)**2-(50+4*50)**2,2016)
check('S6 incremental labor cost',F(100,5*20-4*15),F(5,2))
check('S6 corrected factor budget',30*3+50*5,340)
check('S6 local cost saving',50-30*F(80,100),26)
check('S6 year2 ATC',F(235000+3*545000,5400),F(9350,27))
check('S7 maximum TR',(300*Q-Q**2).subs(Q,150),22500)
check('S7 break-even',F(60000,100-20),750)
check('S7 price target',F(26000+40000,600),110)
optimum('S8 problem1',s.Integer(30),3*Q**2+7*Q+90,s.Rational(23,6),-s.Rational(551,12))
optimum('S8 problem2',s.Integer(10),Q**2/10+2*Q+3,s.Integer(40),157)
check('S8 long-run quantity',s.diff(3*Q**2-2*Q+1,Q).subs(Q,s.Rational(1,3)),0)
check('S8 long-run price',(3*Q**2-2*Q+1).subs(Q,s.Rational(1,3)),s.Rational(2,3))
optimum('S8 problem4',s.Integer(45),50+5*Q*(Q+1),s.Integer(4),30)
optimum('S9 problem1',24-Q/10,Q**2/2+40,s.Integer(20),200)
optimum('S9 problem2',240-2*Q,2*Q**2+70,s.Integer(30),3530)
optimum('S9 problem3',120-Q/10,Q**2/2+4000,s.Integer(100),2000)
optimum('S9 unit tax',118-Q/10,Q**2/2+4000,s.Rational(295,3),s.Rational(5405,3))
optimum('S9 problem5',1500-4*Q,s.Rational(5,6)*Q**3-4*Q**2+500*Q,s.Integer(20),s.Rational(40000,3))
optimum('S10 problem1',130-2*Q,2*Q**2+2*Q,s.Integer(16),1024)
optimum('S10 before advertising',22-Q/2,6*Q**2-4*Q,s.Integer(2),26)
optimum('S10 after advertising',45-Q/2,6*Q**2-4*Q+5*Q+Q**2/2,s.Rational(22,7),s.Rational(484,7))
optimum('S10 problem3',100-2*Q,5*Q**2+30*Q,s.Integer(5),175)
profits=[(70-3*q)*q-ac*q for q,ac in enumerate([80,70,60,50,46,44,48],1)]
assert max(enumerate(profits,1),key=lambda v:v[1])==(6,48)
checks.append('S10 discrete optimum')
q1,q2=s.symbols('q1 q2')
p=206-3*(q1+q2)
check('S11 Cournot firm1',s.diff((p-26)*q1,q1).subs({q1:20,q2:20}),0)
check('S11 Cournot price',p.subs({q1:20,q2:20}),86)
p=200-5*(q1+q2);t1=20*q1**2+50*q1+100;t2=-s.Rational(5,2)*q2**2+140*q2+200
r2=12-q1;r1=3-q2/10
check('S11 Bowley leader1',s.diff((p*q1-t1).subs(q2,r2),q1).subs(q1,s.Rational(9,4)),0)
check('S11 Bowley leader2',s.diff((p*q2-t2).subs(q1,r1),q2).subs(q2,s.Rational(45,4)),0)
v={q1:s.Rational(9,4),q2:s.Rational(45,4)}
check('S11 Bowley actual price',p.subs(v),s.Rational(265,2))
check('S11 Bowley actual profit1',(p*q1-t1).subs(v),-s.Rational(125,8))
check('S11 Bowley actual profit2',(p*q2-t2).subs(v),s.Rational(1025,32))
check('S11 Stackelberg leader',s.diff((280-q1-(280-q1)/2)*q1,q1).subs(q1,140),0)
# New common Cournot/Stackelberg/cartel example and independent maximum via completing the square.
for title,price,cost,q,profit in [
 ('model7',s.Integer(50),100+10*Q+Q**2,20,300),
 ('model9',100-2*Q,100+20*Q,20,700),
 ('model10',80-Q,200+20*Q+Q**2,15,250)]:
 optimum(title,price,cost,s.Integer(q),profit)
check('new cartel deviation',(s.Rational(105,2)-30)*s.Rational(45,2),s.Rational(2025,4))
if __name__=='__main__':
 import json
 print(json.dumps({'passed':len(checks),'checks':checks},ensure_ascii=False,indent=2))
