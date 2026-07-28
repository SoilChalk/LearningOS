# Source 001: NotebookLM / Gemini Notebook

**Title**: 了解 Gemini Notebook (Learn about Gemini Notebook)  
**Organization**: Google  
**URL**: https://support.google.com/gemininotebook/answer/16164461  
**Accessed**: 2026-07-29  
**Source Type**: product_documentation  
**Language**: Chinese (official Google support page)

---

## Core Capabilities (Directly Supported)

1. **Source-grounded responses with inline citations**
   - "与笔记本聊天，基于来源获取有依据的信息以及清晰的文内引用" (Chat with notebook to get grounded information based on sources with clear inline citations)
   - Citations ensure accuracy, transparency, and trust

2. **Supported source types**
   - PDF files, websites, YouTube videos, audio files
   - Google Docs, Google Slides
   - User can upload or discover new sources

3. **Material-constrained responses**
   - "Gemini Notebook 的设计初衷是根据您上传的来源中所提供的信息回答问题" (Gemini Notebook is designed to answer questions based on information provided in sources you upload)
   - System explicitly limits responses to uploaded source corpus

4. **Explanation of response failures**
   - Safety flagging: source content triggers safety markers
   - Unclear phrasing: system retrieves most relevant information based on question
   - No relevant information in sources: cannot answer outside source corpus

5. **Data protection commitments**
   - Workspace/Education users: uploaded content, queries, and responses NOT used for training AI models
   - Workspace/Education users: content NOT subject to human review
   - Personal account users: data NOT used for training unless user provides feedback

---

## Design Implications

1. **Source-bound architecture is feasible**: NotebookLM demonstrates that AI explanations can be constrained to user-provided materials with citation mechanisms

2. **Material scope enforcement requires explicit failure modes**: System distinguishes between "no answer exists in sources" vs. "question unclear" vs. "safety concern"

3. **Course-constrained assistant pattern validated**: If NotebookLM can constrain responses to uploaded PDFs/Docs, similar approach can apply to course materials

4. **Citation transparency is a product feature**: Inline citations presented as accuracy/transparency/trust mechanism, not just academic requirement

---

## Limitations and Non-Inferences

1. **No learning effectiveness evidence**: Page describes features but does NOT claim improved learning outcomes, retention, or comprehension

2. **No pedagogical action specification**: Does not describe when to explain vs. hint vs. question

3. **No learner modeling**: No mention of tracking user knowledge state, misconceptions, or progress

4. **Product status uncertainty**: Page accessed 2026-07-29 shows "Gemini Notebook" branding; earlier known as "NotebookLM"; product may have been renamed or merged

5. **Cannot verify English documentation**: English version inaccessible; relying on Chinese official page

---

## Affected Decisions

- source_grounding_strategy: inline citation mechanism
- course_boundary_enforcement: material corpus constraint pattern
- evidence_collection: distinguish "in-source" from "out-of-scope" queries

---

## Verification Status

**Status**: verified (Chinese official page)  
**English fallback**: inaccessible  
**Alternative verification**: None attempted (Chinese official page sufficient)
