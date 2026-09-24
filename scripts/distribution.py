import os
HERE = os.path.dirname(os.path.abspath(__file__))
# Mack chain ladder on the stitched reported-loss triangle (AY2016-2025) and ODP bootstrap on the paid triangle.
import numpy as np, math
from scipy.stats import lognorm
exec(open(os.path.join(HERE,"jrvr_triangles.py")).read())
AYS=list(range(2016,2026)); n=10
AYR=list(range(2014,2026))
R=np.full((12,n),np.nan)
for V,d in P.items():
    for ay,(i,ib,c) in d.items():
        a=V-ay
        if a<n: R[ay-2014,a]=(i-ib)/1e3
PDm=np.full((n,n),np.nan)
for ay,row in PD.items():
    for a,v in enumerate(row): PDm[ay-2016,a]=v/1e3
carried=np.array([P[2025][ay][0]/1e3 for ay in AYS])
def mack(T,tail,tail_cv=0.0):
    rows=T.shape[0]; n=T.shape[1]; f=np.ones(n-1); s2=np.zeros(n-1)
    for k in range(n-1):
        m=~np.isnan(T[:,k+1])&~np.isnan(T[:,k]); f[k]=T[m,k+1].sum()/T[m,k].sum()
        if m.sum()>1:
            s2[k]=((T[m,k]*(T[m,k+1]/T[m,k]-f[k])**2).sum())/(m.sum()-1)
    # sigma extrapolation for last
    s2[-1]=min(s2[-2]**2/s2[-3],min(s2[-3],s2[-2])) if s2[-3]>0 else s2[-2]
    C=T.copy(); last=np.zeros(rows,int)
    for i in range(rows):
        last[i]=np.max(np.where(~np.isnan(T[i]))[0])
        for k in range(last[i],n-1): C[i,k+1]=C[i,k]*f[k]
    ult=C[:,-1]*tail
    # Mack MSE per AY and total
    mse=np.zeros(rows)
    for i in range(rows):
        s=0
        for k in range(last[i],n-1):
            mm=~np.isnan(T[:,k+1])&~np.isnan(T[:,k]); Sk=T[mm,k].sum()
            s+= s2[k]/f[k]**2*(1/C[i,k]+1/Sk)
        mse[i]=(C[i,-1]**2)*s*tail**2 + (ult[i]*tail_cv)**2
    return f,s2,C,ult,mse,last
def total_mse(T,C,f,s2,mse,last,idx,tail):
    tot=sum(mse[i] for i in idx)
    n=T.shape[1]
    for a in idx:
        for b in idx:
            if b<=a: continue
            s=0
            for k in range(max(last[a],last[b]),n-1):
                mm=~np.isnan(T[:,k+1])&~np.isnan(T[:,k]); Sk=T[mm,k].sum(); s+=2*s2[k]/f[k]**2/Sk
            tot+=C[a,-1]*C[b,-1]*s*tail**2
    return tot
def pct(mean_res,se,ps):
    s2=math.log(1+(se/mean_res)**2); mu=math.log(mean_res)-s2/2
    return [lognorm.ppf(p,s=math.sqrt(s2),scale=math.exp(mu)) for p in ps]
out={}
for label,T,tail in (("reported 3%",R,1.03),("reported 5%",R,1.05),("paid 7%",PDm,1.07)):
    f,s2,C,ult,mse,last=mack(T,tail,tail_cv=0.02)
    off=T.shape[0]-10
    old=list(range(off,off+8))
    latest=np.array([T[i,last[i]] for i in range(T.shape[0])])
    car=np.array([np.nan]*off+list(carried))
    res_old=(ult[old]-latest[old]).sum(); ibnr_old=(car[old]-latest[old]).sum()
    se_old=math.sqrt(total_mse(T,C,f,s2,mse,last,old,tail))
    short_mean=ult[old].sum()-car[old].sum()
    p=pct(res_old,se_old,[0.5,0.75,0.9,0.95])
    shorts=[x-ibnr_old-23.6 for x in p]
    out[label]=(short_mean-23.6,se_old,shorts)
    print(f"{label}: old-book shortfall mean (net of H1 23.6) {short_mean-23.6:6.1f}; SE {se_old:5.1f}; P50 {shorts[0]:6.1f} P75 {shorts[1]:6.1f} P90 {shorts[2]:6.1f} P95 {shorts[3]:6.1f}; prob shortfall>96: {1-lognorm.cdf(96+ibnr_old+23.6,s=math.sqrt(math.log(1+(se_old/res_old)**2)),scale=math.exp(math.log(res_old)-math.log(1+(se_old/res_old)**2)/2)):.2f}")
# ODP bootstrap on paid (old book)
rng=np.random.default_rng(7)
T=PDm; mask=~np.isnan(T)
inc_tri=np.full_like(T,np.nan)
for i in range(n):
    for k in range(n):
        if mask[i,k]: inc_tri[i,k]=T[i,k]-(T[i,k-1] if k>0 else 0)
f,s2,C,ult,mse,last=mack(T,1.0)
# fitted cumulative back from diagonal
fit=np.full_like(T,np.nan)
for i in range(n):
    L=last[i]; fit[i,L]=T[i,L]
    for k in range(L-1,-1,-1): fit[i,k]=fit[i,k+1]/f[k]
finc=np.full_like(T,np.nan)
for i in range(n):
    for k in range(last[i]+1): finc[i,k]=fit[i,k]-(fit[i,k-1] if k>0 else 0)
res=(inc_tri-finc)/np.sqrt(np.abs(finc)); rv=res[mask]
npar=2*n-1; N=mask.sum(); phi=(rv**2).sum()/(N-npar); adj=math.sqrt(N/(N-npar)); rv=rv*adj
sims=[]
for s in range(5000):
    pinc=finc+np.sqrt(np.abs(finc))*rng.choice(rv,size=finc.shape)
    pinc[~mask]=np.nan
    pc=np.nancumsum(pinc,axis=1); pc[~mask]=np.nan
    ff=np.ones(n-1)
    for k in range(n-1):
        m=~np.isnan(pc[:,k+1]); ff[k]=pc[m,k+1].sum()/pc[m,k].sum()
    tot=0
    for i in range(8):
        cum=T[i,last[i]]
        for k in range(last[i],n-1):
            mean_inc=cum*(ff[k]-1)
            draw=rng.gamma(max(mean_inc,1e-6)/phi,phi) if mean_inc>0 else mean_inc
            cum+=draw
        tot+=cum*1.07
    sims.append(tot-carried[:8].sum()-23.6)
sims=np.array(sims)
print("ODP bootstrap paid (7 pct tail), old book shortfall net of H1: mean %.1f P50 %.1f P75 %.1f P90 %.1f P95 %.1f; P(<96) %.2f"%(sims.mean(),*np.percentile(sims,[50,75,90,95]),(sims<96).mean()))
