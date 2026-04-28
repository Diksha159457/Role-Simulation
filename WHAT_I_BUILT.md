# What I Built for DT Fellowship

## The Assignment
Build a deterministic decision tree for end-of-day employee reflection.

## What I Delivered

### Part A: The Tree (Mandatory) ✅
**File:** `tree/reflection-tree.json`

A 40-node decision tree that measures 3 psychological axes:
1. **Locus of Control** (Victim ↔ Victor) - Rotter 1954
2. **Orientation** (Entitlement ↔ Contribution) - Campbell 2004, Organ 1988  
3. **Radius** (Self-Centric ↔ Altrocentric) - Maslow 1969, Batson 2011

**Key Features:**
- Deterministic (no LLM, no randomness)
- 11 questions with cognitive anchors
- 8 non-moralizing reflections
- Invisible decision nodes for natural flow
- Personalized summary based on accumulated signals

### Part B: The Agent (Optional) ✅
**File:** `agent/agent.py`

A Python CLI that walks the tree:
- Interactive mode for real users
- Automated persona testing (victim/victor)
- Transcript saving
- Zero external dependencies for core logic

### Supporting Files ✅
- `tree/tree-diagram.md` - Visual Mermaid diagram
- `transcripts/` - Example sessions
- `README.md` - Full documentation

## How I Controlled AI Hallucination

### During Design (When I Used AI)
1. **Primary Source Verification** - Checked every psychology claim against original papers
2. **Option Testing** - Ran personas through questions to ensure distinct routing
3. **Tone Filter** - "Wise colleague test" for all reflections

### At Runtime (The Actual Tool)
**Zero hallucination risk** - it's a static JSON tree, no LLM calls!

## What Makes This Good

1. **Evidence-Based** - 6 peer-reviewed sources
2. **Deterministic** - Same input = same output, always
3. **Well-Tested** - 2 full persona transcripts
4. **Thoughtful** - Cognitive anchors, no moralizing
5. **Production-Ready** - Clean code, comprehensive docs

## GitHub
https://github.com/Diksha159457/Role-Simulation

## Next Step
Record voice note explaining this + submit!