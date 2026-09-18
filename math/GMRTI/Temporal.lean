import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/-!
# GMRTI Dynamic Re-Anchoring & Lag-Bounded Tracking Formal Model

Formal representation of the Exponential Smoothing heuristic for Artifact Anchors
and verification of the Lag-Bounded Tracking Principle (§4b.3, concept_artifact_anchor.yaml).
-/

namespace GMRTI

/-- Exponential Moving Average update rule (§4b.3):
A_{t+1} = (1 - lambda) A_t + lambda D_t -/
def emaUpdate (lambda : ℝ) (A D : ℝ) : ℝ :=
  (1 - lambda) * A + lambda * D

/-- Error recurrence identity:
The one-step error e_{t+1} = A_{t+1} - D_{t+1} equals (1 - lambda) e_t - (D_{t+1} - D_t). -/
theorem ema_error_recurrence (lambda : ℝ) (A D D_next : ℝ) :
    (emaUpdate lambda A D) - D_next = (1 - lambda) * (A - D) - (D_next - D) := by
  dsimp [emaUpdate]
  ring

/-- One-step error bound under bounded step drift |D_{t+1} - D_t| ≤ δ. -/
theorem ema_error_bound_step (lambda : ℝ) (hlambda_nonneg : 0 ≤ 1 - lambda) (A D D_next : ℝ) (δ : ℝ)
    (h_drift : |D_next - D| ≤ δ) :
    |(emaUpdate lambda A D) - D_next| ≤ (1 - lambda) * |A - D| + δ := by
  rw [ema_error_recurrence]
  have h_tri := abs_sub ((1 - lambda) * (A - D)) (D_next - D)
  refine le_trans h_tri ?_
  rw [abs_mul, abs_of_nonneg hlambda_nonneg]
  exact add_le_add_left h_drift ((1 - lambda) * |A - D|)

/-- Invariant bound: If the tracking error satisfies |A - D| ≤ δ / lambda,
then the updated error satisfies |A_{t+1} - D_{t+1}| ≤ δ / lambda. -/
theorem ema_steady_state_invariant (lambda δ : ℝ) (hlambda_pos : 0 < lambda) (hlambda_le : lambda ≤ 1) (_hδ : 0 ≤ δ)
    (A D D_next : ℝ) (h_drift : |D_next - D| ≤ δ)
    (h_bound : |A - D| ≤ δ / lambda) :
    |(emaUpdate lambda A D) - D_next| ≤ δ / lambda := by
  have h1 : 0 ≤ 1 - lambda := sub_nonneg.mpr hlambda_le
  have h_step := ema_error_bound_step lambda h1 A D D_next δ h_drift
  refine le_trans h_step ?_
  have h_scaled : (1 - lambda) * |A - D| ≤ (1 - lambda) * (δ / lambda) :=
    mul_le_mul_of_nonneg_left h_bound h1
  have h_comb : (1 - lambda) * (δ / lambda) + δ = δ / lambda := by
    calc (1 - lambda) * (δ / lambda) + δ
      _ = (1 - lambda) * (δ / lambda) + lambda * (δ / lambda) := by
          congr 1
          rw [mul_div_cancel₀ δ (ne_of_gt hlambda_pos)]
      _ = ((1 - lambda) + lambda) * (δ / lambda) := by ring
      _ = 1 * (δ / lambda) := by ring
      _ = δ / lambda := one_mul (δ / lambda)
  linarith

/-- Lag-Bounded Tracking Principle (§4b.3):
The lag of the updated anchor relative to the current reference declaration
|A_{t+1} - D_t| is bounded by δ * (1 - lambda) / lambda whenever the prior error is within steady state. -/
theorem lag_bounded_tracking_principle (lambda δ : ℝ) (hlambda_le : lambda ≤ 1)
    (A D : ℝ) (h_bound : |A - D| ≤ δ / lambda) :
    |(emaUpdate lambda A D) - D| ≤ δ * (1 - lambda) / lambda := by
  have h_eq : (emaUpdate lambda A D) - D = (1 - lambda) * (A - D) := by
    dsimp [emaUpdate]
    ring
  rw [h_eq, abs_mul, abs_of_nonneg (sub_nonneg.mpr hlambda_le)]
  have h_ineq : (1 - lambda) * |A - D| ≤ (1 - lambda) * (δ / lambda) :=
    mul_le_mul_of_nonneg_left h_bound (sub_nonneg.mpr hlambda_le)
  have h_div : (1 - lambda) * (δ / lambda) = δ * (1 - lambda) / lambda := by ring
  rwa [h_div] at h_ineq

end GMRTI
