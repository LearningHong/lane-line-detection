# -*- coding: utf-8 -*-
# ——author—— = “hong”
# Email :1424148078@qq.com
# time  :
# function:
R = 145
G = 161
B = 157
I = (145 , 161 , 157)
max=max(I)
print(max)
min=min(I)
V = max
S=(max-min)/max
if R == max:
    H =(G-B)/(max-min)* 60
if G == max:
    H = 120+(B-R)/(max-min)* 60
if B == max:
    H = 240 +(R-G)/(max-min)* 60
if H < 0:
    H = H + 360

print(H,S,V)