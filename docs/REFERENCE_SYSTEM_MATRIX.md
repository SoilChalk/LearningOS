# Learning OS Reference System Matrix

**Generated**: 2026-07-29
**Task**: task-001-core-research
**Stage**: Stage 3 - Eight-Source Synthesis
**Sources**: 8 verified

---

## Purpose

This matrix synthesizes evidence from eight verified sources to inform Learning OS design decisions. Each layer corresponds to a research dimension; each cell maps source evidence to design implications within proper evidence boundaries.

---

## Source Summary

| ID | Title | Type | Key Contribution |
|----|-------|------|------------------|
| src-001 | Google Gemini Notebook | Product documentation | Source-grounding via inline citations from uploaded materials |
| src-002 | OpenAI Study Mode | Product documentation | User-requested pedagogical controls; file upload + section reference |
| src-003 | Google LearnLM | Product documentation + RCT | RCT evidence: 50th to 64th percentile (14 percentile rank difference), math, 8 weeks |
| src-004 | Stanford Tutor CoPilot | Research paper - field evaluation | RCT evidence: +4 to +9 percentage points; human-AI collaboration model |
| src-005 | ALEKS Knowledge Space Theory | Product documentation | Mathematical framework for learner modeling; 350 concepts → millions of states, 25-30 questions |
| src-006 | Knowledge Tracing Survey | Research paper - survey | KT models for structured exercise interactions; side information; task-specific features |
| src-007 | OLM Meta-Synthesis | Research paper - survey | Four OLM categories (26 studies); learner model transparency; SRL scaffolding |
| src-008 | LMS Digital Logs Review | Research paper - survey | Course outcome/risk prediction from behavioral traces (82 models, 39 papers); feature engineering |

---

## Layer 1: Source and Material Grounding

### RQ1.1: Source-Bound Explanations

**Evidence:**
- **src-001** (Gemini Notebook): System provides inline citations from uploaded sources (PDF, websites, YouTube, audio, Google Docs, Slides); designed to answer questions based on uploaded materials; distinguishes failure modes (safety, unclear phrasing, no relevant information)
- **src-002** (Study Mode): File upload (notes, syllabus, worksheet, slides, textbook, problem photos) + manual section reference; documentation states system "does not replace teacher, tutor, course materials"

**Design Implications:**
- Source-grounding via inline citations is demonstrated as a product feature (src-001)
- Material constraint pattern: file upload + manual section pointing (src-001, src-002)
- Explicit failure mode messages support scope enforcement (src-001)

**Limitations:**
- No learning effectiveness evidence for citation-based systems (src-001, src-002)
- Shallow material constraint: requires manual section reference (src-002)
- No evidence on handling ambiguous or conflicting source content (both sources)

### RQ1.2: Material Scope Control

**Evidence:**
- **src-001**: System constrained to uploaded materials; explicit failure message when no relevant information in sources
- **src-002**: File upload establishes basic course boundary; memory feature saves learning goals and topics
- **src-005** (ALEKS): Each domain (Algebra 1, Algebra 2) requires separate pre-built knowledge structure; domain-specific constraint demonstrated

**Design Implications:**
- Material corpus can be defined via file upload (src-001, src-002)
- Domain-specific knowledge structures enable course boundary enforcement (src-005)
- Explicit out-of-scope detection possible (src-001 failure modes)

**Limitations:**
- No evidence on preventing model knowledge leakage when sources incomplete
- Academic integrity boundaries unclear: "Follow AI-use policies of your school" (src-002)
- Cross-domain transfer not demonstrated (src-005)

---

## Layer 2: Course and Task Boundaries

### RQ2.1: Course-Specific Constraint Enforcement

**Evidence:**
- **src-001**: File upload pattern establishes basic course boundary; safety flagging and scope detection present
- **src-005** (ALEKS): Domain-specific knowledge structures; Algebra 1 example with ~350 concepts; each course requires separate pre-built structure

**Design Implications:**
- Course boundaries enforceable via domain-specific knowledge structures (src-005)
- Knowledge modeling feasible at scale: 350 concepts → millions of states, assessment remains tractable with 25-30 questions (src-005)

**Limitations:**
- No evidence on vocabulary/notation constraint enforcement
- Assessment criteria alignment not addressed in verified sources
- Academic integrity preservation mechanisms unclear (src-002 defers to external policy)

### RQ2.2: Task Context Preservation

**Evidence:**
- **src-002**: Memory feature saves learning goals, preferred explanation style, or topics studied before

**Design Implications:**
- Basic session continuity via memory feature (src-002)

**Limitations:**
- No evidence on learning position recovery across interrupted sessions
- Unresolved question tracking not demonstrated
- Multi-session context mechanisms not detailed (src-002 provides existence claim only)

---

## Layer 3: Pedagogical Action Selection

### RQ3.1: Teaching Action Taxonomy

**Evidence:**
- **src-002** (Study Mode): User can instruct system to guide thinking (Socratic), explain in layers, check understanding, or use hints/quizzes/step-by-step; documentation states "there may be times when it gives a direct answer"; user specifies level (middle school, high school, college, beginner, advanced); user can request adjustments (slow down, simpler language, analogy, deeper explanation, more advanced content)
- **src-003** (LearnLM): Expert raters evaluated pedagogical elements (guidance, correcting mistakes) beyond accuracy; with system instructions, Gemini leverages LearnLM to trigger pedagogical behaviors; built with education experts based on rigorous research
- **src-004** (Tutor CoPilot): Analysis of 350,000+ messages shows system increases probing questions and reduces generic praise; system models expert thinking to assist tutors in real time
- **src-007** (OLM): Four OLM categories embed pedagogical strategies: inspectable (transparency/feedback), negotiable (confidence calibration/dialogic feedback), editable (goal-setting/self-assessment), adaptive (AI-driven personalized feedback/nudges)

**Design Implications:**
- User-requested controls documented: Socratic, layered explanation, hints, quizzes (src-002)
- Pedagogical quality evaluable as separate dimension from accuracy (src-003)
- Specific behaviors measurable: probing questions increase, generic praise decreases (src-004)
- Pedagogical strategies: goal-setting, reflective monitoring, confidence calibration, adaptive feedback, dialogic negotiation, performance visualization (src-007)

**Design Inferences (not direct findings):**
- Whether explicit user instruction is technically required vs. available option not directly stated (src-002)
- Whether Socratic is opt-in/default-off vs. context-dependent not technically specified (src-002)
- Whether automatic adjustment never occurs vs. not documented (src-002)

**Limitations:**
- System does NOT automatically detect when to explain vs. hint vs. quiz (src-002)
- Implementation details not disclosed (src-003, src-004)
- How "expert thinking" is modeled and delivered not specified (src-004)

### RQ3.2: Obstacle-Specific Adaptation

**Evidence:**
- **src-002**: Documentation mentions possible direct answers alongside Socratic guidance; unclear phrasing identified as failure mode by src-001
- **src-007**: Negotiable OLMs provide dialogic feedback and confidence calibration; adaptive OLMs use AI/ML for personalized feedback aligned with learner needs

**Design Implications:**
- System responses can vary (direct answer vs. Socratic) but automatic detection not claimed (src-002)
- Adaptive scaffolding acts as co-regulator anticipating learner needs (src-007)

**Limitations:**
- No evidence on terminology gap detection
- Prerequisite knowledge deficit handling not demonstrated
- Language/translation barrier adaptation not addressed
- Procedural vs. conceptual confusion differentiation not shown
- Lost context recovery not detailed

---

## Layer 4: Learning-Behavior Evidence

### RQ4.1: Factual Observation vs. Inference

**Evidence:**
- **src-002**: System observes completion and responses; does not infer mastery; documentation states system "can make mistakes"
- **src-003** (LearnLM): RCT in Sierra Leone with 1,763 middle school students (grades 7-8), 8 weeks, 12+ hours minimum usage; math performance from 50th to 64th percentile (14 percentile rank difference); effect equivalent to 1.8-2.5 additional years of learning progress
- **src-004** (Tutor CoPilot): RCT with 700+ tutors, 1,000+ students from underserved communities; students with tutors using system 4 percentage points more likely to master topics (p<0.01); gains highest for lower-rated tutors: 9 percentage points; cost ~$20/tutor/year
- **src-006** (KT Survey): Side information recorded in structured exercise contexts: response time, opportunity count, tutor intervention, engagement metrics provide richer signals than correctness alone; individualization variants model different learning rates and prior knowledge
- **src-007** (OLM): OLMs collect behavioral data (time-on-task, page views, interaction patterns) + self-reported confidence/goals; 26 studies demonstrate consistent gains in engagement, persistence, outcomes for inspectable OLMs
- **src-008** (Digital Logs): LMS systems capture fine-grained activities with timestamps: frequency, time, patterns; 82 predictive models from 39 papers, average accuracy 0.72 (SD=0.10) after 5.85 weeks; behavioral trace data (views, downloads, submissions, forum contributions) orthogonal to summative performance

**Design Implications:**
- Directly observable: completion, time spent, attempts, explicit requests, response time, opportunity count, engagement metrics (src-002, src-006, src-008)
- RCT evidence for learning effectiveness exists in specific contexts (src-003: Sierra Leone middle school math; src-004: underserved community math tutoring)
- Side information provides richer evidence than correctness alone in structured exercise contexts (src-006)
- Behavioral traces enable outcome prediction before summative assessment (src-008: average 5.85 weeks)
- Feature engineering transforms raw logs into predictive measures (src-008)

**Limitations:**
- Evidence collection sparse: observes completion/responses, does not infer mastery (src-002)
- RCT context-specific: generalization to other subjects, age groups, countries requires caution (src-003, src-004)
- Tutor-mediated interaction, not direct AI-student tutoring (src-004)
- KT models designed for structured exercise interactions; applicability to open reading, debugging, unstructured tasks not established (src-006)
- Prediction models identify correlations; causality not established (src-008)

### RQ4.2: Evidence-Driven State Updates

**Evidence:**
- **src-003**: Minimum engagement threshold exists: 12+ hours over 8 weeks for observed effect
- **src-006**: Forgetting variants model knowledge decay; temporal gap between interactions affects retention; opportunity count tracked
- **src-007**: Negotiable OLMs improve confidence and self-assessment accuracy through calibration; editable OLMs require scaffolding to prevent misjudgment

**Design Implications:**
- Minimum engagement threshold observable for effectiveness (src-003)
- Temporal dynamics matter: forgetting curves, time gaps, opportunity counts affect state evolution in exercise contexts (src-006)
- Confidence calibration improves self-assessment accuracy (src-007)

**Limitations:**
- "Understood example" vs. "can solve independently" distinction not addressed
- Single-instance success vs. consistent performance criteria not specified
- Intervention effectiveness unknown: prediction models reviewed, not intervention studies (src-008)

---

## Layer 5: Learner Model Applicability

### RQ5.1: Knowledge Tracing Data Requirements

**Evidence:**
- **src-005** (ALEKS): Knowledge Space Theory applies combinatorics and stochastic processes; ~350 concepts for Algebra 1 → millions of empirically feasible knowledge states; adaptive assessment using Markovian procedures gauges state in 25-30 questions; system determines "what student knows and ready to learn next"
- **src-006** (KT Survey): Three model categories: Bayesian (BKT, DBKT), Logistic (LFA, PFA, KTM), Deep Learning (DKT, transformers); KT monitors evolving knowledge states during problem-solving; learning sequence formulated as interactions with exercises, KCs, correctness, side information; exercise-level modeling: difficulty and discrimination parameters; forgetting variants integrate exponential decay
- **src-007** (OLM): Four OLM categories: Inspectable (view-only dashboards), Negotiable (confidence calibration), Editable (learner modifies profile), Persuasive/Adaptive (AI/ML personalization); 26 empirical studies in higher education; adaptive OLMs integrate intelligent tutoring, cognitive mapping, recommender algorithms

**Design Implications:**
- Knowledge modeling feasible at scale: efficient assessment with Markovian procedures (src-005)
- Prerequisite relationships mathematically modelable (src-005)
- Domain specificity critical: each course requires separate knowledge structure (src-005)
- KT demonstrates scalable knowledge state modeling for structured exercise interactions (src-006)
- Exercise-level features (difficulty, discrimination) improve model performance (src-006)
- Learner model transparency demonstrated across 26 studies in higher education (src-007)

**Limitations:**
- Learning effectiveness not claimed: ALEKS describes assessment framework, not outcomes (src-005)
- KT survey describes predictive accuracy, not learning outcome improvements from KT-guided interventions (src-006)
- Cold-start problem: new students with no history require different approaches (src-006)
- Explainability tradeoff: deep models more accurate but less interpretable (src-006)
- Domain specificity: STEM predominance may limit humanities/social sciences transferability (src-007)

### RQ5.2: Task-Type-Specific Modeling

**Evidence:**
- **src-006**: Exercise-level modeling with difficulty and discrimination parameters; task-specific modeling demonstrated for structured problem-solving; KT models designed for structured exercise interactions
- **src-007**: Adaptive OLMs personalize based on task type, learner state, and domain; studies demonstrate adaptation in multiple higher education contexts
- **src-008**: Models predict dichotomous outcomes (pass/fail, at-risk/safe, above/below threshold); prediction target is course outcomes, not conceptual mastery states

**Design Implications:**
- Task-specific modeling feasible for structured exercises (src-006)
- Adaptive personalization demonstrated across task types in higher education (src-007)
- Behavioral feature engineering enables outcome prediction (src-008)

**Limitations:**
- Partial coverage: KT limited to structured exercises, not open reading or debugging (src-006)
- Cross-task model unification not directly addressed (src-007)
- Prediction models target outcomes/risk, not fine-grained conceptual mastery or cross-task unified states (src-008)
- Transfer assumptions across task types not demonstrated (no source)
- Unified model across reading, debugging, structured exercises not established (all sources)

---

## Cross-Layer Integration Patterns

### Evidence-Based Pedagogical Action
- Knowledge state estimates enable adaptive resource recommendation (src-006: Application Section V)
- OLM feedback enables informed learning decisions; adaptive models automate action selection (src-007)
- Early prediction (5.85 weeks average) enables proactive intervention (src-008)

### Learner Model Transparency
- Four OLM categories form learner agency continuum: system-guided reflection → learner-driven → adaptive co-regulation (src-007)
- Transparency as pedagogical tool: making models transparent encourages metacognitive engagement (src-007)

### Domain-Specific Training
- KT models require course-specific exercise data (ASSISTments, EdNet) (src-006)
- Each course requires separate knowledge structure (src-005)
- Context specificity affects model performance (src-008)

---

## Unresolved Gaps

### Layer 1: Source and Material Grounding
- Preventing model knowledge leakage when sources incomplete
- Handling ambiguous or conflicting source content
- Quantifying citation accuracy and completeness

### Layer 2: Course and Task Boundaries
- Vocabulary and notation constraint enforcement mechanisms
- Assessment criteria alignment methods
- Academic integrity preservation beyond external policy

### Layer 3: Pedagogical Action Selection
- Automatic obstacle-type detection (terminology gaps, prerequisite deficits, language barriers)
- Procedural vs. conceptual confusion differentiation
- Lost context recovery strategies

### Layer 4: Learning-Behavior Evidence
- "Understood example" vs. "can solve independently" operational definitions
- Single-instance success vs. consistent performance criteria
- Intervention effectiveness: whether acting on predictions improves outcomes

### Layer 5: Learner Model Applicability
- Unified learner model across reading, debugging, and structured exercises
- Transfer assumptions across task types
- Skill decomposition granularity for unstructured tasks
- Cross-domain knowledge state transfer

---

## Summary: Eight-Source Evidence Base

**Demonstrated:**
1. Source-grounding via inline citations (src-001)
2. RCT evidence for learning effectiveness in specific contexts (src-003, src-004)
3. Knowledge modeling at scale for structured exercises (src-005, src-006)
4. Learner model transparency approaches (src-007)
5. Course outcome prediction from behavioral traces (src-008)
6. User-requested pedagogical controls (src-002)
7. Side information enriches structured exercise modeling (src-006)
8. Feature engineering transforms raw interactions into predictive measures (src-008)

**Partially Addressed:**
- Material scope control (file upload pattern, domain structures; leakage prevention unclear)
- Task context preservation (memory feature exists; multi-session mechanisms not detailed)
- Obstacle-specific adaptation (adaptive scaffolding exists; automatic detection not demonstrated)
- Evidence-driven state updates (temporal dynamics modeled; transition criteria not operational)
- Task-type-specific modeling (structured exercises demonstrated; cross-task unification not established)

**Not Addressed:**
- Unified learner model across reading, debugging, exercises
- Automatic obstacle-type detection (terminology, prerequisite, language, conceptual)
- Vocabulary/notation constraint enforcement
- Academic integrity preservation mechanisms
- Cross-domain knowledge state transfer
- Intervention effectiveness (prediction vs. action)

---

**Status**: Stage 3 complete (eight-source synthesis). Matrix ready for Gate 1 exit evaluation.
