import os
HERE = os.path.dirname(os.path.abspath(__file__))
# earned surplus at James River Insurance, run forward under different assumptions. my estimates, base case is in statutory_lock.py
T=0.21
adj={2027:38.0,2028:34.0}; int_at=22.4*(1-T); need=22.4+7.875+1.85
def run(dev,noi,share,em):
    u=142.0; out=[]
    for y in (2026,2027,2028):
        earn=((15.8+21.0*noi) if y==2026 else adj[y]*noi)+int_at
        earn*=share
        u+=earn-dev*(1-T)*em[y]*share-(need-30.0 if y==2026 else need)
        out.append(round(u,1))
    return out
EM={"front 30/35/20":{2026:.30,2027:.35,2028:.20},"reported pattern 30/23/17":{2026:.301,2027:.226,2028:.166}}
for en,em in EM.items():
  for share in (0.60,0.75,0.90):
    print(en,"share",share," Base",run(126.7,1.0,share,em)," Bear",run(268.5,0.85,share,em)," Distress",run(306.5,0.70,share,em))
