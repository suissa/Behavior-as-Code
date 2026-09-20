# Canonical Behavior Skills

These skills define how an Agent/LLM should identify the 12 canonical CRM BehaviorStates used by BehaviorID.

Canonical set: `CUR`, `ENG`, `HES`, `COM`, `RES`, `ACE`, `VAL`, `ABO`, `NEG`, `AAN`, `INP`, `DES`.

Rules:
- states are situational, not personality labels;
- observation and inference stay separate;
- text, prosody, events and temporal context are evidence modalities;
- prosody is normalized per user;
- every inference carries confidence, supporting evidence and contradicting evidence;
- the same transition cost matrix MUST NOT be assumed universal across geographies, locales, domains or cultures;
- BehaviorID remains the transition triple `[b_(t-1)]-[tau_t]-[b_t]`.

Each file below is an atomic skill for one canonical state.