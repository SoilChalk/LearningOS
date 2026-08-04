# Pedagogical Action Decision Tree

**Generated**: 2026-08-01
**Task**: task-002-first-vertical-scenario-design
**Gate**: Gate 2 - First Vertical Scenario Design
**Status**: Provisional Decision Tree for First Vertical Scenario

---

## Purpose

This decision tree maps observable interaction evidence to bounded pedagogical actions for the "Source-Grounded Learning Recovery and Independent Completion Check" scenario. It is **provisional** and **scenario-specific**, not a general teaching framework.

**Design Constraint** (from src-002, RESEARCH_QUESTIONS.md RQ3.2):
- System does NOT automatically detect obstacle types BEFORE user expresses confusion
- Classification happens AFTER user statement
- Tree routes based on observable evidence, not inferred learner states

---

## Decision Tree Structure

### Input to Tree

**Required Inputs**:
1. **User Confusion Statement** (verbatim from Step 3)
2. **Obstacle Classification** (one of six types or null)
3. **Material Scope Status** (in_scope, missing_required_material, outside_supplied_corpus)
4. **Articulation Status** (articulated, cannot_articulate)
5. **Material Context** (section/problem where confusion occurred)
6. **Task Boundary** (concept understanding vs. problem solving)

**Six Core Obstacle Classifications** (when user can articulate):
1. **Terminology Gap**: User mentions unfamiliar term or asks "what does X mean?"
2. **Prerequisite Deficit**: User states "I don't remember Y" or references earlier material
3. **Procedural Confusion**: User understands goal but not steps ("I don't know how to...")
4. **Conceptual Confusion**: User understands steps but not why ("Why does this work?")
5. **Lost Context**: User states "I forgot where I was" or "What am I solving?"
6. **Stuck on Specific Step**: User identifies precise location ("I'm stuck at step 3")

**Note**: When articulation_status is "cannot_articulate", obstacle_classification may be null.

### Output from Tree

**One Pedagogical Action** selected from six options:
1. **Clarify Terminology**
2. **Restore Prerequisite**
3. **Give Bounded Example**
4. **Request Explanation**
5. **Request Fresh Attempt**
6. **Stop and Request More Material**

---

## Decision Rules

### Rule Set 1: Terminology Gap

**Trigger**: User statement contains unfamiliar term OR explicitly asks "what does [term] mean?"

**Observable Evidence**:
- User writes: "I don't understand what [term X] means"
- User writes: "What is [term X]?"
- User uses term incorrectly in their confusion statement

**Action Selected**: **Clarify Terminology**

**Action Specification**:
1. Locate term definition in uploaded material (exact section)
2. Cite material section: "In [Section Y, Page Z], [term X] is defined as..."
3. Use material's exact wording for definition (preserve source vocabulary)
4. If term appears in multiple sections: cite first occurrence OR section closest to user's current position

**Failure Mode**:
- If term NOT in uploaded material: Select "Stop and Request More Material"

**Evidence Collected**:
- Factual: Definition delivered, material section cited
- Inference avoided: Do NOT infer "user will now understand entire concept" from definition alone

**Source Grounding** (src-001, src-002): Definition MUST come from uploaded corpus with citation

---

### Rule Set 2: Prerequisite Deficit

**Trigger**: User statement references earlier material they don't recall OR states "I don't remember [concept Y]"

**Observable Evidence**:
- User writes: "I don't remember how to [do Y]"
- User writes: "We learned [Y] before but I forgot"
- User attempts problem but shows gap in foundational step

**Action Selected**: **Restore Prerequisite**

**Action Specification**:
1. Identify prerequisite concept mentioned by user
2. Locate prerequisite section in uploaded material (earlier chapter/section)
3. Cite prerequisite section: "You covered [concept Y] in [Section A]. Here's the key idea: ..."
4. Provide brief reminder from material (1-2 sentences) with citation
5. Link back to current task: "Now you can apply [Y] to [current problem]"

**Failure Mode**:
- If prerequisite section NOT in uploaded material: Select "Stop and Request More Material"
- If prerequisite too extensive to review briefly: Suggest user review section before returning

**Evidence Collected**:
- Factual: Prerequisite section cited, user acknowledged link
- Observable: User said "okay" or asked follow-up question
- Inference avoided: Do NOT infer "user has re-mastered prerequisite" from brief reminder

**Source Grounding**: Prerequisite reminder MUST cite uploaded material section

---

### Rule Set 3: Procedural Confusion (+ Lost Context)

**Trigger**: User understands goal but not steps ("I don't know how to...") OR lost track of process

**Observable Evidence**:
- User writes: "I don't know how to solve this"
- User writes: "What steps do I follow?"
- User writes: "I forgot what I'm supposed to do here"
- User attempts problem but shows missing/incorrect procedural steps

**Action Selected**: **Give Bounded Example**

**Action Specification**:
1. Locate worked example in uploaded material (similar problem/process)
2. Show example step-by-step WITH material citation
3. Annotate each step: explain what is being done and why (use material's own explanations)
4. Link example to user's current task: "Your problem is similar. Try following these steps..."

**Boundary Constraint**:
- Example MUST come from uploaded material (not generated by system)
- If no similar example exists: Offer to break down current problem into steps (using material's notation/terminology)

**Failure Mode**:
- If no example in material AND user cannot proceed: Select "Stop and Request More Material"

**Evidence Collected**:
- Factual: Example shown, material cited, user viewed steps
- Observable: User said "I see" or "okay" or asked clarifying question
- Inference avoided: Do NOT infer "user can now solve independently" without Step 5 check

**Source Grounding**: Example MUST be from uploaded corpus OR steps MUST use material's exact terminology/notation

---

### Rule Set 4: Conceptual Confusion

**Trigger**: User understands steps but not why ("Why does this work?")

**Observable Evidence**:
- User writes: "Why do we [do X]?"
- User writes: "I can follow the steps but don't understand the reason"
- User completes procedural steps correctly but asks "why?" afterward

**Action Selected**: **Request Explanation**

**Action Specification**:
1. Ask user to explain concept/step in their own words: "Can you explain why [X] works?"
2. Wait for user response
3. Compare user explanation to material's explanation (cite material section)
4. Highlight correct parts: "Yes, that's right because..." (cite material)
5. Clarify misconceptions: "Not quite. The material says [Y because Z]..." (cite material)

**Pedagogical Rationale** (src-002: Socratic guidance, src-007: dialogic feedback):
- Requesting explanation encourages active processing
- User's explanation reveals conceptual understanding gaps
- Comparison to material makes reasoning explicit

**Failure Mode**:
- If user declines to explain: Offer alternative — "Would you like me to explain using the material's reasoning?"
- If user explanation completely off-track: Switch to "Give Bounded Example" to show reasoning

**Evidence Collected**:
- Factual: User provided explanation (verbatim), material comparison made
- Observable: User explanation contained correct/incorrect elements
- Inference avoided: Do NOT infer "user deeply understands" from single correct explanation

**Source Grounding**: Feedback MUST reference material's reasoning with citations

---

### Rule Set 5: Stuck on Specific Step

**Trigger**: User identifies precise location where stuck ("I'm stuck at step 3")

**Observable Evidence**:
- User writes: "I got stuck at [step N]"
- User writes: "I don't know what to do after [action X]"
- User shows partial work up to a specific point then stops

**Action Selected**: **Request Fresh Attempt**

**Action Specification**:
1. Acknowledge user's stuck point: "You've completed steps 1-2 correctly. Let's look at step 3..."
2. Provide targeted hint for NEXT step only (not full solution):
   - Terminology hint: "Remember that [term X] means..."
   - Prerequisite hint: "You need [concept Y] from [Section A]..."
   - Procedural hint: "The next step is to [action Z]..."
3. Ask user to try continuing from that hint
4. Wait for user attempt

**Boundary Constraint**:
- Hint MUST be minimal (reveal next step, not full path)
- Hint MUST use material's terminology and cite material section

**Failure Mode**:
- If user still stuck after hint: Escalate to "Give Bounded Example" (show similar problem)
- If user stuck on multiple steps: Escalate to "Give Bounded Example" (full worked example)

**Evidence Collected**:
- Factual: Hint delivered, user attempted next step
- Observable: User completed step, remained stuck, or requested more help
- Inference avoided: Do NOT infer "user can complete entire problem" from one step success

**Source Grounding**: Hint MUST reference material's problem-solving process

---

### Rule Set 6: Confusion Outside Corpus OR User Cannot Articulate

**Trigger**: User confusion references content not in uploaded material OR user states "I don't know what's confusing"

**Observable Evidence**:
- User asks about topic not in uploaded material
- User writes: "I don't know what I don't know"
- User writes: "Everything is confusing"
- User references external resource not uploaded

**Action Selected**: **Stop and Request More Material**

**Action Specification**:
1. Explicit message: "That topic isn't covered in your uploaded materials"
2. Request: "Can you upload the section covering [topic X], or shall we focus on what you have?"
3. If user uploads additional material: Re-index and return to decision tree with new corpus
4. If user chooses to focus on current material: Route to "Give Bounded Example" or "Request Explanation" for current section

**Alternative for "I don't know what's confusing"**:
- Do NOT fail — this is valid confusion expression (per Gate 3 pilot design)
- Action: Route to "Give Bounded Example" for current section OR "Request Explanation" to prompt articulation

**Evidence Collected**:
- Factual: Out-of-scope detected, material request made, user response
- Observable: User uploaded more material OR declined OR redirected focus

**Source Grounding**: Explicit failure mode from src-001 (no relevant information in sources)

---

## Decision Tree Flow Diagram

```
User Confusion Statement (Step 3)
         |
         v
System Classification
         |
    +---------+---------+---------+---------+---------+
    |         |         |         |         |         |
    v         v         v         v         v         v
  Term     Prereq   Proced.   Concept  Specific  Outside
  Gap      Deficit  Confus.   Confus.  Step      Corpus
    |         |         |         |         |         |
    v         v         v         v         v         v
Clarify   Restore  Give Ex.  Request   Fresh    Stop &
Terminol. Prereq.  (steps)   Explain.  Attempt  Request
                     |                    |         |
                     +--------------------+-- If stuck more
                              |
                              v
                        Give Example (escalate)
```

---

## Action Routing Logic (Pseudocode)

```python
def select_pedagogical_action(user_statement, classification, material_context, task_boundary, material_scope_status, articulation_status):
    """
    Route user confusion to ONE pedagogical action.

    Args:
        user_statement: verbatim user confusion (string)
        classification: one of six types (string)
        material_context: section/problem location (dict)
        task_boundary: concept vs. problem, scope (dict)
        material_scope_status: in_scope | missing_required_material | outside_supplied_corpus
        articulation_status: articulated | cannot_articulate

    Returns:
        action: dict with action_type, action_spec, material_citations
    """

    # Check material scope FIRST (highest priority)
    if material_scope_status == "outside_supplied_corpus":
        return {"action_type": "stop_and_request_more_material",
                "reason": "topic_not_in_corpus"}

    if material_scope_status == "missing_required_material":
        return {"action_type": "stop_and_request_more_material",
                "reason": "required_section_not_uploaded"}

    # Check articulation status
    if articulation_status == "cannot_articulate":
        # User can't express what's confusing
        # Give bounded example from current section OR diagnostic prompt
        example_section = find_worked_example(material_context, task_boundary)
        if example_section:
            return {"action_type": "give_bounded_example",
                    "material_citations": [example_section],
                    "reason": "diagnostic_example_for_unarticulated_confusion"}
        else:
            return {"action_type": "request_explanation",
                    "prompt": "Can you walk through what you've tried so far?",
                    "material_citations": [material_context["current_section"]],
                    "reason": "diagnostic_prompt_for_unarticulated_confusion"}

    # Material in scope, confusion articulated → Route by classification

    # Rule Set 1: Terminology Gap
    if classification == "terminology_gap":
        term = extract_unfamiliar_term(user_statement)
        definition_section = find_term_in_material(term, material_context)
        if definition_section is None:
            return {"action_type": "stop_and_request_more_material",
                    "reason": "term_not_in_corpus"}
        return {"action_type": "clarify_terminology",
                "term": term,
                "material_citations": [definition_section]}

    # Rule Set 2: Prerequisite Deficit
    elif classification == "prerequisite_deficit":
        prerequisite = extract_prerequisite_concept(user_statement)
        prereq_section = find_prerequisite_in_material(prerequisite, material_context)
        if prereq_section is None:
            return {"action_type": "stop_and_request_more_material",
                    "reason": "prerequisite_not_in_corpus"}
        return {"action_type": "restore_prerequisite",
                "prerequisite": prerequisite,
                "material_citations": [prereq_section]}

    # Rule Set 3: Procedural Confusion or Lost Context
    elif classification in ["procedural_confusion", "lost_context"]:
        example_section = find_worked_example(material_context, task_boundary)
        if example_section is None:
            return {"action_type": "stop_and_request_more_material",
                    "reason": "no_similar_example_in_corpus"}
        return {"action_type": "give_bounded_example",
                "material_citations": [example_section]}

    # Rule Set 4: Conceptual Confusion
    elif classification == "conceptual_confusion":
        return {"action_type": "request_explanation",
                "prompt": "Can you explain why [X] works?",
                "material_citations": [material_context["current_section"]]}

    # Rule Set 5: Stuck on Specific Step
    elif classification == "stuck_on_specific_step":
        stuck_step = extract_step_number(user_statement)
        hint = generate_minimal_hint(stuck_step, material_context)
        return {"action_type": "request_fresh_attempt",
                "hint": hint,
                "material_citations": [material_context["current_section"]]}

    # Fallback: Cannot classify
    else:
        # Default to giving example from current section
        return {"action_type": "give_bounded_example",
                "material_citations": [material_context["current_section"]]}
```

---

## Action Escalation Rules

**When to Escalate**:

1. **Terminology → Prerequisite**: If clarified term is itself a concept needing review
2. **Prerequisite → Example**: If prerequisite reminder doesn't resolve confusion
3. **Fresh Attempt → Example**: If user stuck after hint
4. **Explanation → Example**: If user cannot articulate OR explanation completely wrong
5. **Example → Stop**: If no example exists in material

**Escalation Flow**:
```
Clarify Term → Restore Prereq → Give Example → Stop & Request
                                     ↑
Request Explanation → (if fails) ----+
                                     ↑
Request Fresh Attempt → (if stuck) --+
```

**Escalation Evidence**:
- Record escalation count in state: `pedagogical_action_escalations`
- If escalated 3+ times in one session: Suggest user review material offline before returning

---

## Evidence Boundaries and Non-Inferences

### What This Tree Does

✓ Routes user confusion to source-bounded action
✓ Uses observable classification (user statement + material context)
✓ Delivers ONE action per iteration
✓ Cites uploaded material for all actions
✓ Allows escalation based on user response

### What This Tree Does NOT Do

✗ Automatically detect confusion before user expresses it (src-002 limitation)
✗ Infer deep understanding from single action success
✗ Predict future performance or mastery
✗ Model learner knowledge state beyond observable facts
✗ Generate content outside uploaded corpus
✗ Claim optimal action selection (tree is provisional)

---

## Limitations and Assumptions

### Assumptions

1. **User Can Express Confusion**: Even if imprecise, user can say "I'm stuck" or "I don't get it"
2. **Material Contains Examples**: Uploaded material has worked examples, definitions, problem sets
3. **Single Obstacle Per Iteration**: User expresses one primary confusion point (if multiple, address first one)
4. **Natural Language Classification Possible**: System can parse user statement to extract terms, prerequisites, step numbers

### Limitations from Gate 1

**From RESEARCH_QUESTIONS.md RQ3.2:**
- Automatic obstacle-type detection NOT demonstrated in research (src-002, src-007)
- System classification is PROVISIONAL — may require revision based on user response
- Distinction between procedural and conceptual confusion may be ambiguous

**From Task Contract:**
- Do NOT claim automatic mastery classification
- Do NOT infer learner state beyond observable evidence
- Do NOT build general pedagogical framework (scenario-specific only)

### Design Constraints

**From src-001, src-002 (source grounding):**
- All actions MUST cite uploaded material
- If material insufficient: explicit failure (stop and request more)

**From src-002 (user control):**
- User can request action adjustment ("slower", "simpler", "more advanced")
- Adjustment triggers re-routing through decision tree with modified parameters

**From src-007 (learner agency):**
- User can decline actions (e.g., decline to explain)
- Declination recorded in state as evidence level 0

---

## Validation Criteria

**This decision tree satisfies Gate 2 exit conditions:**

- [x] Defines bounded pedagogical actions (six types)
- [x] Maps observable evidence to actions (six classification types)
- [x] Every action source-bounded (cite material or explicit failure)
- [x] Escalation rules defined (5 escalation paths)
- [x] Evidence boundaries explicit (what is/isn't inferred)
- [x] Action selection measurable (classification → action mapping deterministic)
- [x] Does NOT claim automatic obstacle detection before user expression
- [x] Does NOT claim optimal or general teaching framework
- [x] Limitations from Gate 1 acknowledged and carried forward

---

## Provisional Status and Gate 3 Iteration

**This tree is PROVISIONAL for Gate 2 design.**

**Gate 3 pilot will test:**
- Whether six classification types cover most user confusion statements
- Whether action routing produces helpful outcomes
- Whether escalation rules match actual user needs
- Whether single-action-per-iteration is sufficient or too slow

**Gate 3 may revise:**
- Classification granularity (add/merge types)
- Action specifications (adjust hint detail level, example selection)
- Escalation thresholds (when to escalate vs. retry)
- Failure modes (when to stop vs. continue with partial material)

**Gate 2 does NOT claim:**
- This tree is optimal
- This tree generalizes beyond this scenario
- This tree has been validated with real users

---

**Status**: Provisional decision tree for Gate 2 design candidate complete. Awaiting validation and Gate 3 pilot testing.

