# Learning OS Research Questions

**Generated**: 2026-07-29  
**Task**: task-001-core-research  
**Status**: Stage 1 - Structure Established

---

## Research Scope

This document defines the research questions that guide Learning OS core research, organized by the five layers specified in the task contract.

---

## Layer 1: Source and Material Grounding

### RQ1.1: Source-Bound Explanations
How do learning systems maintain explanations tied to user-provided sources rather than generating content from model knowledge alone?

**Dimensions:**
- Source citation mechanisms
- Content attribution boundaries
- Disambiguation between source-derived and inferred content
- Source retrieval and passage anchoring

### RQ1.2: Material Scope Control
How do course-constrained assistants maintain boundaries around specific course materials and prevent drift into general knowledge?

**Dimensions:**
- Explicit material corpus definition
- Out-of-scope query handling
- Material indexing and retrieval strategies

---

## Layer 2: Course and Task Boundaries

### RQ2.1: Course-Specific Constraint Enforcement
What mechanisms enforce course-specific constraints in AI-assisted learning environments?

**Dimensions:**
- Vocabulary and notation constraints
- Acceptable solution method boundaries
- Assessment criteria alignment
- Academic integrity preservation

### RQ2.2: Task Context Preservation
How do systems maintain task context across interrupted or multi-session learning?

**Dimensions:**
- Learning position recovery
- Unresolved question tracking
- Session continuity mechanisms

---

## Layer 3: Pedagogical Action Selection

### RQ3.1: Teaching Action Taxonomy
What teaching actions are distinguished by intelligent tutoring systems, and when is each appropriate?

**Dimensions:**
- Explain vs. hint vs. direct answer
- Question generation vs. guided practice
- Socratic dialogue vs. worked examples
- Error-driven vs. concept-driven instruction

### RQ3.2: Obstacle-Specific Adaptation
How do systems detect and respond to different types of learning obstacles?

**Dimensions:**
- Terminology gaps
- Prerequisite knowledge deficits
- Language/translation barriers
- Procedural vs. conceptual confusion
- Lost context recovery

---

## Layer 4: Learning-Behavior Evidence

### RQ4.1: Factual Observation vs. Inference
What interaction events constitute factual observations vs. inferred learner states?

**Dimensions:**
- Directly observable: completion, time spent, attempts, explicit requests
- Inferred: understanding level, mastery state, engagement
- Reliability boundaries of self-reported understanding

### RQ4.2: Evidence-Driven State Updates
What behavioral evidence is required to justify learner state transitions?

**Dimensions:**
- "Understood example" vs. "can solve independently"
- Single-instance success vs. consistent performance
- Prompted completion vs. unprompted recall

---

## Layer 5: Learner Model Applicability

### RQ5.1: Knowledge Tracing Data Requirements
What data requirements and limitations constrain Bayesian Knowledge Tracing (BKT), Deep Knowledge Tracing (DKT), and related models?

**Dimensions:**
- Minimum interaction count per skill
- Prerequisite skill graph granularity
- Applicability to open-ended vs. structured tasks
- Generalization across problem types

### RQ5.2: Task-Type-Specific Modeling
Should open reading, debugging, and structured exercises share a unified learner model, or require separate modeling approaches?

**Dimensions:**
- Transfer assumptions across task types
- Skill decomposition granularity
- Model complexity vs. data availability tradeoffs
- When to avoid premature learner modeling

---

## Research Method Constraints

### Evidence Standards
- **Product pages**: Support feature existence claims only, not learning effectiveness
- **Search snippets**: Cannot substitute for reading source material
- **Individual reports**: Cannot be generalized to population claims without survey or experimental evidence
- **Dates and metrics**: Require recorded access date when product status may change
- **Academic papers**: Must be classified as survey, controlled experiment, simulation, or field evaluation

### Out of Scope for Task 001
- Complete knowledge graph construction
- Exhaustive question-type taxonomy
- Full error pattern classification
- Multi-agent architecture design
- Provider performance benchmarking
- Frontend implementation details

---

## Mapping to Task Contract Dimensions

| Research Question | Contract Dimension |
|-------------------|--------------------|
| RQ1.1, RQ1.2 | source_and_material_grounding |
| RQ2.1, RQ2.2 | course_and_task_boundaries |
| RQ3.1, RQ3.2 | pedagogical_actions |
| RQ4.1, RQ4.2 | learning_evidence |
| RQ5.1, RQ5.2 | learner_model_applicability |

---

## Next Steps

Stage 2 will identify 8-15 sources that directly address these research questions through:
- Official product/project documentation
- Original research papers
- High-quality surveys
- Field evaluation reports

Sources must provide factual observations, design implications, and explicit limitations rather than marketing claims or unsubstantiated effectiveness assertions.
