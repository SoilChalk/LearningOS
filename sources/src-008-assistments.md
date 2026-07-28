# Source 008: ASSISTments - Assessment + Instruction

**Title**: ASSISTments: Tutoring as You Test  
**Key References**: Koedinger, Heffernan, Junker (multiple papers)  
**Organization**: Carnegie Mellon University / Worcester Polytechnic Institute  
**Source Type**: research_literature + product_system  
**Accessed**: 2026-07-29  
**Language**: English  

---

## Core Capabilities (Directly Supported)

1. **Assessment + instruction integration**  
   - "Online benchmark testing system that tutors as it tests"
   - "Provides instructional assistance during the test"
   - Avoids lost instruction time during assessment

2. **Rapid development framework**  
   - Assistment Builder: system for rapid development, test, and deployment of "pseudo-tutors"
   - Simple cognitive model based on state graph tailored to specific problem
   - Web-based interface allows users with little ITS experience to develop content
   - Novice users can develop tutor for a problem in under 30 minutes

3. **Student modeling during assessment**  
   - "Emphasized using intelligent tutoring system as assessment system"
   - Student modeling informs predictions of state exam performance
   - AI "learns" student abilities to provide increasingly accurate predictions

4. **Prediction capability**  
   - "Artificial intelligence program designed to support math learning"
   - "Provided increasingly accurate predictions of how [students] would do on a standardized mathematics test"
   - IES study: "Using Web-Based Cognitive Assessment Systems for Predicting Student Performance on State Exams"

---

## Design Implications

1. **Assessment and instruction can be combined**: Not separate phases - tutoring happens during testing

2. **Simplified ITS development is possible**: "Pseudo-tutors" with state graphs instead of full production rule systems

3. **Teacher content creation is feasible**: 30-minute development time enables teacher-created content

4. **Formative + summative assessment merge**: System serves both instructional scaffolding and knowledge measurement

5. **Prediction as feature**: Ability to forecast standardized test performance has practical value

---

## Limitations and Non-Inferences

1. **"Pseudo-tutor" vs. full Cognitive Tutor**: Simplified model - tradeoff between development cost and sophistication

2. **State graph limitations**: Simpler than production rule systems - may not capture all problem-solving strategies

3. **Effectiveness evidence not in snippets**: "Designed to support math learning" but learning gains not quantified here

4. **Prediction accuracy not specified**: "Increasingly accurate" but actual prediction metrics not provided

5. **Scale of deployment unclear**: IES study mentioned but student/school count not in snippets

6. **Full papers not accessed**: CMU/WPI publications cited but not fully retrieved

---

## Affected Decisions

- assessment_instruction_integration: combine testing with tutoring to avoid lost time
- content_creation_efficiency: rapid development tools enable teacher authorship
- learner_modeling: student model built during assessment for prediction
- pedagogical_simplification: state-graph pseudo-tutors vs. full cognitive tutors
- prediction_as_feature: forecasting standardized test performance

---

## Verification Status

**Status**: partially_verified (search results from CMU/WPI publications + IES study reference)  
**Key researchers**: Koedinger (CMU), Heffernan (WPI), Junker  
**Funding**: IES study on prediction of state exam performance  
**Product status**: Web-based system, deployment timeline unclear from snippets  
**Limitation**: Full papers not accessed - relying on abstracts and snippets  
