import os
HERE=os.path.dirname(os.path.abspath(__file__))
# FY2025 10-K, E&S excluding commercial auto: cumulative incurred and paid by accident year (USD 000), before E&S ADC
exec(open(os.path.join(HERE,"jrvr_incurred_fy2025.py")).read().split('print("totals')[0])
inc_latest=sum(v[-1] for v in inc.values()); paid_latest=sum(paid.values())
open_before=inc_latest-paid_latest
recoverable_es_adc=434562   # 10-K: "Reinsurance recoverable for E&S ADC"
pre_2016=16282              # 10-K: outstanding prior to 2016, net
net=open_before-recoverable_es_adc+pre_2016
print(f"incurred {inc_latest:,} - paid {paid_latest:,} = open before E&S ADC {open_before:,} (10-K prints 1,332,506)")
print(f"{open_before:,} - {recoverable_es_adc:,} + {pre_2016:,} = {net:,} (10-K prints 914,226)")
assert open_before==1332506 and net==914226
old=sum(inc[ay][-1]-paid[ay] for ay in range(2016,2024)); print(f"open on AY2016-2023 before the cover: {old/1e3:.1f}m")
