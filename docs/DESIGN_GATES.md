# Learning OS Design Gates

**Generated**: 2026-07-29
**Task**: task-001-core-research
**Status**: Stage 2 - Source Verification In Progress

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

### Current Progress (2026-07-29T16:00:00Z)

**Sources Verified**: 5/8 (minimum target not yet met)

**Fully Verified Sources**:
1. src-001: NotebookLM/Gemini Notebook (Google) - source grounding, inline citations
2. src-002: ChatGPT Study Mode (OpenAI) - pedagogical action requires explicit control
3. src-003: LearnLM (Google/DeepMind) - RCT evidence: moved from 50th to 64th percentile
4. src-004: Tutor CoPilot (Stanford) - human-AI collaboration RCT: +4-9 percentile points
5. src-005: ALEKS Knowledge Space Theory (McGraw Hill) - learner modeling framework

**Incomplete Candidates** (access issues after multiple attempts):
- Bayesian Knowledge Tracing papers (Corbett & Anderson 1995)
- Cognitive Tutors/ACT-R publications (Anderson, Koedinger, Corbett)
- ASSISTments research papers
- ITS effectiveness meta-analyses (Kulik & Fletcher, SAGE paywalls)
- Duolingo spaced repetition research (arXiv extraction failures)
- Khan Academy RCT studies (institutional access issues)

**Next Steps**:
- Attempt 3 more distinct accessible candidates for remaining research dimensions
- If additional candidates fail, document stop condition per protocol
- Continue to target minimum 8 verified sources

**Status**: Gate 1 remains IN PROGRESS until minimum source count achieved and all exit conditions met.

---

## Gate 2: First Vertical Scenario Design

**Current Status**: NOT STARTED

### Entry Conditions
- [ ] Gate 1 exit conditions met
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
**Status**: In Progress (5/8 sources verified)
**Next Milestone**: Achieve minimum 8 verified sources, satisfy all Gate 1 exit conditions
**Subsequent Phase**: First Vertical Scenario Design (Gate 2)

---

**Last Updated**: 2026-07-29T16:00:00Z
**Phase**: Gate 1 - Core Research IN PROGRESS
**Next Phase**: Gate 2 - First Vertical Scenario Design (blocked until Gate 1 complete)
