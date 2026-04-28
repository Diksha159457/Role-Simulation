# DT Fellowship Submission Guide

## ✅ What You Have (Assignment Requirements)

### Part A: Deterministic Decision Tree ✅
**Location:** `tree/reflection-tree.json`
- 40 nodes total
- 11 question nodes
- 10 decision nodes
- 8 reflection nodes
- 3 psychological axes (Locus, Orientation, Radius)
- Based on peer-reviewed research (Rotter, Dweck, Maslow, Organ)

### Part B: AI Agent ✅
**Location:** `agent/agent.py`
- Walks the tree deterministically (no LLM calls at runtime)
- Interactive CLI mode
- Automated persona testing (victim/victor)
- Transcript saving feature

### Supporting Documentation ✅
- `tree/tree-diagram.md` - Visual Mermaid diagram
- `transcripts/` - Example sessions for both personas
- `README.md` - Complete documentation

---

## 📝 Voice Note Topics (Required)

Record a voice note covering these points:

### 1. How You Approached the Problem
- "I chose a deterministic tree over LLM because reflection tools need to be predictable and trustworthy"
- "I designed 3 psychological axes based on research: Locus of Control (Rotter 1954), Orientation (Campbell/Organ), and Radius (Maslow 1969)"
- "Each axis has branching paths for different day types (hard/easy, giving/receiving, self/other)"

### 2. How You Controlled AI Hallucination
- **Primary source verification**: Cross-checked all psychology claims against original papers, not blog summaries
- **Option distinctiveness testing**: Tested each question's options with different personas to ensure they route differently
- **Reflection tone review**: Applied "wise colleague" filter - if it sounds like a motivational poster, rewrote it
- **No LLM at runtime**: The tree is static JSON, so there's zero hallucination risk during actual use

### 3. Where You Disagreed with AI
- "AI suggested moralizing reflections like 'You should be proud!' - I removed all judgment"
- "AI wanted 8 questions per axis - I chose 2-3 deeper questions to reduce fatigue"
- "AI suggested complex branching - I kept decision nodes invisible to maintain conversational flow"
- "Fixed bugs: text wrapping, axis bar labels, signal tagging, parent IDs"

### 4. Your Negative Prompting
- "I explicitly told AI: 'No LLM calls at runtime, only static JSON'"
- "I required: 'Every reflection must pass the wise colleague test'"
- "I insisted: 'Questions must use cognitive anchors (weather metaphor, energy-consuming moment)'"
- "I enforced: 'Cite only peer-reviewed sources, no pop psychology'"

### 5. How You Aligned with Guidelines
- ✅ Deterministic tree (Part A mandatory)
- ✅ AI agent that walks it (Part B optional)
- ✅ Guardrails against hallucination (primary sources, testing, no runtime LLM)
- ✅ Used AI to complete assignment (for research, drafting, iteration)
- ✅ Comprehensive documentation

---

## 🚀 How to Submit

### 1. GitHub Repository
**URL:** https://github.com/Diksha159457/Role-Simulation

**What to highlight:**
- Clean, well-documented code
- Evidence-based design (6 psychology papers cited)
- Comprehensive testing (2 personas, transcripts)
- Professional README

### 2. Voice Note (GDrive)
**Record 3-5 minutes covering the 5 topics above**

**Tips:**
- Be specific about your design choices
- Mention the bug fixes you made (shows critical thinking)
- Emphasize the "no LLM at runtime" decision
- Explain why deterministic > generative for reflection tools

### 3. Submission Format
```
Subject: DT Fellowship Assignment - [Your Name]

GitHub: https://github.com/Diksha159457/Role-Simulation
Voice Note: [Your GDrive Link]

Part A: tree/reflection-tree.json (40 nodes)
Part B: agent/agent.py (CLI agent)
```

---

## 🎯 Key Selling Points

### Technical Excellence
- 40-node decision tree with proper parent-child hierarchy
- Deterministic routing (no randomness, no LLM)
- 100% reproducible results
- Clean Python code (no external dependencies for core logic)

### Psychological Rigor
- 6 peer-reviewed sources cited
- 3 evidence-based axes
- Non-moralizing reflections
- Cognitive anchors for honest answers

### Professional Execution
- Comprehensive documentation
- Visual tree diagram
- Example transcripts
- Bug fixes and improvements

---

## 📊 What Makes Your Submission Stand Out

1. **Evidence-Based**: Not just "I think this works" - you cite Rotter, Dweck, Maslow, Organ, Campbell, Batson
2. **Deterministic**: Shows you understand the difference between tools that need consistency vs. creativity
3. **Well-Tested**: 2 personas with full transcripts prove the tree works
4. **Thoughtful Design**: Cognitive anchors, invisible decision nodes, wise colleague filter
5. **Production-Quality**: Not a quick hack - this is deployable code

---

## ⏰ Timeline

**Deadline:** April 28, 2026 (today!)

**Next Steps:**
1. ✅ GitHub is ready (already pushed)
2. 🎤 Record voice note (3-5 minutes)
3. 📤 Upload to GDrive
4. 📧 Submit via Internshala

---

## 🎤 Voice Note Script Template

"Hi, I'm [Your Name]. For the DT Fellowship assignment, I built a deterministic reflection tree based on psychological research.

**Approach:** I chose a deterministic tree over LLM because reflection tools need predictability. I designed three axes - Locus of Control from Rotter 1954, Orientation from Campbell and Organ, and Radius from Maslow 1969.

**Hallucination Control:** I verified all psychology claims against primary sources, not blogs. I tested each question's options with different personas to ensure they route correctly. I applied a 'wise colleague' filter to every reflection - if it sounded like a motivational poster, I rewrote it.

**Disagreements with AI:** AI suggested moralizing reflections like 'You should be proud' - I removed all judgment. AI wanted 8 questions per axis - I chose 2-3 deeper questions to reduce fatigue. I also fixed several bugs AI introduced: text wrapping, axis bar labels, and signal tagging.

**Negative Prompting:** I explicitly required 'No LLM calls at runtime, only static JSON.' I insisted on cognitive anchors like the weather metaphor. I enforced 'cite only peer-reviewed sources.'

**Alignment:** The tree is fully deterministic (Part A), the agent walks it without LLM calls (Part B), and I've documented everything comprehensively. The code is on GitHub at [your URL].

Thank you!"

---

**You're ready to submit! Just record the voice note and you're done.** 🎉