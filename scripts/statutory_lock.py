import os
HERE = os.path.dirname(os.path.abspath(__file__))
# when the special surplus unlocks, and the earned-surplus run-forward. $m. inputs are from filings, the paths are my estimates
exec(open(os.path.join(HERE,"jrvr_triangles.py")).read())
# payout rate history on AY2016-2023 (paid in year / outstanding at start of year)
def outst(V, ays):
    return sum(P[V][ay][0]-PD[ay][V-ay] for ay in ays if ay in P[V] and len(PD[ay])>V-ay)
for V in (2024,2025):
    ays=range(2016,2024)  # old book AY2016-2023 only
    op=outst(V-1,ays)
    cy=sum(PD[ay][V-ay]-PD[ay][V-ay-1] for ay in ays if len(PD[ay])>V-ay)
    print(f"CY{V}: paid on AY2016-2023 {cy/1e3:.1f} / opening outstanding {op/1e3:.1f} = {cy/op*100:.1f}%")
# unlock: cumulative SN recoveries > 313.2 ; SN pays 85% of paid above retention; retention left at 1 Jan 2026 ~176 (165.5-186.3)
def unlock(paths, ret0=176.0):
    ret=ret0; cum=0.0; t=2026.0
    for y,p in paths:
        mo=p/12
        for m in range(12):
            x=mo
            if ret>0:
                u=min(ret,x); ret-=u; x-=u
            cum+=0.85*x
            if cum>313.2: return y+(m+1)/12, cum
    return None,cum
base=[(2026,225),(2027,169),(2028,125),(2029,95),(2030,72),(2031,55)]
flat=[(y,281.0) for y in range(2026,2032)]
print("SN recoveries needed 313.2 = 0.85*307.1 + 52.2 =", round(0.85*307.1+52.2,1), "-> gross paid above retention", round(313.2/0.85,1))
for name,pth in (("base (constant 31.7% payout rate, falling reserve)",base),("+20% pace",[(y,p*1.2) for y,p in base]),("-20% pace",[(y,p*0.8) for y,p in base]),("flat dollars at 2025 level 281/yr",flat)):
    for r0 in (165.5,176.0,186.3):
        t,c=unlock(pth,r0)
        print(f"{name:52s} ret0 {r0}: unlock ~{t:.2f}" if t else f"{name} none")
# bear: more ultimate losses -> more paid. Scale payments by ultimate ratio
for nm,dev in (("reported mid",126.7),("paid median",268.5),("paid P75",306.5)):
    sc=(708.8+dev)/(708.8+126.7)
    t,c=unlock([(y,p*sc) for y,p in base])
    print(f"unlock with payments scaled for {nm} ({sc:.3f}): ~{t:.2f}")
# ---- earned surplus flow test at James River Insurance (JRIC) ----
T=0.21; share=0.75
emerge={2026:0.30,2027:0.35,2028:0.20}
adj={2026:15.8+21.0,2027:38.0,2028:34.0}   # group adjusted op income after tax: H1 2026 actual 15.8 + H2 est 21.0 (model)
int_at=22.4*(1-T)                           # holdco interest, after tax, added back (JRIC earns before holdco interest)
need=22.4+7.875+1.85                        # holdco cash need per year: interest + preferred + common dividend
print(f"\nholdco cash need ~{need:.1f}/yr")
for nm,dev,noi in (("Base",126.7,1.00),("Bear",268.5,0.85),("Distress",306.5,0.70)):
    u=172.0-30.0; path=[]
    for y in (2026,2027,2028):
        earn=(adj[y]*(noi if y>2026 else 1.0)+int_at)*share if y>2026 else (15.8+(21.0*noi)+int_at)*share
        chg=dev*(1-T)*emerge[y]*share
        divs= (need-30.0 if y==2026 else need)*1.0  # JRIC funds all holdco needs (March 30 already paid for 2026)
        u=u+earn-chg-max(divs,0); path.append(round(u,1))
    print(f"{nm:8s} JRIC unassigned (earned) surplus YE26/27/28 after funding holdco: {path}")
    u=172.0-30.0; path=[]
    for y in (2026,2027,2028):
        earn=(adj[y]*(noi if y>2026 else 1.0)+int_at)*share if y>2026 else (15.8+(21.0*noi)+int_at)*share
        chg=dev*(1-T)*emerge[y]*share
        u=u+earn-chg; path.append(round(u,1))
    print(f"{'':8s} ... before any further dividends: {path}")
# ordinary dividend cap: greater of 10% surplus or prior-year statutory NI (ORC 3901.34)
print(f"\n2026 cap: max(10% x 522.9 = {52.29:.1f}, 2025 NI 69.4) = 69.4; 2025 NI ex retro gain = {69.4-43.2:.1f} -> cap would be {max(52.3,69.4-43.2):.1f}")
print("special surplus change 2025 34.4 vs retro gain 43.2: gap", round(43.2-34.4,1), "; 43.2*0.79 =", round(43.2*0.79,1))
