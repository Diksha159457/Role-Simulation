# Write-Up: Daily Reflection Tree — Design Rationale

**Assignment:** DT Fellowship — Part A  
**Word count:** ~900 words

---

## 1. Why These Questions

The hardest design constraint in this assignment is not the branching logic — it's writing questions that a tired person at 7pm would answer *honestly* rather than *optimally*. The temptation is to write questions so that good employees click A and bad employees click D. That's a survey, not a reflection tool.

I broke this by designing around **cognitive anchors**. Each opening question gives the employee a concrete metaphor or memory to hook onto before the psychological content arrives:

- **Axis 1 opener:** "If today were a weather report..." — meteorological framing is neutral and non-threatening. It lets the employee name the emotional texture of the day without immediately assigning blame or credit.
- **Axis 2 opener:** "Think of the most energy-consuming part of your day..." — grounds the abstract question (entitlement vs. contribution) in a specific, recalled moment.
- **Axis 3 opener:** "Whose experience was in your mind..." — "whose" is a perspective-taking prompt that is harder to game than "did you think about others?"

The follow-up questions within each axis are designed to be genuinely hard to distinguish between unless you've actually lived the experience. For example, in A1_Q_EXTERNAL, the options "Not really, the constraint was real" and "I'm not sure — I was too deep in it to notice" both signal external locus, but the tree branches differently because *the self-awareness level is different*. That distinction produces different reflections.

---

## 2. How Branching Was Designed

The core branching principle: **each axis has two entry paths (hard day / easy day, giving / receiving, self / other) and the tree asks different questions on each path while arriving at the same categories of insight**. This means a person who had a great day gets the same psychological mapping as a person who had a terrible one — the tree just takes a different route to get there.

**Trade-offs I made:**

- I chose **depth over breadth** within each axis. Rather than 8 shallow questions per axis, I chose 2–3 deeper questions with 4 options each. This reduces session fatigue (a real risk for an evening tool) while allowing more nuanced routing.
- Decision nodes are **invisible to the user**. This was a deliberate choice to maintain conversational flow. Routing logic should feel like a wise interlocutor reading the room, not a form.
- **Reflections never moralize.** This was the hardest writing constraint. Every reflection went through a "wise colleague" filter: would a colleague who respects you say this? If the answer could appear on a motivational poster, it was rewritten.
- The bridge nodes carry **axis-to-axis semantic continuity**: the A1→A2 bridge says "you've looked at how you handled things — now let's look at what you gave." This frames Axis 2 as a natural extension of Axis 1's inquiry rather than a topic change.

---

## 3. Psychological Sources

**Axis 1 — Locus of Control (Rotter, 1954) + Growth Mindset (Dweck, 2006):**  
Rotter's original I-E scale was a *trait* measure — it classified people. I adapted this into a *state* measure — it surfaces where someone was on a particular day. The key insight from Dweck is that mindset shifts happen at the moment of setback: her research shows people with fixed mindsets attribute failure to talent, while growth-minded people attribute it to strategy and effort. My Axis 1 questions target exactly that moment: "when the day pushed back, what was your first honest instinct?"

**Axis 2 — Psychological Entitlement (Campbell et al., 2004) + OCB (Organ, 1988):**  
Campbell's entitlement scale measures the belief that one *deserves* differential treatment. Organ's OCB framework identifies discretionary helping behaviours as the most reliable predictor of team health. The critical design insight: entitlement is invisible from the inside. So the A2 entitlement branch asks questions that surface it *indirectly* — the employee is asked what they expected to receive, not whether they are entitled.

**Axis 3 — Self-Transcendence (Maslow, 1969) + Perspective-Taking (Batson, 2011):**  
Maslow's 1969 paper, often excluded from the famous hierarchy pyramid, argues that self-transcendence — orientation toward something beyond the self — is the highest state of psychological development. Batson's distinction between empathy (feeling what another feels) and perspective-taking (imagining another's experience cognitively) was useful: Axis 3 targets perspective-taking, not empathy, because cognitive reorientation is more accessible at the end of a long day.

---

## 4. What I Would Improve with More Time

**More nuanced signal accumulation:** The current system tallies binary signals (internal/external). A production version should weight signals differently — an answer to the deeper follow-up question should count more than the opener.

**Temporal continuity across sessions:** The most powerful version of this tool shows employees their axis trends over time: "Last week you were consistently external on Axis 1 — this week, internal. What changed?" This requires a session store, but the deterministic path structure makes it feasible without LLMs.

**Axis 3 deserves a more complex design.** The spectrum from self to transcendence has more gradations than my current 3-option routing captures. A more mature Axis 3 would include intermediate questions about *how* someone's team-awareness affected their behaviour, not just whether it existed.

**Field-tested question calibration:** The only way to know if the A and C options in a question are genuinely distinguishable in practice is to run the session with real employees. Several options in this tree are probably too easy to game once you understand the psychology — this is the core hallucination risk for deterministic systems, and the only fix is iteration with real users.

---

*Design by: Diksha Shahi | April 2026*
