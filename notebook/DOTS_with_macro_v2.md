I used [macro_v2](src/macro_v2), the version of the macro updated as explained [here](https://github.com/mac389/INTOXICATE/issues/8#issuecomment-2028965265), to calculate the INTOXICATE Score (AKA ICU Requirement Score) for the DOTS patients in the spreadsheet populated by Caitlin. 

I validated the macro's ability to calculate Score from patient parameters by doing several by hand and comparing, as well as creating a few "control" patients which were expected to return the lowest possible score (-9), the highest possible score (56), and a score for all base categories (0).

Of the 28 patients included from the DOTS database, 14 were ultimately admitted. A contingency table is shown below

|                     | **Score >6** | **Score </= 6** |        |
|---------------------|--------------|-----------------|--------|
| **Disposition ICU** |       9      |        0        |    9   |
| **Disposition GMF** |       3      |        2        |    5   |
|                     |      12      |        2        | **14** |

Both Fisher's Exact Test (more or less, _Is there an association between classification as Score >6 with classification as Disposition ICU?_) and Cohen's Kappa (_What is the degree of agreement between the two "raters," in our case the real doctors and the algorithm, compared to chance?_) are appropriate here, though they test slightly different hypotheses.

**Fisher's Exact:**
* **OR:** Undefined due to presence of 0 in a cell
* **_p_:** 0.110

**Cohen's Kappa:**
* **kappa:** 0.46, indicated "moderate" agreement
* **_p_:** 0.094 (can be derived from a SE(kappa) which reflects sample size, agreement, and agreement due to chance)

Not particularly surprisingly with the very small sample, neither are statistically significant (_p_(kappa) is borderline (exactly half; p = 0.047, if necessary) with a one-tailed test but I don't think that's good scientific practice in this context and I hate the p=0.05 threshold anyway). It should be kept in mind that the IRS > 6 threshhold is quite low with this current model; 9 of 14 eventual discharges were also predicted to have ICU requirement, and it should also be noted that the results Brandenburg and Zwaag each reported were resulted from applying the score to ICU patients **only**, then retrospectively identifying the patients who did or did not require ICU level care.
