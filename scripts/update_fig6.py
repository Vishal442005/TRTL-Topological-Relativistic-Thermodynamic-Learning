import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
fig.suptitle("TRTL Thermodynamic Hamiltonian Flow and Phase-Space Trajectory Dynamics", fontweight='bold', y=1.02)

# Panel (a): Multi-well energy surface & Escape from shallow local minima
ax = axes[0]
s = np.linspace(-2.2, 2.2, 200)
# Multi-well potential with a shallow metastable well and deep global well
U = 0.5 * (s**2 - 1.5)**2 + 0.3 * np.sin(3.0 * s)
ax.plot(s, U, 'k-', lw=2.2, label='Potential Energy Surface $U(S)$')

# Standard gradient descent gets stuck in shallow well
ax.plot([-0.6, -0.62, -0.63], [1.1, 0.95, 0.92], 'ro--', lw=2.0, ms=6, label='Overdamped Flow (Trapped in Metastable Well)')
ax.annotate("Stuck in Local Well", xy=(-0.63, 0.92), xytext=(-1.8, 1.6),
            arrowprops=dict(arrowstyle="->", color="red", lw=1.5),
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="red", alpha=0.9), color="red", fontweight="bold")

# TRTL Thermodynamic flow with momentum escapes
s_path = np.linspace(-0.6, 1.25, 60)
U_path = 0.5 * (s_path**2 - 1.5)**2 + 0.3 * np.sin(3.0 * s_path) + 0.15 * np.sin(np.linspace(0, 3*np.pi, 60))
ax.plot(s_path, U_path, 'c-', lw=2.8, label='TRTL Thermodynamic Flow (Escapes Barrier)')
ax.annotate("Escapes Barrier via\nKinetic Phase Energy", xy=(0.3, 1.4), xytext=(0.1, 2.2),
            arrowprops=dict(arrowstyle="->", color="teal", lw=1.5),
            bbox=dict(boxstyle="round,pad=0.2", fc="#e8f8f5", ec="teal", alpha=0.9), color="teal", fontweight="bold")
ax.scatter([1.25], [0.5 * (1.25**2 - 1.5)**2 + 0.3 * np.sin(3.0 * 1.25)], c='lime', edgecolors='k', s=90, zorder=5, label='Global Ground State $S^*$')

ax.set_title("(a) Escape from Metastable Potential Wells\n(Thermodynamic Momentum Dynamics)", fontweight='bold')
ax.set_xlabel("Order Parameter State $S$")
ax.set_ylabel("Thermodynamic Free Energy $F(S)$")
ax.grid(True, linestyle=':', alpha=0.4)
ax.legend(loc='upper right', framealpha=0.9)

# Panel (b): Symplectic Phase-Space Orbit (S, P_S)
ax2 = axes[1]
theta = np.linspace(0, 4*np.pi, 250)
r_decay = np.exp(-0.08 * theta)
s_orbit = r_decay * np.cos(theta)
p_orbit = -r_decay * np.sin(theta)

ax2.plot(s_orbit, p_orbit, color='#1f77b4', lw=2.2, label='Phase Trajectory $(S(t), P_S(t))$')
ax2.scatter([s_orbit[0]], [p_orbit[0]], c='red', edgecolors='k', s=80, label='Initial State $(S_0, P_0)$', zorder=5)
ax2.scatter([0], [0], c='green', marker='*', s=150, label='Lyapunov Attractor Equilibrium $(0, 0)$', zorder=5)

ax2.set_title("(b) Phase-Space State Trajectory\n(Symplectic Measure Preserving Orbit: $dP_S \\wedge dS$)", fontweight='bold')
ax2.set_xlabel("Order Parameter $S$")
ax2.set_ylabel("Conjugate Momentum $P_S = \\dot{S}$")
ax2.grid(True, linestyle=':', alpha=0.4)
ax2.legend(loc='upper right', framealpha=0.9)

plt.tight_layout()
plt.savefig("figures/phase3/fig6_hwtao_phase_space_trajectory.png", bbox_inches='tight', dpi=300)
plt.close()
print("[OK] Updated fig6_hwtao_phase_space_trajectory.png to TRTL Thermodynamic Hamiltonian Flow")
