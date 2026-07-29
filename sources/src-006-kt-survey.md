# Source 006: Knowledge Tracing Survey

**Title**: A Survey of Knowledge Tracing: Models, Variants, and Applications
**Authors**: Shuanghong Shen, Qi Liu, Zhenya Huang, Yonghe Zheng, Minghao Yin, Minjuan Wang, Enhong Chen
**Organization**: University of Science and Technology of China, State Key Laboratory of Cognitive Intelligence
**URL**: https://arxiv.org/abs/2105.15106
**arXiv Version**: v4, 11 Apr 2024
**Journal Publication**: IEEE Transactions on Learning Technologies (noted in abstract, arxiv version predates journal)
**Accessed**: 2026-07-29
**Source Type**: research_paper_comprehensive_survey
**Retrieval Method**: Direct PDF download from arXiv (curl), local pdftotext extraction

---

## Core Content (Directly Supported)

1. **Knowledge Tracing Problem Definition**
   - KT monitors students' evolving knowledge states during problem-solving process
   - Learning sequence formulated as X = {([e1, ke1], a1, r1), ..., ([eN, keN], aN, rN)}
   - et = exercise, ket = related knowledge concepts, at = correctness (0/1), rt = side information
   - Goal: predict performance on future exercises given historical interaction sequences

2. **Three Fundamental Model Categories**
   - Bayesian models (BKT, DBKT): Hidden Markov Models tracking mastery states
   - Logistic models (LFA, PFA, KTM): Feature engineering + logistic regression
   - Deep learning models (DKT, DKVMN, SAKT): RNN, memory networks, transformers

3. **Side Information Across Learning (Variants IV.D)**
   - Response time, opportunity count, tutor intervention, engagement metrics recorded
   - "Substantial amount of supplementary information...provides more comprehensive reflection of learning process"
   - Models that utilize side information: AKT, GKT variants
   - Side information types: temporal patterns, attempt counts, hint requests, problem difficulty

4. **Individualization Before Learning (Variants IV.A)**
   - Different students exhibit different learning rates and prior knowledge
   - DKT-DSC: dynamic student classification via K-means clustering
   - FGKT: individual exercise representation + individual prior knowledge assessmen
   - CKT: implicit measurement of individualized learning rates and prior knowledge

5. **Incorporating Engagement During Learning (Variants IV.B)**
   - Attention mechanisms model which past interactions influence current knowledge state
   - SAINT: encoder-decoder transformer architecture with dual attention
   - Models track interaction sequences over time with attention to relevant history

6. **Considering Forgetting After Learning (Variants IV.C)**
   - Students forget knowledge over time, especially without practice
   - DKT-Forget integrates exponential decay with RNN
   - Temporal gap between interactions affects retention

7. **Task-Type and Exercise-Level Modeling**
   - Each exercise has specific difficulty and discrimination parameters
   - Exercise factors (difficulty, discrimination) enhance DKT performance
   - Exercise-level representation critical for knowledge state assessmen
   - FGKT obtains individual exercise representation through knowledge cells and exercise distinctions

---

## Design Implications

1. **Interaction evidence collection**: Side information (response time, hints, attempts) provides richer evidence than correctness alone
2. **Learner state modeling at scale**: Deep learning enables tracking millions of knowledge states with adaptive assessment remaining tractable
3. **Task-specific modeling feasible**: Exercise difficulty, discrimination, and type can be explicitly modeled
4. **Temporal dynamics matter**: Forgetting curves, time gaps, and opportunity counts affect knowledge state evolution
5. **Source-grounding strategy**: KT models trained on specific course/domain data (ASSISTments, EdNet datasets)
6. **Evidence-based pedagogical action**: Knowledge state estimates used for personalized resource recommendation and adaptive learning path generation

---

## Limitations and Non-Inferences

1. **Learning effectiveness**: Survey describes KT models' predictive accuracy, not direct learning outcome improvements from KT-guided interventions
2. **Pedagogical action specification**: Models predict knowledge states; how to act on predictions is application layer (Section V)
3. **Generalization across domains**: Most KT datasets domain-specific (math tutoring systems); cross-domain transfer not demonstrated
4. **Real-time constraints**: Computational complexity varies; transformer models may be too slow for instant feedback
5. **Cold-start problem**: New students with no history require different approaches (mentioned but not solved)
6. **Explainability tradeoff**: Deep learning models more accurate but less interpretable than Bayesian/logistic models

---

## Affected Decisions

- learner_model_applicability: Demonstrates scalable knowledge state modeling with interaction sequences
- evidence_collection: Side information (time, hints, attempts) provides critical learning signals
- task_type_specific_modeling: Exercise-level features (difficulty, discrimination) improve model performance
- source_grounding_strategy: KT models require domain-specific training data for specific courses
- pedagogical_action_selection: Knowledge states enable adaptive resource recommendation (Applications Section V)

---

## Research Questions Addressed

- **RQ5.1** (learner state modeling): Comprehensive coverage of knowledge state representation methods
- **RQ5.2** (task-type-specific modeling): Exercise-level features and difficulty parameters explicitly modeled
- **RQ4.1** (interaction evidence): Side information (response time, hints, engagement) utilized for richer modeling

---

## Verification Status

**Status**: verified
**Publication**: arXiv v4 April 2024; IEEE Transactions on Learning Technologies journal version noted
**Retrieval**: Full PDF downloaded via curl from arxiv.org/pdf/2105.15106.pdf (7.5 MB), extracted to text via pdftotext (3,113 lines)
**Content verification**: Read abstract, introduction, problem definition, fundamental models, variants sections. Located specific subsections on side information (IV.D), individualization (IV.A), engagement (IV.B), forgetting (IV.C), task-type features throughou
