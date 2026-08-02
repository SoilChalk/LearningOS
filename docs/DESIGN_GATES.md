# Learning OS Design Gates

**Generated**: 2026-07-29
**Task**: task-001-core-research
**Status**: Stage 3 - Eight-Source Synthesis Complete

---

## Purpose

Design gates define entry and exit conditions for each major phase of Learning OS development. They prevent premature implementation and ensure research findings inform design decisions.

---

## Gate 1: Core Research Phase

**Current Status**: MET WITH DOCUMENTED LIMITATIONS (task-001-core-research complete)

### Entry Conditions
✓ Project purpose defined
✓ Research scope bounded
✓ Evidence standards established
✓ Source verification protocol defined

### Activities
- Identify 8-15 core sources across five research dimensions
- Document directly supported observations
- Extract design implications with explicit limitations
- Build reference system matrix
- Define first vertical scenario boundaries

### Exit Conditions Evaluation

#### ✓ Source ledger contains 8-15 verified sources
**Status**: PASS
**Evidence**: 8 verified sources in source-ledger.json (src-001 through src-008); minimum target (8) met

#### ✓ Every source includes supported observations, implications, and limitations
**Status**: PASS
**Evidence**: All 8 source records contain `directly_supported_observations`, `design_implications`, and `limitations_and_non_inferences` fields; evidence boundaries corrected in Review 08

#### ✓ Reference system matrix separates product layer from evidence
**Status**: PASS
**Evidence**: REFERENCE_SYSTEM_MATRIX.md rebuilt from eight sources; distinguishes evidence from design implications; documents unresolved gaps explicitly

#### ✓ Design gates document defines subsequent phase conditions
**Status**: PASS
**Evidence**: Gates 2, 3, 4 entry/exit conditions defined below

#### ✓ All JSON validation passes
**Status**: PASS
**Evidence**: source-ledger.json and templates pass json.tool and validate_source_records.py (verified in acceptance commands)

#### ✓ No implementation code, frontend, or private material added
**Status**: PASS
**Evidence**: Repository contains only research documentation, source notes, validation scripts; no frontend code or private materials

### Prohibited Activities
- Frontend implementation ✓ Not performed
- Complete knowledge graph construction ✓ Not performed
- Automatic mastery classification ✓ Not performed
- Exhaustive QuestionType/ErrorPattern taxonomies ✓ Not performed
- Multi-agent free-form collaboration ✓ Not performed
- Provider ranking systems ✓ Not performed
- Complex event-sourced runtime ✓ Not performed

### Current Progress (2026-07-29T18:00:00Z)

**Sources Verified**: 8/8 (minimum target met)

**Fully Verified Sources**:
1. src-001: Gemini Notebook (Google) - source grounding via inline citations from uploaded materials
2. src-002: ChatGPT Study Mode (OpenAI) - user-requested pedagogical controls; design inference about explicit control requirement noted
3. src-003: LearnLM (Google/DeepMind) - RCT evidence: 50th to 64th percentile (14 percentile rank difference), math, 8 weeks
4. src-004: Tutor CoPilot (Stanford) - human-AI collaboration RCT: +4 to +9 percentage points
5. src-005: ALEKS Knowledge Space Theory (McGraw Hill) - mathematical learner modeling framework; 350 concepts → millions of states
6. src-006: Knowledge Tracing Survey (arXiv) - KT models for structured exercise interactions; side information; task-specific features
7. src-007: OLM Meta-Synthesis (Frontiers) - learner model transparency; four OLM categories; SRL scaffolding; 26 studies
8. src-008: Digital Logs Review (PMC) - course outcome/risk prediction from behavioral traces; 82 models, 39 papers; feature engineering

**Incomplete Candidates** (7 candidates deferred after access attempts):
- Bayesian Knowledge Tracing papers (Corbett & Anderson 1995)
- Cognitive Tutors/ACT-R publications (Anderson, Koedinger, Corbett)
- ASSISTments research papers
- ITS effectiveness meta-analyses (Kulik & Fletcher, SAGE paywalls)
- Duolingo spaced repetition research (arXiv extraction failures)
- Khan Academy RCT studies (institutional access issues)
- MDPI learning analytics (Akamai bot detection, DOI resolver failed)

### Gate 1 Exit Decision: MET WITH DOCUMENTED LIMITATIONS

**All exit conditions pass individually**. Unresolved research gaps are documented as limitations to carry forward to Gate 2, not as exit-condition failures.

**Documented Limitations for Gate 2**:
- **Layer 1**: Preventing model knowledge leakage when sources incomplete; handling ambiguous/conflicting sources
- **Layer 2**: Vocabulary/notation constraint enforcement; assessment criteria alignment; academic integrity preservation mechanisms
- **Layer 3**: Automatic obstacle-type detection (terminology gaps, prerequisite deficits, language barriers, procedural vs. conceptual confusion)
- **Layer 4**: Operational definitions for "understood example" vs. "can solve independently"; single-instance vs. consistent performance criteria; intervention effectiveness (prediction vs. action)
- **Layer 5**: Unified learner model across reading, debugging, structured exercises; cross-domain knowledge state transfer; skill decomposition for unstructured tasks

**Research Coverage Summary**:
- 4 of 10 RQs directly covered (RQ1.1, RQ3.1, RQ4.1, RQ5.1)
- 6 of 10 RQs partially covered (RQ1.2, RQ2.1, RQ2.2, RQ3.2, RQ4.2, RQ5.2)
- 0 of 10 RQs uncovered
- All five research dimensions have evidence; depth varies by dimension

**Recommendation**: Gate 1 can advance to Gate 2 **with documented limitations**. The eight-source evidence base provides sufficient foundation to begin first vertical scenario design while acknowledging that some design questions will require implementation experiments rather than literature evidence.

---

## Gate 2: First Vertical Scenario Design

**Current Status**: CANDIDATE COMPLETE (task-002-first-vertical-scenario-design)

### Entry Conditions
- [x] Gate 1 exit conditions met
- [x] Provisional scenario identified from research
- [x] Minimum flow defined
- [x] Source-grounding strategy selected
- [x] Task boundary enforcement approach chosen

### Activities
- [x] Define complete user flow for first scenario
- [x] Specify source material handling
- [x] Design pedagogical action selection rules
- [x] Define minimal persistent state
- [x] Establish evidence collection points
- [x] Document what NOT to build

### Exit Conditions
- [x] Scenario specification document complete (FIRST_VERTICAL_SCENARIO.md)
- [x] Entry/exit criteria for each flow step defined (6 steps, each with explicit criteria)
- [x] Pedagogical action decision tree documented (PEDAGOGICAL_ACTION_DECISION_TREE.md)
- [x] State schema defined (MINIMAL_LEARNING_STATE.schema.json: current_position, task_boundary, observed_difficulty, last_pedagogical_action, independent_check, next_action)
- [x] Success criteria measurable without complex learner model (evidence levels 0/1/2, no mastery inference)

### Design Artifacts Created
- **FIRST_VERTICAL_SCENARIO.md**: Complete 6-step flow (Material Position Recovery → Task Boundary Definition → Confusion Expression → Pedagogical Action → Independent Check → State Persistence); entry/exit criteria per step; failure states; measurable success criteria; explicit non-goals
- **PEDAGOGICAL_ACTION_DECISION_TREE.md**: Six classification types (terminology gap, prerequisite deficit, procedural confusion, conceptual confusion, stuck on step, lost context); six actions (clarify term, restore prerequisite, give example, request explanation, fresh attempt, stop); escalation rules; provisional status acknowledged
- **MINIMAL_LEARNING_STATE.schema.json**: JSON Schema with 11 required fields; evidence_level enum [0,1,2] only; additionalProperties: false; no speculative fields (no knowledge_graph, mastery estimates, cross-domain)
- **validate_task_002.py**: Python validator using standard library only; checks document structure, cross-references, design constraints, Gate 1 limitations
- **test_task_002_negative.sh**: Bash negative test suite (1 positive + 8 negative cases); isolated fixtures; hash verification

### Prohibited Activities
- [x] Building for multiple scenarios simultaneously (single scenario only)
- [x] Implementing learner model before evidence design (state contains observable facts only)
- [x] Creating general-purpose knowledge graph (no knowledge_graph field in schema)
- [x] Developing automated review scheduler (next-action recommendation only, user decides when)

### Documented Limitations Carried Forward
**From Gate 1 RESEARCH_QUESTIONS.md and REFERENCE_SYSTEM_MATRIX.md:**
- **Layer 1**: Model knowledge leakage prevention (partial: explicit failure messages); ambiguous source handling (not addressed)
- **Layer 2**: Vocabulary/notation constraints (assumes consistent material); assessment alignment (use material's examples); academic integrity (defer to external policy)
- **Layer 3**: Automatic obstacle detection (user MUST express confusion first); procedural vs. conceptual distinction (provisional classification)
- **Layer 4**: "Understood" vs. "can solve" definition (evidence levels 0/1/2); single-instance vs. consistent performance (level 2 ≠ mastery); intervention effectiveness (measure in Gate 3)
- **Layer 5**: Unified model across task types (out of scope); cross-task transfer (single task boundary); skill decomposition for unstructured tasks (structured material assumed)

### Gate 2 Validation Results
- All required documents created and validated
- Every flow step has explicit entry/exit criteria
- Decision tree maps observable evidence to source-bounded actions
- State schema contains only fields used in this scenario (no speculative architecture)
- Success criteria measurable without complex learner model
- Design constraints enforced (single scenario, no frontend, no mastery claims)
- Negative tests pass (8 invalid cases correctly rejected)

---

## Gate 3: Minimum Viable Pilot

**Current Status**: NOT STARTED

### Entry Conditions
- [ ] Gate 2 exit conditions met
- [ ] Scenario specification validated
- [ ] Success criteria defined
- [ ] Pilot materials identified (must be real, not synthetic)
- [ ] Evidence collection protocol ready

### Activities
- Implement minimum flow for single scenario
- Conduct pilot with real learning materials
- Collect factual interaction events
- Measure recovery cost, comprehension check success
- Document actual vs. expected behavior
- Identify actual obstacles encountered

### Exit Conditions
- [ ] One complete learning session executed
- [ ] Minimal state successfully saved and recovered
- [ ] Evidence distinguishes factual observations from inferences
- [ ] User can express confusion in natural language
- [ ] At least one independent behavior check completed
- [ ] Pilot report documents what worked and what failed
- [ ] Design revisions documented based on pilot findings

### Success Criteria (from PROJECT_DIRECTION.md)
- New session clarifies previous position within 1 minute
- User expresses "I don't know where I'm confused" without friction
- After one semantic unit, independent behavior evidence exists
- Next session doesn't require reading long chat history
- System maintenance is not the primary activity

### Prohibited Claims After Pilot
- "Learning OS architecture validated"
- "Learner model ready for deployment"
- "Learning effectiveness proven"
- "System scales to multiple courses"

---

## Gate 4: Evidence-Driven Iteration

**Current Status**: NOT STARTED

### Entry Conditions
- [ ] Gate 3 exit conditions met
- [ ] Pilot findings documented
- [ ] Gap analysis complete
- [ ] Iteration priorities ranked by evidence

### Activities
- Revise design based on pilot findings
- Address documented failure modes
- Refine pedagogical action rules
- Adjust state schema if needed
- Run additional pilots with design variations

### Exit Conditions
- [ ] Multiple pilot iterations completed
- [ ] Design changes justified by evidence
- [ ] Failure modes reduced
- [ ] Success criteria met consistently
- [ ] Decision to expand scope or freeze feature set

---

## Anti-Patterns to Avoid

### Premature Generalization
- Building multi-course support before single-course success
- Creating general learner model before task-specific evidence
- Developing scheduling algorithm before manual scheduling works

### Scope Creep
- Adding features not validated by pilot
- Building infrastructure for anticipated future needs
- Implementing "nice to have" before "must have" works

### Evidence Bypass
- Claiming understanding without independent completion
- Inferring mastery from self-report
- Declaring success before measuring recovery cost

### Complexity Addiction
- Choosing complex solution when simple one validates first
- Building abstraction layers before concrete implementation
- Optimizing before functionality exists

---

## Phase Transition Protocol

### Before Advancing to Next Gate
1. Review all exit conditions
2. Run all validation commands
3. Document unresolved issues
4. Confirm no prohibited activities occurred
5. Update CURRENT_STATE.yaml
6. Create phase completion report

### If Exit Conditions Not Met
- Document specific blockers
- Identify required work
- Do NOT advance to next gate
- Do NOT expand scope to compensate
- Consider whether phase objectives need revision

---

**Last Updated**: 2026-07-29T19:00:00Z
**Phase**: Gate 1 - Core Research COMPLETE
**Next Phase**: Gate 2 - First Vertical Scenario Design (ready to begin)
