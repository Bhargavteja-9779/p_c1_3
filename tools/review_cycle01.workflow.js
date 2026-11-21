export const meta = {
  name: 'review-cycle-01',
  description: 'Seven independent reviewer lenses plus a citation audit of the first complete manuscript draft',
  phases: [{ title: 'Review', detail: '7 reviewer lenses + citation/claim audit, each writes REVIEW/cycle01/<lens>.md' }],
}
const ROOT = '/home/user/p_c1_3/Target_Journal_Submission'
const CTX = `You are reviewing a manuscript prepared for submission to the journal Battery Energy (Wiley).
Files (all under ${ROOT}):
- manuscript/Draft_Manuscript.md (rendered main text; figures in figures/*.png, read them as images when relevant)
- manuscript/Supporting_Information.md (rendered SI)
- manuscript/src/*.md (sources with {{KEY}} number tokens; numbers come from results/manuscript_numbers.json)
- code/ (package batscreen under code/src, experiments in code/experiments/suite.py, analysis.py, figures.py, run_all.py, tests/)
- results/ (raw split-level CSVs in results/raw, statistics.json, metrics.json), tables/*.csv|md
- literature/references_verified.json (bibliography), literature/research_design.md (pre-registered design)
Do NOT edit any manuscript, code or result file. Do not run the full experiment suite (it takes hours); small read-only python checks against the result CSVs are fine.
Write your full review as Markdown to ${ROOT}/REVIEW/cycle01/LENSFILE.md (summary, recommendation, numbered issues with location, evidence and concrete fix). Then return the structured issue list. Be specific and evidence-based: cite section/line, file, number. Severity: critical = would cause rejection or a wrong claim; major = must fix before submission; minor = should fix. Mark requires_rerun=true only if fixing needs new or repeated experiments.`
const LENSES = [
  ['R1_statistics', 'Reviewer 1, statistician / conformal-prediction expert. Check Proposition 1 and its proof, the class-conditional calibration, the trajectory-maximum construction, normalisation, finite-sample claims, the PAC variant, the confidence intervals and the paired tests (Wilcoxon, Holm, rank-biserial, cell bootstrap). Verify the code in code/src implements exactly what the Methods state (ranks, ties, the order statistic, the "never decides" case).'],
  ['R2_battery_domain', 'Reviewer 2, battery-testing and degradation expert. Judge practical relevance: lifetime/end-of-life definitions, choice of L*, cost model (cell-cycles vs channel time, RPTs), datasets (MATR/CLO, HUST) and their cleaning, features, the realism of exchangeability in production screening, chemistry limitations, and whether the conclusions for practitioners are justified.'],
  ['R3_evaluation_leakage', 'Reviewer 3, ML evaluation methodologist. Hunt for data leakage and evaluation flaws in code/src and code/experiments: split construction, feature computation (look-ahead beyond checkpoint k, smoothing windows), preprocessing fitted on test data, normalisation scale s_k estimated on which cells, hyper-parameter selection, seeds, how time saved and error rates are computed (denominators, cells with lifetime < checkpoint), E5/E9/E10 split functions. Read the code carefully and give file:line evidence.'],
  ['R4_reproducibility', 'Reviewer 4, reproducibility and code-quality reviewer. Check code/README.md, requirements, configs, run_all.py, tests (you may run `cd ${ROOT}/code && python -m pytest -q -x tests` if it finishes in a few minutes), determinism, documentation of every reported number, the Data/Code Availability statements, licences, and whether a third party can regenerate tables/figures. Check that results/run_config.json and logs match the manuscript.'],
  ['R5_claims_consistency', 'Reviewer 5, results-consistency auditor. For every quantitative claim and every qualitative comparison in Abstract, Results, Discussion and Conclusions of Draft_Manuscript.md, check it against tables/*.csv, results/raw and results/manuscript_numbers.json (recompute a sample directly from raw CSVs with python). Flag wrong numbers, over-claims, claims of significance without a test, inconsistent section cross-references, figure/table captions that do not match the plotted data.'],
  ['R6_presentation', 'Reviewer 6, editor for clarity, structure and figures. Assess the Battery Energy fit and author guidelines (structure, abstract length, keywords, statements), readability for battery engineers, notation consistency, equation numbering, figure quality (open the PNGs: legibility, colours, labels, panel letters, captions), table design, redundancy between main text and SI, and length. Suggest concrete edits.'],
  ['R7_novelty_related', 'Reviewer 7, senior skeptical reviewer on novelty and positioning. Compare the contribution with related work on early cycle-life prediction, uncertainty quantification, conformal prediction (including sequential/anytime-valid, conformal for time series, early-stopping/selection guarantees, conformal classification and Neyman-Pearson classification) and sequential testing. You may use web search to find closely related prior work missing from the reference list. Decide whether the novelty claims are accurate and whether key prior work is missing.'],
  ['A1_citation_audit', 'Citation and claim auditor. For every entry in literature/references_verified.json and every [@key] citation in manuscript/src/*.md: verify that the reference exists with the stated authors, title, venue, year and DOI (use web search / fetch the DOI landing pages), and that the sentence citing it states something the source actually supports. Report non-existent or mis-described references, wrong metadata, unsupported attributions, and claims that need a citation but have none.'],
]
const SCHEMA = { type: 'object', properties: {
  recommendation: { type: 'string', enum: ['accept', 'minor_revision', 'major_revision', 'reject'] },
  summary: { type: 'string' },
  issues: { type: 'array', items: { type: 'object', properties: {
    id: { type: 'string' }, severity: { type: 'string', enum: ['critical', 'major', 'minor'] },
    location: { type: 'string' }, issue: { type: 'string' }, evidence: { type: 'string' },
    fix: { type: 'string' }, requires_rerun: { type: 'boolean' } },
    required: ['id', 'severity', 'location', 'issue', 'evidence', 'fix', 'requires_rerun'] } } },
  required: ['recommendation', 'summary', 'issues'] }
phase('Review')
const res = await parallel(LENSES.map(([name, lens]) => () =>
  agent(`${lens}\n\n${CTX.replace('LENSFILE', name)}`, { label: name, phase: 'Review', schema: SCHEMA })
    .then(r => r ? { reviewer: name, ...r } : null)))
const ok = res.filter(Boolean)
log(`${ok.length}/${LENSES.length} reviews returned`)
return ok