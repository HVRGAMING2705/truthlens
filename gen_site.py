import json
m = json.load(open("model.json"))
vocab, idf, coef, icpt = m["vocabulary"], m["idf"], m["coef"], m["intercept"]
mt = m["metrics"]
acc, auc, base = mt["cv_accuracy"], mt["cv_auc"], mt["baseline_accuracy"]
DOMAIN = "truthlens.vercel.app"
JS_MODEL = f"""const VOCAB = {json.dumps(vocab)};
const IDF = {json.dumps(idf)};
const COEF = {json.dumps(coef)};
const INTERCEPT = {icpt};
function fakeProb(text){{
  const toks = (text.toLowerCase().match(/[a-z0-9_]{{2,}}/g) || []);
  const counts = {{}};
  toks.forEach(t => {{ if (t in VOCAB) counts[t] = (counts[t] || 0) + 1; }});
  const vals = {{}}; let norm = 0;
  for (const t in counts) {{
    const v = (1 + Math.log(counts[t])) * IDF[VOCAB[t]];
    vals[t] = v; norm += v * v;
  }}
  norm = Math.sqrt(norm);
  let z = INTERCEPT;
  if (norm > 0) for (const t in vals) z += (vals[t] / norm) * COEF[VOCAB[t]];
  return 1 / (1 + Math.exp(-z)) * 100;
}}"""
index = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TruthLens — Fake News Detector | AI/ML Project</title>
<meta name="description" content="TruthLens scores a headline as real or fake using a TF-IDF + logistic regression model trained on 188 hand-written headlines. Paste a headline and get an instant verdict in your browser.">
<link rel="canonical" href="https://{DOMAIN}/">
<meta property="og:title" content="TruthLens — Fake News Detector">
<meta property="og:description" content="Paste a headline and instantly check whether it looks real or fake, with a real trained ML model running in your browser.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://{DOMAIN}/">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="TruthLens — Fake News Detector">
<meta name="twitter:description" content="TF-IDF + logistic regression fake news detector. Try the live demo in your browser.">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebApplication","name":"TruthLens","applicationCategory":"NewsApplication","description":"Fake news detector using TF-IDF and logistic regression.","url":"https://{DOMAIN}/"}}</script>
<style>
body{{font-family:Arial,Helvetica,sans-serif;color:#000;background:#fff;max-width:720px;margin:0 auto;padding:24px;line-height:1.5}}
h1{{font-size:2em}} label{{display:block;margin:12px 0 4px;font-weight:bold}}
textarea{{width:100%;padding:10px;font-size:16px;border:1px solid #000;border-radius:4px;box-sizing:border-box}}
button{{margin-top:16px;margin-right:8px;padding:12px 24px;font-size:17px;background:#000;color:#fff;border:none;border-radius:4px;cursor:pointer}}
#result{{margin-top:24px;padding:20px;border:2px solid #000;border-radius:8px;display:none}}
#result b{{font-size:2em}}
.note{{color:#333;font-size:.95em}} code{{background:#f2f2f2;padding:2px 5px}}
</style>
</head>
<body>
<h1>&#128270; TruthLens — Fake News Detector</h1>
<p class="note">A 2nd-year B.Tech AI/ML project by Vikranth Reddy. A TF-IDF + logistic regression model trained on 188 hand-written headlines ({mt['n_real']} real, {mt['n_fake']} fake, {mt['vocab']} words) scores a headline as real or fake. 5-fold CV: <b>accuracy = {acc:.1%}</b>, AUC = {auc:.2f} vs an always-real baseline of {base:.1%}.</p>
<label>Paste a news headline</label>
<textarea id="headline" rows="3">Government announces new railway line connecting Hyderabad and Bengaluru</textarea>
<button onclick="predict()">Check Headline</button>
<button onclick="tryFake()">Try a fake one</button>
<div id="result"></div>
<p class="note">How it works: your headline is split into words, each word gets a TF-IDF weight (common words count less, rare words count more), the weights are multiplied by the model&apos;s learned coefficients and passed through a sigmoid. The exact same weights run in this page and in the Python training script (<code>train.py</code>), so the browser result matches the trained model.</p>
<p class="note">Try it: a real-style headline — &ldquo;University results for final semester examinations published on official portal&rdquo; &rarr; about 30.1% fake (looks real). A fake-style one — &ldquo;Shocking scientists confirm drinking lemon water cures all cancers overnight&rdquo; &rarr; about 77.7% fake.</p>
<p><a href="https://github.com/HVRGAMING2705/truthlens">View source on GitHub</a></p>
<script>
{JS_MODEL}
function show(){{
  const p = fakeProb(document.getElementById("headline").value);
  const verdict = p >= 50 ? "&#9888; LOOKS FAKE — treat this headline with suspicion and verify it from a trusted source." : "&#9989; LOOKS REAL — this headline reads like genuine news.";
  const el = document.getElementById("result");
  el.style.display = "block";
  el.innerHTML = "<b>" + p.toFixed(2) + "% fake</b><br>" + verdict + "<br><span class=note>This is a classroom demo trained on hand-written headlines, not a fact-checking service.</span>";
}}
function predict(){{ show(); }}
function tryFake(){{ document.getElementById("headline").value = "Shocking scientists confirm drinking lemon water cures all cancers overnight"; show(); }}
</script>
</body>
</html>
"""
open("index.html", "w").write(index)
vercel = {
 "headers": [{"headers": [
   {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload"},
   {"key": "X-Content-Type-Options", "value": "nosniff"},
   {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
   {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
   {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"},
   {"key": "Cross-Origin-Opener-Policy", "value": "same-origin"},
   {"key": "Access-Control-Allow-Origin", "value": f"https://{DOMAIN}"},
   {"key": "Content-Security-Policy", "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; base-uri 'self'; frame-ancestors 'self'"}],
  "source": "/(.*)"}]}
open("vercel.json", "w").write(json.dumps(vercel, indent=1))
open("404.html", "w").write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Page Not Found — TruthLens</title><style>body{{font-family:Arial,sans-serif;color:#000;max-width:640px;margin:60px auto;padding:24px}}</style></head><body><h1>404 — Page not found</h1><p>This page does not exist on TruthLens.</p><p><a href="https://{DOMAIN}/">Back to TruthLens</a></p></body></html>""")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
open("sitemap.xml", "w").write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://{DOMAIN}/</loc></url></urlset>
""")
open("README.md", "w").write(f"""# TruthLens — Fake News Detector

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

TF-IDF (word unigrams, sublinear TF, L2) + logistic regression (C=1.0) trained on 188 hand-written headlines ({mt['n_real']} real, {mt['n_fake']} fake; {mt['vocab']} vocabulary words, seed 42).

- 5-fold CV accuracy: {acc:.1%}, AUC: {auc:.2f} (always-real baseline: {base:.1%})
- Live demo: https://{DOMAIN} (runs fully in the browser — no backend)
- `train.py` trains the model and writes `model.json`; `index.html` applies the same weights in JavaScript.
""")
samples = json.load(open("parity_samples.json"))
parity = JS_MODEL + "\n" + "\n".join(
    f"console.log(JSON.stringify({{text: {json.dumps(s['text'])}, js: fakeProb({json.dumps(s['text'])}), py: {s['prob_fake_pct']}}}));"
    for s in samples)
open("parity.js", "w").write(parity)
print("site files written, acc", acc, "auc", auc)
