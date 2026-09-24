import os
HERE = os.path.dirname(os.path.abspath(__file__))
# Mack (1997) calendar-year test on the reported and paid triangles, plus the emergence pattern and the 2024-25 fork
exec(open(os.path.join(HERE,"jrvr_triangles.py")).read())
import math, statistics as st
R={}
for V,d in P.items():
    for ay,(i,ib,c) in d.items(): R.setdefault(ay,{})[V-ay+1]=i-ib
# ---- Mack calendar-year test on reported link ratios ----
AYS=sorted(R); F={}
lab={}  # (ay,j) -> 'S'/'L'/None
for j in range(1,10):
    lr=[(ay,R[ay][j+1]/R[ay][j]) for ay in AYS if j in R[ay] and j+1 in R[ay]]
    if len(lr)<2: continue
    med=st.median([x for _,x in lr])
    for ay,x in lr:
        lab[(ay,j)]= 'S' if x<med else ('L' if x>med else None)
# diagonal of link ratio (ay,j): the later valuation year = ay+j (age j+1)
diag={}
for (ay,j),l in lab.items():
    k=ay+j
    diag.setdefault(k,[]).append(l)
Z=0;EZ=0;VZ=0
print("CY  n  S  L")
for k in sorted(diag):
    s=diag[k].count('S'); l=diag[k].count('L'); n=s+l
    if n<2: continue
    m=(n-1)//2
    ez=n/2-math.comb(n-1,m)*n/2**n
    vz=n*(n-1)/4-math.comb(n-1,m)*n*(n-1)/2**n+ez-ez**2
    Z+=min(s,l); EZ+=ez; VZ+=vz
    print(k,n,s,l)
lo=EZ-1.96*math.sqrt(VZ); hi=EZ+1.96*math.sqrt(VZ)
print(f"Mack CY test: Z={Z}, E[Z]={EZ:.2f}, 95% band [{lo:.2f}, {hi:.2f}] -> {'no significant calendar-year effect' if lo<=Z<=hi else 'CALENDAR-YEAR EFFECT'}")
# ---- emergence of remaining reported development by calendar year (AY2016-23) ----
def facs():
    F={}
    for a in range(1,10):
        pr=[(R[ay][a],R[ay][a+1]) for ay in R if a in R[ay] and a+1 in R[ay]]
        F[a]=sum(q for p,q in pr)/sum(p for p,q in pr)
    return F
F=facs(); tail=1.03
rep_now={ay:R[ay][2025-ay+1] for ay in range(2016,2024)}
path={}
for ay,x0 in rep_now.items():
    a=2025-ay+1; x=x0; cy=2026
    for k in range(a,10):
        nx=x*F[k]; path[cy]=path.get(cy,0)+(nx-x); x=nx; cy+=1
    path[cy]=path.get(cy,0)+x*(tail-1)
tot=sum(path.values())
print("reported emergence of remaining development on AY2016-23, share by CY:",{k:round(v/tot*100,1) for k,v in sorted(path.items())})
c=0
for k in sorted(path):
    c+=path[k]/tot
    if k<=2029: print(" cumulative through",k,round(c*100,1))

# ---- CY test on PAID triangle (independent of case reserving) ----
PD22={2013:[3867,14509,30382,44421,59641,66553,71035,74635,76295,80137],2014:[3412,16969,28212,43891,58774,71549,76523,79980,85433],2015:[4048,17164,34801,55911,73455,87344,94494,103138]}
PA={**{ay:{a+1:v for a,v in enumerate(PD22[ay])} for ay in PD22},**{ay:{a+1:v for a,v in enumerate(PD[ay])} for ay in PD}}
def cytest(T,name):
    lab={}
    for j in range(1,10):
        lr=[(ay,T[ay][j+1]/T[ay][j]) for ay in T if j in T[ay] and j+1 in T[ay]]
        if len(lr)<2: continue
        med=st.median([x for _,x in lr])
        for ay,x in lr: lab[(ay,j)]='S' if x<med else ('L' if x>med else None)
    diag={}
    for (ay,j),l in lab.items(): diag.setdefault(ay+j,[]).append(l)
    Z=EZ=VZ=0; rows=[]
    for k in sorted(diag):
        s=diag[k].count('S'); l=diag[k].count('L'); n=s+l
        if n<2: continue
        m=(n-1)//2; ez=n/2-math.comb(n-1,m)*n/2**n
        vz=n*(n-1)/4-math.comb(n-1,m)*n*(n-1)/2**n+ez-ez**2
        Z+=min(s,l); EZ+=ez; VZ+=vz; rows.append((k,s,l))
    lo=EZ-1.96*math.sqrt(VZ); hi=EZ+1.96*math.sqrt(VZ)
    print(f"{name}: Z={Z} E={EZ:.2f} band [{lo:.2f},{hi:.2f}] {'OK' if lo<=Z<=hi else 'CY EFFECT'} diagonals(S,L) {rows}")
cytest(PA,"PAID (AY2013-2025)")
cytest({ay:R[ay] for ay in R},"REPORTED")
# ---- reported CL using factors from selected calendar years only ----
def cl_sel(cys,tail=1.03):
    F={}
    for a in range(1,10):
        pr=[(R[ay][a],R[ay][a+1]) for ay in R if a in R[ay] and a+1 in R[ay] and (ay+a) in cys]
        if pr: F[a]=sum(q for p,q in pr)/sum(p for p,q in pr)
    Fall=facs()
    ind=0
    for ay in range(2016,2024):
        a=2025-ay+1; x=R[ay][a]
        for k in range(a,10): x*=F.get(k,Fall[k])
        ind+=x*tail-P[2025][ay][0]
    return ind/1e3-23.6
print("reported CL, 3% tail, net of H1 23.6: all CYs", round(cl_sel(set(range(2015,2026))),1),
      "| last two CYs (2024-25) only", round(cl_sel({2024,2025}),1),
      "| excluding 2024-25", round(cl_sel(set(range(2015,2024))),1),
      "| last three CYs", round(cl_sel({2023,2024,2025}),1))
