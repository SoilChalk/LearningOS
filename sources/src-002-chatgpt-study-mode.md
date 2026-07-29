# Source 002: ChatGPT Study Mode

**Title**: Using Study Mode in ChatGPT
**Organization**: OpenAI
**URL**: https://help.openai.com/en/articles/11780217-study-mode
**Accessed**: 2026-07-29
**Source Type**: product_documentation
**Language**: English (official OpenAI help documentation)

---

## Core Capabilities (Directly Supported)

1. **Pedagogical action spectrum**
   - "Guide your thinking" - asks questions instead of giving answer (Socratic approach)
   - "Explain concepts in layers" - starts simple, adds detail when ready
   - "Check your understanding" - asks questions, gives feedback, helps correct misunderstandings
   - Can be instructed to "use hints, quizzes, or step-by-step guidance"

2. **Obstacle-specific adaptation mechanisms**
   - User can request: "slow down, use simpler language, give an analogy, or go deeper"
   - Adjustable difficulty: "too basic" → "more advanced explanation"; "too quickly" → "pause after each step"
   - Level-aware: user specifies "middle school, high school, college, beginner, or advanced"

3. **Material-constrained operation**
   - Can work with uploaded files: notes, syllabus, worksheet, slides, textbook excerpt, problem photos
   - "Study Mode can reference the materials you upload while helping you study"
   - Explicit guidance: "tell ChatGPT which page, section, or question to focus on"

4. **Learning-behavior evidence points**
   - Factual observations: uploads, explicit requests, question answers
   - System can "quiz you one question at a time, wait for your answer, and explain what to review next"
   - Memory feature can save "learning goals, preferred explanation style, or topics you have studied before"

5. **Availability and access**
   - Available globally across web, iOS, Android
   - All ChatGPT models supported
   - Works with any ChatGPT plan (Free, Plus, Pro, Team)

---

## Design Implications

1. **Pedagogical action selection requires explicit controls**: System does NOT automatically choose between explain/hint/question - user must guide the interaction style

2. **Socratic questioning is opt-in, not default**: Documentation emphasizes Study Mode can guide with questions BUT acknowledges "there may be times when it gives a direct answer" - confirms Socratic dialogue should not be universal default

3. **Obstacle types distinguishable by user feedback**: System adjusts based on explicit requests ("slow down", "simpler language", "more advanced") rather than automatic inference

4. **Material grounding strategy**: File upload + explicit section reference, NOT automatic intelligent indexing

5. **Evidence collection is sparse**: System can observe completion and responses, but no mention of automatic mastery inference or knowledge state modeling

---

## Limitations and Non-Inferences

1. **No learning effectiveness claims**: Documentation explicitly states "Study Mode can make mistakes" and "does not replace your teacher, tutor, course materials"

2. **No automatic pedagogy**: System does not automatically detect when to explain vs. hint vs. quiz - requires user instruction

3. **No learner modeling mentioned**: Memory feature saves preferences and topics, NOT knowledge state or mastery level

4. **Material constraint is shallow**: Upload + manual section reference, not intelligent course boundary enforcement

5. **Academic integrity boundaries unclear**: "Follow the AI-use policies of your school" - defers to external policy rather than technical enforcement

6. **Rate limits apply**: "Study Mode does not add extra messages, bypass rate limits, or make unavailable models available"

---

## Affected Decisions

- pedagogical_action_selection: explicit user control over teaching style
- learning_evidence: observe completion and responses, not infer mastery
- course_boundary_enforcement: file upload pattern, not automatic scope constraint
- anti_pattern_avoidance: confirms Socratic questioning should not be universal default

---

## Verification Status

**Status**: verified
**Publication date**: Document updated "23小时前" (23 hours ago) as of 2026-07-29
**Product status**: Launched globally across plans
