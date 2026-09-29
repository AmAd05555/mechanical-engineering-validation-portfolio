"""Static 2D plane-stress FEA benchmark using bilinear Q4 elements.
Units: N, mm, MPa. No external FEA package required.
"""
import math, numpy as np, pandas as pd
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.linalg import spsolve

L,H,T = 250.0,30.0,10.0
E,NU = 210000.0,0.30
P = 600.0

def mesh_rect(nx,ny):
    xs=np.linspace(0,L,nx+1); ys=np.linspace(-H/2,H/2,ny+1)
    nodes=np.array([[x,y] for y in ys for x in xs],float)
    elems=[]
    def n(i,j): return j*(nx+1)+i
    for j in range(ny):
        for i in range(nx): elems.append([n(i,j),n(i+1,j),n(i+1,j+1),n(i,j+1)])
    return nodes,np.array(elems,int)

def q4_ke(coords):
    D=E/(1-NU**2)*np.array([[1,NU,0],[NU,1,0],[0,0,(1-NU)/2]],float)
    Ke=np.zeros((8,8)); gps=[-1/math.sqrt(3),1/math.sqrt(3)]
    for xi in gps:
      for eta in gps:
        dN=0.25*np.array([[-(1-eta),(1-eta),(1+eta),-(1+eta)],[-(1-xi),-(1+xi),(1+xi),(1-xi)]])
        J=dN@coords; detJ=np.linalg.det(J); dNx=np.linalg.inv(J)@dN
        B=np.zeros((3,8))
        for a in range(4):
            B[0,2*a]=dNx[0,a]; B[1,2*a+1]=dNx[1,a]
            B[2,2*a]=dNx[1,a]; B[2,2*a+1]=dNx[0,a]
        Ke += B.T@D@B*detJ*T
    return Ke

def solve(nx=100,ny=12):
    nodes,elems=mesh_rect(nx,ny); ndof=2*len(nodes); K=lil_matrix((ndof,ndof)); F=np.zeros(ndof)
    for el in elems:
        Ke=q4_ke(nodes[el]); dofs=np.array([[2*n,2*n+1] for n in el]).ravel()
        for a,ia in enumerate(dofs):
            for b,ib in enumerate(dofs): K[ia,ib]+=Ke[a,b]
    K=csr_matrix(K)
    traction_y=-P/(T*H)
    rn=np.where(np.isclose(nodes[:,0],L))[0]; rn=rn[np.argsort(nodes[rn,1])]
    for a,b in zip(rn[:-1],rn[1:]):
        q=traction_y*T*abs(nodes[b,1]-nodes[a,1])/2
        F[2*a+1]+=q; F[2*b+1]+=q
    ln=np.where(np.isclose(nodes[:,0],0))[0]
    fixed=np.sort(np.ravel([[2*n,2*n+1] for n in ln])); free=np.setdiff1d(np.arange(ndof),fixed)
    u=np.zeros(ndof); u[free]=spsolve(K[free][:,free],F[free])
    tip=rn[np.argmin(abs(nodes[rn,1]))]
    print(f"Tip vertical deflection = {u[2*tip+1]:.6f} mm")
    I=T*H**3/12; delta=P*L**3/(3*E*I)
    print(f"Euler-Bernoulli ground truth = {-delta:.6f} mm")
    return nodes,elems,u

if __name__=='__main__': solve()
