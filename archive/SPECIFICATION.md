# SPECIFICATION.md
## A Manifesto for Cognitive Load Distribution in AI-Assisted Software Development

> *"The specification artifacts are the shared memory between two cognitive profiles.
> They encode your intent in a form the AI can check against, and they encode the AI's
> implementation decisions in a form you can audit without reading every line of code."*

---

## Preamble

This document is a living methodology manifesto. It exists because a specific and repeatable
problem has emerged at the intersection of human creative vision and AI-assisted implementation:
the gap between *what you intend to build* and *what the AI produces* grows non-linearly as
project scope expands, and no existing methodology in the software engineering canon was
designed with this particular cognitive partnership in mind.

TDD, BDD, DDD, C4 — these are all frameworks built for human-to-human engineering teams,
optimized for correctness, maintainability, and architectural coherence. They are genuinely
useful, and this methodology borrows from all of them. But they share a foundational assumption
this methodology does not: that the entities collaborating on a system share persistent memory,
accumulated context, and evolving mutual understanding over time.

The AI does not. Every session begins from zero. Every context window is finite. Every
handoff between sessions is a lossy compression of everything that came before.

This manifesto describes a methodology — called **Cognitive Load Distribution System (CLDS)**
— designed specifically for that reality. Its central thesis is simple:

**The specification artifacts are not documentation. They are infrastructure.**

They are the mechanism by which your architectural authority, design intent, and accumulated
domain understanding survive the context boundary. Without them, every AI session begins
not where the last one ended, but at a shallow reconstruction of it. With them, the AI
operates as a capable, well-briefed collaborator rather than an amnesiac contractor who
has to be re-onboarded every morning.

**A note on scope and era-contingency.** CLDS is not a permanent methodology claiming
timeless validity. It is the currently optimal response to a specific technological
constraint: AI systems that possess high implementation capability but no persistent
design memory. As that constraint relaxes — as AI systems develop longer-term project
awareness — the specific artifact prescriptions of CLDS will change. The underlying
principles (intent should be explicit, architectural authority should be preserved,
deviations should be surfaced) may survive in some form. The methodology should be
read with this contingency in mind.

**A note on domain.** Although CLDS was discovered in a software development context,
its actual subject is not software. It is the problem of *how intent survives across
cognition boundaries* — wherever one actor holds vision and another holds execution
capability, and shared artifacts must preserve the bridge between them. Software is
the first environment in which the pattern became acute enough to force a systematic
response. It will not be the last.

---

## Part I: The Two Regimes of AI-Assisted Development

### 1.1 Terminal-Goal Software

Some software problems are **externally constrained**. The specification is imposed by
the world rather than invented by the developer. A CLI tool that reverse-engineers an
encrypted API, a data pipeline that must conform to a third-party schema, a scraper that
must match what a CDN actually serves — these are *terminal-goal* problems. They have:

- A single correct order of operations
- A binary success criterion (it works or it doesn't)
- Immediate, tight feedback loops (the output is either valid or visibly broken)
- No meaningful architectural decisions beyond pipeline ordering

In this regime, AI-assisted development is extraordinarily effective because the AI is
performing *vocabulary-bridged composition*: assembling known solutions to known sub-problems
in a fixed sequence. The human's primary contribution is *intent* — knowing what the
pipeline needs to accomplish. The implementation detail is genuinely delegatable.

**In terminal-goal software, vibecoding is often appropriate.** The specification is
the world itself; the feedback loop is tight; the debt surface is bounded.

### 1.2 Open-Ended Creative Tooling

Other software problems are **internally generated**. Every feature, every data model,
every aesthetic decision emerges from the developer's evolving creative vision. A webtoon
editor, a game engine, a content creation workstation — these are *open-ended* problems.
They have:

- Features that generate architecture (each new use case adds structural commitments)
- Success criteria that are subjective, evolving, and only partially knowable in advance
- Feedback loops that are loose (a wrong architectural decision may not reveal itself for weeks)
- Meaningful architectural decisions at every layer

In this regime, AI-assisted development without a CLDS degrades rapidly. The AI implements
locally correct solutions to locally presented problems, without a global invariant to
check against. Each session's output is individually coherent; the aggregate accumulates
structural debt.

**In open-ended creative tooling, vibecoding without CLDS produces a system that works
until it doesn't, and then is very difficult to fix.**

### 1.3 The Asymmetry That Defines CLDS

The AI has:
- Unlimited working memory for syntax and API surface
- Comprehensive knowledge of implementation patterns
- Zero persistent memory for design intent
- No awareness of the *why* behind structural decisions

You have:
- Clear creative vision and domain understanding
- Finite working memory for implementation detail across large systems
- The ability to recognize correct vs. incorrect architectural reasoning
- The judgment to reject outputs that violate unstated invariants

**CLDS is the methodology for distributing cognitive labor across this asymmetry.**

You hold the intent. The AI holds the syntax. The specification artifacts hold the
bridge between them — encoded in forms that both parties can read, reason about,
and check against.

**The bottleneck has inverted.** In traditional software development, the constraint
was typing speed — human thinks fast, types slowly. In CLDS, the constraint is reading
speed — the AI writes hundreds of lines of code faster than you can read the documentation
it produces. Every workflow decision in CLDS is ultimately a decision about minimizing
your reading cost while maximizing the architectural authority you exercise. This inversion
is not incidental. It shapes every layer of the methodology.

---

## Part II: The Development Lifecycle

### 2.1 Dominant Modes, Not Strict Phases

CLDS describes a development lifecycle in terms of **dominant modes** rather than strict
sequential phases. At any point in a project, you are predominantly in one of two modes:

**Exploration Mode** — specification is emergent, iteration is fast, debt is consciously
accepted as the price of learning. The goal is domain understanding, not architectural
correctness. Vibecoding is appropriate. CLDS tooling is deliberately light.

**Design Mode** — specification is authoritative, iteration is disciplined, debt is
actively managed. The goal is architectural integrity, not speed of discovery. Full
CLDS tooling is engaged.

Real projects cycle between these modes. A new subsystem may warrant a return to
exploration mode even within an otherwise designed system. A feature whose domain
turns out to be more complex than anticipated may require a local return to exploration
before design can proceed. This cycling is healthy, not a methodology failure.

The lifecycle described below is the idealized arc of a project's dominant mode.
It describes the *vector* — the general direction of travel — not a rigid sequence
of discrete events.

### 2.2 The Seven Phases

```
Phase 1: CRYSTALLIZATION
  General idea → domain vocabulary → core use case hypothesis
  Mode: Exploration

Phase 2: SHELL
  Vibecode a minimal, functional skeleton → establish basic data flow
  Mode: Exploration

Phase 3: UI PROTOTYPE
  Interface without functionality → force reasoning about user mental model
  before committing to system data model
  Mode: Exploration

Phase 4: MINIMAL FUNCTIONALITY TEST
  Add just enough real behavior to test the actual use case →
  specification crystallizes from collision with reality
  Mode: Exploration → transition beginning

Phase 5: EXPLORATORY ITERATION
  Iterate until bugs, scope pressure, or structural debt signals the
  inflection point → document everything that works
  Mode: Exploration → inflection point

Phase 6: FULL REFACTOR (The Mode Transition)
  CLDS tooling engaged fully → design the system that should exist
  given everything learned → implement only verified working features
  Mode: Design

Phase 7: DISCIPLINED EVOLUTION
  Every new feature passes through the specification loop before
  implementation → the architecture grows with intention
  Mode: Design (with local exploration cycles permitted)
```

### 2.3 The Inflection Point

Recognizing the inflection point — the moment when the exploratory prototype has
accumulated enough real behavior to be *understood* but enough structural debt to be
*untrustworthy* — is one of the most valuable skills in AI-assisted development.

The signals:

- A bug fix in one component breaks something semantically unrelated
- Adding a new feature requires modifying more than three existing files
- You can no longer explain the data flow through the system without consulting the code
- The AI begins generating solutions that conflict with decisions made in earlier sessions
- The README (or its absence) no longer accurately describes what the system actually does

When these signals appear, the correct response is not another iteration. It is the
Full Refactor.

### 2.4 What the Full Refactor Is Not

The Full Refactor is not a rewrite motivated by aesthetic preference. It is not an
opportunity to adopt a new framework or technology stack out of curiosity. It is not
a punishment for having vibecoded the exploratory prototype.

The Full Refactor is a **deliberate mode transition** from exploration to design. It
uses everything learned in the exploratory phase — including the wrong turns — as input
to a specification-first design process.

The exploratory prototype is not wasted. It is the most important input to the specification.

---

## Part III: The CLDS Toolstack

CLDS uses three categories of specification artifact, operating at distinct abstraction
levels. They are not interchangeable. Each one captures something the others cannot.

Critically: the specific tools named here are **implementations of underlying principles**,
not the principles themselves. A README can serve as an architectural model. YAML
acceptance criteria can serve as behavioral contracts. The principle is always more
important than the format. Choose the lightest format that preserves the principle at
your project's scale.

### 3.1 The Architectural Model — Structural Authority

Every project needs a **persistent structural model**: an explicit, maintained artifact
that describes what the system is and how its parts relate. This model serves as the
**rejection filter** — the authority against which proposed changes can be evaluated
without requiring the full architectural context to be reconstructed from code.

The rejection filter function: when the AI proposes adding a new component, hook,
store, or endpoint, the architectural model provides the authority to evaluate that
proposal. Where does this live? What are its declared relationships? Does adding it
violate any structural invariant we have defined?

**Format options, from lightest to most formal:**

- **README-as-architecture**: for a solo developer on a single-container application,
  a well-maintained README with explicit domain entity descriptions, data flow narrative,
  and component responsibilities often provides a sufficient structural model. This is
  the minimum viable architectural artifact and is appropriate for projects of moderate
  complexity.

- **C4 Model**: for systems with multiple containers, external integrations, or team
  members, the C4 hierarchy (Context → Container → Component → Code) provides structured
  zoom levels that README prose cannot. Use C4 when the system's structural complexity
  exceeds what a single readable document can represent without losing important detail.

The choice between them is a scale decision, not a quality decision. A README that
is actually maintained is more valuable than a C4 diagram that has drifted from reality.

**CLDS-specific practices for the architectural model:**

- Load it into context at the start of every session that touches structure
- The C4 audit (or README audit) — mapping what actually exists against what is documented
  — is the first step of every Full Refactor
- When implementation reveals the model was wrong, update the model deliberately and
  annotate the reason; do not silently drift
- When the AI proposes a structural change, it must be ratified before implementation,
  then reflected in the model after

### 3.2 YAML Specification Files — The Contract Surface

YAML specification files are the **single source of truth** for what the system is
supposed to do at the domain entity level. They are more durable than code comments,
more precise than README prose, and more machine-readable than architectural diagrams.

Their structural advantage: YAML enforces completeness. A well-designed specification
schema forces you to define inputs, outputs, dependencies, constraints, and acceptance
criteria as parallel fields. You cannot accidentally omit the acceptance criteria because
the field is present and waiting.

The **constitutional document function**: YAML specs function as constitutional law for
the system. The AI can propose amendments; you ratify them; the spec governs what counts
as a valid implementation. This is the mechanism by which your architectural authority
is preserved across session boundaries.

**Recommended schema for a feature specification:**

```yaml
feature:
  id: FEAT-001
  name: ""
  status: draft | specified | implemented | verified | deprecated
  domain_entity: ""           # Which core entity does this feature touch?

  intent: ""                  # Why does this feature exist? One sentence.
  user_story: ""              # As a [user], I want [goal], so that [value].

  inputs: []                  # What data or events trigger this feature?
  outputs: []                 # What does it produce or mutate?

  dependencies:               # What must exist for this feature to function?
    features: []
    components: []
    external: []

  invariants: []              # What must always be true, regardless of implementation?
                              # See Section 3.4 for invariant graduation criteria.

  acceptance_criteria: []     # Observable conditions that define success.

  implementation_notes: ""    # Constraints, chosen approaches, rejected alternatives.

  architectural_location:     # Where does this live in the structural model?
    container: ""
    component: ""

  refactor_history: []        # Log of significant changes with rationale.
                              # Not optional. Undocumented refactors are invisible debt.
```

**CLDS-specific YAML practices:**

- Every domain entity gets its own specification before implementation begins
- `invariants` are the highest-priority field — they define what must survive any future refactor
- `refactor_history` is not optional; undocumented refactors are invisible debt
- The AI reads the YAML before implementing; you read it before accepting output
- When implementation reveals a mismatch with the spec, resolve at the specification
  level first, then propagate to code — never the reverse

### 3.3 Behavioral Contracts — The Oracle

Behavioral contracts specify the **observable behavior** of the system from the outside,
without reference to implementation. They serve three functions:

**1. Intent clarity**: forces reasoning about the system from the user's perspective.
What precondition makes this behavior meaningful? What action triggers it? What observable
outcome defines success? These are questions with architectural answers.

**2. Regression anchor**: when a feature is refactored, its behavioral contracts define
exactly what observable behaviors must be preserved. This is the primary safeguard against
refactors that improve structure while silently breaking behavior.

**3. Session handoff vehicle**: behavioral contracts are the most efficient way to
communicate expectations to an AI in a new session. "Here are the contracts this
component must satisfy" is more precise and more compact than prose description.

**Format options:**

- **YAML acceptance criteria** (inline in the feature spec): for simple features with
  linear behavior, a flat list of observable conditions in the `acceptance_criteria`
  field is sufficient. This is the minimum viable behavioral contract.

- **Gherkin scenarios**: for complex workflows, multi-step state transitions, or user
  journeys where the sequential Given/When/Then narrative structure genuinely aids
  clarity. Gherkin earns its overhead when behavior is temporal and branching; it is
  overhead when behavior is simple and stateless.

The `@invariant` concept is format-agnostic and should be preserved regardless of
which format is used. Some behavioral properties are non-negotiable across all future
refactors. These must be explicitly marked — whether as `invariants:` fields in YAML
or `@invariant`-tagged Gherkin scenarios. A refactor that breaks a marked invariant
is by definition wrong, regardless of any other improvement it achieves.

### 3.4 Invariant Graduation Criteria

Not every behavioral property deserves to be an invariant. An invariant that is wrong
is worse than no invariant — it encodes false confidence and will eventually cause the
AI to faithfully implement the wrong thing. The question of how a candidate property
graduates to invariant status is the methodology's most important open epistemological
question.

Current best-practice criteria, applicable at different specification levels:

- **Repeated survival**: the property has held true across multiple independent refactors
  without being intentionally violated. Time and change are the strongest validators.

- **Domain necessity**: removing the property would make the system unable to serve its
  core purpose. If the invariant were false, the system would not be the system.

- **User validation**: the property corresponds to observable behavior that users have
  confirmed they depend on. External validation is stronger than internal reasoning.

- **Architectural derivation**: the property follows necessarily from a higher-order
  invariant that is already established. Derived invariants inherit the authority of
  their parents.

These criteria are not equivalent. Domain necessity applies most strongly at the entity
level. User validation applies most strongly at the behavioral contract level.
Architectural derivation applies most strongly at the structural level. Repeated survival
is the universal fallback when other criteria are uncertain.

**The open question**: a complete theory of invariant validation — a principled epistemology
for how claims graduate from ideas to non-negotiable contracts — remains the most important
unresolved extension of CLDS. The criteria above are practical heuristics, not a theory.

---

## Part IV: The Specification Loop

The specification loop is the inner cycle that governs every significant feature addition
or refactor in Design Mode. It replaces the vibecode-and-iterate cycle with a deliberate
sequence that maintains architectural integrity.

### 4.1 The Loop

```
1. DOMAIN CRYSTALLIZATION
   Name the irreducible entities and their relationships.
   If you cannot name them, you are not ready to specify.

2. ARCHITECTURAL PLACEMENT
   Where does this feature live in the structural model?
   If it doesn't fit, the model needs updating — deliberately.

3. YAML SPECIFICATION
   Write the spec before implementation.
   Focus on invariants and acceptance criteria.
   Leave implementation_notes blank until you have something to say.

4. BEHAVIORAL CONTRACTS
   Write the observable oracle.
   Mark invariant contracts explicitly.
   Happy path first; edge cases after domain is stable.
   Use YAML acceptance criteria for simple features;
   Gherkin for complex multi-step workflows.

5. AI-ASSISTED IMPLEMENTATION (via REP — see Part V)
   Share: architectural model + relevant YAML specs + behavioral contracts.
   Instruct: implement to spec, flag any mismatch with reasoning.
   Constraint: propose architectural changes; do not make them unilaterally.

6. SPECIFICATION RECONCILIATION
   Review implementation against spec.
   If implementation reveals spec was wrong: update spec first, then code.
   If implementation drifts from spec without reason: revert and clarify.
   Log all significant decisions in refactor_history.
   Distinguish drift from evolution — see Section 4.2.

7. ARCHITECTURAL MODEL UPDATE
   If the implementation changed the structure, update the model.
   Never let the architectural model drift silently from reality.
```

### 4.2 Drift vs. Evolution

CLDS treats deviation from specification with discipline, but not with blanket suspicion.
Some deviations are mistakes. Others are discoveries — the implementation has revealed
something true about the domain that the specification did not yet know.

The distinction is not in the deviation itself but in its **deliberateness**:

- **Drift**: a change that moves away from specification without awareness. The spec says
  one thing; the code does another; nobody noticed. Drift is harmful because it is
  invisible — it breaks the invariant that the specification describes what the code does,
  silently and cumulatively.

- **Evolution**: a change that moves toward a better understanding of the domain, made
  with awareness and recorded. The implementation revealed that the spec's approach was
  suboptimal; the deviation was surfaced, reasoned about, ratified, and logged in
  `refactor_history`. Evolution is healthy — it is how specifications improve through
  contact with reality.

CLDS is not hostile to emergent architecture. Unix pipes, React hooks, event sourcing
patterns — these crystallized through repeated practical use, not prior specification.
CLDS is hostile specifically to *invisible* emergence. The discipline is making emergence
explicit and deliberate, not preventing it.

The mechanism that separates drift from evolution is the Reconciliation Principle:
when implementation deviates from spec, the deviation is surfaced, decided upon, and
logged. A discovered architectural improvement that goes through this process is
evolution. The same change made silently is drift. The difference is the deliberateness
of the decision, not the content of the change.

### 4.3 The Reconciliation Principle

Specification mismatch is not a failure — it is information. Implementations routinely
reveal that the specification was underspecified, contradictory, or based on incorrect
assumptions about the domain. This is expected and healthy.

The discipline is in *where the resolution happens*. The invariant:

**Specification changes flow downward into code. Code behavior never silently redefines
specification.**

When the AI proposes a deviation from the spec, it must:
- State the deviation explicitly
- Provide reasoning for why the spec's approach is suboptimal
- Propose specific spec language to replace the current spec

You then decide: accept the amendment and update the spec, or reject it and restate the
constraint. The AI implements whatever the ratified spec says.

This is not bureaucratic overhead. This is the mechanism by which you remain the
architectural authority rather than becoming a code reviewer for an AI that has quietly
accumulated design authority through incremental drift.

---

## Part V: The Ratified Execution Protocol (REP)

The Specification Loop describes *what* to specify and *how* to maintain it. The
Ratified Execution Protocol describes the *operational turn sequence* by which a
ratified specification becomes working code.

REP was discovered empirically — not designed from first principles. An AI agent
constrained to read-only mode could not write an implementation plan directly; it
instead produced a *minimal* plan to the CLI for human review. The constraint
accidentally instantiated the most important CLDS principle at the execution level:
the AI proposes, you ratify, before a single line of code is written. The protocol
that emerged from that accident is now the recommended execution layer for all
sufficiently significant implementation work.

The calibration principle governing every REP step: **minimize human reading cost
while maximizing architectural authority exercised.**

### 5.1 The Seven Steps

```
STEP 1 — MINIMAL PLAN REQUEST (Proposal-Only Mode)
  Instruct the AI to produce a minimal implementation plan:
  phases named, major operations listed, no implementation detail.
  Output fits on one screen. Readable in under two minutes.
  The AI cannot execute. It can only propose.

  This is the ratification surface — not a draft of the full plan,
  but the skeleton you annotate architecturally.

STEP 2 — RATIFICATION WITH ARCHITECTURAL ANNOTATIONS
  Read the minimal plan. Annotate directly:
  - Dependency order corrections
  - Scope exclusions
  - Behavioral preservation requirements
  - Approach rejections with alternatives
  These are architectural annotations, not editorial ones.
  They change what will be built, not how it will be described.

STEP 3 — FULL PLAN ELABORATION (Write Mode Enabled)
  The AI writes the full PLAN.md incorporating your annotations.
  This document now carries your ratification before implementation begins.
  It divides work into distinct phases with:
  - Explicit scope per phase
  - Success criteria per phase
  - Dependency order respected
  - No phase leaving the system in an invalid intermediate state

STEP 4 — FINAL APPROVAL
  One pass. Verify annotations were correctly incorporated.
  Check for new architectural assumptions introduced during elaboration.
  This is fast because you already ratified the structure.
  You are scanning for drift between minimal and full, not re-evaluating.

STEP 5 — PHASED EXECUTION
  For heavy implementations: execute phases sequentially, one at a time.
  For lighter scopes: execute all phases in sequence ("let it rip").
  Phase boundaries exist regardless — they are the unit of analysis
  for behavioral testing and problem localization, not just checkpoints.

STEP 6 — LOCAL BEHAVIORAL ANNOTATION PER PHASE
  After each phase (or after the full run for lighter scopes):
  test working features, note behavioral deviations.
  "This doesn't do X." / "This should look like Y."
  These are behavioral annotations — correcting implementation against
  spec — not re-opening architectural decisions.
  They are local: they address the phase that just ran, not the whole system.

STEP 6.5 — PLAN-IMPLEMENTATION ALIGNMENT AUDIT
  A CA — ideally a fresh context, not the one that wrote the implementation
  — is given PLAN.md and the implementation and asked one specific question:
  "Where does the implementation deviate from or fail to cover the plan?"
  The output is a deviation report, not a general quality review.
  Targeted, not open-ended.

  This step is the executable equivalent of Specification Reconciliation
  applied to the plan itself rather than the spec. PLAN.md is treated as
  a behavioral contract: the implementation must account for every scenario
  and fixture it declared. Coverage gaps surfaced here are either resolved
  before Step 7 or explicitly logged as deferred in DECISIONS.md.

  Calibration: do not conflate this with Step 6 (behavioral annotation).
  Step 6 corrects implementation against observable behavior.
  Step 6.5 corrects implementation against declared strategy.
  They are different authorities: spec vs. plan.

STEP 7 — FINAL IRON-OUT
  "Run ESLint and do a final lookaround for kinks."
  Single sentence. The AI performs pattern recognition on its own
  recently-written code: dead imports, unused variables, inconsistent
  naming, edge cases the happy-path testing did not surface.
  This is implementation hygiene, not architectural review.
```

### 5.2 Why Phase Boundaries Matter Even When You "Let It Rip"

When running all phases in a single execution, phase boundaries might appear to be
cosmetic — just headings in a document. They are not. They do two things regardless
of whether you pause between them:

**Scope discipline during planning.** Writing Phase 1 as a distinct unit forces the AI
to reason about what is complete at the end of Phase 1 independently of Phase 2. This
prevents implicit cross-phase dependencies that would make mid-run failure unrecoverable.
Each phase leaves the system in a valid state.

**The vocabulary for behavioral localization.** When testing after a full run reveals
something is wrong, "Phase 3 broke the border rendering" is a dramatically more useful
diagnostic than "something broke." Phase structure gives you a bounded implementation
unit to reason about.

The phases are not execution checkpoints that require your presence. They are the
structural unit of the entire protocol, including the lightweight path.

### 5.3 The Reading Cost Calibration

Every REP step is calibrated to a specific reading cost that is proportionate to the
authority being exercised:

| Step | Reading Cost | Authority Exercised |
|------|-------------|---------------------|
| Minimal plan review | ~2 minutes | Architectural ratification |
| Annotation | ~5 minutes | Structural decisions |
| Full plan review | ~5 minutes | Drift check, not re-evaluation |
| Phase behavioral testing | Variable | Behavioral contract verification |
| Plan-implementation alignment audit | ~5 minutes | Coverage gap detection |
| Final iron-out review | ~2 minutes | Implementation hygiene |

The total human reading investment for a week-equivalent implementation sprint is
measured in minutes, not hours. This is the payoff of ratifying the structure before
execution begins: the implementation phase requires behavioral verification, not
architectural re-adjudication.

---

## Part VI: Session Management

### 6.1 The Context Window as a First-Class Constraint

Every AI session has a finite context window. In long projects, the entire specification
corpus will not fit in a single session. This is a design constraint to architect for,
not a limitation to work around.

CLDS responds with **layered context loading**: load the minimum specification context
necessary to accomplish the session's goal, plus enough architectural context to prevent
local decisions from violating global invariants.

**Standard session opening protocol:**

```
1. Load architectural model (always — it is the structural authority)
2. Load YAML specs for components being touched in this session
3. Load behavioral contracts for features being implemented or modified
4. State the session goal explicitly: "In this session we are implementing FEAT-003"
5. State what is out of scope: "We are not touching the state management layer today"
```

The out-of-scope declaration is as important as the in-scope declaration. It prevents
the AI from making locally tempting improvements that violate session discipline.

### 6.2 The Session Closing Protocol

At the end of every productive session, before closing the context:

```
1. Update any YAML spec that changed during the session
2. Update architectural model if structure changed
3. Add any new behavioral contracts that emerged from implementation
4. Note unresolved decisions in DECISIONS.md for the next session
5. Summarize what was accomplished in a form the next session can read in 30 seconds
```

The session closing protocol is the investment that makes the next session cheaper.
Its absence is the primary source of context reconstruction debt — the tax paid at
the start of every session to re-establish what the previous session already knew.

### 6.3 The DECISIONS.md Convention

DECISIONS.md is a flat log of unresolved architectural questions, deferred decisions,
and known technical debt. It is not a task list. It is specifically for decisions that are:

- Too architectural for a code comment
- Too implementation-specific for the YAML spec
- Too unresolved to go in `refactor_history`
- Too important to lose between sessions

Format:

```markdown
## OPEN

### [DATE] — [Decision title]
Context: [What situation produced this decision point?]
Options: [What are the viable approaches?]
Blocking: [What cannot proceed until this is decided?]

## RESOLVED

### [DATE] — [Decision title]
Decision: [What was chosen?]
Rationale: [Why?]
Impact: [What changed in the spec/architecture/implementation?]
```

---

## Part VII: The Refactor Phase in Detail

### 7.1 The Architectural Audit

The Full Refactor begins with an architectural audit: a systematic mapping of what
*actually exists* in the codebase against what was *intended* to exist. This is
performed before any specification is written, because the specification must be
grounded in reality, not aspiration.

The audit produces three lists:
- **Components that exist as intended** — carry forward
- **Components that exist but deviate from intent** — specify the deviation; decide
  whether to align to original intent or ratify the deviation
- **Components that exist without design rationale** — the most dangerous category;
  these are the accumulated decisions of AI sessions that had no architectural
  authority to check against

### 7.2 Domain Model Crystallization

After the architectural audit, before writing a single YAML spec, name the irreducible
domain entities. These are the nouns the system is fundamentally about — entities that
would survive a complete technology stack replacement.

For a webtoon editor: Project, Chapter, Panel, TextGroup, TextBlock.
For a 3D asset pipeline: Asset, Stream, DecryptionKey, MeshBuffer, OutputFile.

The domain entities are the anchor points for everything else. Every YAML spec, every
behavioral contract, every architectural component ultimately traces back to one of
these entities. If a component cannot be expressed in terms of the domain entities,
that is a signal that either the entity list is incomplete or the component is
architectural debt wearing a feature's clothing.

### 7.3 The Feature Inventory

After domain crystallization, inventory every feature in the exploratory prototype:

```
VERIFIED WORKING     — behavior is correct, tested, and intentional
WORKING BUT UNSPECIFIED — behavior exists but rationale is unclear
PARTIALLY WORKING    — happy path works; edge cases are broken
BROKEN               — does not function as intended
SCOPE CREEP          — exists but is not core to the system's purpose
DUPLICATE            — same behavior is implemented in multiple places
```

The Full Refactor carries forward only VERIFIED WORKING features. Everything else is
specified first and then re-implemented — or consciously dropped.

The temptation is to carry forward PARTIALLY WORKING features because most of the
behavior is correct. Resist this. A PARTIALLY WORKING feature implemented without a
spec is a future broken feature with no contract defining what "fixed" means.

### 7.4 Specification-First Implementation

For every feature carried into the refactored system:

1. Write the YAML spec
2. Write the behavioral contracts
3. Confirm architectural placement
4. Execute via REP

This order is not negotiable in the refactor phase. In exploratory iteration (Phases 2–5),
you are learning — specification-first would be premature. In the Full Refactor, you
have learned. The specification is the product of the exploration.

---

## Part VIII: Principles

These are the foundational principles of CLDS. They are listed in order of priority;
when principles conflict, earlier ones take precedence.

### Principle 1: The Specification Is Infrastructure

Specification artifacts are not documentation written after the fact. They are
load-bearing infrastructure that makes the AI's implementation checkable and your
architectural authority persistent. Treat their maintenance with the same seriousness
as the codebase itself.

### Principle 2: Intent Flows Downward

Design intent flows from specification into implementation, never the reverse. When
implementation and specification conflict, the conflict is resolved at the specification
level first, then propagated into code. Code that silently redefines the specification
is the primary vector of architectural drift.

### Principle 3: The AI Proposes; You Ratify

The AI is the implementation engine. You are the architectural authority. The AI may
propose amendments to the specification — this is valuable and expected. You ratify
or reject them. Once ratified, the AI implements to the spec. Settled decisions are
not re-opened without surfacing the re-opening explicitly.

### Principle 4: Deviation Must Be Explicit

When the AI deviates from specification — for any reason, including good ones — the
deviation must be stated, reasoned, and decided upon. Silent deviation, even when
locally correct, is invisible debt because it breaks the invariant that the
specification describes what the code does.

### Principle 5: The Exploratory Prototype Is Input, Not Output

The exploratory prototype is an epistemic instrument for learning the domain. Its
output is not a deliverable system; it is a specification. Mine it for domain
understanding, inventory its working features, and then design the system that should
exist given everything it taught you.

### Principle 6: Invariants Are Non-Negotiable

Invariants, once declared and marked, are non-negotiable behavioral contracts. Any
refactor that breaks a marked invariant is wrong by definition. If an invariant needs
to change, that change is a deliberate architectural decision — ratified, logged, and
propagated — not a side effect of an unrelated refactor.

### Principle 7: Specification Debt Is Worse Than Code Debt

Code debt is expensive. Specification debt is more expensive, because it hides code
debt. An undocumented architectural decision cannot be evaluated; it can only be lived
with or accidentally overwritten. A missing invariant will eventually be violated by an
AI that had no way to know it existed. Specification debt compounds invisibly.

### Principle 8: The Feedback Loop Determines the Methodology

In terminal-goal software with tight, binary feedback loops, CLDS overhead is
disproportionate to the benefit. Vibecoding with aggressive iteration is appropriate.
In open-ended creative tooling with loose, subjective feedback loops, CLDS overhead
is the minimum viable investment in architectural integrity. Know which regime you
are in.

### Principle 9: Architecture Is Negotiable; Architectural Authority Is Not

Not all structural decisions carry equal weight. File naming, utility organization,
and component decomposition within an already-defined container are **implementation
decisions** — delegatable to the AI within the bounds of established invariants. State
management patterns, data model shape, and API boundary design are **architectural
invariants** — requiring explicit human ratification before implementation.

CLDS does not require you to ratify every line of code. It requires you to maintain
clear authority over the decisions that define the system's structure. Delegate
implementation decisions freely. Ratify architectural ones always.

### Principle 10: Minimum Viable Specification

More specification is not always better. Beyond a threshold, specification maintenance
competes with implementation effort. An outdated invariant is worse than a missing one.
A stale YAML file describing behavior that no longer exists creates false confidence.

The minimum viable specification surface for a solo developer on a single-container
application: one architectural model (README or C4) + one domain schema + explicit
invariants + a DECISIONS.md. Everything above this floor is additive and should be
adopted based on felt need, not methodology prescription.

Treat the specification surface itself as a design problem: the right amount for your
project at your scale, no more.

---

## Part IX: Anti-Patterns

### Anti-Pattern 1: The Perpetual Prototype

Symptom: the exploratory prototype is never refactored because it always *mostly works*,
and refactoring feels like losing progress.

Consequence: the system's architecture is permanently defined by the accumulated decisions
of AI sessions that had no architectural authority to check against. The system becomes
progressively harder to extend without breaking existing behavior.

Resolution: a PARTIALLY WORKING system with no specification is not progress — it is
potential energy for future regression. The Full Refactor is not loss; it is crystallization.

### Anti-Pattern 2: The Specification as Ceremony

Symptom: specification artifacts are written but never loaded into session context.
They exist to satisfy a process requirement rather than to guide the AI.

Consequence: specification and implementation drift silently. The specification becomes
stale documentation rather than living infrastructure.

Resolution: if the specification is not in the context window, it does not exist for
that session. Session opening protocol is non-optional.

### Anti-Pattern 3: The Unilateral AI Refactor

Symptom: the AI proposes and implements a structural change within a session without
explicitly flagging it as an architectural decision.

Consequence: the architectural model is silently invalidated. Future sessions inherit
an inaccurate structural model.

Resolution: instruct the AI explicitly at session opening — "architectural proposals
must be surfaced as proposals, not implementations. Describe the change and your
reasoning. Do not implement it until I ratify it."

### Anti-Pattern 4: The Over-Specified Prototype

Symptom: CLDS tooling is applied to exploratory phases before the domain is understood.

Consequence: the specification reflects premature assumptions that the exploratory
prototype would have corrected. The specification becomes a constraint on learning.

Resolution: exploratory phases are intentionally under-specified. CLDS tooling engages
fully at the Full Refactor. The discipline is distinguishing exploration from design.

### Anti-Pattern 5: The Invisible Debt

Symptom: WORKING BUT UNSPECIFIED features are carried into the refactored system
without specification.

Consequence: the refactored system inherits unknown constraints. Future refactors
encounter behavior that cannot be changed safely because no one knows whether it
is intentional.

Resolution: the feature inventory is non-optional. Every feature entering the
refactored system must be classified. WORKING BUT UNSPECIFIED features must be
specified before implementation.

### Anti-Pattern 6: The Specification Bureaucracy

Symptom: the full CLDS toolstack (C4 + YAML + Gherkin + DECISIONS.md + session
protocols) is applied uniformly regardless of project scale or complexity.

Consequence: specification maintenance cost competes with implementation effort.
The methodology becomes a burden rather than infrastructure.

Resolution: apply the Minimum Viable Specification principle. README-as-architecture
and YAML acceptance criteria are legitimate artifacts at appropriate scales. Gherkin
is not mandatory. C4 is not mandatory. The principles are mandatory; the formats are
not. Start at the floor and add overhead only when its absence creates felt pain.

### Anti-Pattern 7: The Silent Execution

Symptom: the AI is given a specification and immediately begins implementation without
a proposal-and-ratification cycle. The plan is implicit, not explicit.

Consequence: architectural assumptions embedded in the AI's interpretation of the spec
are never surfaced for review. The implementation may be technically correct against
the spec while violating unstated architectural intent.

Resolution: REP. Always. For any implementation that is sufficiently significant to
warrant a PLAN.md, the minimal-plan-then-ratify cycle is the non-negotiable first step.
The plan carries your ratification before execution begins.

### Anti-Pattern 8: The Unverified Plan

Symptom: a CA produces PLAN.md and then implements it. No step verifies that
the implementation actually covers what the plan declared. Coverage gaps —
untested scenarios, missing fixtures, undeclared deviations — go unnoticed
because both the plan and the implementation were produced by AI, and no
authority checked the gap between them.

Consequence: PLAN.md becomes retrospective documentation rather than an
executable contract. The gap between declared strategy and actual
implementation is invisible — until a scenario the plan specified, but the
implementation skipped, causes a regression.

Resolution: REP Step 6.5. After execution, a CA (preferably in a fresh
context) performs a plan-implementation alignment audit: given PLAN.md and
the implementation, report every scenario, fixture, or teardown requirement
the plan declared that the implementation does not cover. This is a deviation
report, not a quality review. The output is the coverage gap, stated plainly.

Note: this anti-pattern is frequently avoided *accidentally* by developers
who manually test against PLAN.md. Making the avoidance deliberate and
CA-delegated is the CLDS response — it costs nothing and catches exactly the
class of silent gaps that manual testing catches inconsistently.

---

## Appendix A: Quick Reference

### Dominant Modes
- **Exploration Mode** — emergent spec, fast iteration, debt consciously accepted
- **Design Mode** — authoritative spec, disciplined iteration, debt actively managed

### The Seven Phases
1. **CRYSTALLIZATION** — Domain vocabulary, core use case hypothesis
2. **SHELL** — Minimal skeleton, basic data flow
3. **UI PROTOTYPE** — Interface without functionality
4. **MINIMAL FUNCTIONALITY TEST** — Just enough to test the actual use case
5. **EXPLORATORY ITERATION** — Iterate until inflection point
6. **FULL REFACTOR** — Mode transition; specification-first; working features only
7. **DISCIPLINED EVOLUTION** — Every feature through the specification loop

### The CLDS Toolstack
- **Architectural Model** — Structural authority and rejection filter (README or C4)
- **YAML Specification Files** — Contract surface, constitutional document
- **Behavioral Contracts** — Observable oracle, regression anchor (YAML or Gherkin)
- **DECISIONS.md** — Unresolved decision log, cross-session memory

### The Specification Loop
1. Domain crystallization
2. Architectural placement
3. YAML specification
4. Behavioral contracts
5. AI-assisted implementation (via REP)
6. Specification reconciliation
7. Architectural model update

### The Ratified Execution Protocol (REP)
1. Minimal plan request (proposal-only mode)
2. Ratification with architectural annotations
3. Full plan elaboration (write mode)
4. Final approval
5. Phased execution
6. Local behavioral annotation per phase
6.5. Plan-implementation alignment audit
7. Final iron-out

### The Inflection Point Signals
- A bug fix breaks something semantically unrelated
- A new feature requires modifying more than three existing files
- You cannot explain data flow without consulting the code
- The AI generates solutions conflicting with earlier session decisions
- The README no longer describes what the system actually does

### The Ten Principles
1. The specification is infrastructure
2. Intent flows downward
3. The AI proposes; you ratify
4. Deviation must be explicit
5. The exploratory prototype is input, not output
6. Invariants are non-negotiable
7. Specification debt is worse than code debt
8. The feedback loop determines the methodology
9. Architecture is negotiable; architectural authority is not
10. Minimum viable specification

---

## Appendix B: Minimum Viable Specification by Scale

| Scale | Architectural Model | Contract Surface | Behavioral Contracts |
|-------|--------------------|--------------------|----------------------|
| Solo, single container, moderate complexity | README-as-architecture | YAML schema file | Inline acceptance criteria |
| Solo, single container, high complexity | README + C4 Component diagram | YAML per domain entity | YAML + Gherkin for complex flows |
| Small team, multi-container | Full C4 (Context + Container + Component) | YAML per domain entity | Gherkin for all user-facing features |

Apply the floor for your scale. Add overhead only when its absence creates felt pain.

---

## Appendix C: Glossary

**CLDS (Cognitive Load Distribution System)** — The methodology described in this
document. The practice of distributing cognitive labor across the asymmetry between
human design intent and AI implementation capability through structured specification
artifacts.

**REP (Ratified Execution Protocol)** — The operational turn sequence by which a
ratified specification becomes working code. Seven steps from minimal plan proposal
through final iron-out, calibrated to minimize human reading cost while maximizing
architectural authority exercised.

**Terminal-Goal Software** — Software whose specification is externally imposed by
a fixed protocol, format, or third-party system. Tight feedback loops, binary success
criteria, bounded debt surface. Vibecoding is often appropriate.

**Open-Ended Creative Tooling** — Software whose specification is generated by the
developer's evolving creative vision. Loose feedback loops, subjective success criteria,
unbounded debt surface without CLDS.

**Exploration Mode** — Dominant mode in which specification is emergent, iteration is
fast, and debt is consciously accepted as the price of domain learning.

**Design Mode** — Dominant mode in which specification is authoritative, iteration is
disciplined, and debt is actively managed.

**Rejection Filter** — The function the architectural model serves: an externalized
structural description against which proposed changes can be evaluated without
reconstructing full architectural context from code.

**Invariant** — A behavioral property that must remain true across all future refactors.
Explicitly marked in specification. The non-negotiable contract between specification
and implementation.

**Invariant Graduation** — The process by which a candidate behavioral property earns
invariant status through one or more of: repeated survival, domain necessity, user
validation, or architectural derivation.

**Drift** — A change that moves away from specification without awareness. Harmful
because invisible; the primary mechanism of architectural decay.

**Evolution** — A change that moves toward a better understanding of the domain, made
with awareness, surfaced, ratified, and logged. Healthy; the mechanism by which
specifications improve through contact with reality.

**Specification Reconciliation** — The process of resolving mismatches between
specification and implementation at the specification level first. The mechanism
preventing code behavior from silently redefining specification intent.

**Feature Inventory** — Classification of all features in an exploratory prototype
before Full Refactor: VERIFIED WORKING, WORKING BUT UNSPECIFIED, PARTIALLY WORKING,
BROKEN, SCOPE CREEP, or DUPLICATE.

**Context Reconstruction Debt** — The cost paid at the start of every AI session to
re-establish what the previous session already knew, in the absence of a session
closing protocol.

**Vocabulary-Bridged Composition** — The mode in which AI-assisted development is
most effective: assembling known solutions to known sub-problems in a fixed sequence,
where the human contributes intent and the AI contributes implementation fluency.

**Constitutional Document** — The function YAML specification files serve: the
authoritative record of what the system is supposed to do, which the AI checks against
and proposes amendments to, but which only the human ratifies.

**Minimum Viable Specification** — The smallest artifact set that preserves core CLDS
properties without inducing maintenance overhead that competes with development effort.
Floor: one architectural model + one domain schema + explicit invariants + DECISIONS.md.

**Plan-Implementation Alignment Audit** — REP Step 6.5. A targeted CA review
— preferably in a fresh context — that compares PLAN.md against the
implementation and reports only coverage gaps and deviations. Distinguished
from behavioral annotation (Step 6), which checks implementation against
observable behavior, and from the final iron-out (Step 7), which checks
implementation hygiene. The alignment audit's authority is the plan itself,
treated as a behavioral contract: every scenario, fixture, and teardown the
plan declared must be accounted for in the implementation or explicitly
deferred.

**Ratification Surface** — The minimal plan produced in REP Step 1. Not a draft of
the full plan but the skeleton against which architectural annotations are made before
any implementation begins.

---

*SPECIFICATION.md is itself a living document. It describes a methodology in active
use and should be updated as the methodology evolves through practical application.
Every significant revision should be logged with a rationale, modeling the same
discipline it prescribes.*

*Version 1.0 — Initial manifesto*
*Version 1.1 — Amendments from DISSONANCE.md review and REP discovery:*
  *- C4 decoupled from Architectural Authority Principle; README-as-architecture*
  *  formalized as minimum viable alternative*
  *- Gherkin replaced as mandatory with Behavioral Contracts as the primitive;*
  *  YAML acceptance criteria formalized as the minimum viable contract format*
  *- Minimum Viable Specification principle added (Principle 10 + Appendix B)*
  *- Negotiable vs non-negotiable architecture distinction added (Principle 9)*
  *- Phase model reframed as dominant modes rather than strict sequence*
  *- Drift vs Evolution distinction added (Section 4.2)*
  *- CLDS acknowledged as era-contingent (Preamble)*
  *- CLDS acknowledged as distributed cognition framework, not software methodology*
  *  specifically (Preamble)*
  *- Invariant graduation criteria added (Section 3.4)*
  *- REP (Ratified Execution Protocol) added as Part V — the operational layer*
  *  discovered empirically through accidental read-only mode constraint*
  *- Anti-Pattern 6 (Specification Bureaucracy) and Anti-Pattern 7 (Silent Execution)*
  *  added*
  *- Bottleneck inversion noted as design constraint shaping all workflow decisions*
*Version 1.2 — Amendment from AAA_*.py test suite workflow observation:*
  *- REP Step 6.5 (Plan-Implementation Alignment Audit) added between*
  *  Step 6 and Step 7. Discovered through the observation that PLAN.md*
  *  and AAA_tests.py had a coverage gap (teardown tests, Scenario C modal*
  *  operator testing) that neither the plan author nor the implementor*
  *  surfaced. The gap was detected by manual comparison — which REP now*
  *  delegates to a CA in a fresh context.*
  *- Anti-Pattern 8 (The Unverified Plan) added: the pattern of assuming*
  *  plan coverage because both plan and implementation were CA-produced.*
  *- Reading Cost Calibration table updated with Step 6.5 row.*
  *- Glossary entry added for Plan-Implementation Alignment Audit.*
  *- Distinction between Step 6 authority (spec/behavior) and Step 6.5*
  *  authority (plan/strategy) made explicit in Step 6.5 text.*
