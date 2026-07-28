# Learning OS Design Gates

**Generated**: 2026-07-29  
**Task**: task-001-core-research  
**Status**: Stage 1 - Structure Established

---

## Purpose

Design gates define entry and exit conditions for each major phase of Learning OS development. They prevent premature implementation and ensure research findings inform design decisions.

---

## Gate 1: Core Research Phase

**Current Status**: IN PROGRESS (task-001-core-research)

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

### Exit Conditions
- [ ] Source ledger contains 8-15 verified sources
- [ ] Every source includes supported observations, implications, and limitations
- [ ] Reference system matrix separates product layer from evidence
- [ ] Design gates document defines subsequent phase conditions
- [ ] All JSON validation passes
- [ ] No implementation code, frontend, or private material added

### Prohibited Activities
- Frontend implementation
- Complete knowledge graph construction
- Automatic mastery classification
- Exhaustive QuestionType/ErrorPattern taxonomies
- Multi-agent free-form collaboration
- Provider ranking systems
- Complex event-sourced runtime

---

## Gate 2: First Vertical Scenario Design

**Current Status**: NOT STARTED

### Entry Conditions
- [x] Gate 1 exit conditions met
- [ ] Provisional scenario identified from research
- [ ] Minimum flow defined
- [ ] Source-grounding strategy selected
- [ ] Task boundary enforcement approach chosen

### Activities
- Define complete user flow for first scenario
- Specify source material handling
- Design pedagogical action selection rules
- Define minimal persistent state
- Establish evidence collection points
- Document what NOT to build

### Exit Conditions
- [ ] Scenario specification document complete
- [ ] Entry/exit criteria for each flow step defined
- [ ] Pedagogical action decision tree documented
- [ ] State schema defined (current_position, observed_difficulty, evidence_level, next_action)
- [ ] Success criteria measurable without complex learner model

### Prohibited Activities
- Building for multiple scenarios simultaneously
- Implementing learner model before evidence design
- Creating general-purpose knowledge graph
- Developing automated review scheduler

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

## Current Phase Summary

**Phase**: Core Research (Gate 1)  
**Started**: 2026-07-29  
**Status**: In Progress  
**Next Milestone**: Complete 8 verified sources, exit Gate 1  
**Subsequent Phase**: First Vertical Scenario Design (Gate 2)

---

## Gate 1 Completion Status (Updated 2026-07-29T14:00:00Z)

### Entry Conditions: ✅ ALL MET
✓ Project purpose defined  
✓ Research scope bounded  
✓ Evidence standards established  
✓ Source verification protocol defined  

### Activities: ✅ ALL COMPLETE
✓ 8 verified sources across five research dimensions (src-001 through src-008)  
✓ Directly supported observations documented for each source  
✓ Design implications extracted with explicit limitations  
✓ Reference system matrix created (docs/REFERENCE_SYSTEM_MATRIX.md)  
✓ First vertical scenario boundaries informed by findings  

### Exit Conditions: ✅ ALL MET
✅ Source ledger contains 8 verified sources (target minimum achieved)  
✅ Every source includes supported observations, implications, and limitations  
✅ Reference system matrix separates product features from learning effectiveness evidence  
✅ Design gates document updated with completion status  
✅ JSON validation passes (source-ledger.json valid)  
✅ No implementation code, frontend, or private material added  

### Key Findings Summary

**Layer 1 - Source Grounding:**
- NotebookLM demonstrates inline citations from uploaded materials
- File upload + explicit reference pattern validated (ChatGPT, NotebookLM)
- Citation transparency presented as trust mechanism

**Layer 2 - Course/Task Boundaries:**
- Material corpus constraint feasible (file upload pattern)
- Domain-specific knowledge structures require expert construction (ALEKS: 350 concepts for Algebra 1)
- Rapid content creation possible with simplified models (ASSISTments: 30 min per problem)

**Layer 3 - Pedagogical Action Selection:**
- Explicit user control validated (ChatGPT Study Mode)
- AI can guide human tutors effectively (Tutor CoPilot: +9 p.p. for lower-rated tutors)
- Cognitive models enable step-by-step guidance but require expensive expert construction
- Socratic questioning is opt-in, NOT universal default

**Layer 4 - Learning-Behavior Evidence:**
- RCT evidence exists: LearnLM +14 p.p. (50th → 64th percentile), Tutor CoPilot +4 to +9 p.p.
- Efficient assessment: ALEKS 25-30 questions sufficient despite millions of possible states
- External prediction validated: BKT predicts standardized test performance
- Evidence quality hierarchy: RCT > external prediction > long-term deployment > product features

**Layer 5 - Learner Modeling:**
- Knowledge Space Theory (ALEKS) and Bayesian Knowledge Tracing (BKT) demonstrate mathematical frameworks at scale
- Cognitive Tutors deployed 15+ years with production rules + BKT
- Tradeoff: expensive sophisticated models (Cognitive Tutors) vs. rapid simplified models (ASSISTments pseudo-tutors)

**Critical Gaps Identified:**
1. No system combines source grounding + learner modeling
2. Automatic pedagogical decision-making requires expensive cognitive model or embedded training (LearnLM details not public)
3. Course boundary intelligence without pre-built structures not demonstrated
4. Automatic obstacle-type detection not found
5. Evidence primarily from math subjects; other domains not validated

### Prohibited Activities Check: ✅ COMPLIANT
- No frontend implementation
- No complete knowledge graph construction
- No automatic mastery classification
- No exhaustive Question Type/Error Pattern taxonomies
- No multi-agent free-form collaboration
- No provider ranking systems
- No complex event-sourced runtime

### Unresolved Issues
None. Gate 1 exit conditions fully satisfied.

### Recommendation for Gate 2
Proceed to First Vertical Scenario Design with following constraints:
1. Start with source grounding + file upload pattern (simpler than ALEKS knowledge structures)
2. Make pedagogical action selection explicit user choice (ChatGPT pattern)
3. Collect sparse evidence (observable behaviors, not inferred mastery)
4. Focus on single subject initially (math has most evidence; consider FDS/Digital Logic for actual user need)
5. Avoid claiming learning effectiveness without pilot validation

**GATE 1 STATUS: READY TO EXIT**

---

**Last Updated**: 2026-07-29T14:00:00Z  
**Phase**: Gate 1 - Core Research COMPLETE  
**Next Phase**: Gate 2 - First Vertical Scenario Design  
