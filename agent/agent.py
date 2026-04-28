#!/usr/bin/env python3
"""
Daily Reflection Tree Agent
============================
A deterministic, LLM-free agent that walks reflection-tree.json.

Usage:
    python agent.py                          # Interactive mode
    python agent.py --auto-path victor       # Run a preset persona path
    python agent.py --auto-path victim       # Run a preset persona path
    python agent.py --tree ../tree/reflection-tree.json   # Custom tree path
"""

import json
import sys
import time
import argparse
import textwrap
from pathlib import Path
from typing import Optional

# ─── ANSI colours ────────────────────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
CYAN    = "\033[36m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
MAGENTA = "\033[35m"
BLUE    = "\033[34m"
DIM     = "\033[2m"

def c(text, colour): return f"{colour}{text}{RESET}"
def wrap(text, width=72): return "\n".join(textwrap.wrap(text, width))

# ─── Preset persona answer maps (for automated transcript generation) ─────────
PERSONAS = {
    "victim": {
        "A1_OPEN":        "Stormy — things went sideways",
        "A1_Q_HARD":      "I felt blocked by things or people outside me",
        "A1_Q_EXTERNAL":  "Not really, the constraint was real",
        "A2_OPEN":        "I felt I wasn't getting enough back for what I gave",
        "A2_Q_ENTITLEMENT": "I expected more acknowledgment than I got",
        "A3_OPEN":        "Mine — I was focused on getting through it",
        "A3_Q_SELF":      "Probably yes, but I didn't have bandwidth to notice",
    },
    "victor": {
        "A1_OPEN":        "Partly cloudy — mixed bag",
        "A1_Q_EASY":      "I prepared for it or adapted deliberately",
        "A1_Q_AGENCY":    "I chose how I responded to someone's difficult behaviour",
        "A2_OPEN":        "I gave more than was expected of me",
        "A2_Q_CONTRIBUTION": "Yes — I helped a colleague with something not in my job description",
        "A3_OPEN":        "Someone downstream — the end user or someone we serve",
        "A3_Q_BEYOND":    "It grounded me — reminded me why this matters",
    }
}

# ─── State ────────────────────────────────────────────────────────────────────
class State:
    def __init__(self):
        self.answers: dict[str, str] = {}
        self.signals: dict[str, int] = {
            "axis1_internal": 0, "axis1_external": 0,
            "axis2_contribution": 0, "axis2_entitlement": 0,
            "axis3_self": 0, "axis3_collective": 0, "axis3_transcendent": 0,
        }

    def record_answer(self, node_id: str, answer: str):
        self.answers[node_id] = answer

    def record_signal(self, signal: Optional[str]):
        if not signal:
            return
        key = signal.replace(":", "_")
        if key in self.signals:
            self.signals[key] += 1

    def dominant(self, axis: str) -> str:
        if axis == "axis1":
            return "internal" if self.signals["axis1_internal"] >= self.signals["axis1_external"] else "external"
        if axis == "axis2":
            return "contribution" if self.signals["axis2_contribution"] >= self.signals["axis2_entitlement"] else "entitlement"
        if axis == "axis3":
            counts = {
                "self": self.signals["axis3_self"],
                "collective": self.signals["axis3_collective"],
                "transcendent": self.signals["axis3_transcendent"],
            }
            return max(counts, key=counts.get)
        return "unknown"

    def interpolate(self, text: str, summary_map: dict) -> str:
        """Replace {placeholders} with recorded values."""
        for node_id, answer in self.answers.items():
            text = text.replace(f"{{{node_id}.answer}}", answer)
        for axis in ["axis1", "axis2", "axis3"]:
            dom = self.dominant(axis)
            text = text.replace(f"{{{axis}.dominant}}", dom)
            if axis in summary_map:
                summary_text = summary_map[axis].get(dom, "")
                text = text.replace(f"{{{axis}.summary}}", summary_text)
        return text


# ─── Tree loader ──────────────────────────────────────────────────────────────
class Tree:
    def __init__(self, path: str):
        with open(path) as f:
            data = json.load(f)
        self.nodes: dict[str, dict] = {n["id"]: n for n in data["nodes"]}
        self.routing_rules = data.get("routing_rules", {})
        self.bridge_targets: dict[str, str] = self.routing_rules.get("bridge_targets", {})
        # Build parent→children map
        self.children: dict[str, list[str]] = {}
        for node in data["nodes"]:
            pid = node["parentId"]
            if pid:
                self.children.setdefault(pid, []).append(node["id"])

    def get(self, node_id: str) -> dict:
        return self.nodes[node_id]

    def next_node(self, node: dict, state: State) -> Optional[str]:
        nid = node["id"]
        ntype = node["type"]

        # Explicit target overrides everything
        if node.get("target"):
            return node["target"]

        # Bridge target map
        if nid in self.bridge_targets:
            return self.bridge_targets[nid]

        # Decision node: evaluate routing conditions
        if ntype == "decision":
            options = node.get("options", [])
            last_answer = self._last_answer(node, state)
            for opt in options:
                if isinstance(opt, dict):
                    cond = opt["condition"]
                    if cond == "always":
                        return opt["target"]
                    if cond.startswith("answer="):
                        values = cond[len("answer="):].split("|")
                        if last_answer in values:
                            return opt["target"]
            return None

        # Non-decision: first child
        children = self.children.get(nid, [])
        return children[0] if children else None

    def _last_answer(self, decision_node: dict, state: State) -> str:
        """Walk up to find the most recent question answer in scope."""
        pid = decision_node.get("parentId")
        if pid and pid in state.answers:
            return state.answers[pid]
        # Fall back: last recorded answer
        if state.answers:
            return list(state.answers.values())[-1]
        return ""


# ─── Agent runner ─────────────────────────────────────────────────────────────
class Agent:
    def __init__(self, tree: Tree, persona: Optional[str] = None):
        self.tree = tree
        self.state = State()
        self.persona = persona
        self.transcript: list[dict] = []

    def run(self):
        current_id = "START"
        while current_id:
            node = self.tree.get(current_id)
            ntype = node["type"]
            handler = getattr(self, f"_handle_{ntype}", self._handle_default)
            next_id = handler(node)
            current_id = next_id

    # ── Node handlers ──────────────────────────────────────────────────────────

    def _handle_start(self, node: dict) -> Optional[str]:
        print()
        print(c("━" * 72, CYAN))
        print(c(f"  🌙  DAILY REFLECTION TREE", BOLD + CYAN))
        print(c("━" * 72, CYAN))
        print()
        self._display_text(node["text"], CYAN)
        self._pause()
        self.state.record_signal(node.get("signal"))
        return self.tree.next_node(node, self.state)

    def _handle_question(self, node: dict) -> Optional[str]:
        text = self.state.interpolate(node["text"], {})
        print()
        print(c(f"┌─ Question {'─' * 58}", BLUE))
        for line in textwrap.wrap(text, 66):
            print(c("│  ", BLUE) + c(line, BOLD))
        print(c(f"└{'─' * 70}", BLUE))
        options = node["options"]
        for i, opt in enumerate(options, 1):
            print(f"  {c(str(i) + '.', YELLOW)} {opt}")
        print()

        answer = self._get_answer(node["id"], options)
        self.state.record_answer(node["id"], answer)
        self.state.record_signal(node.get("signal"))
        self.transcript.append({"node": node["id"], "type": "question", "q": text, "a": answer})
        return self.tree.next_node(node, self.state)

    def _handle_decision(self, node: dict) -> Optional[str]:
        # Silent internal routing — not shown to user
        return self.tree.next_node(node, self.state)

    def _handle_reflection(self, node: dict) -> Optional[str]:
        text = self.state.interpolate(node["text"], {})
        print()
        print(c(f"  💡  Reflection", BOLD + GREEN))
        print(c("  " + "─" * 68, GREEN))
        print(c("  " + wrap(text, 68).replace("\n", "\n  "), GREEN))
        print()
        self.state.record_signal(node.get("signal"))
        self.transcript.append({"node": node["id"], "type": "reflection", "text": text})
        self._continue_prompt()
        return self.tree.next_node(node, self.state)

    def _handle_bridge(self, node: dict) -> Optional[str]:
        text = self.state.interpolate(node["text"], {})
        print()
        print(c("  ·  ·  ·", DIM))
        print(c(f"  {text}", MAGENTA + BOLD))
        print(c("  ·  ·  ·", DIM))
        print()
        self._pause(0.8)
        self.state.record_signal(node.get("signal"))
        return self.tree.next_node(node, self.state)

    def _handle_summary(self, node: dict) -> Optional[str]:
        summary_map = node.get("summary_map", {})
        text = self.state.interpolate(node["text"], summary_map)
        print()
        print(c("━" * 72, YELLOW))
        print(c("  📊  TODAY'S REFLECTION SUMMARY", BOLD + YELLOW))
        print(c("━" * 72, YELLOW))
        print()
        print(wrap(text, 70))
        print()
        self._axis_breakdown()
        self.transcript.append({"node": node["id"], "type": "summary", "text": text})
        return self.tree.next_node(node, self.state)

    def _handle_end(self, node: dict) -> Optional[str]:
        for line in textwrap.wrap(node["text"], 70):
            print(c(f"  {line}", DIM))
        print()
        print(c("━" * 72, CYAN))
        print()
        return None

    def _handle_default(self, node: dict) -> Optional[str]:
        return self.tree.next_node(node, self.state)

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _display_text(self, text: str, colour: str = RESET):
        for line in wrap(text, 70).split("\n"):
            print(c(f"  {line}", colour))

    def _pause(self, seconds: float = 0.4):
        if not self.persona:
            time.sleep(seconds)

    def _continue_prompt(self):
        if self.persona:
            return
        input(c("  [ Press Enter to continue ]", DIM))

    def _get_answer(self, node_id: str, options: list[str]) -> str:
        if self.persona and node_id in PERSONAS[self.persona]:
            preset = PERSONAS[self.persona][node_id]
            print(c(f"  → Auto: {preset}", DIM))
            return preset

        while True:
            try:
                raw = input(c("  Your choice (number): ", BOLD))
                idx = int(raw.strip()) - 1
                if 0 <= idx < len(options):
                    return options[idx]
                print(c(f"  Please enter a number between 1 and {len(options)}.", YELLOW))
            except (ValueError, EOFError):
                print(c("  Please enter a valid number.", YELLOW))

    def _axis_breakdown(self):
        s = self.state.signals
        print(c("  Axis breakdown:", DIM))
        self._bar("Axis 1 — Locus",
                  "internal", s["axis1_internal"],
                  "external", s["axis1_external"])
        self._bar("Axis 2 — Orientation",
                  "contribution", s["axis2_contribution"],
                  "entitlement", s["axis2_entitlement"])
        a3_counts = {
            "self": s["axis3_self"],
            "collective": s["axis3_collective"],
            "transcendent": s["axis3_transcendent"],
        }
        a3_dom = max(a3_counts, key=a3_counts.get)
        a3_total = sum(a3_counts.values()) or 1
        print(c(f"  Axis 3 — Radius:      dominant → {a3_dom} ({a3_counts[a3_dom]}/{a3_total})", DIM))
        print()

    def _bar(self, label: str, pos_label: str, pos: int, neg_label: str, neg: int):
        total = pos + neg or 1
        filled = round(pos / total * 20)
        bar = "█" * filled + "░" * (20 - filled)
        dom_label = pos_label if pos >= neg else neg_label
        dom_count = pos if pos >= neg else neg
        print(c(f"  {label:<28} [{bar}] {dom_label} ({dom_count}/{total})", DIM))

    def save_transcript(self, path: str):
        with open(path, "w") as f:
            f.write("# Reflection Session Transcript\n\n")
            f.write(f"**Persona:** {self.persona or 'interactive'}\n\n")
            for entry in self.transcript:
                if entry["type"] == "question":
                    f.write(f"**Q [{entry['node']}]:** {entry['q']}\n\n")
                    f.write(f"**A:** {entry['a']}\n\n")
                    f.write("---\n\n")
                elif entry["type"] == "reflection":
                    f.write(f"**Reflection [{entry['node']}]:** {entry['text']}\n\n")
                    f.write("---\n\n")
                elif entry["type"] == "summary":
                    f.write(f"## Summary\n\n{entry['text']}\n\n")


# ─── Entry point ─────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Daily Reflection Tree Agent")
    parser.add_argument("--tree", default="../tree/reflection-tree.json", help="Path to tree JSON")
    parser.add_argument("--auto-path", choices=["victor", "victim"], help="Run a preset persona")
    parser.add_argument("--save-transcript", help="Save transcript to file")
    args = parser.parse_args()

    tree_path = Path(args.tree)
    if not tree_path.exists():
        # Try relative to this script
        script_dir = Path(__file__).parent
        tree_path = script_dir / "../tree/reflection-tree.json"

    try:
        tree = Tree(str(tree_path))
    except FileNotFoundError:
        print(f"Error: Could not find tree file at {tree_path}")
        sys.exit(1)

    agent = Agent(tree, persona=args.auto_path)
    agent.run()

    if args.save_transcript:
        agent.save_transcript(args.save_transcript)
        print(f"Transcript saved to {args.save_transcript}")


if __name__ == "__main__":
    main()
