import Mathlib.Data.Finset.Basic
import Mathlib.Data.Finset.Card
import Mathlib.Data.Real.Basic
import GMRTI.Covenant

/-!
# GMRTI Functional Congruence and Comosí Formal Model

Formal representation of functional distance under an operational observation
suite, and the Comosí predicate defining apparent understanding within bounded
tolerance epsilon(DRC) (§0.4, §3c.3).
-/

namespace GMRTI

/-- An operational probe tests a specific inference or behavioral output on a covenant. -/
structure OperationalProbe (V : Type) where
  evaluate : Covenant V → Bool

/-- Functional distance over a finite suite of operational test probes:
the proportion of probes on which two covenants produce differing outcomes. -/
noncomputable def functionalDistance {V : Type} (probes : Finset (OperationalProbe V))
    (C₁ C₂ : Covenant V) : ℝ :=
  if probes.card = 0 then 0
  else ((probes.filter (fun p ↦ p.evaluate C₁ ≠ p.evaluate C₂)).card : ℝ) / (probes.card : ℝ)

/-- Comosí Predicate (§0.4, §3c.3): C₁ and C₂ achieve a Comosí within tolerance epsilon
under test suite `probes` if their functional distance does not exceed epsilon. -/
def comosi {V : Type} (probes : Finset (OperationalProbe V))
    (C₁ C₂ : Covenant V) (epsilon : ℝ) : Prop :=
  functionalDistance probes C₁ C₂ ≤ epsilon

/-- Functional distance is symmetric. -/
theorem functionalDistance_comm {V : Type} (probes : Finset (OperationalProbe V))
    (C₁ C₂ : Covenant V) :
    functionalDistance probes C₁ C₂ = functionalDistance probes C₂ C₁ := by
  dsimp [functionalDistance]
  split_ifs with h
  · rfl
  · congr 2
    congr 1
    ext p
    simp only [Finset.mem_filter]
    constructor
    · rintro ⟨hp, hne⟩; exact ⟨hp, Ne.symm hne⟩
    · rintro ⟨hp, hne⟩; exact ⟨hp, Ne.symm hne⟩

/-- Comosí is symmetric. -/
theorem comosi_symm {V : Type} (probes : Finset (OperationalProbe V))
    (C₁ C₂ : Covenant V) (epsilon : ℝ) (h : comosi probes C₁ C₂ epsilon) :
    comosi probes C₂ C₁ epsilon := by
  rwa [comosi, functionalDistance_comm]

/-- Reflexivity: Any covenant is in Comosí with itself for all non-negative epsilon. -/
theorem comosi_refl {V : Type} (probes : Finset (OperationalProbe V))
    (C : Covenant V) {epsilon : ℝ} (hepsilon : 0 ≤ epsilon) :
    comosi probes C C epsilon := by
  dsimp [comosi, functionalDistance]
  split_ifs with h
  · exact hepsilon
  · have hempty : (probes.filter (fun p ↦ p.evaluate C ≠ p.evaluate C)) = ∅ := by
      ext p
      simp
    rw [hempty, Finset.card_empty]
    simp only [Nat.cast_zero, zero_div]
    exact hepsilon

end GMRTI
