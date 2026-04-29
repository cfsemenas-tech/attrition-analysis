# Video Script — Fraud Detection Assignment
### "What Changed in Our Attrition Model, and Why It Matters"
**Audience:** Business leaders | **Length:** ~60 seconds | **No code shown**

---

## [0:00 – 0:10] Hook

> "We recently found a quiet but serious flaw in how our people analytics model
> was measuring employee risk — and fixing it changed the story the data tells."

---

## [0:10 – 0:30] What the Old Formula Was Doing Wrong

> "Our model was supposed to answer:
> *'Of the employees at each satisfaction level, how many actually left?'*
>
> But the old formula was accidentally answering a different question:
> *'What share of all our departures came from each group?'*
>
> That sounds similar — but it's not.
> Think of it this way: if Level 1 employees are a small group but leave at
> a very high rate, the old number would still look small just because there
> aren't many of them. The model was hiding the true alarm signal."

---

## [0:30 – 0:48] What the Fix Does

> "The corrected formula now measures the right thing:
> for every 100 employees at a given satisfaction level, how many walked out
> the door?
>
> [Show chart]
>
> You can see here that the new numbers look different across the board.
> Level 1 — our most dissatisfied employees — now shows a significantly higher
> attrition rate than the old formula suggested. That's the real risk
> the business needs to act on."

---

## [0:48 – 1:00] Why This Matters for Decisions

> "When the metric is wrong, the priorities are wrong.
> With the corrected model, HR and department heads can now target
> retention efforts where they'll actually have impact —
> starting with the employees who are most at risk of leaving,
> not just the largest group that happened to leave."

---

*Chart file: `output/satisfaction_rate_comparison.png`*
