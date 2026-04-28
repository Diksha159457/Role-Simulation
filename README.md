# Daily Reflection Tree — DT Fellowship Assignment

A deterministic, LLM-free end-of-day reflection tool that walks employees through three psychological axes: **Locus of Control** (Victim ↔ Victor), **Orientation** (Entitlement ↔ Contribution), and **Radius** (Self-Centric ↔ Altrocentric).

> **The tool itself contains no LLM calls.** AI was used to research psychology, draft questions, and iterate on tree structure during design — but the final product is a static JSON tree walked by a simple Python agent.

---

## Repository Structure

```
/tree/
  reflection-tree.json      ← Part A: the full tree data (40+ nodes)
  tree-diagram.md           ← Part A: Mermaid visual of branching structure

/agent/
  agent.py                  ← Part B: Python CLI agent

/transcripts/
  persona-1-victim-transcript.md   ← "Victim" persona session
  persona-2-victor-transcript.md   ← "Victor" persona session

write-up.md                 ← Design rationale (Part A requirement)
README.md                   ← This file
```

---

## Part A: Reading the Tree

`reflection-tree.json` is a flat array of node objects. Every path through the tree can be traced by following node IDs:

```json
{
  "id": "A1_Q_HARD",
  "parentId": "A1_D1",
  "type": "question",
  "text": "You said it felt '{A1_OPEN.answer}'. When the day pushed back, what was your first honest instinct?",
  "options": ["I looked for what I could still control", "..."],
  "signal": "axis1:external"
}
```

| Field | Purpose |
|-------|---------|
| `id` | Unique node identifier |
| `parentId` | Parent in the hierarchy |
| `type` | `start`, `question`, `decision`, `reflection`, `bridge`, `summary`, `end` |
| `text` | What the employee sees. `{NODE_ID.answer}` is replaced at runtime. |
| `options` | Fixed choices (question nodes) or routing conditions (decision nodes) |
| `signal` | What this node records in axis state |
| `target` | Explicit jump target (overrides child-lookup) |

**Decision node routing** uses condition strings:
```
"answer=Stormy — things went sideways|Overcast — low energy, just got through it" → target A
"answer=Partly cloudy — mixed bag|Clear — things flowed"                          → target B
"always"                                                                           → unconditional
```

**Axis signal tallying:**
- Each `question` and `reflection` node has a `signal` field (`axis1:internal`, `axis2:entitlement`, etc.)
- At `SUMMARY`, `axis1.dominant = "internal"` if `axis1_internal >= axis1_external`, else `"external"`
- The summary text is assembled from `summary_map` in the SUMMARY node using the dominant values

**Tree statistics:**

| Metric | Count |
|--------|-------|
| Total nodes | 40 |
| Question nodes | 11 |
| Decision nodes | 10 |
| Reflection nodes | 8 |
| Bridge nodes | 2 |
| Summary node | 1 |
| End node | 1 |
| Start node | 1 |

---

## Part B: Running the Agent

**Requirements:** Python 3.8+, no external dependencies.

### Interactive mode (real session)
```bash
cd agent
python agent.py
```

### Automated persona paths
```bash
# Run the "victim" persona (external locus, entitlement, self-centric)
python agent.py --auto-path victim

# Run the "victor" persona (internal locus, contribution, transcendent)
python agent.py --auto-path victor
```

### Custom tree path
```bash
python agent.py --tree /path/to/your-tree.json
```

### Save transcript
```bash
python agent.py --auto-path victim --save-transcript my-transcript.md
```

---

## Design Philosophy

### No LLM at runtime — why this matters

Reflection tools must be **predictable and trustworthy**. If an employee's end-of-day conversation varies based on model temperature, API latency, or prompt drift, the tool loses credibility. A deterministic tree gives the same quality of reflection every session — because a human encoded the intelligence into the structure.

### The three axes are a sequence, not three quizzes

- **Axis 1 (Locus)** surfaces agency — did you navigate, or were you navigated?
- **Axis 2 (Orientation)** builds on that — if you had agency, where did you direct it?
- **Axis 3 (Radius)** widens the frame — the *towards what* and *towards whom* of your day

An employee who recognises their agency naturally asks what they did with it. An employee who reflects on what they gave naturally wonders who they were giving *for*. The tree exploits this progression.

### Guardrails against AI hallucination in design

During the *design* phase (where AI was used as a collaborator), three practices prevented hallucination from contaminating the tree:

1. **Primary source verification:** All psychological claims (Rotter 1954, Dweck 2006, Campbell et al. 2004, Organ 1988, Maslow 1969, Batson 2011) were cross-checked against original or peer-reviewed sources, not blog summaries.
2. **Option distinctiveness testing:** Each question's options were tested by asking an LLM to roleplay as different employee archetypes. If two options produced the same routing, they were revised until they were genuinely distinguishable.
3. **Reflection tone review:** Every reflection node was checked against a "wise colleague" filter. Any reflection that could appear on a motivational poster was rewritten.

---

## Psychological Sources

- Rotter, J.B. (1954). *Social learning and clinical psychology.* Prentice-Hall.
- Dweck, C.S. (2006). *Mindset: The New Psychology of Success.* Random House.
- Campbell, W.K., Bonacci, A.M., Shelton, J., Exline, J.J., & Bushman, B.J. (2004). Psychological entitlement: Interpersonal consequences and validation of a self-report measure. *Journal of Personality Assessment, 83*(1), 29–45.
- Organ, D.W. (1988). *Organizational citizenship behavior: The good soldier syndrome.* Lexington Books.
- Maslow, A.H. (1969). The farther reaches of human nature. *Journal of Transpersonal Psychology, 1*(1), 1–9.
- Batson, C.D. (2011). *Altruism in humans.* Oxford University Press.
# Role-Simulation
