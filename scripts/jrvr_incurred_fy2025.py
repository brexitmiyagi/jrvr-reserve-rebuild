inc = {
2016:[138507,125093,126050,126971,125097,132235,135491,141242,148400,151612],
2017:[144349,131897,132136,124265,128674,134272,147196,155593,158714],
2018:[167004,158458,146633,150687,151563,167237,173186,180931],
2019:[214653,194759,189671,188061,204844,228076,237568],
2020:[239897,211732,207210,231658,273883,296540],
2021:[304435,286343,274120,307338,321722],
2022:[340436,293402,320146,342533],
2023:[369255,330330,335617],
2024:[360426,345686],
2025:[351985]}
paid = {2016:141710,2017:141347,2018:155337,2019:191455,2020:211509,2021:204642,2022:177429,2023:109278,2024:48871,2025:8824}
assert sum(v[-1] for v in inc.values())==2722908
assert sum(paid.values())==1390402
print("totals tie: incurred 2,722,908 / paid 1,390,402")
# calendar-year development on prior accident years
for cy in (2023,2024,2025):
    k=cy-2016
    tot=0; old=0; newest=None
    for ay,v in inc.items():
        age_now=cy-ay; 
        if age_now<1 or age_now>=len(v): continue
        d=v[age_now]-v[age_now-1]; tot+=d
        if ay==cy-1: newest=d
        else: old+=d
    print(f"CY{cy}: prior-AY development {tot/1e3:+.1f}m | newest AY {newest/1e3:+.1f}m | all OLDER AYs {old/1e3:+.1f}m")
print()
# low point vs latest
for ay,v in inc.items():
    lo=min(v); i=v.index(lo)
    print(f"AY{ay}: first {v[0]/1e3:6.1f} low {lo/1e3:6.1f} (age {i+1}) latest {v[-1]/1e3:6.1f}  low->latest {(v[-1]/lo-1)*100:+5.1f}%  first->latest {(v[-1]/v[0]-1)*100:+5.1f}%")
print()
# age-to-age factors, simple average, from company history
f={}
for a in range(1,9):
    rs=[v[a]/v[a-1] for v in inc.values() if len(v)>a]
    f[a]=sum(rs)/len(rs)
    print(f"age {a}->{a+1}: n={len(rs)} avg factor {f[a]:.4f}")
def to_latest_mature(ay, v, max_age=9):
    # project to age 10 using avg factors (age 9->10 from AY2016 only)
    x=v[-1]; a=len(v)
    for k in range(a,10):
        fac=f.get(k, 1.0) if k<9 else (inc[2016][9]/inc[2016][8])
        x*=fac
    return x
print()
tot_ind=0
for ay in (2023,2024,2025):
    v=inc[ay]; ult=to_latest_mature(ay,v)
    ind=ult-v[-1]; tot_ind+=ind
    print(f"AY{ay}: carried {v[-1]/1e3:.1f}m -> history-path to age 10 {ult/1e3:.1f}m  indicated +{ind/1e3:.1f}m")
print(f"AY2023-2025 indicated development if they follow 2016-2022's path: +{tot_ind/1e3:.1f}m pre-tax")
# AY2024-25 uncovered outstanding
print(f"\nAY2024+2025 outstanding (never covered): {(inc[2024][-1]+inc[2025][-1]-paid[2024]-paid[2025])/1e3:.1f}m")
print(f"AY2023 outstanding (cover exhausted): {(inc[2023][-1]-paid[2023])/1e3:.1f}m")
print()
out={ay:inc[ay][-1]-paid[ay] for ay in inc}
for ay,v in out.items(): print(ay, round(v/1e3,1))
old=sum(v for ay,v in out.items() if ay<=2023)
new=sum(v for ay,v in out.items() if ay>=2024)
print("AY2016-2023 outstanding", old/1e3, "+pre2016 16.282 =", old/1e3+16.282)
print("AY2024-25", new/1e3, " total", (old+new)/1e3+16.282, " vs recon 1332.506")
print("old book retained after ADC recoverable 434.562:", old/1e3+16.282-434.562)
print()
pd = {2016:[5180,22852,46045,70105,90166,102072,116059,126916,133928,141710],2017:[5290,22956,42764,64924,81303,102866,120229,132182,141347],2018:[6000,26160,50679,76494,105538,124903,138319,155337],2019:[8235,31346,62227,103836,136289,166472,191455],2020:[8642,34561,73106,117892,168550,211509],2021:[11693,55070,100649,154168,204642],2022:[12713,51537,108960,177429],2023:[10927,49094,109278],2024:[11096,48871],2025:[8824]}
for age in (1,2,3):
    print("age",age, {ay: round(pd[ay][age-1]/inc[ay][age-1]*100,1) for ay in inc if len(pd[ay])>=age})
for ay in (2023,2024):
    v=inc[ay]
    print(ay,[round(v[a]/v[a-1],4) for a in range(1,len(v))],"hist",[round(f[a],4) for a in range(1,len(v))])
# scenarios
import statistics
for label,scale in (("full history",1.0),("half",0.5)):
    tot=0
    for ay in (2023,2024,2025):
        v=inc[ay]; x=v[-1]
        for k in range(len(v),10):
            fac=f.get(k,1.0) if k<9 else inc[2016][9]/inc[2016][8]
            x*= 1+(fac-1)*scale
        tot+=x-v[-1]
    print(label, round(tot/1e3,1))
# only rise phase: factors from age3 onward, leave cuts out? (history-consistent already)
# median factors
fm={}
for a in range(1,9):
    rs=[v[a]/v[a-1] for v in inc.values() if len(v)>a]; fm[a]=statistics.median(rs)
tot=0
for ay in (2023,2024,2025):
    v=inc[ay]; x=v[-1]
    for k in range(len(v),10):
        fac=fm.get(k,1.0) if k<9 else inc[2016][9]/inc[2016][8]
        x*=fac
    tot+=x-v[-1]
print("median factors", round(tot/1e3,1))
# excluding AY2020 (covid/social inflation outlier)
fx={}
for a in range(1,9):
    rs=[v[a]/v[a-1] for ay,v in inc.items() if len(v)>a and ay!=2020]; fx[a]=sum(rs)/len(rs)
tot=0
for ay in (2023,2024,2025):
    v=inc[ay]; x=v[-1]
    for k in range(len(v),10):
        fac=fx.get(k,1.0) if k<9 else inc[2016][9]/inc[2016][8]
        x*=fac
    tot+=x-v[-1]
print("ex-2020 avg", round(tot/1e3,1))
print("\nONE-YEAR-FORWARD (calendar 2026) indicated development by AY, avg factors:")
f9=inc[2016][9]/inc[2016][8]
tot=0; oldtot=0
for scale in (1.0,0.5):
  tot=0; oldtot=0; rows=[]
  for ay,v in inc.items():
    a=len(v)
    if a>=10: continue
    fac=f.get(a,None) if a<9 else f9
    d=v[-1]*(1+(fac-1)*scale)-v[-1]
    rows.append((ay,round(d/1e3,1)))
    tot+=d
    if ay<=2023: oldtot+=d
  print("scale",scale,rows,"TOTAL",round(tot/1e3,1),"old book AY<=2023",round(oldtot/1e3,1))
print("actual CY2025 older AYs:",88.3,"CY2024:",146.9)
print("\nOld book (AY2016-2023) outstanding at each year-end, from triangle:")
for cy in (2023,2024,2025):
    s=0; pdcy=0
    for ay in range(2016,2024):
        a=cy-ay
        if a<0: continue
        if a>=len(inc[ay]): continue
        s+=inc[ay][a]-pd[ay][a]
    # paid in CY on old book
    pp=0; dev=0
    for ay in range(2016,2024):
        a=cy-ay
        if a<1 or a>=len(pd[ay]): continue
        pp+=pd[ay][a]-pd[ay][a-1]; dev+=inc[ay][a]-inc[ay][a-1]
    print(cy,"outstanding",round(s/1e3,1),"paid in yr",round(pp/1e3,1),"dev in yr",round(dev/1e3,1))
print("\nCSV_A")
hdr=["Year of development"]+[f"AY{ay}" for ay in range(2016,2025)]
print(",".join(hdr))
for a in range(10):
    row=[str(a+1)]
    for ay in range(2016,2025):
        v=inc[ay]
        row.append(f"{v[a]/v[0]*100:.1f}" if a<len(v) else "")
    print(",".join(row))
