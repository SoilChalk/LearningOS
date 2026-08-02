# First Vertical Scenario

**Generated**: 2026-08-01
**Task**: task-002-first-vertical-scenario-design
**Gate**: Gate 2 - First Vertical Scenario Design
**Status**: Design Phase

---

## Scenario Identity

**Name**: Source-Grounded Learning Recovery and Independent Completion Check

**User Problem**: The learner has real course material (textbook chapter, lecture notes, problem set) but has lost their position in the learning flow, cannot identify where they're confused, or cannot tell whether an explanation has become independently usable knowledge.

**Scope**: Single real-material learning session for one learner using one course's materials.

---

## Actor

**Primary User**: Individual learner engaging with real course material

**Characteristics**:
- Has access to specific course materials (uploaded files, textbook sections, lecture notes)
- May be at any point in the learning process: starting new material, stuck mid-task, or reviewing
- May not know precise terminology to describe confusion
- Needs evidence that understanding has transferred to independent capability

**Not in Scope** (per Gate 1 limitations):
- Multiple simultaneous learners
- Instructors managing learner groups
- Learners without any course materials
- Cross-course or general knowledge queries

---

## Real-Material Input

**Required Inputs**:
1. **Course Material Corpus**: User-provided files uploaded at session start
   - Examples: PDF textbook chapters, lecture slides, problem sets, worked examples
   - Format constraints: Text-extractable PDFs, plain text, or structured documents
   - Minimum: One source document with identifiable sections

2. **Current Learning Context** (if returning):
   - Last material position (section/page reference)
   - Last attempted task or problem
   - Saved confusion statement (if expressed in previous session)

**Input Constraints** (from src-001, src-002):
- All responses must cite uploaded material sections
- System cannot introduce content outside uploaded corpus
- Material scope enforcement: explicit failure message if query outside corpus

---

## Preconditions

### Session Entry Preconditions

**For New Session**:
- ✓ User has uploaded at least one course material file
- ✓ Material is text-extractable and sectioned
- ✓ User can express current learning goal or confusion in natural language

**For Returning Session**:
- ✓ Previous session state exists (minimal_learning_state.json)
- ✓ Material corpus from previous session is accessible
- ✓ Last position and task boundary are recorded

### System Preconditions
- ✓ Material indexing complete (sections identified, citation anchors established)
- ✓ Pedagogical decision tree loaded
- ✓ State persistence mechanism functional

---

## Complete Step-by-Step Flow

### Step 1: Material Position Recovery

**Entry Criteria**:
- Material corpus uploaded and indexed
- User at session start (new or returning)

**Actions**:
1. **If NEW session**: Prompt user: "What are you trying to learn or understand?"
   - Accept natural language goal statement
   - Do NOT require structured input or taxonomy selection
   
2. **If RETURNING session**: Present saved position from state
   - Show: last section/page, last attempted task, last confusion statement
   - Prompt: "Do you want to continue from [saved position] or start somewhere else?"

3. **Locate Current Position**:
   - Map user statement to material sections via uploaded corpus
   - Identify: specific section, page range, or problem reference
   - Confirm with user: "It looks like you're working on [Section X: Topic]. Is that right?"

**Exit Criteria**:
- ✓ Current material position identified and confirmed by user
- ✓ Position recorded: `current_position` field in state

**Recovery Behavior**:
- If user statement too vague: Request clarification with material context ("Are you working on [Section A] or [Section B]?")
- If material section not found: Explicit failure message ("I don't see that topic in your uploaded materials. Can you point me to the section?")
- If user rejects suggested position: Return to Step 1 action 1

**Evidence Collection**:
- Factual: User confirmation of position (explicit "yes" or selection)
- Timestamp: Position recovery duration
- Inference avoided: Do NOT infer "user understands section" from confirmation

**Success Criterion**:
- User can confirm current material position within 1 minute (Gate 3 pilot metric from DESIGN_GATES.md)

---

### Step 2: Task Boundary Definition

**Entry Criteria**:
- ✓ Current material position confirmed

**Actions**:
1. **Identify Learning Unit Boundary**:
   - Determine semantic unit scope: one concept, one worked example, one problem
   - Bounded by: section heading, example number, problem statement
   - Confirm with user: "Are you working on understanding [Concept X] or trying to solve [Problem Y]?"

2. **Establish Completion Criterion**:
   - For concept understanding: "You'll know you understand when you can [explain X] or [apply to example]"
   - For problem-solving: "You'll know you can do this when you can [solve similar problem independently]"
   - Make criterion observable and task-specific

3. **Record Task Boundary**:
   - Store: material section range, task type (understand concept vs. solve problem), completion criterion
   - Update state: `task_boundary` field

**Exit Criteria**:
- ✓ Task boundary defined (start section, end section, task type)
- ✓ Observable completion criterion established
- ✓ User confirms task scope ("Yes, that's what I'm trying to do")

**Recovery Behavior**:
- If user uncertain about task: Offer options based on material structure ("Do you want to understand the concept first, or try solving a problem?")
- If task too broad: Propose narrower scope ("That section covers 3 concepts. Want to start with [Concept 1]?")

**Evidence Collection**:
- Factual: User confirmation of task boundary
- Material scope: Recorded section range
- Inference avoided: Do NOT infer task difficulty or prerequisite gaps yet

---

### Step 3: Confusion or Obstacle Expression

**Entry Criteria**:
- ✓ Task boundary defined

**Actions**:
1. **Invite Natural-Language Confusion**:
   - Prompt: "What's confusing or unclear?" OR "What's blocking you?"
   - Accept ANY natural language statement, including:
     - "I don't know where I'm confused"
     - "The whole thing doesn't make sense"
     - "I got stuck at step 3"
     - "I tried but my answer doesn't match"

2. **Classify Observable Evidence** (do NOT require user to classify):
   - **Terminology gap** (`terminology_gap`): User mentions unfamiliar term
   - **Prerequisite deficit** (`prerequisite_deficit`): User references earlier material they don't recall
   - **Procedural confusion** (`procedural_confusion`): User understands goal but not steps
   - **Conceptual confusion** (`conceptual_confusion`): User understands steps but not why
   - **Lost context** (`lost_context`): User forgot where they were or what they're solving
   - **Stuck on specific step** (`stuck_on_specific_step`): User identifies precise location

3. **Record Confusion Statement**:
   - Store verbatim user statement in state: `observed_difficulty.user_statement`
   - Store system classification: `observed_difficulty.system_classification` (one of six types above)
   - Store material context: section/problem where confusion occurred

**Exit Criteria**:
- ✓ User confusion statement recorded (even if "I don't know what's confusing")
- ✓ System classification assigned (for decision tree routing)
- ✓ Material context linked to confusion

**Recovery Behavior**:
- If user cannot articulate confusion: Accept "I don't know" and proceed with clarification action (see Step 4)
- If user states "everything is clear": Skip to Step 5 (independent check)

**Evidence Collection**:
- Factual: User's actual words
- Observable: User mentioned term, referenced section, described symptom
- Inference avoided: Do NOT infer "user will fail problem" or "user lacks prerequisite mastery"

**Design Constraint** (from src-002 Study Mode limitation):
- System does NOT automatically detect confusion type before user expresses it
- Classification is provisional (guides action selection but may be revised)

---

### Step 4: Bounded Pedagogical Action Selection

**Entry Criteria**:
- ✓ Confusion statement recorded and classified

**Actions**:
1. **Route to Pedagogical Decision Tree** (see PEDAGOGICAL_ACTION_DECISION_TREE.md):
   - Input: confusion classification, material context, task boundary
   - Output: ONE pedagogical action from tree

2. **Execute Selected Action** (source-bounded):
   - **Clarify Terminology**: Define term using uploaded material's exact definition (with citation)
   - **Restore Prerequisite**: Point to earlier section in uploaded material covering prerequisite concept
   - **Give Bounded Example**: Show worked example from uploaded material, explain steps
   - **Request Explanation**: Ask user to explain concept/step in their own words
   - **Request Fresh Attempt**: Ask user to try problem again (if procedural/stuck-on-step)
   - **Stop and Request More Material**: If confusion outside uploaded corpus scope

3. **Deliver Action with Material Citation**:
   - ALL explanations/examples MUST cite specific uploaded material sections (src-001 constraint)
   - Use exact terminology and notation from uploaded material (preserve source vocabulary)
   - If action requires content outside corpus: explicit failure message and stop

4. **Record Action Taken**:
   - Store action type: `last_pedagogical_action.action_type`
   - Store material sections cited: `last_pedagogical_action.material_citations`
   - Store timestamp: `last_pedagogical_action.timestamp`

**Exit Criteria**:
- ✓ ONE pedagogical action executed
- ✓ Action grounded in uploaded material (or explicit failure)
- ✓ Action recorded in state

**Recovery Behavior**:
- If user still confused after action: Record continued confusion, return to Step 3 (re-classify)
- If action requires clarification: System asks user to confirm understanding before proceeding

**Evidence Collection**:
- Factual: Action delivered, user response to action
- Observable: User requested clarification, acknowledged, or stated "still confused"
- Inference avoided: Do NOT infer "user now understands" without independent check

**Design Constraint** (from src-002):
- System may give direct answer "if appropriate" but default is guided (Socratic/layered)
- User can request action adjustment ("slower", "simpler", "more advanced") - system re-routes through decision tree

---

### Step 5: Independent Completion Evidence Request

**Entry Criteria**:
- ✓ Pedagogical action executed
- ✓ User has not stated continued confusion

**Actions**:
1. **Request Observable Independent Behavior**:
   - **For concept understanding**: "Can you explain [concept] in your own words?" OR "Can you apply [concept] to this example?"
   - **For problem-solving**: "Can you solve this similar problem?" (provide from uploaded material or slight variation)
   - Make request TASK-SPECIFIC and OBSERVABLE

2. **Collect User Response**:
   - Accept: written explanation, worked solution, step-by-step process
   - Do NOT accept: "I understand now" without demonstration
   - Do NOT accept: "Yes" without elaboration

3. **Evaluate Response Against Observable Criteria** (from src-002, src-003, src-007):
   - **Terminology check**: Does user use correct terms from material?
   - **Step completion**: Did user complete all required steps?
   - **Correctness**: Is answer/explanation aligned with material?
   - NOT EVALUATED: Deep understanding, transfer to different domain, long-term retention

4. **Classify Evidence Level**:
   - **Level 0 - No Evidence**: User declined, gave "I understand", or provided incomplete response
   - **Level 1 - Partial Evidence**: User attempted but incomplete/incorrect
   - **Level 2 - Single-Instance Evidence**: User completed ONE correct demonstration
   - NOT CLAIMED: Level 3 - Consistent mastery (requires multiple instances, not in this scenario scope)

5. **Record Evidence**:
   - Store evidence level: `independent_check.evidence_level` (0, 1, or 2)
   - Store user response: `independent_check.user_response` (verbatim or summary)
   - Store evaluation: `independent_check.evaluation` (what was correct/incorrect)

**Exit Criteria**:
- ✓ Independent behavior check requested
- ✓ User response collected (even if none)
- ✓ Evidence level classified and recorded

**Recovery Behavior**:
- If user response incomplete (Level 1): Option to try again OR move to next session
- If user declines (Level 0): Record and save state for next session
- If user requests hint: Return to Step 4 (new pedagogical action)

**Evidence Collection**:
- Factual: User provided response, response content
- Observable: Terminology used, steps shown, correctness of answer
- Inference avoided: Do NOT infer "user has mastered topic" from single instance (src-002: does not infer mastery)

**Design Constraint** (from Task Contract and src-003, src-006):
- Single-instance success ≠ mastery
- Evidence level 2 means "demonstrated ONCE" not "can always do it"
- Consistent performance requires multiple trials (Gate 3 pilot data collection, not Gate 2 design claim)

---

### Step 6: Minimal State Persistence

**Entry Criteria**:
- ✓ Independent check completed (any evidence level)

**Actions**:
1. **Save Minimal State** (see MINIMAL_LEARNING_STATE.schema.json):
   - Current position: section, page, problem
   - Task boundary: scope and completion criterion
   - Observed difficulty: user statement and classification
   - Last pedagogical action: type and citations
   - Independent check: evidence level and response
   - Next action: recommendation for next session

2. **Generate Next-Action Recommendation**:
   - **If Evidence Level 2**: "Try [next problem/concept in sequence]"
   - **If Evidence Level 1**: "Review [specific prerequisite section], then retry [current task]"
   - **If Evidence Level 0**: "Continue from [current position] with [suggested action]"

3. **Confirm State Saved**:
   - Write state file: `minimal_learning_state.json`
   - Display to user: "Saved your progress at [position]. Next time: [next action]"

**Exit Criteria**:
- ✓ State file written and validated
- ✓ Next action recommendation generated
- ✓ User notified of save

**Recovery Behavior**:
- If state write fails: Retry once, then display state to user as text backup

**Evidence Collection**:
- Factual: State file exists, contains required fields
- Observable: File write timestamp

---

## Complete Flow Summary

1. **Material Position Recovery** → Confirm where user is in material
2. **Task Boundary Definition** → Define what user is trying to achieve
3. **Confusion Expression** → Accept natural language confusion statement
4. **Pedagogical Action** → Execute ONE source-bounded action
5. **Independent Check** → Request observable demonstration
6. **State Persistence** → Save minimal state for next session

**Total Steps**: 6
**Estimated Duration**: 10-30 minutes for one semantic unit
**Success Path**: Steps 1→2→3→4→5→6 with evidence level 2
**Recovery Paths**: Step 3→4→3 (re-classify), Step 5→4 (hint), Step 5→6 (save incomplete)

---

## Measurable Success Criteria

### Gate 3 Pilot Metrics (from DESIGN_GATES.md)

**These are PILOT MEASUREMENTS, not Gate 2 design claims:**

1. **Position Recovery Speed**:
   - Metric: Time from session start to confirmed position
   - Target: < 1 minute for returning session
   - Evidence: timestamp difference

2. **Confusion Expression Friction**:
   - Metric: User able to express "I don't know what's confusing" without rejection
   - Target: System accepts ANY natural language confusion statement
   - Evidence: No error messages, confusion recorded

3. **Independent Evidence Collection**:
   - Metric: At least ONE independent behavior check completed per session
   - Target: 100% of sessions reach Step 5
   - Evidence: `independent_check` field exists in state

4. **State Minimal and Resumable**:
   - Metric: Next session does NOT require reading long chat history
   - Target: State file < 2KB, loads in < 1 second
   - Evidence: File size measurement

5. **Maintenance Not Primary Activity**:
   - Metric: Pedagogical action steps > administrative/debugging steps
   - Target: Steps 4-5 duration > Steps 1-2 duration
   - Evidence: timestamp analysis

### Gate 2 Design Validation (This Document)

**These CAN be verified in Gate 2:**

1. ✓ Every flow step has explicit entry/exit criteria
2. ✓ Recovery behaviors defined for failure modes
3. ✓ Evidence collection distinguishes factual from inferred
4. ✓ All actions source-bounded (cite uploaded material)
5. ✓ Success criteria measurable without complex learner model
6. ✓ State schema contains only fields used in this scenario

---

## Failure States and Recovery

### Failure State 1: Material Not Uploaded

**Symptom**: User starts session without uploading files

**Recovery**:
1. Display: "Please upload your course materials (textbook, notes, problem set)"
2. Wait for upload
3. Resume from Step 1

**Prevention**: Session entry precondition check

---

### Failure State 2: Position Recovery Fails

**Symptom**: User statement does not map to any material section

**Recovery**:
1. Display uploaded material table of contents
2. Ask user to select section manually
3. Resume from Step 1 action 3 (confirm position)

**Evidence**: User manual selection counts as confirmed position

---

### Failure State 3: Confusion Outside Corpus

**Symptom**: User confusion references content not in uploaded materials

**Recovery**:
1. Display: "That topic isn't in your uploaded materials. Can you upload the relevant section, or shall we work with what you have?"
2. If user uploads more: Re-index and return to Step 3
3. If user chooses to work with current: Re-route through decision tree to "Stop and Request More Material" action

**Evidence**: Explicit out-of-scope detection (src-001 failure mode)

---

### Failure State 4: User Declines Independent Check

**Symptom**: User says "I understand" or declines to demonstrate

**Recovery**:
1. Record evidence level 0
2. Suggest: "Okay. Next time, try [next action]."
3. Save state with next-action recommendation
4. Exit scenario

**Evidence**: User autonomy preserved (src-007: learner agency)

---

### Failure State 5: Independent Check Shows Level 1 (Partial)

**Symptom**: User attempts but response incomplete/incorrect

**Recovery Options** (user chooses):
1. **Try Again**: Return to Step 5 with same request
2. **Get Help**: Return to Step 4 with new pedagogical action
3. **Save and Continue Later**: Save state as-is, exit

**Evidence**: User choice recorded in state

---

### Failure State 6: State Persistence Fails

**Symptom**: File write error or validation failure

**Recovery**:
1. Retry write once
2. If retry fails: Display state JSON to user as text
3. Instruct: "Copy this to save your progress manually"

**Evidence**: State delivered to user by ANY means (prevents loss)

---

## Explicit Non-Goals

### NOT in This Scenario

1. **Multiple Scenarios**: Only source-grounded recovery and check. No multi-course, no cross-topic.

2. **Automatic Mastery Classification**: Evidence level ≠ mastery inference. Level 2 = single correct instance, not consistent performance.

3. **Complex Learner Model**: State contains observable facts only (position, task, confusion statement, action taken, evidence level). No hidden states, no knowledge graphs.

4. **Scheduled Review**: Next-action recommendation ≠ spaced repetition scheduler. User decides when to return.

5. **Multi-Agent Collaboration**: Single learner, single material corpus, single session flow.

6. **Effectiveness Claims**: Gate 2 is DESIGN. Learning effectiveness measured in Gate 3 pilot, not claimed in Gate 2.

7. **General Pedagogical Strategy**: Decision tree is PROVISIONAL and BOUNDED for this scenario. Not a general teaching framework.

8. **Frontend Implementation**: This is scenario specification. UI/UX design in Gate 3.

9. **Cross-Domain Transfer**: Source-grounding specific to uploaded corpus. No cross-course knowledge claims.

10. **Long-Term Retention**: Evidence level measures immediate demonstration, not retention after days/weeks.

---

## Design Assumptions and Limitations

### Assumptions

1. **User Can Upload Materials**: User has digital access to course content
2. **Materials Are Structured**: Content has sections, headings, problems (not pure unstructured text)
3. **User Literate in Material Language**: Can read and express confusion in material's language
4. **Single Session Focus**: User commits to one learning unit per session
5. **Observable Criteria Exist**: Course materials include problems or examples suitable for independent checks

### Limitations Carried Forward from Gate 1

**From RESEARCH_QUESTIONS.md and REFERENCE_SYSTEM_MATRIX.md:**

1. **Layer 1 Gaps**:
   - Preventing model knowledge leakage when sources incomplete (partial mitigation: explicit failure messages)
   - Handling ambiguous or conflicting source content (not addressed in this scenario)

2. **Layer 2 Gaps**:
   - Vocabulary/notation constraint enforcement (assume material uses consistent notation)
   - Assessment criteria alignment (use material's own examples/problems as gold standard)
   - Academic integrity preservation (defer to external policy per src-002)

3. **Layer 3 Gaps**:
   - Automatic obstacle-type detection (user MUST express confusion; system classifies after expression)
   - Procedural vs. conceptual confusion distinction (provisional classification, may be revised)

4. **Layer 4 Gaps**:
   - "Understood example" vs. "can solve independently" operational definition (use evidence levels 0/1/2, not binary)
   - Single-instance vs. consistent performance (explicitly distinguish: level 2 ≠ mastery)
   - Intervention effectiveness (measure in Gate 3, not claimed in Gate 2)

5. **Layer 5 Gaps**:
   - Unified learner model across reading, debugging, exercises (out of scope: this scenario is structured material only)
   - Cross-task transfer (single task boundary per session)
   - Skill decomposition for unstructured tasks (structured material assumed)

### Design Constraints Enforced

1. **Source Grounding** (src-001, src-002): All explanations cite uploaded material
2. **Evidence Boundaries** (src-002): Observe completion/responses, do not infer mastery
3. **User Agency** (src-007): User can decline checks, request different actions, express "I don't know"
4. **Minimal State** (task contract): Only data needed for THIS scenario
5. **No Premature Generalization** (DESIGN_GATES.md anti-patterns): One scenario, one flow, one material corpus

---

## Gate 2 Exit Validation Checklist

**This document must satisfy all Gate 2 exit conditions:**

- [x] Scenario specification document complete
- [x] Actor, problem, scope, and non-goals defined
- [x] Every flow step has explicit entry/exit criteria
- [x] Recovery behaviors documented for failure states
- [x] Evidence collection points identified (Steps 1, 3, 4, 5)
- [x] Measurable success criteria defined (Gate 3 pilot metrics)
- [x] Success criteria measurable without complex learner model
- [x] Pedagogical action decision tree referenced (separate document)
- [x] Minimal state schema referenced (separate document)
- [x] Limitations from Gate 1 carried forward explicitly
- [x] Explicit non-goals documented
- [x] Design assumes real course materials, not synthetic

---

**Status**: Gate 2 design candidate complete. Awaiting validation (validate_task_002.py) and Gate 2 exit review.

