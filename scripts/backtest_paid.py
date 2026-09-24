import os
HERE = os.path.dirname(os.path.abspath(__file__))
# Paid chain-ladder back-test, no look-ahead. FY2022 10-K paid triangle (E&S ex-CA, AY2013-2022, $000),
# acc 0001620459-23-000026 jrvr-20221231.htm, table "Cumulative paid losses and LAE, net of reinsurance". Pulled 23 Sep 2026.
exec(open(os.path.join(HERE,"jrvr_triangles.py")).read())
PD22={2013:[3867,14509,30382,44421,59641,66553,71035,74635,76295,80137],
2014:[3412,16969,28212,43891,58774,71549,76523,79980,85433],
2015:[4048,17164,34801,55911,73455,87344,94494,103138],
2016:[5180,22852,46045,70105,90166,102072,116059],2017:[5290,22956,42764,64924,81303,102866],
2018:[6000,26160,50679,76494,105538],2019:[8235,31346,62227,103836],2020:[8642,34561,73106],2021:[11693,55070],2022:[12713]}
# consistency with FY2025 triangle
for ay in range(2016,2023):
    assert PD22[ay]==PD[ay][:len(PD22[ay])], ay
def cl(T):
    F={}
    for a in range(1,10):
        pr=[(T[ay][a-1],T[ay][a]) for ay in T if len(T[ay])>a]
        if pr: F[a]=sum(q for p,q in pr)/sum(p for p,q in pr)
    return F
F=cl(PD22); print("paid factors end-2022", {k:round(v,3) for k,v in F.items()})
for tail in (1.00,1.03,1.07,1.10):
    ind=0; rows=[]
    for ay in range(2016,2022):
        x=PD22[ay][-1]
        for k in range(len(PD22[ay]),10): x*=F[k]
        x*=tail; d=x-P[2022][ay][0]; ind+=d; rows.append(round(d/1e3,1))
    print(f"tail {tail}: paid CL indicated deficiency AY2016-21 at end-2022 {ind/1e3:.1f}  by AY {rows}")
act=sum(P[2025][ay][0]-P[2022][ay][0] for ay in range(2016,2022)); print("actual development end-2022 -> end-2025 AY2016-21:", round(act/1e3,1))
carried=sum(P[2022][ay][0] for ay in range(2016,2022)); print("carried end-2022 AY2016-21", round(carried/1e3,1))
# AY2022 young-year check
x=PD22[2022][0]
for k in range(1,10): x*=F[k]
print("AY2022 paid CL at end-2022 (tail1.07):", round((x*1.07-P[2022][2022][0])/1e3,1), " actual AY2022 move to 2025:", round((P[2025][2022][0]-P[2022][2022][0])/1e3,1))
# payment speed: paid / reported (case-incurred) at the same age, by AY
print("\npaid / reported(case-incurred) by age")
R={}
for V,d in P.items():
    for ay,(i,ib,c) in d.items(): R.setdefault(ay,{})[V-ay+1]=i-ib
ALLP=dict(PD); ALLP.update({ay:PD22[ay] for ay in (2013,2014,2015)})
for ay in range(2014,2026):
    s=[]
    for a in range(1,11):
        if ay in ALLP and len(ALLP[ay])>=a and a in R.get(ay,{}): s.append(f"{ALLP[ay][a-1]/R[ay][a]*100:5.1f}")
        else: s.append("   . ")
    print(ay," ".join(s))
# paid / incurred at same age
print("\npaid / incurred by age")
for ay in range(2014,2026):
    s=[]
    for a in range(1,11):
        V=ay+a-1
        if ay in ALLP and len(ALLP[ay])>=a and V in P and ay in P[V]: s.append(f"{ALLP[ay][a-1]/P[V][ay][0]*100:5.1f}")
        else: s.append("   . ")
    print(ay," ".join(s))
# calendar-year payments on AY2016-2023
for V in (2023,2024,2025):
    cy=sum(PD[ay][V-ay]-(PD[ay][V-ay-1] if V-ay-1>=0 else 0) for ay in range(2016,2024) if len(PD[ay])>V-ay)
    print("CY",V,"paid on AY2016-23:",round(cy/1e3,1))
