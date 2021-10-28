# Web height
hv = 460.0
# Web thickness
tv = 8.0

# Flange width
hh = 300.0
# Flange thickness
th = 40.0 

# Flange cross section area
Av = hv*tv
print(f"Av : {Av}")

# Web cross section area
Ah = hh*th
print(f"Ah : {Ah}")

# Total cross-section area
A = Ah + Av
print(f"A : {A}")

# Web static area moment relative to flange center
Sv = Av * (th*0.5 + hv*0.5)
print(f"Sv : {Sv}")

# Flange static area moment relative to his center
Sh = Ah * (0)
print(f"Sh : {Sh}")

# Distance from flange center towards inertia center of whole cross section
yc = (Sv+Sh)/(Av+Ah)
print(f"yc : {yc}")


# Flange area moment of inertia (acc. to self axis)
Iv = (hv**3 * tv)/12
print(f"Iv : {Iv}")

# Flange area moment of inertia (rel. to yc)
Ivc = Iv + Av * (((hv+th)*0.5 - yc)**2)
print(f"Ivc : {Ivc}")

# Web area moment of inertia (acc. to self axis)
Ih = (th**3 * hh)/12 
print(f"Ih : {Ih}")

# Web area moment of inertia (rel. to yc)
Ihc = Ih + Ah * ((yc)**2)
print(f"Ihc : {Ihc}")

# Area moment of inertia of whole section
Ic = Ivc + Ihc
print(f"Ic : {Ic}")

# Section modulus above inertia center
Wy_upper = Ic / ( hv + th - (yc + th/2) )
print(f"Wy_upper : {Wy_upper}")

# Section modulus below inertia center
Wy_lower = Ic / (yc + th/2)
print(f"Wy_lower : {Wy_lower}")