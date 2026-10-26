# Content Needed (Data / Artifacts Pending Verification)

This document tracks all data points, metrics, and claims removed or hidden across the public portfolio in accordance with the project's **Hard Rules** (zero invented facts, zero unverified estimates). To display any of these items on the public site, provide the verified data in `USER_FACTS` or repository documentation.

---

## 1. Publications & Citations (`index.html`, `about.html`, `assets/delvadiya_icmlde2025.bib`)
- **Paper PDF URL:** The `[PDF]` action link has been hidden because it previously linked to `assets/cv.pdf`. Supply the actual paper PDF or open-access preprint link.
- **Paper DOI:** The `[DOI]` link and previous placeholder alert have been hidden. Supply the official conference proceedings DOI upon indexing.
- **Conference Publisher:** Removed `publisher={IEEE/Springer}` guess from `delvadiya_icmlde2025.bib` and inline BibTeX blocks. Supply official publisher when proceedings are finalized.

---

## 2. MedOptm Clinical VLM (`index.html`, `projects.html`, `project-medoptm.html`)
- **Baseline Comparative Rows:** Removed `MiniGPT-4`, `LLaVA-Med`, and `BiomedCLIP-Linear` comparison rows, inference latencies (48 ms, 192 ms, 174 ms, 28 ms), and VRAM footprints (7.8 GB, 18.2 GB, 16.4 GB, 3.1 GB).
- **BLEU-4 Metric:** Hidden `[TODO: 0.28]` and placeholder baselines (`0.31`, `0.32`, `0.19`).
- **Dataset Pairs & Modality:** Removed "ROCO & MedQuAD (120k pairs)" (MedQuAD is text-only QA; VQA/image-caption pairing unverified).
- **Compute Hardware Badge:** Removed "1× NVIDIA RTX 4090 / 3080 (36 hrs)" badge until confirmed.
- **Weights Checkpoint:** Removed `[TODO: Upload to Hugging Face]` pill and claims of public checkpoints until public URL is available.
- **Verified Facts Retained:** 0.33 METEOR score, 75% token compression (256 → 64 tokens), CvT-24 encoder + 1.7B LLaMA backbone, Advisor Prof. Raj Hakani at GTU.

---

## 3. Brain MRI Surface Registration (`index.html`, `projects.html`, `project-brain-mri.html`)
- **Quantitative Benchmark Table:** Replaced with `"Quantitative results are being finalized."`
  - Removed unverified Chamfer distances: Ours `[TODO: 0.82 mm]`, SyN `[TODO: 1.45 mm]`, Rigid `[TODO: 2.38 mm]`, FreeSurfer `[TODO: 0.79 mm]`.
  - Removed unverified Surface Dice scores: Ours `[TODO: 88.4%]`, SyN `[TODO: 81.2%]`, Rigid `[TODO: 71.5%]`, FreeSurfer `[TODO: 89.1%]`.
  - Removed unverified runtimes (1.4 sec, 420 sec, 0.2 sec, 28,800 sec) and folding error claims (14 vs 0).
- **Figure 1 SVG:** Relabeled from empirical Freeview observation to "Figure 1: Schematic (illustrative)".

---

## 4. CvT-24 From First Principles (`projects.html`, `project-cvt24.html`)
- **Parameter & GFLOP Specs:** Removed claims of "exact parameter parity (20.0M)" and "4.5 GFLOPs" (these match CvT-13 rather than CvT-24).
- **Quantitative Benchmark Table:** Replaced with `"Quantitative results are being finalized."`
  - Removed `[TODO: 82.3%]`, `[TODO: 79.8%]`, `[TODO: 78.5%]` top-1 accuracy claims and throughput numbers (640, 280, 820 img/s).
  - Removed unsubstantiated claim of "superior sample efficiency over vanilla ViT".
- **Figure 1 SVG:** Relabeled to "Figure 1: Schematic (illustrative)".

---

## 5. BrainScan AI (`projects.html`, `project-brainscan-ai.html`)
- **Per-Class Metrics & Baseline Rows:**
  - Removed unverified `[TODO: 97.9%]` precision, `[TODO: 97.8%]` recall, and `[TODO: 97.8%]` F1-score pills.
  - Removed unverified baseline rows: Single-Stage VGG16 (`92.4%`), ResNet-50 (`94.1%`), and CNN from scratch (`84.6%`).
  - Table replaced with `"Quantitative results are being finalized."` (while retaining the verified 97.88% overall test accuracy in narrative and headline).
- **Dataset Claims:** Removed "multi-sequence T1/T2/FLAIR" and "heterogeneous/cross-scanner" claims pending dataset documentation.
- **Figure 1 SVG:** Relabeled from empirical 653-scan confusion matrix to "Figure 1: Schematic (illustrative)".

---

## 6. Fashion Multimodal Semantic Retrieval (`projects.html`, `project-fashion-retrieval.html`)
- **Quantitative Benchmark Table:** Replaced with `"Quantitative results are being finalized."`
  - Removed unverified Recall@1 (`64.2%`, `58.1%`, `51.4%`, `38.2%`), Recall@5 (`87.1%`, `81.3%`, `74.8%`, `59.0%`), Attribute Disambiguation (`82.4%`, `54.6%`, `48.2%`, `42.1%`), and latencies (0.78 ms, 0.72 ms, 0.74 ms, 1.20 ms).
- **Figure 1 SVG:** Relabeled from empirical error elimination comparison to "Figure 1: Schematic (illustrative)".

---

## 7. Industry Experience & Unprovable Claims (`about.html`, `research.html`, `index.html`)
- **Infosys Springboard:** Removed from research stream, about page, and `news.json` (absent from CV; exact dates and details unconfirmed).
- **Project 06 (Autonomous Research Pipeline):** Removed from `projects.html` (no public repository; unverifiable claims).
- **Academic Standing Claims:** Removed "Consistently ranked among the top percentile..." and "Top Academic Standing" phrasing (retained verified CGPAs: 9.35 and 9.32).
- **Authorship Phrasing:** Reconciled "Lead Undergraduate Author" to "First author" / "Author" to match CV.
- **Footer Labels:** Replaced "Verified Profiles" with "Profiles" across all pages.
- **Figures / Screenshots:** If real screenshots are available in `/assets/figures/`, provide them with file names to replace illustrative SVG schematics.

---

## 8. audria.tech placeholder metrics (`research.html`) - REPLACE BEFORE PUBLISHING
Search for `data-ph` in `research.html`. These values are random test numbers, highlighted with a dashed yellow style so they cannot be missed:
- `120 hours` (audio evaluated), `3.2x` (speedup of the linear ISA pipeline), `18.4%` to `12.1%` (diarization error rate before and after).
- Also confirm: exact start date (currently "Sep 2026"), the expansion of "ISA", and whether the evaluation set may be described as "internal".
- `verify_site.py` fails while any `data-ph` marker remains, so it doubles as a publish gate. After replacing the numbers, also remove the `class="ph" data-ph` wrapper.

---

## 9. Redesign follow-ups (Warm Paper Lab)
- **Infosys Springboard** is back (Nov 2025 to Jan 2026), taken from the resume, with the certificate link. No GitHub repo is linked because none was identified. Add the repo URL if one exists.
- **Accuracy figures to reconcile:** the resume says 97.88% (GTU brain tumor entry, ICMLDE 2025) and 98.77% (Elsevier Procedia Computer Science paper). If these are the same paper, pick one number.
- **Missing links:** the resume marks the Hugging Face dataset, the Elsevier paper and the n8n article-automation project with link icons, but the URLs were not available. Add them to `index.html`/`projects.html` (via `_build/build.py`).
- **MedOptm** is shown under Projects only, per the earlier decision, although the resume lists it under experience.
- **Phone number** from the resume is intentionally not published.
- Pages are generated by `_build/build.py`. Edit it and re-run, or edit the HTML directly.
