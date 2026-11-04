# TruthLens — Fake News Detector

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

TF-IDF (word unigrams, sublinear TF, L2) + logistic regression (C=1.0) trained on 188 hand-written headlines (97 real, 91 fake; 889 vocabulary words, seed 42).

- 5-fold CV accuracy: 94.7%, AUC: 1.00 (always-real baseline: 51.6%)
- Live demo: https://truthlens.vercel.app (runs fully in the browser — no backend)
- `train.py` trains the model and writes `model.json`; `index.html` applies the same weights in JavaScript.
