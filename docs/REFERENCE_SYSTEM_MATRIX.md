# Reference System Matrix

**Generated**: 2026-07-29T17:00:00Z
**Task**: task-001-core-research
**Sources**: 5 verified sources
**Purpose**: Map research findings from verified sources to Learning OS design decisions

**Note**: This matrix is built from five verified sources reviewed so far. Claims about what systems exist, patterns observed, or gaps identified are limited to this reviewed sample unless explicitly noted otherwise.

---

## Verified Sources Summary

| ID | Title | Organization | Type | Language |
|----|-------|--------------|------|----------|
| src-001 | 了解 Gemini Notebook | Google | Product Documentation | zh-CN |
| src-002 | Using Study Mode in ChatGPT | OpenAI | Product Documentation | en |
| src-003 | Gemini 中的 LearnLM | Google Cloud/DeepMind | Product Documentation | zh-CN |
| src-004 | Tutor CoPilot | Stanford SCALE | Research Paper (Field Evaluation) | en |
| src-005 | ALEKS Knowledge Space Theory | McGraw Hill / Doignon & Falmagne | Product Documentation | en |

---

## Layer 1: Source Grounding

### Directly Supported Observations

**src-001 (NotebookLM/Gemini Notebook)**:
- System provides inline citations from uploaded sources (PDF, websites, YouTube videos, audio files, Google Docs, Google Slides)
- Gemini Notebook designed to answer questions based on information provided in uploaded sources
- System distinguishes three failure modes: safety flagging, unclear phrasing, no relevant information in sources
- For Workspace/Education users: uploaded content NOT used for AI training; NOT subject to human review

### Design Implications (from reviewed sample)

- Source-bound AI architecture demonstrated as product feature (src-001)
- Material scope enforcement requires explicit failure mode messages (src-001)
- Citation mechanism presented as accuracy/transparency/trust feature (src-001)
- File upload pattern establishes basic course boundary (src-001, src-002)

### Limitations Observed

- No learning effectiveness evidence provided in product documentation (src-001)
- Citation transparency exists as feature but effectiveness not evaluated (src-001)
- English documentation for NotebookLM not accessible; relying on Chinese official page (src-001)

---

## Layer 2: Course/Task Boundaries

### Directly Supported Observations

**src-001 (NotebookLM)**:
- System distinguishes "in-source" vs. "out-of-scope" queries
- Explicit failure modes for different types of query failures

**src-002 (ChatGPT Study Mode)**:
- Can upload files (notes, syllabus, worksheet, slides, textbook excerpt, problem photos)
- User must reference specific sections manually

**src-005 (ALEKS)**:
- Algebra 1 modeled as approximately 350 basic concepts giving rise to millions of empirically feasible knowledge states
- Each domain (e.g., Algebra 1, Algebra 2) requires separate pre-built knowledge structure
- Adaptive assessment using Markovian procedures can gauge student knowledge state in 25-30 questions

### Design Implications (from reviewed sample)

- Material corpus constraint feasible via file upload (src-001, src-002)
- Domain-specific knowledge structures enable fine-grained modeling but require expert construction (src-005)
- Efficient assessment possible: 25-30 questions sufficient despite millions of states (src-005)

### Limitations Observed

- Material constraint in ChatGPT Study Mode is shallow: requires manual section pointing (src-002)
- ALEKS granularity tradeoff unclear: is 350 concepts for Algebra 1 the right level? (src-005)
- Knowledge state construction method not detailed in product page (src-005)

---

## Layer 3: Pedagogical Action Selection

### Directly Supported Observations

**src-002 (ChatGPT Study Mode)**:
- User can instruct system to guide thinking (Socratic), explain in layers, check understanding, or use hints/quizzes/step-by-step
- User specifies level: middle school, high school, college, beginner, or advanced
- User can request: slow down, simpler language, analogy, deeper explanation, more advanced content
- Documentation states "there may be times when it gives a direct answer"

**src-003 (LearnLM)**:
- With appropriate system instructions, Gemini leverages LearnLM learning science research to trigger pedagogical behaviors
- Expert raters evaluated LearnLM on pedagogical elements like guidance and correcting mistakes beyond mere accuracy

**src-004 (Tutor CoPilot)**:
- System models expert thinking to assist tutors in real time
- Analysis of 350,000+ messages shows system increases probing questions and reduces generic praise
- Human-AI collaboration: AI assists tutors who then interact with students

### Design Implications (from reviewed sample)

- Observed interface pattern: ChatGPT Study Mode documents user-requested teaching styles (src-002)
- System instructions can trigger pedagogical behaviors when principles embedded via training (src-003)
- AI can guide pedagogical behaviors of human tutors with measurable effects (src-004)
- Pedagogical quality evaluated as separate dimension from accuracy (src-003)

### Limitations Observed

- ChatGPT Study Mode documents available behaviors but does not prove that pedagogical selection requires explicit user control as a technical constraint (src-002)
- Implementation details not disclosed: how LearnLM principles embedded or how Tutor CoPilot models expert thinking (src-003, src-004)
- Tutor-mediated interaction in src-004, not direct AI-student tutoring

---

## Layer 4: Learning-Behavior Evidence

### Directly Supported Observations

**src-002 (ChatGPT Study Mode)**:
- Memory feature saves learning goals, preferred explanation style, or topics studied before
- Documentation states Study Mode "does not replace your teacher, tutor, course materials" and "can make mistakes"

**src-003 (LearnLM)**:
- RCT in Sierra Leone: 1,763 middle school students (grades 7-8), 8 weeks, 12+ hours usage minimum
- Effect: math performance moved from the 50th to the 64th percentile (a difference of 14 percentile ranks)
- Effect equivalent to 1.8 to 2.5 additional years of learning progress

**src-004 (Tutor CoPilot)**:
- RCT with 700+ tutors and 1,000+ students from underserved communities
- Students with tutors using Tutor CoPilot 4 percentage points more likely to master math topics (p<0.01)
- Gains highest for students of lower-rated tutors: 9 percentage points
- System cost: approximately $20/tutor/year

**src-005 (ALEKS)**:
- Adaptive assessment: 25-30 questions sufficient to gauge knowledge state despite millions of possible states
- System determines "precisely what each individual student knows, and what the student is ready to learn next"

### Design Implications (from reviewed sample)

- Learning effectiveness measurable via RCT methodology in specific contexts (src-003, src-004)
- Minimum engagement threshold observed: 12+ hours over 8 weeks for LearnLM effect (src-003)
- AI assistance to human tutors bridges skill gaps: larger gains for lower-rated tutors (src-004)
- Efficient assessment demonstrated: 25-30 questions for complete picture (src-005)
- Economic viability consideration: $20/tutor/year for Tutor CoPilot (src-004)

### Limitations Observed

- RCT contexts specific: Sierra Leone middle school math (src-003), tutoring organizations underserved communities math (src-004)
- Generalization to other subjects, age groups, or countries requires caution (src-003, src-004)
- ChatGPT Study Mode: sparse evidence collection, no mastery inference mentioned (src-002)
- ALEKS: describes assessment framework, not learning outcomes (src-005)

---

## Layer 5: Learner Modeling / Knowledge Tracing Applicability

### Directly Supported Observations

**src-005 (ALEKS)**:
- Knowledge Space Theory applies combinatorics and stochastic processes to modeling specific knowledge domains
- Mathematical framework for knowledge states: prerequisite relationships modelable
- "Ready to learn" is computable from knowledge state and structure
- Domain specificity critical: each course requires separate knowledge structure
- Authoritative source: Learning Spaces by Doignon & Falmagne (Springer-Verlag, 2011)

### Design Implications (from reviewed sample)

- Knowledge modeling feasible at scale: 350 concepts → millions of states, assessment remains tractable (src-005)
- Prerequisite relationships mathematically modelable via combinatorial framework (src-005)
- Adaptive assessment can be efficient using stochastic (Markovian) procedures (src-005)

### Limitations Observed

- Pedagogical action selection not addressed by Knowledge Space Theory (src-005)
- "Empirically feasible" knowledge state definition not provided (src-005)
- Question selection algorithm not disclosed (src-005)

---

## Cross-Source Observations

### Pedagogical Quality vs. Accuracy

- LearnLM evaluation: "pedagogical elements like guidance and correcting mistakes beyond mere accuracy" (src-003)
- Tutor CoPilot: probing questions ↑, generic praise ↓ (specific behaviors measured) (src-004)
- **Observation from sample**: Pedagogy evaluated as separate dimension from correctness in reviewed sources

### Human-AI Collaboration Models Observed

- Direct AI interaction with user-controlled pedagogy: ChatGPT Study Mode (src-002), LearnLM (src-003)
- AI-assisted human tutoring: Tutor CoPilot (src-004)
- **Observation from sample**: Multiple collaboration models exist in reviewed sources

### Evidence Quality in Reviewed Sample

- **RCT with external assessment**: LearnLM Sierra Leone study, Tutor CoPilot study (src-003, src-004)
- **Product features described**: Not ebookLM, ChatGPT Study Mode, ALEKS (src-001, src-002, src-005)
- **Observation**: Learning effectiveness claims supported by RCT in specific contexts; product pages describe features without effectiveness evidence

---

## Patterns Not Observed in Five Verified Sources

The following were not found in the five verified sources reviewed so far. This does not mean they do not exist in the broader literature—only that they were not present in this specific sample:

1. **Source grounding + learner modeling integration**: No verified source combined material-constrained responses with probabilistic knowledge state tracking
2. **Automatic pedagogical decision-making**: Observed patterns require either user instruction (src-002) or embedded training with undisclosed details (src-003)
3. **Automatic obstacle-type detection**: Not described in any verified source
4. **Non-math subject validation**: All RCT evidence in reviewed sources focused on mathematics (src-003, src-004)
5. **Sophisticated learner modeling systems**: ALEKS describes framework (src-005) but detailed systems like Bayesian Knowledge Tracing or Cognitive Tutors not accessible for verification

---

## Claims Requiring Qualification

The following claims from earlier analysis have been revised based on review requirements:

1. **"Socratic questioning is opt-in, not universal default"**
   - **Revised**: ChatGPT Study Mode documentation describes that "there may be times when it gives a direct answer" and user can request Socratic approach (src-002). This documents interface behavior; whether Socratic is technically "opt-in" or "default-off" is a design inference, not directly stated.

2. **"Pedagogical action selection requires explicit user control"**
   - **Revised**: ChatGPT Study Mode documents user-requested teaching styles (src-002). LearnLM uses system instructions to trigger behaviors (src-003). Observed pattern in these sources: explicit specification used, but cannot generalize to "requires" as universal constraint.

3. **"No system combines source grounding + learner modeling"**
   - **Revised**: Not observed in the five verified sources reviewed so far. Cannot claim exhaustive search without systematic literature review.

---

## Deferred Candidates

The following candidates were identified but could not be verified due to access restrictions:

| Candidate | Reason | Research Questions |
|-----------|--------|-------------------|
| Bayesian Knowledge Tracing (Corbett & Anderson 1995) | Primary papers not accessible; PDF blocks | RQ4.1, RQ5.1, RQ5.2 |
| Cognitive Tutors/ACT-R | CMU PACT publications blocked | RQ3.1, RQ3.2, RQ4.1, RQ5.1 |
| ASSISTments | Institutional repository PDFs inaccessible | RQ2.1, RQ3.1, RQ4.1 |
| ITS Effectiveness Meta-Analysis | SAGE/IDA paywalls (HTTP 403) | RQ4.1, RQ4.2 |
| Duolingo Spaced Repetition | arXiv extraction errors | RQ4.1, RQ5.1 |
| Khan Academy RCT Studies | Primary study documents not directly accessible | RQ4.1, RQ4.2 |

---

## Design Recommendations (from reviewed sample)

### Based on Verified Evidence

1. **Source grounding pattern demonstrated**: File upload + inline citation feasible (src-001)
2. **RCT evidence exists for specific contexts**: LearnLM +14 percentile ranks in Sierra Leone middle school math; Tutor CoPilot +4-9 percentage points in tutoring organizations (src-003, src-004)
3. **User-controlled pedagogy documented**: ChatGPT Study Mode interface allows explicit teaching style requests (src-002)
4. **Efficient assessment demonstrated**: ALEKS shows 25-30 questions sufficient for millions of states (src-005)

### Inferences from Reviewed Sample

1. **Consider explicit pedagogical controls**: Observed pattern in src-002 and src-003 suggests explicit specification over automatic inference
2. **Consider human-AI collaboration**: Tutor CoPilot shows larger gains for lower-rated tutors (src-004)
3. **Consider material corpus constraint**: Simpler than pre-built knowledge structures (src-001, src-002 vs. src-005)

---

**End of Reference System Matrix**
**Last Updated**: 2026-07-29T17:00:00Z
**Status**: Built from 5 verified sources; Task 001 in progress (5/8 minimum target)
