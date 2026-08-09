#!/usr/bin/env python3
"""Thin interactive session runner for the FIRST_VERTICAL_SCENARIO (task-004).

This module is the minimal interactive session runner that makes ONE
real-material learning session with a human learner runnable. It is the thin
vertical seam for Gate 3 — NOT a helper-module build-out, NOT a product, NOT a
learner model.

Six scenario steps (authoritative behavior in docs/FIRST_VERTICAL_SCENARIO.md):
  1. Material Position Recovery — returning session: load the saved minimal
     state via scripts/learning_state.load_state and present the saved
     position; new session: accept a natural-language goal.
  2. Task Boundary — record task_boundary (material section range, task type,
     observable completion criterion) and confirm with the user.
  3. Confusion Expression — accept ANY natural-language confusion statement
     (including "I don't know where I'm confused") without rejection.
  4. Bounded Pedagogical Action — select ONE action via the six documented
     decision-tree rules in docs/PEDAGOGICAL_ACTION_DECISION_TREE.md and cite
     the relevant material section. Thin rule implementation only: no
     automatic obstacle-type detection before the user speaks.
  5. Independent Check — request an observable demonstration and record
     evidence_level 0|1|2.
  6. State Persistence — save the minimal state via learning_state.save_state
     (reused unchanged), generate the next-action recommendation, and display
     a "Saved your progress" confirmation.

Evidence discipline: recorded evidence contains only factual observations
(verbatim user statements, user-confirmed positions, the delivered action, and
the learner's observable demonstration outcome). Nothing infers that the user
understands a section from position confirmation alone; there is no mastery
classifier.

Reuse, do NOT rebuild: templates/MINIMAL_LEARNING_STATE.schema.json (unchanged),
scripts/learning_state.py (unchanged API), docs/FIRST_VERTICAL_SCENARIO.md and
docs/PEDAGOGICAL_ACTION_DECISION_TREE.md (authoritative behavior references).

Explicitly NOT built (must not be): generic indexing service, vector DB,
learner model, automatic mastery classifier, scheduler, frontend,
multi-course support, generic orchestration, persistence framework, chat
history summarization.
"""

import argparse
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import learning_state as ls  # reused unchanged (allowed read-only dependency)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TASK_TYPES = [
    "understand_concept",
    "solve_problem",
    "apply_to_example",
    "explain_reasoning",
]

ACTION_TYPES = [
    "clarify_terminology",
    "restore_prerequisite",
    "give_bounded_example",
    "request_explanation",
    "request_fresh_attempt",
    "stop_and_request_more_material",
]

_SECTION_RE = re.compile(r"^(#{1,6})\s+(.+)$")
_NAMED_SECTION_RE = re.compile(
    r"^(chapter|section|lesson|unit|part|module)\s+[\dIVX]+[.:]?\s*(.*)$",
    re.IGNORECASE,
)
_NUMBERED_HEADING_RE = re.compile(r"^(\d+(?:\.\d+)*)\s+(.+)$")

_COMMON = set(
    "the and for are you your this that with from have what why how does do is "
    "it not in on of to a i we they he she can could will would was were be been "
    "being where when who which there here then than".split()
)

_VAGUE = {
    "know", "knows", "learn", "learns", "learned", "learning", "understand",
    "understands", "remember", "remembered", "forgot", "explain", "explains",
    "confused", "confusing", "unclear", "stuck", "step", "steps", "material",
    "notes", "note", "section", "sections", "course", "something", "everything",
    "thing", "things", "mean", "means", "work", "works", "working", "right",
    "wrong", "question", "answer", "problem", "problems", "example", "examples",
    "reason", "reasons", "progress", "again", "next", "previous", "topic",
    "topics", "part", "parts", "different", "confused",
}


# ---------------------------------------------------------------------------
# Material loading (thin seam: a path to a text/sectioned document)
# ---------------------------------------------------------------------------


def match_section_heading(line):
    """Return a section heading for *line*, or None. Thin: markdown '#' plus
    a few plain-text numbered/worded patterns. No parser framework."""
    s = line.strip()
    if not s:
        return None
    m = _SECTION_RE.match(s)
    if m:
        return m.group(2).strip()
    if _NAMED_SECTION_RE.match(s) or _NUMBERED_HEADING_RE.match(s):
        return s
    return None


def load_material(path):
    """Load a text/sectioned document into a thin in-memory structure.

    Returns a dict with keys: name, path, text, lines, sections (list of
    {"heading", "start_line", "end_line"}). No indexing service, no vector DB.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"material file not found: {path}")
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    sections = []
    current = None
    for i, line in enumerate(lines):
        heading = match_section_heading(line)
        if heading:
            if current is not None:
                current["end_line"] = i
            current = {"heading": heading, "start_line": i, "end_line": len(lines)}
            sections.append(current)
    if not sections:
        sections = [{"heading": path.name, "start_line": 0, "end_line": len(lines)}]
    return {
        "name": path.name,
        "path": str(path),
        "text": text,
        "lines": lines,
        "sections": sections,
    }


def _section_body(material, section_heading):
    for sec in material["sections"]:
        if sec["heading"] == section_heading:
            return "\n".join(material["lines"][sec["start_line"]: sec["end_line"]])
    return material["text"]


def _find_example_section(material, current_section):
    markers = ("example", "worked", "problem", "exercise", "sample")
    for sec in material["sections"]:
        h = sec["heading"].lower()
        if any(m in h for m in markers):
            return sec["heading"]
    return None


def _find_section_with_term(material, term):
    if not term:
        return None
    term_l = term.lower()
    for sec in material["sections"]:
        if term_l in sec["heading"].lower():
            return sec["heading"]
    for sec in material["sections"]:
        body = "\n".join(material["lines"][sec["start_line"]: sec["end_line"]])
        if term_l in body.lower():
            return sec["heading"]
    return None


def _distinctive_tokens(text_l):
    return [
        t for t in re.findall(r"[a-z]{4,}", text_l)
        if t not in _COMMON and t not in _VAGUE
    ]


def _find_prerequisite_section(material, statement, current_section):
    idx = None
    for i, sec in enumerate(material["sections"]):
        if sec["heading"] == current_section:
            idx = i
            break
    cues = _distinctive_tokens(statement.lower())
    for i, sec in enumerate(material["sections"]):
        if idx is not None and i >= idx:
            continue
        body = "\n".join(material["lines"][sec["start_line"]: sec["end_line"]]).lower()
        for cue in cues:
            if cue and (cue in sec["heading"].lower() or cue in body):
                return sec["heading"]
    if idx is not None and idx > 0:
        return material["sections"][idx - 1]["heading"]
    return None


def _extract_term(statement):
    s = statement.strip()
    m = re.search(r"what does\s+([a-zA-Z][\w '.-]*?)\s+mean\b", s, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    m = re.search(r"what(?:'s| is)\s+([a-zA-Z][\w '.-]{1,40}?)(?:\s+mean\b|\?|\.|$)", s, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    m = re.search(r"don't understand\s+(?:the\s+)?([a-zA-Z][\w '.-]{1,40})", s, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    m = re.search(r"([a-zA-Z][\w '.-]{1,40})\s+means\b", s, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return None


def _extract_prerequisite(statement):
    m = re.search(
        r"(?:don't remember|forgot|didn't learn|haven't seen)\s+(?:the\s+|about\s+)?([a-zA-Z][\w '.-]{1,40})",
        statement,
        re.IGNORECASE,
    )
    return m.group(1).strip() if m else None


# ---------------------------------------------------------------------------
# Step 3: Confusion classification (thin, AFTER the user speaks)
# ---------------------------------------------------------------------------


def classify_confusion(statement, material=None):
    """Classify a confusion statement. Thin keyword routing only.

    Runs strictly AFTER the user speaks (never before). Returns the
    observed_difficulty payload (minus expressed_at, added by the runner).
    """
    text = statement.strip().lower()

    cannot_articulate = any(
        marker in text
        for marker in (
            "i don't know where i'm confused",
            "i dont know where i'm confused",
            "can't articulate",
            "cannot articulate",
            "don't know what's confusing",
            "don't know what is confusing",
            "not sure where i'm confused",
            "everything is confusing",
            "can't even say what's confusing",
        )
    )
    articulation = "cannot_articulate" if cannot_articulate else "articulated"

    scope = "in_scope"
    if any(m in text for m in ("don't have the", "missing the section", "missing material", "need the section", "required material")):
        scope = "missing_required_material"
    elif any(
        m in text
        for m in (
            "not in the material", "not in my notes", "not covered", "isn't in",
            "isn't covered", "doesn't cover", "didn't cover", "not in the course",
            "not uploaded", "haven't uploaded", "need more material", "outside the",
            "beyond the material", "a different topic", "different topic",
        )
    ):
        scope = "outside_supplied_corpus"
    elif material is not None and _references_uncovered_topic(statement, material):
        scope = "outside_supplied_corpus"

    classification = None
    if articulation == "articulated":
        if any(
            m in text
            for m in (
                "stuck at step", "stuck on step", "can't get past step",
                "cannot get past step", "step 1", "step 2", "step 3", "step 4",
                "step 5", "stuck at the", "can't get past the",
            )
        ):
            classification = "stuck_on_specific_step"
        elif any(
            m in text
            for m in ("what does", " what is", "what's", "means", "mean?", "terminolog", "definition", "don't understand the word", "not sure what", "meaning of")
        ):
            classification = "terminology_gap"
        elif any(
            m in text
            for m in ("don't remember", "forgot", "learned before", "didn't learn", "haven't seen", "remind me", "prerequisite", "earlier section", "from before", "before this")
        ):
            classification = "prerequisite_deficit"
        elif any(
            m in text
            for m in ("why does", "why do", "why is", "reason", "concept", "logic", "understand why", "works this way", "does this work", "why it works", "why this works")
        ):
            classification = "conceptual_confusion"
        elif any(
            m in text
            for m in ("don't know how", "how do i", "how to", "steps", "procedure", "process", "what do i do", "how does one")
        ):
            classification = "procedural_confusion"
        elif any(
            m in text
            for m in ("where was i", "forgot where", "lost", "what was i doing", "where am i", "context")
        ):
            classification = "lost_context"

    section = None
    if material is not None and material["sections"]:
        section = material["sections"][0]["heading"]

    return {
        "user_statement": statement,
        "obstacle_classification": classification,
        "material_scope_status": scope,
        "articulation_status": articulation,
        "material_context": {"section": section, "page": None, "problem": None},
    }


def _references_uncovered_topic(statement, material):
    """Conservative topical check: only capitalized mid-sentence or quoted
    terms count as explicit topic references. Common lowercase words never
    trigger an out-of-scope classification on their own."""
    material_text = material["text"].lower()
    words = re.findall(r"[A-Za-z][A-Za-z-]{2,}", statement)
    candidates = set()
    for i, w in enumerate(words):
        if i == 0 or words[i - 1].endswith((".", "!", "?")):
            continue  # skip sentence-initial words
        if w[0].isupper():
            candidates.add(w.lower())
    for quoted in re.findall(r"['\"]([^'\"]{2,40})['\"]", statement):
        candidates.add(quoted.lower().strip())
    return any(c not in material_text for c in candidates)


# ---------------------------------------------------------------------------
# Step 4: Bounded Pedagogical Action (six decision-tree rules)
# ---------------------------------------------------------------------------


def select_pedagogical_action(difficulty, material, task_boundary=None,
                              current_section=None, material_name="material.txt"):
    """Select exactly ONE of the six documented decision-tree actions.

    Rules (docs/PEDAGOGICAL_ACTION_DECISION_TREE.md), evaluated in order:
      scope -> cannot_articulate -> terminology -> prerequisite ->
      procedural/lost_context -> conceptual -> stuck -> fallback.
    """
    if material["sections"]:
        fallback_section = current_section or material["sections"][0]["heading"]
    else:
        fallback_section = current_section or "Current section"

    def citation(section):
        return {"file": material_name, "section": section, "page": None}

    scope = difficulty.get("material_scope_status", "in_scope")
    if scope in ("outside_supplied_corpus", "missing_required_material"):
        return {
            "action_type": "stop_and_request_more_material",
            "action_details": {
                "stop_reason": (
                    "The topic you're asking about isn't covered in the uploaded "
                    "material. Please upload the relevant section, or we can focus "
                    "on the material you have."
                )
            },
            "material_citations": [],
            "reason": "material_scope_not_supplied",
        }

    if difficulty.get("articulation_status") == "cannot_articulate":
        example = _find_example_section(material, fallback_section)
        if example is not None:
            return {
                "action_type": "give_bounded_example",
                "action_details": {"example_shown": example},
                "material_citations": [citation(example)],
                "reason": "unarticulated_confusion_diagnostic_example",
            }
        return {
            "action_type": "request_explanation",
            "action_details": {"explanation_requested": "Can you walk through what you've tried so far?"},
            "material_citations": [citation(fallback_section)],
            "reason": "unarticulated_confusion_diagnostic_explanation",
        }

    classification = difficulty.get("obstacle_classification")
    statement = difficulty.get("user_statement", "")

    if classification == "terminology_gap":
        term = _extract_term(statement)
        section = _find_section_with_term(material, term) if term else None
        if section is None:
            return {
                "action_type": "stop_and_request_more_material",
                "action_details": {
                    "stop_reason": f"The term '{term or 'you mentioned'}' isn't defined in the uploaded material. Please upload the relevant section."
                },
                "material_citations": [],
                "reason": "term_not_in_corpus",
            }
        return {
            "action_type": "clarify_terminology",
            "action_details": {"term_clarified": term},
            "material_citations": [citation(section)],
            "reason": "rule_1_terminology_gap",
        }

    if classification == "prerequisite_deficit":
        prereq = _extract_prerequisite(statement)
        section = _find_prerequisite_section(material, statement, fallback_section)
        if section is None:
            return {
                "action_type": "stop_and_request_more_material",
                "action_details": {
                    "stop_reason": "The prerequisite isn't present in the uploaded material. Please upload it, or we'll focus on the material you have."
                },
                "material_citations": [],
                "reason": "prerequisite_not_in_corpus",
            }
        return {
            "action_type": "restore_prerequisite",
            "action_details": {"prerequisite_concept": prereq or statement},
            "material_citations": [citation(section)],
            "reason": "rule_2_prerequisite_deficit",
        }

    if classification in ("procedural_confusion", "lost_context"):
        example = _find_example_section(material, fallback_section)
        if example is None:
            return {
                "action_type": "stop_and_request_more_material",
                "action_details": {
                    "stop_reason": "No similar worked example exists in the uploaded material. Please upload one, or we'll work from the current section."
                },
                "material_citations": [],
                "reason": "no_similar_example_in_corpus",
            }
        return {
            "action_type": "give_bounded_example",
            "action_details": {"example_shown": example},
            "material_citations": [citation(example)],
            "reason": "rule_3_procedural_or_lost_context",
        }

    if classification == "conceptual_confusion":
        return {
            "action_type": "request_explanation",
            "action_details": {"explanation_requested": "Can you explain why this works in your own words?"},
            "material_citations": [citation(fallback_section)],
            "reason": "rule_4_conceptual_confusion",
        }

    if classification == "stuck_on_specific_step":
        return {
            "action_type": "request_fresh_attempt",
            "action_details": {"hint_provided": "Re-read the material's example for the step you're on, then try that step again."},
            "material_citations": [citation(fallback_section)],
            "reason": "rule_5_stuck_on_specific_step",
        }

    return {
        "action_type": "give_bounded_example",
        "action_details": {"example_shown": fallback_section},
        "material_citations": [citation(fallback_section)],
        "reason": "fallback_unclassified_confusion",
    }


def _describe_action(action):
    action_type = action["action_type"].replace("_", " ")
    details = action.get("action_details") or {}
    extra = ""
    for key in (
        "term_clarified", "prerequisite_concept", "example_shown",
        "explanation_requested", "hint_provided", "stop_reason",
    ):
        if details.get(key):
            extra = f" — {details[key]}"
            break
    citations = "; ".join(
        f"{c.get('file')} → section '{c.get('section')}'"
        for c in action.get("material_citations", [])
    ) or "no citation (material request)"
    return f"Action: {action_type}{extra}. Citing: {citations}."


# ---------------------------------------------------------------------------
# Step 5: Independent check
# ---------------------------------------------------------------------------


def _check_request(task_boundary):
    ttype = task_boundary.get("task_type")
    scope = task_boundary.get("scope_description") or "the task"
    criterion = task_boundary.get("completion_criterion") or ""
    if ttype == "solve_problem":
        return ("solve_similar_problem",
                f"Can you solve a similar problem independently? (completion: {criterion})")
    if ttype == "apply_to_example":
        return ("apply_to_example", f"Can you apply '{scope}' to a new example?")
    if ttype == "explain_reasoning":
        return ("explain_concept", f"Can you explain your reasoning for '{scope}' step by step?")
    return ("explain_concept",
            f"Can you explain '{scope}' in your own words? (completion: {criterion})")


def _evaluation_for(evidence_level):
    """Factual-only evaluation notes. Never a mastery claim."""
    if evidence_level == 2:
        return {
            "correct_elements": ["Learner provided a demonstration response matching the request (recorded verbatim)."],
            "incorrect_elements": [],
        }
    if evidence_level == 1:
        return {
            "correct_elements": [],
            "incorrect_elements": ["Learner's demonstration was partial per the recorded response."],
        }
    return {
        "correct_elements": [],
        "incorrect_elements": ["No completed demonstration this session."],
    }


# ---------------------------------------------------------------------------
# Step 6: next-action recommendation
# ---------------------------------------------------------------------------


def build_next_action(state):
    evidence = state["independent_check"]["evidence_level"]
    section = state["current_position"]["section"]
    tb = state["task_boundary"]
    last = state["last_pedagogical_action"]
    if evidence == 2:
        recommendation = f"Try the next problem or concept after '{section}'."
        rationale = "evidence_level_2_achieved_proceed_to_next"
    elif evidence == 1:
        recommendation = (
            f"Review the prerequisite for '{section}', then retry: {tb.get('completion_criterion', 'the task')}."
        )
        rationale = "evidence_level_1_review_and_retry"
    else:
        recommendation = (
            f"Continue from '{section}' with the suggested action ({last.get('action_type', 'suggested action').replace('_', ' ')})."
        )
        rationale = "evidence_level_0_continue_from_current"
    return {
        "recommendation": recommendation,
        "rationale": rationale,
        "suggested_material_section": section,
    }


# ---------------------------------------------------------------------------
# Session I/O
# ---------------------------------------------------------------------------


class SessionIO:
    """Thin I/O seam: interactive (default) or scripted (tests)."""

    def __init__(self, input_fn=None, output_fn=None):
        self.input_fn = input_fn if input_fn is not None else input
        self.output_fn = output_fn if output_fn is not None else print

    def say(self, text=""):
        self.output_fn(text)

    def ask(self, prompt=""):
        return str(self.input_fn(prompt)).strip()


def _ask_yes_no(io, prompt, default="yes"):
    while True:
        ans = io.ask(prompt).strip().lower()
        if not ans and default:
            ans = default
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        io.say("Please answer yes or no.")


def _ask_task_type(io):
    io.say("Task type options:")
    for i, t in enumerate(TASK_TYPES, 1):
        io.say(f"  {i}. {t}")
    while True:
        ans = io.ask("Task type (number or name):").strip().lower()
        if ans.isdigit():
            n = int(ans)
            if 1 <= n <= len(TASK_TYPES):
                return TASK_TYPES[n - 1]
        elif ans in TASK_TYPES:
            return ans
        io.say(f"Please choose one of: {', '.join(TASK_TYPES)}")


def _select_section(io, material):
    sections = material["sections"]
    io.say("Sections in your material:")
    for i, sec in enumerate(sections, 1):
        io.say(f"  {i}. {sec['heading']}")
    while True:
        ans = io.ask("Which section are you working on? (number or name):").strip()
        if ans.isdigit():
            n = int(ans)
            if 1 <= n <= len(sections):
                return sections[n - 1]["heading"]
        else:
            for sec in sections:
                if ans.lower() in sec["heading"].lower():
                    return sec["heading"]
        io.say("I don't see that section. Please choose from the list.")


def _ask_evidence_level(io):
    while True:
        ans = io.ask("How did your demonstration go? Enter 2, 1, or 0:").strip().lower()
        if ans in ("2", "0", "1"):
            return int(ans)
        io.say("Please enter 2 (completed), 1 (partial), or 0 (could not).")


# ---------------------------------------------------------------------------
# The 6-step runner
# ---------------------------------------------------------------------------


def _new_session_state(material, now):
    return {
        "schema_version": "1.0",
        "scenario_id": "source-grounded-learning-recovery-and-independent-completion-check",
        "session_id": "session-" + now.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "created_at": now.isoformat(timespec="seconds"),
        "updated_at": now.isoformat(timespec="seconds"),
        "current_position": None,
        "task_boundary": None,
        "observed_difficulty": None,
        "last_pedagogical_action": None,
        "independent_check": None,
        "next_action": None,
        "session_metadata": {
            "duration_seconds": None,
            "position_recovery_seconds": None,
            "steps_completed": [],
        },
    }


def _load_saved_state(state_path):
    path = Path(state_path)
    if not path.exists():
        return None
    try:
        return ls.load_state(path)
    except (ls.LearningStateError, ValueError, OSError):
        return None


def _step1_position_recovery(io, material, state, saved, now):
    io.say("--- Step 1: Material Position Recovery ---")
    if saved is not None:
        pos = saved["current_position"]
        page = f", page {pos.get('page')}" if pos.get("page") else ""
        io.say(f"Saved position: section '{pos['section']}' in '{pos['material_file']}'{page}")
        tb = saved.get("task_boundary") or {}
        diff = saved.get("observed_difficulty") or {}
        io.say(f"Last attempted task: {tb.get('scope_description', '(none recorded)')}")
        io.say(f"Last confusion: {diff.get('user_statement', '(none recorded)')}")
        if _ask_yes_no(io, "Do you want to continue from this saved position? (yes/no)"):
            state["current_position"] = {
                "material_file": material["name"],
                "section": pos["section"],
                "page": pos.get("page"),
                "problem_number": pos.get("problem_number"),
                "confirmed_by_user": True,
                "confirmed_at": now.isoformat(timespec="seconds"),
            }
            io.say("Position confirmed — factual observation that you confirmed the position. This does not imply you understand the section.")
            return True
        io.say("Starting fresh position recovery.")
    goal = io.ask("What are you trying to learn or understand?").strip()
    io.say(f"Goal recorded (verbatim): {goal or '(no goal given)'}")
    while True:
        section = _select_section(io, material)
        io.say(f"It looks like you're working on [{section}]. Is that right?")
        if _ask_yes_no(io, "(yes/no)"):
            state["current_position"] = {
                "material_file": material["name"],
                "section": section,
                "page": None,
                "problem_number": None,
                "confirmed_by_user": True,
                "confirmed_at": now.isoformat(timespec="seconds"),
            }
            io.say("Position confirmed — factual observation that you confirmed the position. This does not imply you understand the section.")
            return True


def _step2_task_boundary(io, material, state, now, saved):
    io.say("--- Step 2: Task Boundary ---")
    if saved is not None:
        tb = saved.get("task_boundary")
        if tb:
            io.say(
                f"Saved task boundary: type={tb.get('task_type')}, scope='{tb.get('scope_description')}', "
                f"sections='{tb.get('start_section')}' → '{tb.get('end_section') or tb.get('start_section')}', "
                f"completion='{tb.get('completion_criterion')}'"
            )
            if _ask_yes_no(io, "Reuse this saved task boundary? (yes/no)"):
                state["task_boundary"] = dict(tb)
                return
    while True:
        task_type = _ask_task_type(io)
        scope = io.ask("What are you trying to achieve?").strip()
        start = io.ask(
            f"Start section (default: '{state['current_position']['section']}'):"
        ).strip() or state["current_position"]["section"]
        end = io.ask("End section (default: same as start):").strip() or None
        criterion = io.ask("What observable result shows you're done?").strip()
        tb = {
            "task_type": task_type,
            "scope_description": scope,
            "start_section": start,
            "end_section": end,
            "completion_criterion": criterion,
        }
        io.say("Task boundary to confirm:")
        io.say(f"  type: {task_type}")
        io.say(f"  scope: {scope}")
        io.say(f"  sections: {start} → {end or start}")
        io.say(f"  completion: {criterion}")
        if _ask_yes_no(io, "Is this the task you're working on? (yes/no)"):
            state["task_boundary"] = tb
            return


def _step3_confusion(io, material, state, now):
    io.say("--- Step 3: Confusion Expression ---")
    statement = io.ask(
        "What's confusing or unclear? (ANY answer is fine — including 'I don't know where I'm confused'):"
    )
    if not statement:
        statement = "I don't know where I'm confused"
    diff = classify_confusion(statement, material)
    diff["expressed_at"] = now.isoformat(timespec="seconds")
    state["observed_difficulty"] = diff
    io.say("Recorded verbatim. No rejection; any natural-language statement is accepted.")


def _step4_action(io, material, state, now):
    io.say("--- Step 4: Bounded Pedagogical Action ---")
    difficulty = state["observed_difficulty"]
    action = select_pedagogical_action(
        difficulty,
        material,
        state["task_boundary"],
        current_section=state["current_position"]["section"],
        material_name=material["name"],
    )
    # Schema constraint: a stop action with no citations requires the observed
    # difficulty to be missing/outside scope.
    if action["action_type"] == "stop_and_request_more_material" and not action["material_citations"]:
        if difficulty["material_scope_status"] == "in_scope":
            difficulty["material_scope_status"] = "missing_required_material"
    action["delivered_at"] = now.isoformat(timespec="seconds")
    action["user_response"] = None
    action["escalation_count"] = 0
    state["last_pedagogical_action"] = action
    io.say(_describe_action(action))
    # 'reason' documents the decision-tree rule internally but is not part of
    # the schema; keep it out of the persisted state.
    action.pop("reason", None)
    resp = io.ask("How does that land for you? (optional — press Enter to continue):").strip()
    if resp:
        action["user_response"] = resp


def _step5_check(io, state, now):
    io.say("--- Step 5: Independent Check ---")
    tb = state["task_boundary"]
    check_type, request = _check_request(tb)
    io.say(f"Independent check: {request}")
    response = io.ask("Your demonstration / response:").strip() or "(no response provided)"
    io.say("Evidence level: 2 = completed ONE correct demonstration; 1 = partial/incorrect attempt; 0 = no demonstration.")
    level = _ask_evidence_level(io)
    state["independent_check"] = {
        "requested": True,
        "check_type": check_type,
        "user_response": response,
        "evidence_level": level,
        "evaluation": _evaluation_for(level),
        "checked_at": now.isoformat(timespec="seconds"),
    }
    io.say(f"Evidence level {level} recorded — an observable classification of your demonstration, not a mastery claim.")


def _step6_persist(io, state, state_path, now, duration_seconds, position_recovery_seconds):
    io.say("--- Step 6: State Persistence ---")
    state["next_action"] = build_next_action(state)
    state["updated_at"] = now.isoformat(timespec="seconds")
    state["session_metadata"]["duration_seconds"] = duration_seconds
    state["session_metadata"]["position_recovery_seconds"] = position_recovery_seconds
    state["session_metadata"]["steps_completed"] = [1, 2, 3, 4, 5, 6]
    path = Path(state_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    ls.save_state(state, path)
    io.say(f"Saved your progress at {state['current_position']['section']}.")
    io.say(f"Next time: {state['next_action']['recommendation']}")


def run_session(material_path, state_path, io, now=None):
    """Run one 6-step pilot session. Returns the final minimal state dict."""
    now_fn = now if now is not None else (lambda: datetime.now(timezone.utc))
    material = load_material(material_path)
    state_path = Path(state_path)
    started = time.monotonic()

    saved = _load_saved_state(state_path)
    if saved is not None:
        saved_pos = saved["current_position"]
        if saved_pos.get("material_file") != material["name"]:
            io.say(f"Note: saved state was for '{saved_pos.get('material_file')}' but you're now using '{material['name']}'; starting a new position.")
            saved = None

    state = _new_session_state(material, now_fn())
    position_confirmed = _step1_position_recovery(io, material, state, saved, now_fn())
    position_recovery_seconds = int(time.monotonic() - started) if position_confirmed else None

    _step2_task_boundary(io, material, state, now_fn(), saved)
    _step3_confusion(io, material, state, now_fn())
    _step4_action(io, material, state, now_fn())
    _step5_check(io, state, now_fn())
    _step6_persist(
        io, state, state_path, now_fn(),
        int(time.monotonic() - started), position_recovery_seconds,
    )
    return state


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="pilot_session.py",
        description="Thin interactive session runner for the FIRST_VERTICAL_SCENARIO 6-step flow (Gate 3).",
    )
    parser.add_argument(
        "--material", required=True,
        help="Path to the real course material (text/sectioned document), provided at runtime.",
    )
    parser.add_argument(
        "--state", default="minimal_learning_state.json",
        help="Path to the minimal learning state file (default: ./minimal_learning_state.json).",
    )
    args = parser.parse_args(argv)
    run_session(args.material, args.state, SessionIO())
    return 0


if __name__ == "__main__":
    sys.exit(main())
