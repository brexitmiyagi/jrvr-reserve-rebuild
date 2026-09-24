import os
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE,"jrvr_triangles.py")).read())
# reported (case incurred = incurred - IBNR) triangle and IBNR ratio by age
R={}; IB={}; INC={}; CNT={}
for V,d in P.items():
    for ay,(i,ib,c) in d.items():
        a=V-ay+1
        R.setdefault(ay,{})[a]=i-ib; IB.setdefault(ay,{})[a]=ib/i; INC.setdefault(ay,{})[a]=i; CNT.setdefault(ay,{})[a]=c
print("IBNR share of incurred, by age:")
for ay in range(2014,2026):
    print(ay, " ".join(f"{IB[ay].get(a,float('nan'))*100:5.1f}" for a in range(1,11)))
print("\nReported (case-incurred) $m by age:")
for ay in range(2014,2026):
    print(ay, " ".join(f"{R[ay].get(a,float('nan'))/1e3:6.1f}" for a in range(1,11)))
# reported age-to-age factors using AYs 2014-2022 only (pre-2023 regime) and all
import statistics as st
def facs(ays):
    F={}
    for a in range(1,10):
        rs=[R[ay][a+1]/R[ay][a] for ay in ays if a in R[ay] and a+1 in R[ay]]
        if rs: F[a]=(sum(R[ay][a+1] for ay in ays if a in R[ay] and a+1 in R[ay])/sum(R[ay][a] for ay in ays if a in R[ay] and a+1 in R[ay]), len(rs), [round(x,3) for x in rs])
    return F
F=facs(range(2014,2026))
print("\nReported volume-weighted age-to-age factors (all AYs):")
for a,(f,n,rs) in F.items(): print(a,"->",a+1, round(f,4), "n=",n, rs)

def cdf(F, a, tail):
    x=1.0
    for k in range(a,10): x*=F[k][0]
    return x*tail
carried={ay:P[2025][ay][0] for ay in P[2025]}
print("\nREPORTED chain ladder (vol-wtd, all AYs), tail 1.03:")
tot={}
for tail in (1.03,1.05):
    s_old=0;s_new=0
    rows=[]
    for ay in range(2016,2026):
        a=2025-ay+1; rep=R[ay][a]; ult=rep*cdf(F,a,tail); d=ult-carried[ay]
        rows.append((ay,round(rep/1e3,1),round(cdf(F,a,tail),3),round(ult/1e3,1),round(carried[ay]/1e3,1),round(d/1e3,1)))
        if ay<=2023: s_old+=d
        else: s_new+=d
    if tail==1.03:
        for r in rows: print(r)
    print("tail",tail,"indicated minus carried: AY2016-23",round(s_old/1e3,1)," AY2024-25",round(s_new/1e3,1)," total",round((s_old+s_new)/1e3,1))
# paid chain ladder
PF={}
for a in range(1,10):
    num=sum(PD[ay][a] for ay in PD if len(PD[ay])>a); den=sum(PD[ay][a-1] for ay in PD if len(PD[ay])>a)
    PF[a]=num/den
print("\npaid factors",{a:round(v,3) for a,v in PF.items()})
for ptail in (1.07,1.10):
    s_old=0;s_new=0;rows=[]
    for ay in range(2016,2026):
        a=len(PD[ay]); x=PD[ay][-1]
        for k in range(a,10): x*=PF[k]
        ult=x*ptail; d=ult-carried[ay]
        rows.append((ay,round(ult/1e3,1),round(d/1e3,1)))
        if ay<=2023: s_old+=d
        else: s_new+=d
    if ptail==1.07: print(rows)
    print("paid tail",ptail,"old",round(s_old/1e3,1),"new",round(s_new/1e3,1))
# incurred CL (vol-weighted, from current triangle)

# incurred CL to ultimate (vol-weighted), from FY2025 triangle
exec(open(os.path.join(HERE,"jrvr_incurred_fy2025.py")).read().split('print("totals')[0])
IF={}
for a in range(1,10):
    num=sum(inc[ay][a] for ay in inc if len(inc[ay])>a); den=sum(inc[ay][a-1] for ay in inc if len(inc[ay])>a); IF[a]=num/den
print("\nincurred vol-wtd factors",{a:round(v,4) for a,v in IF.items()})
for itail in (1.00,1.02):
    so=sn=0; rows=[]
    for ay in inc:
        a=len(inc[ay]); x=inc[ay][-1]
        for k in range(a,10): x*=IF[k]
        x*=itail; d=x-inc[ay][-1]; rows.append((ay,round(d/1e3,1)))
        if ay<=2023: so+=d
        else: sn+=d
    print("inc tail",itail,rows,"old",round(so/1e3,1),"new",round(sn/1e3,1))
