# Seasonal Elo Analysis — Critical Review

_Review of the analysis work merged from the `seasonal` branch._
_Author: Claude (Opus 4.8). Date: 2026-06-27._

This document collects two reviews of the seasonal Elo study:
1. A critique of the project read as a **modeling / inference** project.
2. A re-read of the same project as an **exploratory data analysis (EDA)** project.

---

## Part 1 — Read as a modeling project

Short version: the study's **weakest** claims hold up; its **strongest** ones do not.
The accuracy ranking is directionally believable but stated with far more confidence
than the evidence supports, and the gambling result is essentially an artifact of how
the simulation is built.

### Where I agree
- **Elo beats the naive controls.** True, but trivially — the controls are strawmen,
  so this isn't strong evidence of much.
- **"Prior history barely helps mid-season; the simple model is hard to beat."** The
  most defensible conclusion. The per-season `idxmin` flipping around supports the
  spirit of it: no config stably dominates, so the elaborate machinery isn't buying
  anything.

### Deficiencies (roughly by severity)

**1. No train/test split — the "winner" is chosen in-sample.**
The 28-config grid is both tuned and evaluated on the same 2014–2023 data. Top three
finish at 0.1619 / 0.1622 / 0.1639 — third-decimal gaps with no standard errors and no
significance test. Declaring `default` the winner over `k60osa20` by 0.0003 is
noise-mining. The honest version tunes K/OSA on 2014–2019 and reports test RMSE on
2020–2023. Each weekly *prediction* is properly sequential (good), but the *ranking* of
configs is overfit.

**2. The gambling "profit" is circular and shows no edge.**
Odds are generated from the model's own probabilities, shaded by a vig derived from the
model's own error (`mean + 2·std`). The model then bets into a market that is literally
itself. Betting at your own fair prices is zero-EV by construction; adding vig makes it
negative-EV. A +72.9-unit "profit" therefore can't be predictive skill — it's variance
or an asymmetry in the payout/spread-scaling formula. Says nothing about beating a real
sportsbook. Needs an independent market (real historical odds, or a separate model).

**3. The metric conflates two prediction problems and quietly favors "score" over
"trinary."**
RMSE is computed between a win *probability* and `true_score` = home's fractional
*category share* (∈ [0,1]) — a Brier-style score against a continuous target. The
minimizer of squared error is the conditional mean of that continuous outcome, so the
continuous-`score` Elo is structurally advantaged and trinary models are structurally
penalized (they emit win/loss/tie, charged squared error against a fractional target).
So "continuous beats trinary" is partly an artifact of the chosen target.

**4. Format change is a major uncontrolled confound.**
2014 (0.078) and 2016 (0.065) are far more predictable than the 9-cat seasons
(0.18–0.21) because those two are Points scoring (flagged in the R script). The global
RMSE pools two genuinely different prediction problems, and the easy points-seasons can
drag the ranking around. Report per-format, not pooled.

**5. Baselines are mis-specified, not just weak.**
`historic_wins_share` / `season_wins_share` are raw win-count shares used directly as
probabilities — a 2–0 team "predicts" 1.0 (guaranteed miscalibration); early season
collapses to 0.5. Beating these (0.230, 0.292) proves little. Fair baselines: logistic
fit on win%, a Massey/Colley rating, or prior-season finish. Note the absolute lift is
modest: blind-0.5 is already 0.179, best Elo 0.162 — a ~9% reduction.

**6. No calibration analysis.**
For anything betting-adjacent, calibration is what matters, and RMSE/Brier blends
calibration with resolution. Not a single reliability diagram.

**7. Sample size and generality.**
One league, ~8 managers/year, a few hundred matchups, 480 total positive-EV moneyline
bets, heavy roster turnover. Any claim that a specific K/OSA generalizes beyond this
league is unsupported.

**8. Reproducibility rot.**
Hardcoded `~/activity/FantasyNBATools` and `/home/syrax/` paths in the R script; the
champions map stops at 2021 though data runs to 2023; vig defined in squared-error units
with no theoretical basis. The figures can't be regenerated as-is.

### Net assessment
The defensible takeaway is narrow: *a simple season-reset continuous Elo is no worse
than the more elaborate cross-season/regression-tuned variants on this league's data.*
The study instead states "default is best" and "the model can win moneyline bets" — both
overclaim. Highest-value fixes: (1) replace the self-referential gambling market with
real odds; (2) temporal train/test split with bootstrap CIs on per-matchup error
differences so the third-decimal ranking can be believed or dismissed.

---

## Part 2 — Read as an EDA project

This reframe is largely right and is the more honest reading. It dissolves about half of
Part 1, and converts two "deficiencies" into the project's best findings.

### What the EDA framing earns back
- **In-sample tuning / no split** — fine. The 28-config grid is a descriptive sweep of
  the parameter landscape, not a model-selection claim. Only sin left is linguistic:
  "best" → "not beaten."
- **No significance tests** — not required; EDA generates hypotheses, doesn't confirm.
- **Weak baselines** — fine as orientation lines (`blind=0.5` at 0.179 is a useful
  floor).

### Criticisms that don't dissolve — they become the findings
- **The format effect is the headline, and it's buried.** Points seasons ~0.07 vs 9-cat
  ~0.18–0.21 is a ~3× predictability difference — the largest, most robust descriptive
  fact in the data. Good EDA leads with it and isolates it; here it's pooled into a
  global average it silently drives.
- **`idxmin` flipping year to year** is a clean finding: no configuration stably
  dominates; signal-to-noise is low enough that the yearly winner is essentially random.
- **The vig = mean + 2·std exercise**, stripped of the betting story, is a descriptive
  statistic: error dispersion is large relative to signal. Informative that way; circular
  and useless as a "profit" simulation.

### What EDA's own standards still ask for, and the project skips
- **Never examines the target.** No distribution of `true_score`, by format or week.
  EDA starts there; this starts at aggregate RMSE tables.
- **Computes scoreboards instead of exploring.** The notebooks produce ranked error
  tables and group-bys — summaries, not exploration. The one place the data gets *seen*
  (R script: per-player Elo trajectories, champion highlighting) is the broken,
  incomplete, hardcoded-path part. The most EDA-spirited artifact is the least finished.
- **No residual structure.** Where does the model fail — blowouts, coin-flip matchups,
  specific managers? The per-manager coverage table is the only thing edging toward this,
  and it's wrapped in the betting framing.
- **No calibration view.** Not a "rigor" demand under EDA, just *looking* — and absent.

### The honest characterization
This is a **modeling project that halted at the EDA stage.** The infrastructure is
modeling-grade (full off-season rescaling, a 28-cell grid, 10 years × multiple configs of
generated CSVs) — far more apparatus than EDA needs — but the output never got past
exploratory scoreboards. The commit trail says exactly this: "ready to set up grid search
to gather data" → built the apparatus → "mostly retired."

Graded as EDA, it's a solid pass with two real findings (format predictability gap; no
stable config winner) and one dead limb (the gambling sim). The cheap, high-value next
step is the same either way: split error by format, and actually plot the target and the
residuals — that's where the data is still trying to tell you something.
