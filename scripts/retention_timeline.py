import os
HERE = os.path.dirname(os.path.abspath(__file__))
# how much of the retention has been paid, when State National starts paying, and the gain release. $m. the forward bits are my estimates
out_ye23_10k = 1063.570          # FY2023 10-K: total outstanding E&S ex-CA net at 31 Dec 2023 (AY2014-23 + pre-2014)
subject_1jan24 = 1023.7          # 8-K 9 Jul 2024 Ex 99.2: Subject Reserves
dev_2024 = 108.0; dev_2025 = 88.3  # triangle: CY development on AY2016-2023 (2024 incl AY2023 release; 2025 excl AY2024)
out_ye25_old = 692.5 + 16.282    # FY2025: AY2016-23 outstanding + pre-2016
# Path A: paid from triangle AY2016-23 in CY2024+CY2025, plus pre-2016 runoff
paid_A = 262.3 + 281.0 + ((94.877-89.769)+(118.599-110.860)+11.111 - 16.282)
# Path B: roll-forward
paid_B = out_ye23_10k + dev_2024 + dev_2025 - out_ye25_old
scale = subject_1jan24/out_ye23_10k
print(f"Paid since 1 Jan 2024 to YE2025: path A {paid_A:.1f}, path B {paid_B:.1f}; scaled to subject perimeter {paid_A*scale:.1f}-{paid_B*scale:.1f}")
ret=716.6
lo=ret-max(paid_A,paid_B); hi=ret-min(paid_A,paid_B)*scale
print(f"Retention left at YE2025: {lo:.1f} to {hi:.1f}")
pace2025 = 281.0/885.3
annual2026 = pace2025*out_ye25_old
print(f"2025 payout as % of opening old-book outstanding {pace2025*100:.1f}%; 2026 implied paid {annual2026:.1f}/yr = {annual2026/12:.1f}/month")
h1=annual2026/2
print(f"Retention left at 30 Jun 2026: {lo-h1:.1f} to {hi-h1:.1f}; months to cross {(lo-h1)/(annual2026/12):.1f} to {(hi-h1)/(annual2026/12):.1f}")
# gain release ratios
print(f"ADC gain per $ recovered {83.793/397.0:.3f}; Top Up {22.235/75.0:.3f}")
# economic book
dg=107.836; tce_ex=522.601-181.831-31.905; sh=46.239030
eb=tce_ex+dg*0.79
print(f"TCE ex-DG {tce_ex:.3f} (${tce_ex/sh:.2f}); DG after tax {dg*0.79:.2f} (${dg*0.79/sh:.2f}); economic book {eb:.2f} (${eb/sh:.2f})")
PX=3.59  # Nasdaq close 23 Sep 2026
mc=PX*sh
print(f"market cap {mc:.1f}; implied after-tax shortfall vs economic book {eb-mc:.1f} (${(eb-mc)/sh:.2f}); pre-tax {(eb-mc)/0.79:.1f}")
for n,x in [('rep3',105.8),('rep5',147.6),('paid7',268.5),('paid10',333.4)]:
    b=(eb-x*0.79)/sh; print(n, f"book after ${b:.2f}, price/book {PX/b:.2f}x")
# covenant: each $ of gain released raises CNW by 0.79 and the floor by 0.25*0.79 (if quarterly NI positive)
print(f"Cushion gain from full $106.0 release: {106.0*0.79*0.75:.1f}")
