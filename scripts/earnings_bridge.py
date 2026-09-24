import os
HERE = os.path.dirname(os.path.abspath(__file__))
# 2027 adjusted operating income bridge. Inputs from the Q2 2026 press release (8-K Ex 99.1, 10 Aug 2026).
# H1 2026: E&S NEP 269.132 (incl. -7.2 reinstatement premium, mostly E&S), E&S NWP 266.342 (-5.5% y/y; Q2 -11.4%),
# E&S AY loss ratio 64.8%, expense ratio 28.0%; SA UW loss -4.602; corporate opex -16.530; NII 41.604; interest 11.202;
# other income (non-fee) 0.902; preferred dividends 3.938; adjusted NOI 15.830.
T=0.21; PREF=7.875
def noi(nep,cr,nii=80.0,corp=31.0,sa=-4.0,oth=1.5,intr=22.4):
    uw=nep*(1-cr)
    return (uw+sa-corp+nii+oth-intr)*(1-T)-PREF, uw
nep27=500.0
print("E&S NEP 2026E ~", round(269.132+268,0), "; 2027E", nep27, "(-7%, NWP running -5.5% H1 / -11.4% Q2)")
for cr in (0.920,0.928,0.932,0.940,0.947,0.955,0.960):
    n,uw=noi(nep27,cr); print(f"E&S CR {cr*100:.1f}% -> UW {uw:5.1f} -> adjusted NOI {n:5.1f}  (diluted ~${(n+PREF)/60.4:.2f})")
# solve for CR giving 38 and 32
for tgt in (38.0,32.0,27.0):
    lo,hi=0.85,1.05
    for _ in range(60):
        m=(lo+hi)/2
        (lo,hi)=(m,hi) if noi(nep27,m)[0]>tgt else (lo,m)
    print(f"NOI {tgt} needs E&S CR {m*100:.1f}%")
print("H1 2026 E&S CR 94.6% incl reinstatement; underlying AY LR 64.8 + expense 28.0 = 92.8 ex development")
print("rate ~3% vs trend ~8%: loss-ratio drift (1.08/1.03-1)*64.8 =", round((1.08/1.03-1)*64.8,1), "pts/yr if fully unpriced")
print("Consensus 2027 adj EPS $0.68 (Nasdaq, 2 est) -> implied NOI ~", round(0.68*60.4-PREF,1))
