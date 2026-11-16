[Corresponding author name]
[Department, Institution]
[Address]
[E-mail] · [Telephone]

[Date]

The Editor-in-Chief
*Battery Energy*
John Wiley & Sons

Dear Editor,

**Submission of an original research article: "Stopping Cycle-Life Tests Early With Guaranteed Error Rates: Distribution-Free Sequential Screening of Lithium-Ion Cells From Truncated Test Campaigns"**

On behalf of all authors, I submit the above manuscript for consideration as a Research Article in *Battery Energy*.

Cycle-life testing is the slowest step in developing and qualifying lithium-ion cells. Early-cycle predictions of lifetime are now widely used to shorten it, but when such predictions are used to pass or reject cells, the error rate of those decisions is neither specified nor controlled — and the common practice of re-checking a prediction as cycling proceeds and stopping at the first confident call inflates it further.

Our manuscript addresses this with a statistically guaranteed screening procedure. Pass and reject thresholds are calibrated on the maximum, over a sequence of early checkpoints, of normalised model scores of held-out calibration cells. We prove that this bounds the probability of passing a cell that will not reach the cycle-life specification, and of rejecting one that will, at user-chosen levels under any data-dependent stopping time, and that calibration cells need to be cycled only to the specification rather than to end of life. On {{D.n_total}} commercial LiFePO~4~/graphite cells from two laboratories (public MATR/CLO and HUST data), with 1,000 random splits per data set, the procedure met its 10% error targets while reducing cycling by {{E1.mc.proposed.sav}}% and {{E1.h.proposed.sav}}% relative to cycling every cell to the specification. Naive sequential use of individually valid thresholds exceeded the targets by up to a factor of {{RATIO.naive_max}}. We also report base-predictor comparisons, ablations, robustness and sensitivity analyses, batch- and laboratory-shift experiments in which the guarantee fails without recalibration, and an error analysis.

We believe the work fits *Battery Energy* because it addresses battery testing and qualification — a practical bottleneck for battery development — with a method that sits on top of any lifetime predictor, including those published in the journal, and because recent reviews in *Battery Energy* identify uncertainty-aware lifetime prediction as an open need. We have been careful not to overstate the contribution: the paper does not propose a more accurate predictor, all cells share one chemistry, and the guarantees are statements about error rates under exchangeability, whose failure under distribution shift we document.

All data are public, and the complete code that regenerates every number, table and figure from the raw data will be made openly available at [repository / archival DOI].

We confirm that this manuscript is original, has not been published previously, and is not under consideration for publication elsewhere. All authors have approved the manuscript and agree with its submission. The study used only previously published battery cycling data and involved no human participants or animals. The authors declare no conflict of interest [to be confirmed]. [Generative-AI use statement as required by Wiley policy, to be completed by the authors.]

[Optional: suggested reviewers with institutional e-mail addresses and no conflict of interest; reviewers to exclude.]

Thank you for considering our manuscript.

Sincerely,

[Corresponding author name]
on behalf of all authors
