import os
HERE = os.path.dirname(os.path.abspath(__file__))
import math, random
exec(open(os.path.join(HERE,"jrvr_triangles.py")).read())
AYS=list(range(2014,2026))
def rep_tri():
    T={ay:{} for ay in AYS}
    for V,d in P.items():
        for ay,(i,ib,c) in d.items():
            if ay in T: T[ay][V-ay+1]=(i-ib)/1000
    return T
def paid_tri():
    return {ay:{k+1:v/1000 for k,v in enumerate(PD[ay])} for ay in AYS if ay in PD}
carried={ay:P[2025][ay][0]/1000 for ay in range(2016,2026)}
def mack(T,tail):
    n=10
    AY=[a for a in AYS if a in T]
    f={};s2={}
    for k in range(1,n):
        pairs=[(T[ay][k],T[ay][k+1]) for ay in AY if k in T[ay] and k+1 in T[ay]]
        f[k]=sum(b for a,b in pairs)/sum(a for a,b in pairs)
        if len(pairs)>1:
            s2[k]=sum(a*(b/a-f[k])**2 for a,b in pairs)/(len(pairs)-1)
    # extrapolate missing sigma (Mack)
    ks=sorted(s2)
    for k in range(1,n):
        if k not in s2:
            s2[k]=min(s2[ks[-1]]**2/s2[ks[-2]], s2[ks[-1]], s2[ks[-2]])
    res={}
    for ay in [a for a in AY if a>=2016]:
        a=max(T[ay]); C=T[ay][a]; ult=C; mse_rel=0
        cols={}
        for k in range(a,n):
            colsum=sum(T[j][k] for j in AY if k in T[j] and k+1 in T[j])  # sum over AYs with k+1 observed
            Chat=ult
            mse_rel += s2[k]/f[k]**2*(1/Chat + 1/colsum)
            ult*=f[k]
        ult_t=ult*tail
        se=ult_t*math.sqrt(mse_rel)
        res[ay]=(ult_t,se)
    return f,s2,res
def lognorm_pct(mean,sd,p):
    s2=math.log(1+(sd/mean)**2); mu=math.log(mean)-s2/2
    z={0.5:0,0.75:0.6745,0.9:1.2816,0.95:1.6449}[p]
    return math.exp(mu+z*math.sqrt(s2))
for name,T,tails in [("REPORTED",rep_tri(),(1.03,1.05)),("PAID",paid_tri(),(1.07,1.10))]:
    for tail in tails:
        f,s2,res=mack(T,tail)
        old=[ay for ay in range(2016,2024)]
        mean_ult=sum(res[a][0] for a in old); car=sum(carried[a] for a in old)
        # aggregate se: sum of variances (ignoring cov) and fully-correlated bound
        se_ind=math.sqrt(sum(res[a][1]**2 for a in old)); se_cor=sum(res[a][1] for a in old)
        se=(se_ind+se_cor)/2  # midpoint between independence and full correlation
        short_mean=mean_ult-car
        # percentiles of ultimate via lognormal, then minus carried and minus 23.6 already emerged
        out=[]
        for p in (0.5,0.75,0.9,0.95):
            u=lognorm_pct(mean_ult,se,p); out.append(round(u-car-23.6,1))
        print(f"{name} tail {tail}: mean still-to-come {short_mean-23.6:.1f}; se {se:.1f} (indep {se_ind:.1f}, corr {se_cor:.1f}); P50/P75/P90/P95 still-to-come {out}")
# link-ratio bootstrap on reported triangle (parameter + resampled development)
random.seed(7)
T=rep_tri()
links={k:[T[ay][k+1]/T[ay][k] for ay in AYS if k in T[ay] and k+1 in T[ay]] for k in range(1,10)}
wts={k:[T[ay][k] for ay in AYS if k in T[ay] and k+1 in T[ay]] for k in range(1,10)}
sims=[]
old=[ay for ay in range(2016,2024)]; car=sum(carried[a] for a in old)
for s in range(20000):
    # resample factors per age (volume weighted mean of resample) and apply a random realised link per AY
    fk={}
    for k in range(1,10):
        L=links[k];W=wts[k];idx=[random.randrange(len(L)) for _ in L]
        fk[k]=sum(L[i]*W[i] for i in idx)/sum(W[i] for i in idx)
    tot=0
    for ay in old:
        a=max(T[ay]); x=T[ay][a]
        for k in range(a,10):
            x*= random.choice(links[k]) if random.random()<0.5 else fk[k]
        tot+=x*1.03
    sims.append(tot-car-23.6)
sims.sort()
pc=lambda p: sims[int(p*len(sims))]
print("BOOTSTRAP reported (3pct tail) still-to-come: mean %.1f P50 %.1f P75 %.1f P90 %.1f P95 %.1f P(>96)=%.2f"%(sum(sims)/len(sims),pc(.5),pc(.75),pc(.9),pc(.95),sum(1 for v in sims if v>96)/len(sims)))
