<!-- Director -> specialist brief, <= 300 words. Pass paths, not content. -->
BRIEF <id> to <agent-id>  (phase <n>, approved by user on <date>)
goal: <one sentence>
inputs: [paths]          reuse: [existing findings / shared tables to use]
outputs: [paths]         must not touch: [paths outside ownership]
method notes: <constraints, thresholds, exclusions>
budget: max turns <n>; compute <limit>; credits: none | <approved amount>
stop when: <condition>; return a handoff per knowledge/_system/templates/handoff.md
