from pptx import Presentation
from pptx.util import Inches, Pt
import sys
DOMAIN = sys.argv[1] if len(sys.argv) > 1 else "truthlens.vercel.app"
prs = Presentation(); prs.slide_width = Inches(13.33); prs.slide_height = Inches(7.5)
def add(i, title, lines):
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = title
    tf = s.placeholders[1].text_frame; tf.word_wrap = True
    for j, ln in enumerate(lines):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.text = ln; p.font.size = Pt(20); p.space_after = Pt(10)
add(0, "TruthLens — Fake News Detector", ["An AI/ML project by Vikranth Reddy", "B.Tech CSE (AI & ML), 2nd Year — Woxsen University", "TF-IDF + logistic regression that scores a headline as real or fake, right in your browser"])
add(1, "The Problem", ["Fake headlines spread faster than real news on social media", "Sensational wording tricks readers — miracle cures, secret plans, shocking claims", "Reading every headline carefully takes time, and most people share before checking", "An automatic first check helps readers pause and verify before believing or sharing"])
add(2, "The Solution — TruthLens", ["Paste any news headline into the browser demo", "A trained model returns a fake-news percentage and a verdict", "Below 50% looks real, above 50% looks fake", "Runs fully in the browser — no backend, no waiting"])
add(3, "Tech Stack", ["Python + scikit-learn: dataset and model training", "TF-IDF (word unigrams, sublinear TF, L2 normalisation) + logistic regression (C = 1.0)", "HTML, CSS and vanilla JavaScript for the interactive demo", "GitHub for source control, Vercel for free hosting"])
add(4, "Architecture", ["Dataset: 188 hand-written headlines — 97 real, 91 fake, 889-word vocabulary", "Text -> tokens -> TF-IDF weights -> logistic regression -> model.json", "model.json ships with the site; JavaScript applies the same formula and a sigmoid", "Training script: train.py; site generator: gen_site.py"])
add(5, "Live Demo", ["Try it: paste a headline and press Check Headline", "Real example: University results for final semester examinations published on official portal -> about 30.11% fake (looks real)", "Fake example: Shocking scientists confirm drinking lemon water cures all cancers overnight -> about 77.71% fake", f"Demo: https://{DOMAIN}"])
add(6, "Results", ["5-fold cross-validation accuracy: 94.7%", "AUC: 0.996 — the model ranks fake headlines well above real ones", "Baseline (always guessing real): 51.6% accuracy", "Browser demo matches Python predictions exactly on all test samples"])
add(7, "Future Scope", ["Train on a larger, real-world labelled news dataset", "Add source-credibility and author-history features", "Try character n-grams to catch sensational phrasing better", "Add a browser extension that scores headlines as you scroll"])
add(8, "Thank You", ["TruthLens — Fake News Detector", "Vikranth Reddy, B.Tech CSE (AI & ML), Woxsen University", "Source: github.com/HVRGAMING2705/truthlens", "Questions welcome!"])
prs.save("/home/hatch/workspace/goals/daily-ai-ml-project-factory/files/AIML_TruthLens_2026-11-04.pptx")
print("slides:", len(prs.slides._sldIdLst))
