# jrvr-reserve-rebuild

Data and code behind my Seeking Alpha piece on James River Group (JRVR), "James River: The Old Book Is Still Short, And The Cushion Is Locked", September 2026.

James River doesn't publish a reported-loss triangle for its E&S casualty book. Every 10-K prints the pieces though. For each accident year you get incurred losses and IBNR. Take one from the other and you have what adjusters have actually reserved on real claims. I lined up ten years of filings, FY2016 to FY2025, and built the triangle from that. Anything in the article that comes out of a model comes out of the scripts here.

It's all public data. If you think I got something wrong, rerun it and tell me.

Not investment advice. I have no position in JRVR.

## Running it

Python 3.10 or later, plus numpy and scipy.

    pip install -r requirements.txt
    python3 scripts/backtest_reported.py

The scripts find their inputs in their own folder, so you can run them from anywhere. My outputs from 24 Sep 2026 are in results/. Yours should match line for line. I ran it on Python 3.10.12, numpy 2.2.6 and scipy 1.15.3.

## What each script does

- tieout.py checks the triangle against the 10-K. 1,332.5m open, less 434.6m recoverable under the State National cover, plus 16.3m on pre-2016 years, gives the 914.2m of net reserves the 10-K prints. It throws an error if that doesn't tie.
- chain_ladders.py runs reported, paid and incurred chain ladders on the FY2025 filing.
- backtest_reported.py reruns the method using only what was public at the end of 2021, 2022 and 2023. At the end of 2022 it said 2016-21 was 229.9m short. Those years have added 244.1m since.
- backtest_paid.py does the same for the paid method, using the paid triangle in the FY2022 10-K. 181.2m indicated at a 7% tail. It also has the payment-speed checks.
- distribution.py is the Mack chain ladder for the range, plus an ODP bootstrap on paid as a cross-check.
- calendar_year_test.py is Mack's 1997 test for calendar-year effects. Both triangles fail it. That's where the 20m / 228m fork in the article comes from.
- peers.py and kinsale_cuts.py run the same back-test on Kinsale, RLI, Markel and Skyward, and compare second-year cuts (Bowhead included, it only has years from 2021).
- retention_timeline.py works out how much of the 716.6m retention has been paid (551.0m and 551.1m, two different ways) and when State National starts paying.
- statutory_lock.py and surplus_sensitivity.py cover when the special surplus unlocks and the earned-surplus run-forward.
- earnings_bridge.py shows what E&S combined ratio each 2027 earnings number needs.
- comps.py is price to tangible book against ROE for eight listed insurers.
- model.py has the four scenarios and the 4.28 target.
- jrvr_triangles.py and jrvr_incurred_fy2025.py hold the transcribed data. mack_bootstrap.py is a working file I used early on, left in because it fed the rest.

The same inputs are in data/ as CSV if you'd rather use a spreadsheet.

## Where the numbers come from

- James River 10-Ks, FY2016 to FY2025, claims development note: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001620459&type=10-K
- FY2022 10-K (paid triangle): https://www.sec.gov/Archives/edgar/data/1620459/000162045923000026/jrvr-20221231.htm
- FY2025 10-K: https://www.sec.gov/Archives/edgar/data/1620459/000162045926000009/jrvr-20251231.htm
- Q2 2026 10-Q: https://www.sec.gov/Archives/edgar/data/1620459/000162045926000045/jrvr-20260630.htm
- Q2 2026 results release: https://www.sec.gov/Archives/edgar/data/1620459/000162045926000044/a2q26jrvrpressrelease.htm
- James River Insurance Company 2025 statutory statement, Ohio Department of Insurance: https://legacy.insurance.ohio.gov/FRAnnuals/2025/Annual/KS/12203A2025KS.pdf
- NAIC Issue Paper 75 on retroactive reinsurance: https://content.naic.org/sites/default/files/inline-files/075_m.pdf
- Ohio Revised Code 3901.34: https://codes.ohio.gov/ohio-revised-code/section-3901.34
- Peer triangles are from the FY2025 10-Ks of Kinsale (casualty occurrence), RLI (casualty primary occurrence), Skyward (multi-line solutions), Bowhead (casualty) and Markel (insurance segment).
- Peer valuations are from stockanalysis.com on 23 Sep 2026, checked against finviz.

## Things to be careful with

The reported triangle depends on how the company sets case reserves, and both triangles fail the calendar-year test, so read the output as a range. Figures are as printed in each year's filing and later filings sometimes restate a year slightly. The covenant numbers are my reconstruction from public filings, and the credit agreement's own definitions could differ. Payout pace, the 75% share, the earnings path and the scenario weights are my calls. They're written out at the top of the scripts that use them.

## License

The code is MIT licensed, see LICENSE. The data is transcribed from public filings, so use it however you like. Just credit the filings and link back here.

## Corrections

If I got something wrong, say so in the comments on the article or open an issue here. I'll log the fix below with the date and leave the old number up.

None so far.
