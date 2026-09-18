import Mathlib.Data.Finset.Basic
import Mathlib.Data.Finset.Card
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import GMRTI.Covenant

/-!
# GMRTI Semantic Entropy Formal Model

Formal representation of Hartley Semantic Entropy H_s(S) as the log-cardinality
of the hypothesis space of receiving-covenant topologies compatible with signal S (§1a.6, §8b.1).
-/

namespace GMRTI

/-- A surface signal specifies relational constraints that a receiving
covenant must satisfy in order to be considered compatible with the signal. -/
structure Signal (V : Type) where
  constraints : List (DirectedEdge V)

/-- A covenant satisfies a signal if it contains all relational edges
prescribed by the signal. -/
def satisfiesSignal {V : Type} [DecidableEq V] (C : Covenant V) (S : Signal V) : Prop :=
  ∀ e ∈ S.constraints, e.type ∈ C.edges e.src e.dst

instance {V : Type} [DecidableEq V] (C : Covenant V) (S : Signal V) :
    Decidable (satisfiesSignal C S) := by
  dsimp [satisfiesSignal]
  infer_instance

/-- Given a finite universe of candidate receiving covenants `U`, the
set of compatible topologies is the sub-finset satisfying the signal. -/
def compatibleCovenants {V : Type} [DecidableEq V] [DecidableEq (Covenant V)]
    (U : Finset (Covenant V)) (S : Signal V) : Finset (Covenant V) :=
  U.filter (fun C ↦ satisfiesSignal C S)

/-- Hartley Semantic Entropy H_s(S) = log₂ |compatibleCovenants| (§1a.6, §8b.1). -/
noncomputable def semanticEntropy {V : Type} [DecidableEq V] [DecidableEq (Covenant V)]
    (U : Finset (Covenant V)) (S : Signal V) : ℝ :=
  Real.log ((compatibleCovenants U S).card : ℝ) / Real.log 2

/-- Adding constraints to a signal monotonically restricts the compatible topologies. -/
theorem compatible_subset {V : Type} [DecidableEq V] [DecidableEq (Covenant V)]
    (U : Finset (Covenant V)) (S₁ S₂ : Signal V)
    (h : ∀ e ∈ S₁.constraints, e ∈ S₂.constraints) :
    compatibleCovenants U S₂ ⊆ compatibleCovenants U S₁ := by
  intro C hC
  rw [compatibleCovenants, Finset.mem_filter] at hC ⊢
  refine ⟨hC.1, ?_⟩
  intro e he
  exact hC.2 e (h e he)

/-- Monotonicity of candidate count: more constraints yield fewer or equal compatible graphs. -/
theorem compatible_card_mono {V : Type} [DecidableEq V] [DecidableEq (Covenant V)]
    (U : Finset (Covenant V)) (S₁ S₂ : Signal V)
    (h : ∀ e ∈ S₁.constraints, e ∈ S₂.constraints) :
    (compatibleCovenants U S₂).card ≤ (compatibleCovenants U S₁).card :=
  Finset.card_le_card (compatible_subset U S₁ S₂ h)

/-- Semantic entropy is monotonically nonincreasing under constraint accumulation
when the remaining candidate count is positive. -/
theorem semanticEntropy_mono {V : Type} [DecidableEq V] [DecidableEq (Covenant V)]
    (U : Finset (Covenant V)) (S₁ S₂ : Signal V)
    (h : ∀ e ∈ S₁.constraints, e ∈ S₂.constraints)
    (hpos : 0 < (compatibleCovenants U S₂).card) :
    semanticEntropy U S₂ ≤ semanticEntropy U S₁ := by
  dsimp [semanticEntropy]
  have hcard := compatible_card_mono U S₁ S₂ h
  have hpos_real : (0 : ℝ) < ((compatibleCovenants U S₂).card : ℝ) := Nat.cast_pos.mpr hpos
  have hle_real : ((compatibleCovenants U S₂).card : ℝ) ≤ ((compatibleCovenants U S₁).card : ℝ) :=
    Nat.cast_le.mpr hcard
  have hlog : Real.log ((compatibleCovenants U S₂).card : ℝ) ≤ Real.log ((compatibleCovenants U S₁).card : ℝ) :=
    Real.log_le_log hpos_real hle_real
  have hlog2_pos : 0 < Real.log 2 := Real.log_pos (by norm_num)
  exact div_le_div_of_nonneg_right hlog (le_of_lt hlog2_pos)

end GMRTI
