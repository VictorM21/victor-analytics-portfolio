"""
Sample Size Calculator Dashboard
Author: Victor Makanju
Purpose: Interactive exploration of sample size requirements for A/B tests
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import math

def calculate_sample_size(baseline, effect, alpha=0.05, power=0.8):
    """Calculate required sample size per group"""
    
    treatment = baseline * (1 + effect)
    p_pooled = (baseline + treatment) / 2
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)
    
    # FIXED: Correct exponent syntax
    n = (2 * p_pooled * (1 - p_pooled) * (z_alpha + z_beta)**2) / (treatment - baseline)**2
    return math.ceil(n)

# Generate data for visualization
baseline_rates = [0.01, 0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
effect_sizes = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]

# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Sample size by baseline rate (different effects)
ax1 = axes[0, 0]
for effect in [0.05, 0.10, 0.15, 0.20]:
    sample_sizes = [calculate_sample_size(b, effect) for b in baseline_rates]
    ax1.plot([b*100 for b in baseline_rates], sample_sizes, 
             marker='o', linewidth=2, label=f'{effect:.0%} effect')

ax1.set_xlabel('Baseline Conversion Rate (%)', fontsize=12)
ax1.set_ylabel('Sample Size per Group', fontsize=12)
ax1.set_title('Sample Size vs. Baseline Rate', fontsize=14, fontweight='bold')
ax1.set_yscale('log')
ax1.grid(True, alpha=0.3)
ax1.legend(title='Minimum Detectable Effect')
ax1.set_ylim(bottom=100)

# 2. Sample size by effect size (different baselines)
ax2 = axes[0, 1]
for baseline in [0.02, 0.05, 0.10, 0.20]:
    sample_sizes = [calculate_sample_size(baseline, e) for e in effect_sizes]
    ax2.plot([e*100 for e in effect_sizes], sample_sizes, 
             marker='s', linewidth=2, label=f'{baseline:.0%} baseline')

ax2.set_xlabel('Minimum Detectable Effect (%)', fontsize=12)
ax2.set_ylabel('Sample Size per Group', fontsize=12)
ax2.set_title('Sample Size vs. Effect Size', fontsize=14, fontweight='bold')
ax2.set_yscale('log')
ax2.grid(True, alpha=0.3)
ax2.legend(title='Baseline Rate')
ax2.set_ylim(bottom=100)

# 3. Heatmap of sample sizes
ax3 = axes[1, 0]
baseline_grid, effect_grid = np.meshgrid(baseline_rates, effect_sizes)
sample_grid = np.zeros_like(baseline_grid)

for i, b in enumerate(baseline_rates):
    for j, e in enumerate(effect_sizes):
        sample_grid[j, i] = calculate_sample_size(b, e)

im = ax3.imshow(sample_grid, cmap='YlOrRd', aspect='auto',
                extent=[min(baseline_rates)*100, max(baseline_rates)*100,
                        min(effect_sizes)*100, max(effect_sizes)*100],
                origin='lower')

ax3.set_xlabel('Baseline Conversion Rate (%)', fontsize=12)
ax3.set_ylabel('Minimum Detectable Effect (%)', fontsize=12)
ax3.set_title('Sample Size Heatmap', fontsize=14, fontweight='bold')
plt.colorbar(im, ax=ax3, label='Sample Size per Group')

# Add text annotations (only for smaller sample sizes to avoid clutter)
for i, b in enumerate(baseline_rates):
    for j, e in enumerate(effect_sizes):
        n = sample_grid[j, i]
        if n < 50000:  # Only show if not too large
            ax3.text(b*100, e*100, f'{int(n):,}', 
                    ha='center', va='center', fontsize=8, color='black')

# 4. Power curves
ax4 = axes[1, 1]
effect_range = np.linspace(0, 0.2, 50)
for n in [1000, 5000, 10000, 50000]:
    powers = []
    for e in effect_range:
        # Approximate standard error
        se = math.sqrt(2 * 0.1 * 0.9 / n)
        z_alpha = stats.norm.ppf(1 - 0.05/2)
        z_beta = e / se - z_alpha
        power = stats.norm.cdf(z_beta)
        powers.append(power)
    ax4.plot(effect_range*100, powers, linewidth=2, label=f'n={n:,}')

ax4.axhline(y=0.8, color='gray', linestyle='--', alpha=0.7, label='80% Power')
ax4.set_xlabel('Effect Size (%)', fontsize=12)
ax4.set_ylabel('Statistical Power', fontsize=12)
ax4.set_title('Power Curves by Sample Size', fontsize=14, fontweight='bold')
ax4.grid(True, alpha=0.3)
ax4.legend()
ax4.set_ylim(0, 1)

plt.tight_layout()
plt.savefig('../results/sample_size_dashboard.png', dpi=100, bbox_inches='tight')
plt.show()

print("\n✅ Sample Size Calculator Dashboard created successfully!")
print("📊 Visualization saved to: results/sample_size_dashboard.png")