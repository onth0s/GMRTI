import Mathlib.Data.Multiset.Basic
import Mathlib.Data.Finset.Basic

/-!
# GMRTI Semantic Covenant Formal Model

Formal representation of a Semantic Covenant as a labeled directed multigraph.
In GMRTI, a covenant is not a static dictionary, but a topology of meaning-relations
held by a rational entity at a given moment (§0.4, §2a).
-/

namespace GMRTI

/-- The GMRTI Edge Taxonomy classification types (§2a, §2f, concept_edge.yaml). -/
inductive EdgeType where
  | Causal
  | Inferential
  | Procedural
  | Affective
  | Normative
  | Identity
  | Referential
  | Structural
  deriving DecidableEq, Repr

/-- A directed labeled edge between two semantic nodes. -/
structure DirectedEdge (V : Type) where
  src : V
  dst : V
  type : EdgeType
  deriving DecidableEq, Repr

/-- A Semantic Covenant over vertex universe `V` is modeled as a
labeled directed multigraph: mapping any pair of vertices to the
multiset of edge types connecting them. -/
structure Covenant (V : Type) where
  edges : V → V → Multiset EdgeType

/-- Two covenants are equal if their edge distributions coincide. -/
@[ext]
theorem Covenant.ext {V : Type} (C₁ C₂ : Covenant V)
    (h : ∀ u v, C₁.edges u v = C₂.edges u v) : C₁ = C₂ := by
  cases C₁; cases C₂; congr; funext u v; exact h u v

/-- The empty covenant containing no relational edges. -/
def emptyCovenant (V : Type) : Covenant V where
  edges := fun _ _ ↦ ∅

/-- Sub-covenant relation: C₁ is a sub-covenant of C₂ if all its edge
multisets are contained within C₂. -/
def Covenant.le {V : Type} (C₁ C₂ : Covenant V) : Prop :=
  ∀ u v, C₁.edges u v ≤ C₂.edges u v

instance {V : Type} : LE (Covenant V) where
  le := Covenant.le

/-- Reflexivity of covenant containment. -/
theorem Covenant.le_refl {V : Type} (C : Covenant V) : C ≤ C :=
  fun _ _ ↦ le_rfl

/-- Transitivity of covenant containment. -/
theorem Covenant.le_trans {V : Type} {C₁ C₂ C₃ : Covenant V}
    (h₁ : C₁ ≤ C₂) (h₂ : C₂ ≤ C₃) : C₁ ≤ C₃ := by
  intro u v
  exact _root_.le_trans (h₁ u v) (h₂ u v)

instance {V : Type} : Preorder (Covenant V) where
  le := Covenant.le
  le_refl := Covenant.le_refl
  le_trans := fun _ _ _ ↦ Covenant.le_trans

/-- Add a typed edge constraint to an existing covenant. -/
def Covenant.addEdge {V : Type} [DecidableEq V] (C : Covenant V) (e : DirectedEdge V) : Covenant V where
  edges := fun u v ↦
    if u = e.src ∧ v = e.dst then
      e.type ::ₘ C.edges u v
    else
      C.edges u v

/-- Adding an edge preserves the prior covenant as a sub-covenant. -/
theorem Covenant.le_addEdge {V : Type} [DecidableEq V] (C : Covenant V) (e : DirectedEdge V) :
    C ≤ C.addEdge e := by
  intro u v
  dsimp [Covenant.addEdge]
  split_ifs with h
  · exact Multiset.le_cons_self (C.edges u v) e.type
  · exact le_rfl

end GMRTI
