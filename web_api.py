#!/usr/bin/env python3
"""
Daily Reflection Tree — Web API
===============================
A Flask web server that exposes the reflection tree as a REST API.
Deployable to Heroku, Railway, Render, etc.
"""

import json
import os
from pathlib import Path
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Import the existing agent logic
import sys
sys.path.append('.')

# We'll reuse the Tree and State classes from agent.py
# For simplicity, I'll copy the core logic here
class State:
    def __init__(self):
        self.answers = {}
        self.signals = {
            "axis1_internal": 0, "axis1_external": 0,
            "axis2_contribution": 0, "axis2_entitlement": 0,
            "axis3_self": 0, "axis3_collective": 0, "axis3_transcendent": 0,
        }

    def record_answer(self, node_id, answer):
        self.answers[node_id] = answer

    def record_signal(self, signal):
        if not signal:
            return
        key = signal.replace(":", "_")
        if key in self.signals:
            self.signals[key] += 1

    def dominant(self, axis):
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

    def interpolate(self, text, summary_map):
        for node_id, answer in self.answers.items():
            text = text.replace(f"{{{node_id}.answer}}", answer)
        for axis in ["axis1", "axis2", "axis3"]:
            dom = self.dominant(axis)
            text = text.replace(f"{{{axis}.dominant}}", dom)
            if axis in summary_map:
                summary_text = summary_map[axis].get(dom, "")
                text = text.replace(f"{{{axis}.summary}}", summary_text)
        return text


class Tree:
    def __init__(self, path="tree/reflection-tree.json"):
        with open(path) as f:
            data = json.load(f)
        self.nodes = {n["id"]: n for n in data["nodes"]}
        self.routing_rules = data.get("routing_rules", {})
        self.bridge_targets = self.routing_rules.get("bridge_targets", {})
        self.children = {}
        for node in data["nodes"]:
            pid = node["parentId"]
            if pid:
                self.children.setdefault(pid, []).append(node["id"])

    def get(self, node_id):
        return self.nodes[node_id]

    def next_node(self, node, state):
        nid = node["id"]
        ntype = node["type"]

        if node.get("target"):
            return node["target"]

        if nid in self.bridge_targets:
            return self.bridge_targets[nid]

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

        children = self.children.get(nid, [])
        return children[0] if children else None

    def _last_answer(self, decision_node, state):
        pid = decision_node.get("parentId")
        if pid and pid in state.answers:
            return state.answers[pid]
        if state.answers:
            return list(state.answers.values())[-1]
        return ""


# Flask app
app = Flask(__name__)
CORS(app)

# Load tree once
tree = Tree()

# Persona answer maps
PERSONAS = {
    "victim": {
        "A1_OPEN": "Stormy — things went sideways",
        "A1_Q_HARD": "I felt blocked by things or people outside me",
        "A1_Q_EXTERNAL": "Not really, the constraint was real",
        "A2_OPEN": "I felt I wasn't getting enough back for what I gave",
        "A2_Q_ENTITLEMENT": "I expected more acknowledgment than I got",
        "A3_OPEN": "Mine — I was focused on getting through it",
        "A3_Q_SELF": "Probably yes, but I didn't have bandwidth to notice",
    },
    "victor": {
        "A1_OPEN": "Partly cloudy — mixed bag",
        "A1_Q_EASY": "I prepared for it or adapted deliberately",
        "A1_Q_AGENCY": "I chose how I responded to someone's difficult behaviour",
        "A2_OPEN": "I gave more than was expected of me",
        "A2_Q_CONTRIBUTION": "Yes — I helped a colleague with something not in my job description",
        "A3_OPEN": "Someone downstream — the end user or someone we serve",
        "A3_Q_BEYOND": "It grounded me — reminded me why this matters",
    }
}


@app.route('/')
def index():
    """Home page with interactive demo"""
    return render_template('index.html')


@app.route('/reflect', methods=['POST'])
def reflect():
    """Run a reflection session"""
    data = request.json or {}
    persona = data.get('persona')
    
    state = State()
    path = []
    current_id = "START"
    
    while current_id:
        node = tree.get(current_id)
        path.append({
            "id": node["id"],
            "type": node["type"],
            "text": state.interpolate(node.get("text", ""), {})
        })
        
        if node["type"] == "question":
            # Get answer from persona or use first option
            if persona and persona in PERSONAS and node["id"] in PERSONAS[persona]:
                answer = PERSONAS[persona][node["id"]]
            else:
                answer = node["options"][0] if node["options"] else ""
            
            state.record_answer(node["id"], answer)
            state.record_signal(node.get("signal"))
            
            path[-1]["answer"] = answer
            path[-1]["signal"] = node.get("signal")
        
        elif node["type"] == "reflection":
            state.record_signal(node.get("signal"))
            path[-1]["signal"] = node.get("signal")
        
        elif node["type"] == "summary":
            summary_map = node.get("summary_map", {})
            path[-1]["summary_text"] = state.interpolate(node["text"], summary_map)
        
        current_id = tree.next_node(node, state)
    
    # Build response
    summary_node = tree.get("SUMMARY")
    summary_map = summary_node.get("summary_map", {})
    summary_text = state.interpolate(summary_node["text"], summary_map)
    
    return jsonify({
        "persona": persona,
        "path": path,
        "summary": summary_text,
        "signals": {
            "axis1": {"dominant": state.dominant("axis1"), "counts": {"internal": state.signals["axis1_internal"], "external": state.signals["axis1_external"]}},
            "axis2": {"dominant": state.dominant("axis2"), "counts": {"contribution": state.signals["axis2_contribution"], "entitlement": state.signals["axis2_entitlement"]}},
            "axis3": {"dominant": state.dominant("axis3"), "counts": {"self": state.signals["axis3_self"], "collective": state.signals["axis3_collective"], "transcendent": state.signals["axis3_transcendent"]}}
        },
        "answers": state.answers
    })


@app.route('/tree')
def get_tree():
    """Return the full tree structure"""
    with open("tree/reflection-tree.json") as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/stats')
def get_stats():
    """Get tree statistics"""
    with open("tree/reflection-tree.json") as f:
        data = json.load(f)
    
    nodes = data["nodes"]
    counts = {}
    for node in nodes:
        ntype = node["type"]
        counts[ntype] = counts.get(ntype, 0) + 1
    
    return jsonify({
        "total_nodes": len(nodes),
        "node_counts": counts,
        "axes": data["meta"]["axes"],
        "description": data["meta"]["description"]
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)