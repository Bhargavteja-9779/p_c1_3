[Corresponding author name]
[Department], Vellore Institute of Technology
Vellore 632014, Tamil Nadu, India
[E-mail] · [Telephone]

[Date]

The Editor-in-Chief
*Battery Energy*
John Wiley & Sons

Dear Editor,

**Submission of an original research article: "Stopping Cycle-Life Tests Early With Distribution-Free Error Control: Sequential Screening of Lithium-Ion Cells Calibrated on Truncated Test Campaigns"**

On behalf of all authors, I submit the above manuscript for consideration as a Research Article in *Battery Energy*.

Cycle-life testing is the slowest step in developing and qualifying lithium-ion cells. Early-cycle lifetime predictions are increasingly used to shorten it, but when they are used to pass or reject cells, the error rate of those decisions is neither specified nor controlled — and the common practice of re-checking a prediction as cycling proceeds and stopping at the first confident call inflates it.

The manuscript presents a screening layer that works on top of any lifetime predictor. Pass and reject thresholds are calibrated on the maximum, over a sequence of early checkpoints, of normalised model scores of held-out calibration cells. This bounds the class-conditional false-pass and false-reject probabilities at user-chosen levels under any data-dependent stopping time (on average over calibration campaigns), and the calibration cells need to be cycled only to the specification, not to end of life. On {{D.n_total}} commercial LiFePO~4~/graphite cells from two laboratories (public MATR/CLO and HUST data, 1,000 random splits per data set), the error rates stayed below the 10% targets while {{E1.mc.proposed.sav}}% and {{E1.h.proposed.sav}}% of the cycling needed to observe every cell to the specification was saved. Re-checking with individually valid per-checkpoint thresholds, as done in practice, exceeded the targets by up to a factor of {{RATIO.naive_max}}.

We have tried to report the limits as carefully as the gains. A single checkpoint chosen on training cells was as efficient as the sequential rule, so the contribution is valid error control under repeated looks rather than faster screening; the guarantee holds on average over calibration campaigns, and we report how often a single campaign misses the target; it failed under batch shift until thresholds were recalibrated on cells of the new batch; and all cells share one chemistry. Thirteen experiments (base predictors, checkpoint grids, robustness, sensitivity, batch and laboratory shift, protocol-disjoint splits, calibration-conditional control, fairer comparators, physical interpretation and error analysis) support these statements.

We believe the work fits *Battery Energy* because it addresses battery testing and qualification, a practical bottleneck in battery development, and because uncertainty-aware decision processes for lifetime prediction are an open need highlighted in the journal. The method complements, rather than competes with, the lifetime predictors published there.

All data are public, and the code that regenerates every number, table and figure from the raw data is available from the corresponding author on request.

We confirm that this manuscript is original, has not been published previously, and is not under consideration for publication elsewhere. All authors have approved the manuscript and agree with its submission. The study used only previously published battery cycling data and involved no human participants or animals. The authors declare no conflict of interest, and the work received no specific funding. [Generative-AI use statement as required by Wiley policy, to be completed by the authors.]

[Optional: suggested reviewers with institutional e-mail addresses and no conflict of interest; reviewers to exclude.]

Thank you for considering our manuscript.

Sincerely,

[Corresponding author name]
on behalf of all authors
