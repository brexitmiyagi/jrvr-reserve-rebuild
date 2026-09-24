import os
HERE = os.path.dirname(os.path.abspath(__file__))
# scenarios and target. 2026H2-2028 earnings and book, four scenarios, takeout range. $m. earnings path from earnings_bridge.py, price is the 23 Sep 2026 close
SH=46.239030; PX=3.59; T=0.21
TCE_EX=522.601-181.831-31.905          # XBRL + 10-Q 30 Jun 2026
DG_ADC=83.793; DG_TOP=22.235; DG_CA=1.808   # 10-Q retro tables
CUSHION0=75.8                          # CNW 486.9 vs floor ~411.1 (reconstruction)
# ---- clock 1: reinsurer payments and gain release (estimate) ----
paid={2026:225.0,2027:169.0,2028:125.0,2029:95.0,2030:72.0}   # old-book claims paid; 2025 payout rate 31.7% of opening reserve, declining book
ret_left_yearstart=176.0              # mid of 165.5-186.3 at YE2025
sn_left=397.0; top_left=75.0; rel={}
ret=ret_left_yearstart
for y in sorted(paid):
    p=paid[y]; toSN=max(0,p-ret); ret=max(0,ret-p)
    sn=min(sn_left,0.85*toSN); sn_left-=sn
    over=max(0,toSN-sn/0.85); tp=min(top_left,over); top_left-=tp
    rel[y]=(sn,tp,DG_ADC*sn/397.0+DG_TOP*tp/75.0)
for y,(sn,tp,g) in rel.items(): print(f"{y}: State National pays {sn:6.1f}, Enstar {tp:5.1f}, gain released {g:5.1f}")
def pv(r):
    return sum(rel[y][2]*(1-T)/(1+r)**(y-2026+0.5) for y in rel)
for r in (0.10,0.12): print(f"PV of after-tax gain at {r:.0%}: {pv(r):.1f} (nominal {(DG_ADC+DG_TOP)*(1-T):.1f}); per share {pv(r)/SH:.2f}")
DGPV=pv(0.11)+DG_CA*(1-T)
EB0=TCE_EX+DGPV
print(f"Economic book today with discounted gain: {EB0:.1f} = ${EB0/SH:.2f}/sh (undiscounted $8.52)")
# ---- clock 2: retained development, scenarios ----
emerge={2026:0.30,2027:0.35,2028:0.20}  # share of scenario development recognised in each year; remainder after 2028
adj={2026:19.0,2027:32.0,2028:27.0}     # from earnings_bridge.py: 2027 E&S CR ~94.7% on NEP ~$500m, 2028 about 1.5pt worse
div=1.85
scen={
 "Bull":dict(desc="reported method, young years release $60m",dev=105.8-60,p=0.20,noi=1.00,mult=0.80,rz=0),
 "Base":dict(desc="reported method, 3-5% tail midpoint",dev=126.7,p=0.40,noi=1.00,mult=0.65,rz=0),
 "Bear":dict(desc="paid method, earned surplus gone, $40m raise at $3.00",dev=268.5,p=0.25,noi=0.85,mult=0.45,rz=40.0,rzpx=3.00),
 "Distress":dict(desc="paid P75, downgrade, $60m raise at $2.50",dev=306.5,p=0.15,noi=0.70,mult=0.35,rz=60.0,rzpx=2.50),
}
tgt=0; rows=[]
print()
for name,s_ in scen.items():
    eb=EB0; cush=CUSHION0; minc=cush; nis=[]; ebs={}
    for y in (2026,2027,2028):
        d=s_['dev']*emerge[y]; g=rel[y][2]
        a_=adj[y]*s_['noi']
        ni=a_-d*(1-T)+g*(1-T)
        eb+= a_-d*(1-T)-div*(0.5 if y==2026 else 1)
        eb+= (EB0-TCE_EX)*0.11*(0.5 if y==2026 else 1)   # unwinding of the gain discount
        cush+= ni-0.25*max(ni,0)-div*(0.5 if y==2026 else 1)
        minc=min(minc,cush); nis.append(round(ni,1)); ebs[y]=eb
    sh=SH
    if s_['rz']: sh=SH+s_['rz']/s_['rzpx']; ebs[2027]+=s_['rz']
    bv27=ebs[2027]/sh
    roe=adj[2027]*s_['noi']/ebs[2027]
    mult=s_['mult']
    val=bv27*mult
    tgt+=s_['p']*val
    rows.append((name,s_['desc'],s_['p'],nis,minc,bv27,roe,mult,val))
    print(f"{name:8s} p={s_['p']:.2f} GAAP NI 26H2/27/28 {nis} | min cushion {minc:5.1f} | YE27 econ BV/sh {bv27:5.2f} | ROE {roe:.1%} | {mult:.2f}x | value ${val:.2f}")
print(f"\nProbability-weighted value (YE2027 basis): ${tgt:.2f} vs ${PX} ({(tgt/PX-1)*100:+.0f}%)")
# downside-weighted
down=sum(r[2]*r[8] for r in rows if r[8]<PX); pdown=sum(r[2] for r in rows if r[8]<PX)
print(f"Probability of ending below price: {pdown:.0%}; average value in those cases ${down/pdown:.2f}")
# front-loaded breach test: what share of the paid-method mean in Q3 alone breaches?
for bm in (0.55,0.65,0.75):
    t2=sum(r[2]*(r[5]*(bm if r[0]=="Base" else r[7])) for r in rows); print(f"base multiple {bm}: weighted ${t2:.2f}")
print(f"Market multiple on discounted economic book today: {PX/(EB0/SH):.2f}x")
print(f"Pre-tax retained charge that uses the whole cushion at once: {CUSHION0/(1-T):.1f}")
# ---- takeout ----
pref_gain=133.115-112.5
for lpt_limit,price in ((165.6,0.55),(165.6,0.70)):
    cost=lpt_limit*price*(1-T)
    adjb=EB0-cost+pref_gain
    print(f"Takeout: cap old book at P90 {lpt_limit} for {price:.0%} of limit -> after-tax cost {cost:.1f}; adjusted book {adjb:.1f} (${adjb/SH:.2f}); at 0.8x-1.0x ${0.8*adjb/SH:.2f}-${adjb/SH:.2f}")
print(f"Cash a buyer must fund at close: pref put 112.5 + accrued, revolver 210.8 (change of control), senior debentures 15.0; junior sub 104.1 can stay")
