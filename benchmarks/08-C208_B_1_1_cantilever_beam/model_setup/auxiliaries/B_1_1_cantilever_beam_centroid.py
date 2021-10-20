hv = 460.0
tv = 8.0

hh = 300.0
th = 40.0 

Av = hv*tv
print(f"Av : {Av}")

Ah = hh*th
print(f"Ah : {Ah}")

A = Ah + Av
print(f"A : {A}")

Sv = Av * (th*0.5 + hv*0.5)
print(f"Sv : {Sv}")

Sh = Ah * (0)
print(f"Sh : {Sh}")

yc = (Sv+Sh)/(Av+Ah)
print(f"yc : {yc}")


# Area moment of inertia (acc. to self axis)
Iv = (hv**3 * tv)/12
print(f"Iv : {Iv}")
# Area moment of inertia (rel. to yc)
Ivc = Iv + Av * (((hv+th)*0.5 - yc)**2)
print(f"Ivc : {Ivc}")

# Area moment of inertia (acc. to self axis)
Ih = (th**3 * hh)/12 
print(f"Ih : {Ih}")
# Area moment of inertia (rel. to yc)
Ihc = Ih + Ah * ((yc)**2)
print(f"Ihc : {Ihc}")

# Area moment of inertia of whole section
Ic = Ivc + Ihc
print(f"Ic : {Ic}")

# Section modulus on upper part of section
Wy_upper = Ic / ( hv + th - (yc + th/2) )
print(f"Wy_upper : {Wy_upper}")
# Section modulus on lower part of section
Wy_lower = Ic / (yc + th/2)
print(f"Wy_lower : {Wy_lower}")