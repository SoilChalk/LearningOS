# Reference System Matrix

**Generated**: 2026-07-29  
**Task**: task-001-core-research  
**Sources**: 8 verified sources  
**Purpose**: Map research findings to Learning OS design decisions  

---

## Matrix Structure

| System/Research Line | System Layer | Directly Supported Capability | Required Conditions | Design Implication | Limitations | Source IDs |
|---------------------|--------------|-------------------------------|--------------------|--------------------|-------------|------------|

---

## Layer 1: Source Grounding

| System/Research Line | System Layer | Directly Supported Capability | Required Conditions | Design Implication | Limitations | Source IDs |
|---------------------|--------------|-------------------------------|--------------------|--------------------|-------------|------------|
| NotebookLM / Gemini Notebook | Source grounding | Inline citations from uploaded sources; material-constrained responses | User uploads PDF/Docs/websites/videos; explicit source corpus | Source-bound AI architecture is feasible; citation mechanism provides transparency | No learning effectiveness evidence; product status uncertain (naming change) | src-001 |
| ChatGPT Study Mode | Source grounding | File upload + manual section reference | User uploads materials and specifies section/page | Material grounding pattern: upload + explicit reference, NOT auto-indexing | Shallow constraint - requires manual section pointing | src-002 |

**Key Finding**: Source-grounded responses with inline citations are demonstrated (NotebookLM), but require explicit material upload and may need manual section specification (ChatGPT).

---

## Layer 2: Course/Task Boundaries

| System/Research Line | System Layer | Directly Supported Capability | Required Conditions | Design Implication | Limitations | Source IDs |
|---------------------|--------------|-------------------------------|--------------------|--------------------|-------------|------------|
| NotebookLM / Gemini Notebook | Course boundary | System distinguishes "in-source" vs. "out-of-scope" queries; explicit failure modes | Source corpus uploaded | Material scope enforcement requires distinct error messages for different failure types | No mention of pedagogical boundaries or topic prerequisites | src-001 |
| ChatGPT Study Mode | Course boundary | File upload pattern constrains responses to uploaded materials | User uploads course files | File upload establishes basic boundary but NOT intelligent scope enforcement | No automatic topic sequencing or prerequisite detection | src-002 |
| ALEKS | Course boundary | Domain-specific knowledge structures (e.g., Algebra 1 = 350 concepts with millions of states) | Pre-built knowledge structure for each domain | Each course/subject requires separate knowledge structure | Domain specificity means cross-domain learning not addressed | src-005 |
| ASSISTments | Course boundary | Content created per-problem with state graphs | Teacher/expert creates content for specific problems | Rapid content creation (30 min per problem) enables fine-grained boundaries | Pseudo-tutors simpler than full cognitive models | src-008 |

**Key Finding**: Course boundaries can be enforced through uploaded material corpus (NotebookLM, ChatGPT) or pre-built knowledge structures (ALEKS). Domain-specific structures enable fine-grained modeling but require expert construction.

---

## Layer 3: Pedagogical Action Selection

| System/Research Line | System Layer | Directly Supported Capability | Required Conditions | Design Implication | Limitations | Source IDs |
|---------------------|--------------|-------------------------------|--------------------|--------------------|-------------|------------|
| ChatGPT Study Mode | Pedagogical action | Guide thinking (Socratic), explain in layers, check understanding, hints/quizzes/step-by-step | User explicitly instructs desired teaching style | Pedagogical action requires EXPLICIT user control; Socratic questioning opt-in, NOT default | System does NOT automatically choose when to explain vs. hint vs. question | src-002 |
| LearnLM | Pedagogical action | System instructions trigger pedagogical behaviors; trained on pedagogical instruction following | Appropriate system instructions provided | Learning science principles can be embedded in LLMs via training; system instructions enable behavior | Product page doesn't detail specific principles or training methods | src-003 |
| Tutor CoPilot | Pedagogical action | Models expert thinking to assist tutors; increases probing questions, reduces generic praise | Human tutor mediates; AI provides real-time guidance | AI can guide pedagogical behaviors of human tutors; specific behavior changes measurable (probing questions ↑, generic praise ↓) | Tutor-mediated, not direct AI-student; implementation details not disclosed | src-004 |
| Cognitive Tutors | Pedagogical action | Model tracing provides just-in-time feedback and on-demand solution-sensitive hints | Production rule cognitive model of expert problem-solving | Cognitive model drives step-by-step guidance; hints derived from expert model, not generic | Cognitive model construction expensive (expert brainstorming + refinement) | src-007 |
| ASSISTments | Pedagogical action | Tutors during testing; state-graph pseudo-tutors provide scaffolding | Simplified state graph per problem | Assessment + instruction can be combined to avoid lost time | Simplified vs. full Cognitive Tutors - tradeoff between development cost and sophistication | src-008 |

**Key Finding**: Pedagogical action selection ranges from explicit user control (ChatGPT) to model-driven guidance (Cognitive Tutors). AI can guide human tutors (Tutor CoPilot) or provide direct feedback (Cognitive Tutors), but automatic pedagogical decision-making requires either explicit training (LearnLM) or expert cognitive models (Cognitive Tutors).

---

## Layer 4: Learning-Behavior Evidence

| System/Research Line | System Layer | Directly Supported Capability | Required Conditions | Design Implication | Limitations | Source IDs |
|---------------------|--------------|-------------------------------|--------------------|--------------------|-------------|------------|
| ChatGPT Study Mode | Evidence collection | Observes uploads, explicit requests, question answers, completion | User interacts with system; Memory feature saves preferences | Sparse evidence: completion and responses observable, but NO automatic mastery inference | No learner modeling or knowledge state tracking mentioned | src-002 |
| LearnLM | Evidence collection | RCT: 1,763 students, 8 weeks, 12+ hours usage → +14 percentile points (50th to 64th) | Minimum 12 hours engagement over 8 weeks | Learning effectiveness measurable with RCT methodology; usage threshold exists (12+ hours for effect) | Specific context: Sierra Leone, middle school math; generalization requires caution | src-003 |
| Tutor CoPilot | Evidence collection | RCT: 700+ tutors, 1,000+ students → +4 p.p. mastery; +9 p.p. for lower-rated tutors | 350,000+ messages analyzed | Large-scale message analysis enables pedagogical behavior measurement; effects larger for less skilled tutors | Math tutoring in underserved communities; tutor-mediated | src-004 |
| ALEKS | Evidence collection | Adaptive assessment: 25-30 questions sufficient to gauge knowledge state despite millions of possible states | Pre-built knowledge structure; Markovian assessment procedures | Efficient assessment possible (25-30 questions for complete picture) | Assessment methodology, not learning outcomes | src-005 |
| Bayesian Knowledge Tracing | Evidence collection | Predicts performance within ITS AND on external paper post-tests; tracks skill mastery over practice attempts | Four parameters per skill fitted from student data | Probabilistic skill-based model enables prediction outside tutoring environment | Skill decomposition manual; parameter fitting requires data | src-006 |
| Cognitive Tutors | Evidence collection | BKT + production rules track knowledge acquisition in real time | Cognitive model + BKT parameters | Two-layer: cognitive model (what to teach) + learner model (what student knows) | Implementation: 15+ years deployment, 8,000+ students in studies | src-007 |
| ASSISTments | Evidence collection | Student model predicts standardized test performance; "learns" student abilities for increasingly accurate predictions | Usage during assessment | Prediction as feature: forecast external test performance | Prediction accuracy not quantified in sources accessed | src-008 |

**Key Finding**: Evidence collection ranges from sparse observation (ChatGPT) to sophisticated probabilistic modeling (BKT). RCT evidence exists for learning effectiveness (LearnLM: +14 p.p., Tutor CoPilot: +4 to +9 p.p.). Efficient assessment (ALEKS: 25-30 questions) and external prediction (BKT, ASSISTments) are demonstrated.

---

## Layer 5: Learner Modeling / Knowledge Tracing Applicability

| System/Research Line | System Layer | Directly Supported Capability | Required Conditions | Design Implication | Limitations | Source IDs |
|---------------------|--------------|-------------------------------|--------------------|--------------------|-------------|------------|
| ALEKS | Learner modeling | Knowledge Space Theory: combinatorial + stochastic model of knowledge states; determines "what student knows and ready to learn next" | Domain-specific knowledge structure (e.g., 350 concepts for Algebra 1) | Mathematical framework for knowledge states; prerequisite relationships modelable; "ready to learn" computable | Granularity tradeoff (350 concepts for Algebra 1 - right level?); construction method not detailed | src-005 |
| Bayesian Knowledge Tracing | Learner modeling | Four-parameter probabilistic model per skill; tracks mastery evolution over practice; predicts in-system + external test performance | Skill decomposition; parameters fitted from student data | Skill-based probabilistic modeling validated at scale; transfer to external assessments proven | Skill decomposition manual; what constitutes "knowledge component" not algorithmic | src-006 |
| Cognitive Tutors | Learner modeling | Production rules + BKT = two-layer architecture (cognitive model of domain + learner model of student) | Expert-designed production rules; BKT parameters per skill | Deployed at scale (15+ years, thousands of students); improves upon classroom instruction | Cognitive model construction expensive; ACT-R specificity may limit flexibility | src-007 |
| ASSISTments | Learner modeling | State-graph pseudo-tutors; student model for test prediction | Simplified state graphs per problem; rapid development (<30 min per problem) | Simplified modeling reduces development cost; teachers can create content | Pseudo-tutors less sophisticated than full cognitive models | src-008 |

**Key Finding**: Sophisticated learner modeling exists (BKT: probabilistic skills; ALEKS: knowledge space theory) and is deployed at scale (Cognitive Tutors: 15+ years). Tradeoff: full cognitive models (expensive, sophisticated) vs. simplified models (rapid development, teacher-authorable).

---

## Cross-Cutting Observations

### 1. Pedagogical Quality vs. Accuracy
- LearnLM evaluation: "pedagogical elements like guidance and correcting mistakes **beyond mere accuracy**"
- Tutor CoPilot: probing questions ↑, generic praise ↓ (specific pedagogical behaviors measured)
- **Implication**: Pedagogy is a separate evaluation dimension from correctness

### 2. Human-AI Collaboration Models
- Direct AI tutoring: Cognitive Tutors, ALEKS, ASSISTments
- AI-assisted human tutoring: Tutor CoPilot (+9 p.p. for lower-rated tutors)
- User-controlled AI: ChatGPT Study Mode (explicit instruction required)
- **Implication**: Multiple collaboration models exist; AI assistance to humans shows promise for bridging skill gaps

### 3. Development Cost vs. Sophistication
- High-cost, high-sophistication: Cognitive Tutors (expert brainstorming + refinement)
- Medium-cost: ALEKS Knowledge Spaces (requires domain expert + mathematician)
- Low-cost: ASSISTments pseudo-tutors (30 min per problem, teacher-authorable)
- Prompt-based: ChatGPT, LearnLM (system instructions, no custom model)
- **Implication**: Cost-sophistication spectrum; simpler models enable scaling but may sacrifice capability

### 4. Evidence Quality Hierarchy
- **Gold standard**: Pre-registered RCT with external assessments (LearnLM Sierra Leone, Tutor CoPilot)
- **Strong**: Prediction of standardized tests (BKT, ASSISTments)
- **Moderate**: Deployed at scale for years (Cognitive Tutors, ALEKS)
- **Weak**: Product features described without learning outcomes (ChatGPT Study Mode, NotebookLM)
- **Implication**: Learning effectiveness claims require RCT or longitudinal deployment evidence

### 5. Socratic Questioning Constraint
- ChatGPT Study Mode: "there may be times when it gives a direct answer" - confirms Socratic dialogue NOT universal default
- LearnLM: "guide your thinking" - asks questions instead of giving answer (Socratic approach as option)
- **Implication**: Socratic questioning is opt-in pedagogical choice, not default for all learning contexts

---

## Identified Gaps and Open Questions

### Gap 1: Source Grounding + Learner Modeling Integration
- NotebookLM demonstrates source grounding with citations
- BKT/ALEKS demonstrate learner modeling
- **No system found** combining both: material-constrained responses PLUS probabilistic knowledge state tracking
- **Open question**: Can we integrate source-grounded LLM with BKT-style knowledge tracing?

### Gap 2: Automatic Pedagogical Decision-Making
- ChatGPT requires explicit user instruction
- LearnLM has embedded principles but details not public
- Cognitive Tutors use cognitive model but require expensive expert construction
- **Open question**: Can pedagogical action selection be automatic without expensive cognitive model construction?

### Gap 3: Course Boundary Intelligence
- File upload provides basic boundary (NotebookLM, ChatGPT)
- ALEKS has sophisticated knowledge structures but requires expert construction per domain
- **Open question**: Can course boundaries be intelligently enforced without pre-built knowledge structures?

### Gap 4: Obstacle-Type Detection
- ChatGPT: user explicitly requests "slow down", "simpler language", "more advanced"
- **No system found** automatically detecting obstacle types from student responses
- **Open question**: Can we automatically distinguish "didn't understand prerequisite" vs. "misread question" vs. "correct method, arithmetic error"?

### Gap 5: Evidence Collection for Real-World Courses
- RCT evidence exists for curated contexts (Sierra Leone math, tutoring organizations)
- **Missing**: Evidence for learning effectiveness in arbitrary real-world courses (e.g., user's FDS or Digital Logic courses)
- **Open question**: Do these systems work for non-math subjects? For advanced CS topics?

---

## Design Recommendations for Learning OS

### Recommendation 1: Start with Source Grounding + Basic Evidence
- **Why**: NotebookLM demonstrates feasibility; ChatGPT shows user-controlled pedagogy works
- **How**: Material upload + inline citation + explicit pedagogical instructions
- **Defer**: Complex learner modeling (BKT) until basic functionality validated

### Recommendation 2: Make Pedagogical Action Selection Explicit, Not Automatic
- **Why**: ChatGPT Study Mode shows users CAN control teaching style; Tutor CoPilot shows guidance works
- **How**: User selects: "explain directly", "guide with questions", "provide hints only"
- **Avoid**: Assuming system knows best pedagogical action without user context

### Recommendation 3: Use File Upload for Course Boundaries Initially
- **Why**: Simpler than building knowledge structures (ALEKS requires expert + mathematician)
- **How**: User uploads course materials; system constrains responses to uploaded corpus
- **Future**: Explore automatic knowledge structure extraction if basic approach insufficient

### Recommendation 4: Collect Sparse Evidence, Don't Overfit
- **Why**: ChatGPT collects sparse evidence (completion, responses); still useful
- **How**: Record: questions asked, answers given, explicit feedback, completion status
- **Avoid**: Claiming mastery inference without validation; focus on observable behaviors first

### Recommendation 5: Distinguish Fact Claims from Design Possibilities
- **Supported by evidence**: Source grounding works (NotebookLM), RCT effects exist (LearnLM +14 p.p.)
- **Demonstrated at scale**: BKT deployed 15+ years, ALEKS used widely
- **Possible but unproven**: Automatic obstacle detection, cross-domain knowledge structures
- **How**: Label all design claims with evidence level

---

## Claims Requiring Review

1. **"AI tutoring improves learning outcomes"**  
   - **Status**: Supported for specific contexts (LearnLM +14 p.p. in Sierra Leone math; Tutor CoPilot +4 to +9 p.p. in tutoring orgs)
   - **Requires**: Qualification of context, dosage (12+ hours), subject (math)

2. **"Source-grounded responses prevent hallucination"**  
   - **Status**: Feature exists (NotebookLM inline citations) but effectiveness claim not evaluated
   - **Requires**: Evidence that citations improve accuracy or user trust

3. **"Learner modeling enables personalization"**  
   - **Status**: Mechanisms exist (BKT, ALEKS) but "personalization" undefined
   - **Requires**: Specific definition of what personalizes (content sequence? difficulty? pedagogy?)

4. **"Socratic questioning improves understanding"**  
   - **Status**: Not claimed by sources; ChatGPT/LearnLM offer it as option, not default
   - **Requires**: Evidence that questioning > explaining for specific learning contexts

5. **"Learning OS works for any subject"**  
   - **Status**: Evidence primarily from math; other subjects not validated
   - **Requires**: Subject-specific validation or clear domain limitations

---

**End of Reference System Matrix**
