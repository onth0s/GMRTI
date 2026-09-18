import Mathlib.Data.Finset.Basic
import GMRTI.Covenant
import GMRTI.Entropy

/-!
# GMRTI Refinement Cycle Convergence Formal Model

Formal representation of the Refinement Cycle (§3) as an iterative constraint-injection
process that monotonically contracts the compatible-covenant hypothesis space.
-/

namespace GMRTI

/-- A single step in the Refinement Cycle (§3) augments the signal
with an additional edge constraint produced via Divergence Localization. -/
def refinementStep {V : Type} (S : Signal V) (repair : DirectedEdge V) : Signal V where
  constraints := repair :: S.constraints

/-- Adding a repair constraint preserves all existing constraints. -/
theorem refinementStep_contains {V : Type} (S : Signal V) (repair : DirectedEdge V) :
    ∀ e ∈ S.constraints, e ∈ (refinementStep S repair).constraints := by
  intro e he
  dsimp [refinementStep]
  exact List.mem_cons_of_mem repair he

/-- Refinement Monotonicity: Each targeted repair step weakly decreases the compatible
candidate space cardinality. -/
theorem refinement_candidates_monotone {V : Type} [DecidableEq V] [DecidableEq (Covenant V)]
    (U : Finset (Covenant V)) (S : Signal V) (repair : DirectedEdge V) :
    (compatibleCovenants U (refinementStep S repair)).card ≤ (compatibleCovenants U S).card :=
  compatible_card_mono U S (refinementStep S repair) (refinementStep_contains S repair)

/-- Refinement Entropy Non-increasing Theorem: Under positive candidate count,
each refinement step weakly decreases or preserves Hartley Semantic Entropy (§1a.6, §3). -/
theorem refinement_entropy_nonincreasing {V : Type} [DecidableEq V] [DecidableEq (Covenant V)]
    (U : Finset (Covenant V)) (S : Signal V) (repair : DirectedEdge V)
    (hpos : 0 < (compatibleCovenants U (refinementStep S repair)).card) :
    semanticEntropy U (refinementStep S repair) ≤ semanticEntropy U S :=
  semanticEntropy_mono U S (refinementStep S repair) (refinementStep_contains S repair) hpos

/-- Effective Repair Theorem: If a repair actively discriminates against at least one
candidate covenant currently in the compatible set, the candidate set strictly shrinks. -/
theorem refinement_effective_strict_shrink {V : Type} [DecidableEq V] [DecidableEq (Covenant V)]
    (U : Finset (Covenant V)) (S : Signal V) (repair : DirectedEdge V)
    (C_invalid : Covenant V)
    (h_mem : C_invalid ∈ compatibleCovenants U S)
    (h_not : ¬ satisfiesSignal C_invalid (refinementStep S repair)) :
    (compatibleCovenants U (refinementStep S repair)).card < (compatibleCovenants U S).card := by
  have hsub := compatible_subset U S (refinementStep S repair) (refinementStep_contains S repair)
  have hnot_in : C_invalid ∉ compatibleCovenants U (refinementStep S repair) := by
    intro hc
    rw [compatibleCovenants, Finset.mem_filter] at hc
    exact h_not hc.2
  have hne : compatibleCovenants U (refinementStep S repair) ≠ compatibleCovenants U S := by
    intro heq
    apply hnot_in
    rw [heq]
    exact h_mem
  exact Finset.card_lt_card (Finset.ssubset_iff_subset_ne.mpr ⟨hsub, hne⟩)

end GMRTI
