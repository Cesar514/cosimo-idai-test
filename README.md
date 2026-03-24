# AI Course for Research, Science, Engineering, and Education

This repository is being reorganized into a multi-chapter course on practical AI and agentic systems for research, science, engineering, and education.

The current robotics material has been moved into `chapters/chapter10/casestudy_robotics/` as the opening case study. The rest of the repository will evolve around the course structure below.

## Part I. Foundations

### Chapter 1. What AI is good at, what agents are good at
Goal: separate plain prompting, workflow automation, and true agents.

Core lesson:

- LLM as reasoner/writer
- tool-using assistant
- single-agent loop
- multi-agent system
- human-in-the-loop system

End product:

- one diagram showing increasing capability and increasing failure modes

### Chapter 2. Prompting that survives contact with reality
Goal: teach prompt design as engineering, not magic.

Based on current OpenAI and Anthropic guidance:

- define the task
- define success criteria
- define exact output contract
- define ambiguity behavior
- define what `done` means
- define citation rules
- define verification step

End product:

- a reusable prompt template for research, education, and engineering

### Chapter 3. Context engineering
Goal: teach that agent quality depends on what is in context, not only how prompts are worded.

Cover:

- system instructions
- workspace/project context
- files and references
- tool results
- memory/history
- retrieval vs overload
- compaction/summarization
- loss of grounding in long sessions

End product:

- a `context budget` worksheet

## Part II. Core agent workflows

### Chapter 4. Tools, actions, and safe boundaries
Goal: show that tools are part of the prompt contract.

Cover:

- search tools
- file tools
- code tools
- spreadsheets
- calendar/email
- destructive vs non-destructive tools
- tool descriptions and schemas
- when not to let an agent act automatically

End product:

- a table for tool design: purpose, inputs, outputs, failure modes, guardrails

### Chapter 5. Single-agent systems first
Goal: build the first serious agent the right way.

OpenAI explicitly recommends starting with strong foundations and simple orchestration before moving to multi-agent patterns.

Cover:

- while-loop agent pattern
- plan -> act -> observe -> verify -> stop
- retry logic
- exit conditions
- when a single agent is enough

End product:

- one generic single-agent architecture for research tasks

### Chapter 6. Multi-agent systems without nonsense
Goal: show when decomposition helps and when it only adds latency and errors.

Use OpenAI’s two common patterns:

- manager agent calling specialists as tools
- peer agents handing off to each other

Suggested specialist set:

- planner
- retriever
- critic/verifier
- coder
- report writer
- experiment designer

End product:

- one architecture comparison table: single-agent vs manager-agent vs peer handoff

## Part III. Domain application chapters

### Chapter 7. AI for research
Goal: literature review, synthesis, citation discipline, gap finding.

Use the official research framing:

- web search for recency
- deep research for multi-step synthesis
- citations mandatory
- source comparison
- empty-result recovery
- claim verification before conclusion

Mini-projects:

- literature review
- benchmark matrix
- identify gaps in a field
- create a reproducibility checklist

### Chapter 8. AI for education
Goal: use agents to teach, not only answer.

Cover:

- explanation ladder: beginner -> intermediate -> expert
- Socratic tutor agent
- quiz generator with verifier
- misconception detector
- lesson planner from papers, slides, or notes

Important point:

- evaluation here is learning outcome, not just fluent text

Mini-projects:

- build a tutor for one engineering topic
- convert a paper into a teachable lesson
- create adaptive exercises

### Chapter 9. AI for engineering
Goal: practical workflows for coding, design, debugging, experiments, documentation.

OpenAI’s current guidance is strong on coding/terminal agents with explicit tool boundaries, structured contracts, and verification loops.

Mini-projects:

- design review agent
- code generation + test agent
- debugging agent
- experiment planner
- requirements-to-spec agent

## Part IV. Hard problems and case studies

### Chapter 10. Robotics case study: solving challenging problems with agentic systems

This chapter is the worked case study for the current robotics paper and supporting artifacts.
It captures a difficult, real-world system that requires careful orchestration, strong evaluation, and clear failure handling.

## License

This project is licensed under the MIT License.

Copyright (c) 2026 Cesar Contreras

For the full license text, see the `LICENSE` file.

## Author

Cesar Contreras

- Website: [cesar514.com](https://cesar514.com)
- Email: `cac214@student.bham.ac.uk`

## Repository Layout

- `chapters/chapter10/casestudy_robotics/`: robotics case study and paper artifacts
- `chapters/chapter10/`: robotics case study chapter
- `paper/` and `robotics_maze/`: compatibility links to the Chapter 10 case study
- `chapters/`: chapter drafts and supporting content
- `docs/`: generated documentation and reference material
- `presentation_assets/`: slides, visuals, and source references

## Next Step

The next implementation step is to turn each chapter into a draft with examples, diagrams, and reusable exercises.
