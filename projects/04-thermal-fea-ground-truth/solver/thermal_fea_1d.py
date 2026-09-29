import numpy as np

# 1D steady thermal FE benchmark: rectangular aluminum fin with side convection and convective tip.
# Linear 2-node conduction elements + consistent convection matrix.

def solve_fin(L=0.200, b=0.030, t=0.004, k=205.0, h=15.0, Tb=100.0, Tinf=25.0, nel=40):
    A=b*t
    P=2*(b+t)
    nn=nel+1
    le=L/nel
    K=np.zeros((nn,nn))
    F=np.zeros(nn)
    ke_cond=(k*A/le)*np.array([[1.,-1.],[-1.,1.]])
    ke_conv=(h*P*le/6.)*np.array([[2.,1.],[1.,2.]])
    fe_conv=(h*P*Tinf*le/2.)*np.array([1.,1.])
    for e in range(nel):
        ids=[e,e+1]
        ke=ke_cond+ke_conv
        for i in range(2):
            F[ids[i]]+=fe_conv[i]
            for j in range(2):
                K[ids[i],ids[j]]+=ke[i,j]
    K[-1,-1]+=h*A
    F[-1]+=h*A*Tinf
    free=np.arange(1,nn)
    T=np.empty(nn)
    T[0]=Tb
    T[free]=np.linalg.solve(K[np.ix_(free,free)], F[free]-K[np.ix_(free,[0])].flatten()*Tb)
    x=np.linspace(0,L,nn)
    return x,T

if __name__=='__main__':
    x,T=solve_fin()
    print('Tip temperature [C]:',T[-1])
