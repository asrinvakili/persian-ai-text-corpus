# Datasheet — Persian AI-Text Corpus

Following the *Datasheets for Datasets* template (Gebru et al., 2021).

---

## Motivation

**For what purpose was the dataset created?**
To enable empirical research on detecting AI-generated text in Persian, a low-resource language for this task. Existing AI-text-detection benchmarks are dominated by English and Chinese; Persian and other Perso-Arabic-script languages lack comparable resources.

**Who created the dataset?**
Asrin Vakili, Department of Computer Engineering, National University of Skills, Tehran.

**What support was needed?**
Wikipedia API for human text; AvalAI gateway (https://avalai.ir) for access to commercial LLMs.

---

## Composition

**What do the instances represent?**
Each instance is a short Persian text (40–250 words) in encyclopedic style.

**How many instances are there?**
4,000 total: 1,000 human-written, 3,000 AI-generated.

**Does the dataset contain all possible instances, or is it a sample?**
A stratified sample. 1,000 topics were drawn from five domains, with a cap on the number of articles per Wikipedia subcategory to prevent over-representation.

**What data does each instance consist of?**
A text body plus metadata fields (see schema in the README). Every record includes `id`, `human_id`, `label`, `source`, `category`, `subcategory`, `title`, `num_words`, and `text`. AI records additionally include `model`, `target_words`, and `generation_date`. Human records additionally include `revision_id`, `revision_date`, and `url`.

**Is there a label or target?**
Yes. `label`: 0 = human-written, 1 = AI-generated. The `model` field identifies the specific LLM for AI records.

**Are relationships between individual instances made explicit?**
Yes, via `human_id`. Each human record's `human_id` equals its own `id`. Each AI record's `human_id` references the human record it was generated from. A given `human_id` always has exactly four records: one human, three AI (one per generator model).

**Are there recommended data splits?**
Yes. `data/splits/{train,val,test}.jsonl` provide a 70/10/20 stratified split by (label, category, model), with seed 42. Researchers can rebuild custom splits from `data/full/` if needed.

---

## Collection Process

**How was the human data acquired?**
Via the Persian Wikipedia API, with these constraints:

- **Pre-2020 only.** Each article revision was restricted to those committed before 31 December 2019, predating widespread LLM availability. This ensures human authorship.
- **Stratified sampling.** Five top-level domains were defined (theoretical sciences, engineering, medical, humanities, history & biography). Within each, articles were drawn from multiple subcategories with a 15-article cap per subcategory to prevent over-representation of large categories.
- **Quality filters.** Articles below 40 words or above 300 words were excluded. Reference markers like `[1]` and parenthetical question marks were stripped.

**How was the AI data generated?**
Three LLMs were called via the AvalAI gateway:

- `deepseek-v3.1` (DeepSeek)
- `gpt-4o-mini` (OpenAI)
- `gemini-2.5-flash-lite` (Google)

For each of the 1,000 human topics, each model produced one Persian text on the same topic with the same target length.

**Topic anchoring.**
Persian named entities can mislead LLMs (e.g., "روز مول" — Mole Day in chemistry — was initially generated as content about Rumi the poet). To prevent this, the first 15 words of each human article were passed to the model as a "topic anchor," then the anchor was stripped from the output if echoed verbatim. Human and AI versions therefore share no sentences.

**Over what timeframe was the data collected?**
Human revisions: pre-December 2019. AI generation: 16–17 June 2026.

---

## Preprocessing

**What preprocessing was done to the human text?**

- Removed numbered references (`[1]`, `[12]`, ...)
- Removed parenthetical question marks (Wikipedia uncertainty markers)
- Collapsed repeated whitespace
- Truncated texts longer than 300 words
- Discarded texts shorter than 40 words

**Was the raw data saved?**
Not directly, but each human record includes `revision_id` and `url`, so the raw revision can always be retrieved from Wikipedia.

---

## Uses

**For what tasks is this dataset suitable?**

- Training and evaluating Persian AI-text detectors (e.g., ParsBERT fine-tuning).
- Cross-generator generalization studies.
- Robustness benchmarks (e.g., paraphrasing, back-translation).
- LLM stylometry in Persian.

**For what tasks should it not be used?**

- Training generative LLMs (the short, encyclopedic texts are unsuitable for fine-tuning).
- Conclusions about informal or dialectal Persian (out of scope).
- Forensic or legal applications (this is a research benchmark, not a production tool).

---

## Limitations

**Domain bias.** Encyclopedic prose only.

**Generator coverage.** Three frontier LLMs available via AvalAI in June 2026. Notable absences: Claude, Llama family, Persian-native LLMs (e.g., MaralGPT, Aya).

**Time snapshot.** LLMs evolve; this captures a single moment.

**Class imbalance.** 1:3 ratio is inherent to the matched design and should be managed during training (see README).

**Medical subcategory diversity.** The medical domain had fewer candidate articles (669) than other domains, leading to slightly higher concentration in some subcategories.

---

## Ethical Considerations

**Privacy.** All texts are from public Wikipedia and contain no personal information.

**Misuse potential.** The dataset is designed to train detectors, not generators. Its structure (short encyclopedic snippets) is not suitable for fine-tuning generative models.

**Transparency.** Every AI text is explicitly labeled with its generator model and generation date.

**Provider terms.** Use of AI-generated text is subject to each provider's terms of service. Released for academic research only.

---

## Distribution

**License.**
- Code: MIT.
- Human texts: CC BY-SA 4.0 (inherited from Wikipedia).
- AI texts: subject to provider terms (OpenAI, DeepSeek, Google).

**Format.** JSONL with UTF-8 encoding and LF line endings.

**Hosting.** GitHub repository.

---

## Maintenance

**Maintainer.** Asrin Vakili (Department of Computer Engineering, National University of Skills, Tehran).

**Versioning.** Current version 1.0 (June 2026). Changes will be tracked in a CHANGELOG.

**Feedback.** Via GitHub Issues.

---

## References

Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., & Crawford, K. (2021). Datasheets for Datasets. *Communications of the ACM*, 64(12), 86–92.
