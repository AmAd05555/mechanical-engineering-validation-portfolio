# Analytical ground-truth calculation — N, mm, MPa
L=250.0
h=30.0
t=10.0
P=600.0
E=210000.0
yield_strength=250.0
I=t*h**3/12
sigma_root=P*L*(h/2)/I
delta=P*L**3/(3*E*I)
fos=yield_strength/sigma_root
print("I [mm^4] =",I)
print("Root bending stress [MPa] =",sigma_root)
print("Tip deflection [mm] =",delta)
print("Nominal FOS =",fos)
