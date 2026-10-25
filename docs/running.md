# How to run

Offline, CPU only, free. Python 3.12+.

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
pytest -q                          # full suite
python scripts/count_tests.py      # prints the real test count
recfair demo --board               # 400 candidates + 4,000 scale check, about 15 s
recfair demo --n 1000 --seed 3 --out /tmp/run   # other sizes and seeds
python scripts/render_docs.py      # write numbers into README/docs
python scripts/render_docs.py --check
python scripts/check_brands.py
```

Set `RECFAIR_HMAC_KEY` to your own secret before using real-shaped data; the built-in key is for the demo only. There is no cloud step.
