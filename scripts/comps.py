import os
HERE = os.path.dirname(os.path.abspath(__file__))
# Valuation cross-check. P/TBV and ROE: S&P Global via stockanalysis.com statistics pages, 23 Sep 2026.
# Cross-check: finviz P/B and ROE, 23 Sep 2026 (ROE identical; P/B within 0.14x). JRVR close $3.59 (Nasdaq official, finviz).
import numpy as np
C={"KNSL":(3.90,30.27,3.94,3.80),"RLI":(3.14,25.16,3.04,2.98),"SKWD":(3.09,17.34,1.96,1.92),"BOW":(2.35,14.10,2.35,2.35),
   "MKL":(1.49,12.46,1.15,1.14),"UFCS":(1.41,15.46,1.41,1.41),"AMSF":(1.82,18.23,1.82,1.81),"GBLI":(0.58,4.88,0.56,0.51)}
x=np.array([v[1] for v in C.values()]); y=np.array([v[0] for v in C.values()])
b,a=np.polyfit(x,y,1); r=np.corrcoef(x,y)[0,1]
print(f"P/TBV = {a:.3f} + {b:.4f} x ROE%  (n={len(x)}, r2={r*r:.2f})")
for roe in (4.93,8,10,12): print(f"  ROE {roe}% -> P/TBV {a+b*roe:.2f}")
# ex-SKWD (P/TBV vs P/B gap)
m=[k!="SKWD" for k in C]; b2,a2=np.polyfit(x[m],y[m],1); print(f"ex-SKWD: {a2:.3f} + {b2:.4f} x ROE; ROE10 -> {a2+b2*10:.2f}; ROE5 -> {a2+b2*4.93:.2f}")
# P/B version
yb=np.array([v[3] for v in C.values()]); b3,a3=np.polyfit(x,yb,1); print(f"P/B(finviz) = {a3:.3f}+{b3:.4f}xROE ; ROE10 -> {a3+b3*10:.2f}; ROE5 -> {a3+b3*4.93:.2f}")
# the multiples I use in the piece, for comparison
tce_ex=6.68; eb=7.99
print("JRVR now: price/TCE ex-gain", round(3.59/tce_ex,2), " price/econ book", round(3.59/eb,2))
print("Base $5.21 / YE27 econ book 8.01 =", round(5.21/8.01,2))
