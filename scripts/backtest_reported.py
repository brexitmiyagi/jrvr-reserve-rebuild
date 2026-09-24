import os
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE,"jrvr_triangles.py")).read())
def build(maxV):
    R={}
    for V,d in P.items():
        if V>maxV: continue
        for ay,(i,ib,c) in d.items(): R.setdefault(ay,{})[V-ay+1]=i-ib
    return R
def factors(R):
    F={}
    for a in range(1,10):
        pairs=[(R[ay][a],R[ay][a+1]) for ay in R if a in R[ay] and a+1 in R[ay]]
        if pairs: F[a]=sum(q for p,q in pairs)/sum(p for p,q in pairs)
    return F
for maxV in (2021,2022,2023):
    R=build(maxV); F=factors(R)
    # missing late factors -> use 1.03 each beyond available, tail 1.03
    ind=0; rows=[]
    for ay in range(2016,maxV+1):
        a=maxV-ay+1; x=R[ay][a]
        for k in range(a,10): x*=F.get(k,1.03)
        x*=1.03
        carried=P[maxV][ay][0]; d=x-carried; ind+=d; rows.append((ay,round(d/1e3,1)))
    actual=sum(P[2025][ay][0]-P[maxV][ay][0] for ay in range(2016,maxV+1))
    print(maxV,"factors",{k:round(v,3) for k,v in F.items()})
    print("  indicated deficiency AY2016-",maxV,":",round(ind/1e3,1),rows)
    print("  actual development since (to FY2025):",round(actual/1e3,1))
    if maxV>=2022:
        ind21=sum(d for ay,d in rows if ay<=2021); act21=sum(P[2025][ay][0]-P[maxV][ay][0] for ay in range(2016,2022))
        print("  AY2016-2021 only: indicated",round(ind21,1)," actual since",round(act21/1e3,1))
