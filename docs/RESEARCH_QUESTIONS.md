# Learning OS Research Questions

**Generated**: 2026-07-29
**Task**: task-001-core-research
**Status**: Stage 3 - Eight-Source Coverage Assessment
**Sources Verified**: 8

---

## Research Scope

This document defines the research questions that guide Learning OS core research, organized by the five layers specified in the task contract. Each RQ is classified as directly_covered, partially_covered, or not_covered based on verified source evidence.

---

## Source Coverage Summary

| RQ | Coverage Status | Sources | Evidence Note |
|----|----------------|---------|---------------|
| RQ1.1 | directly_covered | src-001, src-002 | Source-bound explanations via inline citations and file upload demonstrated |
| RQ1.2 | partially_covered | src-001, src-002, src-005 | File upload and domain structures shown; leakage prevention mechanisms unclear |
| RQ2.1 | partially_covered | src-001, src-005 | Domain-specific structures demonstrated; vocabulary/notation constraints not addressed |
| RQ2.2 | partially_covered | src-002 | Memory feature exists; multi-session mechanisms not detailed |
| RQ3.1 | directly_covered | src-002, src-003, src-004, src-007 | Teaching actions documented; automatic detection not claimed |
| RQ3.2 | partially_covered | src-002, src-007 | Adaptive scaffolding exists; automatic obstacle-type detection not demonstrated |
| RQ4.1 | directly_covered | src-002, src-003, src-004, src-006, src-007, src-008 | Observable vs. inferred distinguished; RCT evidence in specific contexts |
| RQ4.2 | partially_covered | src-003, src-006, src-007, src-008 | Temporal dynamics modeled; transition criteria not operational; intervention effectiveness unknown |
| RQ5.1 | directly_covered | src-005, src-006, src-007 | KT data requirements and limitations documented for structured exercises |
| RQ5.2 | partially_covered | src-006, src-007, src-008 | Structured exercise modeling demonstrated; cross-task unification not established |

---

## Layer 1: Source and Material Grounding

### RQ1.1: Source-Bound Explanations
**Coverage**: directly_covered
**Sources**: src-001, src-002

How do learning systems maintain explanations tied to user-provided sources rather than generating content from model knowledge alone?

**Evidence:**
- src-001 (Gemini Notebook): System provides inline citations from uploaded sources (PDF, websites, YouTube, audio, Google Docs, Slides); designed to answer based on uploaded materials
- src-002 (Study Mode): File upload + manual section reference pattern; documentation states system "does not replace teacher, tutor, course materials"

**Dimensions:**
- Source citation mechanisms: Inline citations demonstrated (src-001)
- Content attribution boundaries: Failure modes when no relevant information in sources (src-001)
- Disambiguation between source-derived and inferred content: Explicit failure messages (src-001)
- Source retrieval and passage anchoring: File upload pattern (src-001, src-002)

### RQ1.2: Material Scope Control
**Coverage**: partially_covered
**Sources**: src-001, src-002, src-005
**Gap**: Preventing model knowledge leakage when sources incomplete

How do course-constrained assistants maintain boundaries around specific course materials and prevent drift into general knowledge?

**Evidence:**
- src-001: System constrained to uploaded materials; explicit failure message when no relevant information
- src-002: File upload establishes basic course boundary; memory feature saves learning goals
- src-005 (ALEKS): Each domain requires separate pre-built knowledge structure; domain-specific constraint

**Dimensions:**
- Explicit material corpus definition: File upload (src-001, src-002), domain structures (src-005) ✓
- Out-of-scope query handling: Failure mode messaging (src-001) ✓
- Material indexing and retrieval strategies: Not detailed in sources ✗

---

## Layer 2: Course and Task Boundaries

### RQ2.1: Course-Specific Constraint Enforcement
**Coverage**: partially_covered
**Sources**: src-001, src-005
**Gap**: Vocabulary/notation constraints, assessment criteria alignment

What mechanisms enforce course-specific constraints in AI-assisted learning environments?

**Evidence:**
- src-001: File upload pattern establishes basic course boundary
- src-005 (ALEKS): Domain-specific knowledge structures; ~350 concepts for Algebra 1; each course requires separate structure

**Dimensions:**
- Vocabulary and notation constraints: Not addressed ✗
- Acceptable solution method boundaries: Not addressed ✗
- Assessment criteria alignment: Not addressed ✗
- Academic integrity preservation: src-002 defers to external policy; mechanisms unclear ✗

### RQ2.2: Task Context Preservation
**Coverage**: partially_covered
**Sources**: src-002
**Gap**: Multi-session mechanisms not detailed

How do systems maintain task context across interrupted or multi-session learning?

**Evidence:**
- src-002: Memory feature saves learning goals, preferred explanation style, or topics studied before

**Dimensions:**
- Learning position recovery: Not detailed ✗
- Unresolved question tracking: Not demonstrated ✗
- Session continuity mechanisms: Memory feature exists (src-002) but not detailed ✓

---

## Layer 3: Pedagogical Action Selection

### RQ3.1: Teaching Action Taxonomy
**Coverage**: directly_covered
**Sources**: src-002, src-003, src-004, src-007

What teaching actions are distinguished by intelligent tutoring systems, and when is each appropriate?

**Evidence:**
- src-002 (Study Mode): User can instruct: Socratic, layered explanation, hints/quizzes/step-by-step; documentation states "there may be times when it gives a direct answer"
- src-003 (LearnLM): Expert raters evaluated pedagogical elements beyond accuracy; system instructions trigger pedagogical behaviors
- src-004 (Tutor CoPilot): Analysis of 350,000+ messages shows increased probing questions, reduced generic praise
- src-007 (OLM): Four OLM categories embed strategies: transparency, confidence calibration, goal-setting, adaptive feedback

**Dimensions:**
- Explain vs. hint vs. direct answer: User-requested controls documented (src-002) ✓
- Question generation vs. guided practice: Probing questions measured (src-004) ✓
- Socratic dialogue vs. worked examples: Socratic available as request (src-002) ✓
- Error-driven vs. concept-driven instruction: Pedagogical quality evaluated (src-003) ✓

**Note**: Automatic detection not claimed; system does NOT automatically detect when to explain vs. hint vs. quiz (src-002)

### RQ3.2: Obstacle-Specific Adaptation
**Coverage**: partially_covered
**Sources**: src-002, src-007
**Gap**: Automatic obstacle-type detection not demonstrated

How do systems detect and respond to different types of learning obstacles?

**Evidence:**
- src-002: Documentation mentions possible direct answers alongside Socratic guidance
- src-007: Adaptive OLMs use AI/ML for personalized feedback; adaptive scaffolding acts as co-regulator

**Dimensions:**
- Terminology gaps: Not addressed ✗
- Prerequisite knowledge deficits: Not demonstrated ✗
- Language/translation barriers: Not addressed ✗
- Procedural vs. conceptual confusion: Not demonstrated ✗
- Lost context recovery: Not detailed ✗

---

## Layer 4: Learning-Behavior Evidence

### RQ4.1: Factual Observation vs. Inference
**Coverage**: directly_covered
**Sources**: src-002, src-003, src-004, src-006, src-007, src-008

What interaction events constitute factual observations vs. inferred learner states?

**Evidence:**
- src-002: System observes completion and responses; does not infer mastery
- src-003 (LearnLM): RCT evidence: 50th to 64th percentile (14 percentile rank difference), 1,763 students, 8 weeks, math
- src-004 (Tutor CoPilot): RCT: +4 to +9 percentage points; 700+ tutors, 1,000+ students
- src-006 (KT): Side information (response time, hints, attempts, engagement) in structured exercise contexts
- src-007 (OLM): Behavioral data (time-on-task, page views, patterns) + self-reported confidence; 26 studies
- src-008 (Digital Logs): 82 predictive models, 0.72 average accuracy after 5.85 weeks; behavioral traces orthogonal to grades

**Dimensions:**
- Directly observable: completion, time, attempts, explicit requests, response time, hints, engagement (src-002, src-006, src-008) ✓
- Inferred: understanding level, mastery state, engagement - observability limits acknowledged (src-002) ✓
- Reliability boundaries of self-reported understanding: src-007 shows confidence calibration improves accuracy ✓

### RQ4.2: Evidence-Driven State Updates
**Coverage**: partially_covered
**Sources**: src-003, src-006, src-007, src-008
**Gap**: Transition criteria not operational; intervention effectiveness unknown

What behavioral evidence is required to justify learner state transitions?

**Evidence:**
- src-003: Minimum engagement threshold: 12+ hours over 8 weeks for observed effect
- src-006: Forgetting variants model decay; temporal gap affects retention; opportunity count tracked
- src-007: Confidence calibration improves self-assessment; editable OLMs require scaffolding to prevent misjudgment
- src-008: Prediction models identify correlations; causality not established; intervention effectiveness not evaluated

**Dimensions:**
- "Understood example" vs. "can solve independently": Not addressed ✗
- Single-instance success vs. consistent performance: Not specified ✗
- Prompted completion vs. unprompted recall: Not addressed ✗

---

## Layer 5: Learner Model Applicability

### RQ5.1: Knowledge Tracing Data Requirements
**Coverage**: directly_covered
**Sources**: src-005, src-006, src-007

What data requirements and limitations constrain Bayesian Knowledge Tracing (BKT), Deep Knowledge Tracing (DKT), and related models?

**Evidence:**
- src-005 (ALEKS): Knowledge Space Theory; ~350 concepts → millions of states; 25-30 questions sufficient via Markovian procedures
- src-006 (KT Survey): Three model categories (Bayesian, Logistic, Deep Learning); KT for structured exercise interactions; side information, forgetting, individualization variants
- src-007 (OLM): Four OLM categories; 26 studies in higher education; learner model transparency approaches

**Dimensions:**
- Minimum interaction count per skill: 25-30 questions (src-005); context-dependent (src-006) ✓
- Prerequisite skill graph granularity: ~350 concepts for Algebra 1 (src-005) ✓
- Applicability to open-ended vs. structured tasks: KT for structured exercises; open reading/debugging not established (src-006) ✓
- Generalization across problem types: Domain-specific; cross-domain not demonstrated (src-005, src-006) ✓

### RQ5.2: Task-Type-Specific Modeling
**Coverage**: partially_covered
**Sources**: src-006, src-007, src-008
**Gap**: Cross-task model unification not established

Should open reading, debugging, and structured exercises share a unified learner model, or require separate modeling approaches?

**Evidence:**
- src-006: Exercise-level modeling (difficulty, discrimination); KT for structured exercises; applicability to open reading/debugging not established
- src-007: Adaptive OLMs personalize based on task type, learner state, domain; cross-task unification not directly addressed
- src-008: Models predict course outcomes/risk, not conceptual mastery states; fine-grained cross-task modeling not addressed

**Dimensions:**
- Transfer assumptions across task types: Not demonstrated ✗
- Skill decomposition granularity: Exercise-level for structured tasks (src-006) ✓
- Model complexity vs. data availability tradeoffs: Discussed for KT (src-006) ✓
- When to avoid premature learner modeling: Cold-start problem noted (src-006); explainability tradeoff (src-006) ✓

---

## Research Method Constraints

### Evidence Standards
- **Product pages**: Support feature existence claims only, not learning effectiveness
- **Search snippets**: Cannot substitute for reading source material
- **Individual reports**: Cannot be generalized to population claims without survey or experimental evidence
- **Dates and metrics**: Require recorded access date when product status may change
- **Academic papers**: Must be classified as survey, controlled experiment, simulation, or field evaluation

### Evidence Boundaries Observed
- RCT evidence context-specific: src-003 (Sierra Leone middle school math), src-004 (underserved community tutoring)
- KT models limited to structured exercises; open reading/debugging not established (src-006)
- OLM transparency demonstrated; cross-task model unification not addressed (src-007)
- Outcome prediction distinct from conceptual mastery estimation (src-008)

### Out of Scope for Task 001
- Complete knowledge graph construction
- Exhaustive question-type taxonomy
- Full error pattern classification
- Multi-agent architecture design
- Provider performance benchmarking
- Frontend implementation details

---

## Eight-Source Coverage Summary

**Directly Covered (4 of 10 RQs):**
- RQ1.1: Source-bound explanations (src-001, src-002)
- RQ3.1: Teaching action taxonomy (src-002, src-003, src-004, src-007)
- RQ4.1: Factual observation vs. inference (src-002, src-003, src-004, src-006, src-007, src-008)
- RQ5.1: Knowledge tracing data requirements (src-005, src-006, src-007)

**Partially Covered (6 of 10 RQs):**
- RQ1.2: Material scope control (leakage prevention unclear)
- RQ2.1: Course-specific constraints (vocabulary/notation not addressed)
- RQ2.2: Task context preservation (multi-session mechanisms not detailed)
- RQ3.2: Obstacle-specific adaptation (automatic detection not demonstrated)
- RQ4.2: Evidence-driven state updates (transition criteria not operational)
- RQ5.2: Task-type-specific modeling (cross-task unification not established)

**Not Covered (0 of 10 RQs):**
None - all RQs have at least partial coverage

---

## Mapping to Task Contract Dimensions

| Research Question | Contract Dimension | Coverage Status |
|-------------------|--------------------|-----------------|
| RQ1.1 | source_and_material_grounding | directly_covered |
| RQ1.2 | source_and_material_grounding | partially_covered |
| RQ2.1 | course_and_task_boundaries | partially_covered |
| RQ2.2 | course_and_task_boundaries | partially_covered |
| RQ3.1 | pedagogical_actions | directly_covered |
| RQ3.2 | pedagogical_actions | partially_covered |
| RQ4.1 | learning_evidence | directly_covered |
| RQ4.2 | learning_evidence | partially_covered |
| RQ5.1 | learner_model_applicability | directly_covered |
| RQ5.2 | learner_model_applicability | partially_covered |

---

**Status**: Stage 3 complete. Eight verified sources provide direct coverage for 4 RQs and partial coverage for 6 RQs. No RQs remain uncovered. Remaining gaps documented for each partially covered RQ.
