# Seed Corpus Attribution

The four documents in this directory are extracted-text versions of open-access
articles from the main `ai-research-assistant` corpus. They're the only entries
in the full 19-document corpus (see `corpus_manifest.json`) licensed plain
CC BY 4.0 — no NC (non-commercial) or ND (no-derivatives) restriction — which
is what makes them safe to commit directly to this repo, unlike the rest of
the corpus, which carries mixed licensing and must be downloaded individually
per the main README.

These four are ingested automatically on first run against an empty
collection (see `_seed_if_empty()` in `main.py`), giving a working demo with
zero manual setup. Set `SEED_ON_EMPTY=false` to disable this — e.g. when
ingesting the full 19-document corpus locally via `ingest_corpus.py` instead.

Text extracted and added to this repo: 2026-08-18.

## onco-lung-liquidbiopsy.txt

- **Title:** Liquid biopsy biomarkers for cancer detection, treatment monitoring, and clinical outcome prediction
- **Authors:** Akshee Batra, Xena Zheng, Dan Morgenstern-Kaplan, Carey C. Thomson, Gilberto Lopes, Chinmay Jani
- **Journal:** Frontiers in Cell and Developmental Biology
- **DOI:** [10.3389/fcell.2026.1874565](https://doi.org/10.3389/fcell.2026.1874565)
- **License:** CC BY 4.0
- **Summary:** Narrative review of liquid biopsy's role across the lung cancer continuum — screening and diagnosis, plasma-based genotyping in advanced NSCLC, ctDNA-based minimal residual disease detection, and resistance profiling at progression. Covers cfDNA methylation, fragmentomics, and circulating tumor RNA as complementary modalities (especially when tumor shedding is low), CSF ctDNA for CNS metastases, liquid-vs-tissue biopsy concordance, and cost/access barriers. Notes no multi-cancer early detection test has yet shown a mortality benefit.

## cardio-cad-ct-angiography.txt

- **Title:** Development of a MACE risk prediction model based on CCTA-derived quantitative parameters: a proof-of-concept study
- **Authors:** Tianyang Gao, Mingyu Zou, Wei Zhou, Yu Zhong, Shu Zhou, Sen Xu, Libo Zhang
- **Journal:** Frontiers in Cardiovascular Medicine
- **DOI:** [10.3389/fcvm.2026.1884303](https://doi.org/10.3389/fcvm.2026.1884303)
- **License:** CC BY 4.0
- **Summary:** Retrospective cohort study (280 CAD patients, derivation; 288, external validation) building a nomogram from CCTA-derived quantitative parameters — plaque length, fibrous plaque volume, plaque burden, coronary calcium score, perivascular fat attenuation, minimal lumen area — to predict 1-year major adverse cardiovascular events (MACE). Combined model reached AUC 0.936 (derivation) and 0.932 (external validation); framed by the authors as proof-of-concept given a short follow-up window and low events-per-variable ratio.

## outlier-microbiome-tuberculosis.txt

- **Title:** Harnessing the gut microbiome to combat tuberculosis: a technological and clinical review
- **Authors:** Weiguo Sun, Meng Xiao, Syed Luqman Ali, Chanyuan Jin, Asifullah Khan, Shakirullah, Ruizi Ni, Yajing An, Mingming Zhang, Yuan Tian, Shradha Kaushik, Yuhang Zhang, Wenping Gong
- **Journal:** Frontiers in Cellular and Infection Microbiology
- **DOI:** [10.3389/fcimb.2026.1847443](https://doi.org/10.3389/fcimb.2026.1847443)
- **License:** CC BY 4.0
- **Summary:** Technological and clinical review of the gut microbiome's role in tuberculosis via the gut–lung axis — reduced microbial diversity and enriched pro-inflammatory taxa in TB patients, omics- and AI-driven biomarker discovery for diagnosis and outcome prediction, and microbiome-targeted interventions (probiotics, dietary adjustment, fecal microbiota transplantation). Also discusses translational limitations: unvalidated causal mechanisms, delayed clinical translation of biomarkers, and poor accessibility of these technologies in resource-scarce regions.

## diabetes-cardiovascular-outcomes.txt

- **Title:** Sleep loss as a cardiometabolic risk factor: a narrative review of clinical and public health implications
- **Authors:** Firas K. Ghanem, Hrayr Attarian, Zeina Al-Khalil, Colette S. Kabrita
- **Journal:** Journal of Clinical Sleep Medicine
- **DOI:** [10.1007/s44470-026-00144-1](https://doi.org/10.1007/s44470-026-00144-1)
- **License:** CC BY 4.0
- **Summary:** Narrative review (not systematic — no PRISMA protocol) synthesizing 102 studies on how sleep deprivation, impaired sleep architecture, and circadian misalignment affect cardiovascular and metabolic regulation via autonomic, hormonal, inflammatory, and behavioral pathways. Covers sympathetic activation and cortisol elevation, leptin/ghrelin/endocannabinoid disruption driving weight gain and insulin resistance, and shift-work circadian misalignment. Cites Sadhu et al. on daylight saving time transitions and MI risk (24% increase after the spring transition, 21% decrease after the fall transition), Cappuccio et al. on short-sleep cardiovascular risk, and Leproult et al. on sleep extension and insulin sensitivity.