# [Task 001] Core Research Workflow

## Summary

Task 001 (core-research) is **IN PROGRESS**. Stage 1 (structure establishment) complete. Stage 2 (source verification) in progress with 5/8 minimum sources verified.

## Current Status

**Sources Verified**: 5 of 8 minimum required  
**Gate 1**: NOT MET  
**Review Cycle**: task-001-review-02 corrections applied  
**Branch**: agent/task-001-core-research  
**PR Status**: Draft  

## Files Changed

### Documentation
- `docs/RESEARCH_QUESTIONS.md` - 10 research questions across 5 layers (RQ1.1-RQ5.2)
- `docs/DESIGN_GATES.md` - 4 phase gates; Gate 1 in progress
- `docs/REFERENCE_SYSTEM_MATRIX.md` - Synthesis of 5 verified sources

### Sources (5 verified)
- `sources/src-001-notebooklm.md` - Google Gemini Notebook (source grounding, inline citations)
- `sources/src-002-chatgpt-study-mode.md` - OpenAI Study Mode (user-requested teaching styles)
- `sources/src-003-learnlm.md` - Google LearnLM (RCT: moved from 50th to 64th percentile, a difference of 14 percentile ranks)
- `sources/src-004-tutor-copilot.md` - Stanford Tutor CoPilot (RCT: +4 to +9 percentage points)
- `sources/src-005-aleks-kst.md` - ALEKS Knowledge Space Theory (learner modeling framework)

### Templates & Scripts
- `templates/SOURCE_RECORD.json` - Schema for individual source records
- `templates/SOURCE_LEDGER.schema.json` - Schema for complete source ledger
- `scripts/validate_source_records.py` - Deterministic JSON Schema validation

### State & Control
- `sources/source-ledger.json` - Structured ledger with 5 verified sources, 6 incomplete candidates
- `state/CURRENT_STATE.yaml` - Phase: core_research IN PROGRESS
- `agent-control/results/task-001.json` - Task result with review-02 changes applied

## Review 02 Changes Applied

1. **Matrix rebuilt from five-source ledger**: All references to removed sources eliminated
2. **Negative gap claims scoped**: Changed "No system found" to "Not observed in the five verified sources reviewed so far"
3. **LearnLM percentile wording corrected**: "moved from 50th to 64th percentile (a difference of 14 percentile ranks)" - not "percentage points"
4. **Study Mode claims downgraded**: Separated documented interface behavior from design inferences about technical requirements
5. **Schema architecture fixed**: Created `SOURCE_LEDGER.schema.json` with proper reference to `SOURCE_RECORD.json`
6. **Deterministic validation added**: `validate_source_records.py` uses jsonschema library, returns nonzero on failure
7. **Stage 2 kept in progress**: Gate 1 status remains not_met
8. **All files synchronized**: Consistent in_progress status, 5 sources, Gate 1 not_met

## Validation Commands

```bash
# JSON format validation
python3 -m json.tool sources/source-ledger.json >/dev/null
# Exit code: 0 (PASSED)

python3 -m json.tool templates/SOURCE_RECORD.json >/dev/null
# Exit code: 0 (PASSED)

python3 -m json.tool templates/SOURCE_LEDGER.schema.json >/dev/null
# Exit code: 0 (PASSED)

# Schema validation
python3 scripts/validate_source_records.py
# Exit code: 0 (PASSED)

# File structure check
find . -maxdepth 3 -type f | sort
# Exit code: 0 (PASSED)

# Prohibited term check
# Checks that removed source IDs and incorrect percentile terminology do not appear
# Exit code: 0 (PASSED)
# Exit code: 0 (PASSED)
```

## Key Findings (from 5 verified sources)

### Layer 1: Source Grounding
- **Demonstrated**: Inline citations from uploaded materials (NotebookLM src-001)
- **Pattern**: File upload + explicit section reference
- **Limitation**: Citation transparency exists but effectiveness not evaluated

### Layer 2: Course/Task Boundaries
- **Feasible**: Material corpus constraint via file upload (src-001, src-002)
- **Sophisticated**: Domain-specific knowledge structures (ALEKS src-005: 350 concepts → millions of states)
- **Efficient assessment**: 25-30 questions sufficient (src-005)

### Layer 3: Pedagogical Action Selection
- **Documented behavior**: ChatGPT Study Mode allows explicit teaching style requests (src-002)
- **Design inference**: Whether pedagogical selection requires explicit user control is an inference, not directly stated
- **Embedded training**: LearnLM uses system instructions to trigger behaviors (src-003)
- **Critical observation**: Socratic questioning documented as opt-in; "there may be times when it gives a direct answer" (src-002)

### Layer 4: Learning-Behavior Evidence
- **RCT evidence (LearnLM)**: Math performance moved from 50th to 64th percentile (a difference of 14 percentile ranks), 12+ hours over 8 weeks, Sierra Leone middle school math (src-003)
- **RCT evidence (Tutor CoPilot)**: +4 percentage points average, +9 percentage points for lower-rated tutors, 700+ tutors, 1,000+ students (src-004)
- **Context-specific**: Evidence from specific populations and subjects; generalization requires caution

### Layer 5: Learner Modeling
- **Mathematical framework**: Knowledge Space Theory (ALEKS src-005)
- **Efficient at scale**: 350 concepts → millions of states, assessment remains tractable
- **Limitation**: Pedagogical action selection not addressed by Knowledge Space Theory

## Patterns Not Observed in Five Verified Sources

The following were **not observed in the five verified sources reviewed so far**:

1. **Source grounding + learner modeling integration**: No verified source combined material-constrained responses with knowledge state tracking
2. **Automatic pedagogical decision-making**: Observed patterns require either user instruction (src-002) or embedded training with undisclosed details (src-003)
3. **Automatic obstacle-type detection**: Not described in any verified source
4. **Non-math subject validation**: All RCT evidence focused on mathematics
5. **Sophisticated learner modeling systems**: ALEKS describes framework; detailed systems like Bayesian Knowledge Tracing or Cognitive Tutors not accessible for verification

## Incomplete Candidates (6 deferred due to access issues)

- **Bayesian Knowledge Tracing** (Corbett & Anderson 1995): Primary papers not accessible; PDF blocks
- **Cognitive Tutors/ACT-R**: CMU PACT publications blocked
- **ASSISTments**: Institutional repository PDFs inaccessible
- **ITS Effectiveness Meta-Analysis**: SAGE/IDA paywalls (HTTP 403)
- **Duolingo Spaced Repetition**: arXiv extraction errors
- **Khan Academy RCT Studies**: Primary study documents not directly accessible

## Gate 1 Status

**Entry Conditions**: ✅ ALL MET  
**Activities**: 🔄 PARTIALLY COMPLETE (5/8 sources)  
**Exit Conditions**: ❌ NOT MET  
**Prohibited Activities Check**: ✅ COMPLIANT  
**Status**: **IN PROGRESS**

**Blockers**:
- Source count 5/8 (minimum 8 required)
- 6 incomplete candidates due to access restrictions

## Unresolved Issues

1. Source count below minimum: 5/8
2. Research question RQ5.2 not covered by current sources
3. Multiple academic sources inaccessible due to paywalls, PDF blocks, or HTTP errors

## Next Steps

- [ ] Attempt 3 more distinct accessible candidates for remaining research dimensions
- [ ] Document stop condition if additional candidates fail per protocol
- [ ] Continue to Stage 3 (synthesis matrix rebuild) only after minimum 8 sources achieved
- [ ] Push updates to task branch (Draft PR #2 remains draft)
- [ ] **DO NOT MERGE; DO NOT START TASK 002**

---

**Task ID**: task-001-core-research  
**Status**: IN PROGRESS  
**Last Updated**: 2026-07-29T18:00:00Z  
**Branch**: agent/task-001-core-research  
**Review Cycle**: task-001-review-02 corrections applied

