"""
A/B Testing Simulation and Analysis
Author: Victor Makanju
Purpose: Demonstrate end-to-end A/B testing workflow including sample size calculation,
         experiment simulation, statistical analysis, and results interpretation.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import math
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class ABTestingSimulator:
    """
    Complete A/B Testing simulator with sample size calculation,
    experiment execution, and statistical analysis.
    """
    
    def __init__(self, experiment_name="A/B Test"):
        self.experiment_name = experiment_name
        self.results = {}
        
    def calculate_sample_size(self, baseline_rate, minimum_detectable_effect, 
                             alpha=0.05, power=0.8, two_tailed=True):
        """
        Calculate required sample size for A/B test
        
        Parameters:
        -----------
        baseline_rate : float
            Current conversion rate (control group)
        minimum_detectable_effect : float
            Minimum relative improvement we want to detect (e.g., 0.10 for 10%)
        alpha : float
            Significance level (Type I error probability)
        power : float
            Statistical power (1 - Type II error probability)
        two_tailed : bool
            Whether to use two-tailed test
            
        Returns:
        --------
        dict: Sample size results and parameters
        """
        
        # Calculate treatment rate
        treatment_rate = baseline_rate * (1 + minimum_detectable_effect)
        
        # Pooled proportion
        p_pooled = (baseline_rate + treatment_rate) / 2
        
        # Z-scores
        if two_tailed:
            z_alpha = stats.norm.ppf(1 - alpha/2)
        else:
            z_alpha = stats.norm.ppf(1 - alpha)
            
        z_beta = stats.norm.ppf(power)
        
        # Sample size formula for two proportions - FIXED SYNTAX HERE
        n = (2 * p_pooled * (1 - p_pooled) * (z_alpha + z_beta)**2) / (treatment_rate - baseline_rate)**2
        
        # Round up to nearest integer
        n_per_group = math.ceil(n)
        
        # Store results
        result = {
            'baseline_rate': baseline_rate,
            'treatment_rate': treatment_rate,
            'minimum_detectable_effect': minimum_detectable_effect,
            'absolute_effect': treatment_rate - baseline_rate,
            'alpha': alpha,
            'power': power,
            'z_alpha': z_alpha,
            'z_beta': z_beta,
            'n_per_group': n_per_group,
            'total_sample_size': n_per_group * 2,
            'two_tailed': two_tailed
        }
        
        self.results['sample_size'] = result
        return result
    
    def print_sample_size_summary(self):
        """Print formatted sample size calculation results"""
        if 'sample_size' not in self.results:
            print("No sample size calculation found. Run calculate_sample_size() first.")
            return
            
        r = self.results['sample_size']
        
        print("\n" + "="*60)
        print(f"SAMPLE SIZE CALCULATION: {self.experiment_name}")
        print("="*60)
        print(f"Baseline conversion rate: {r['baseline_rate']:.2%}")
        print(f"Treatment conversion rate: {r['treatment_rate']:.2%}")
        print(f"Minimum detectable effect: {r['minimum_detectable_effect']:.1%} relative")
        print(f"Absolute effect size: {r['absolute_effect']:.2%}")
        print(f"Significance level (α): {r['alpha']:.2%}")
        print(f"Statistical power (1-β): {r['power']:.0%}")
        print(f"Z-score (α): {r['z_alpha']:.3f}")
        print(f"Z-score (β): {r['z_beta']:.3f}")
        print("-" * 60)
        print(f"Required sample size per group: {r['n_per_group']:,} users")
        print(f"Total sample size needed: {r['total_sample_size']:,} users")
        print("="*60)
        
    def simulate_experiment(self, n_per_group, baseline_rate, treatment_rate, 
                           random_seed=42):
        """
        Simulate A/B test results
        
        Parameters:
        -----------
        n_per_group : int
            Number of users in each group
        baseline_rate : float
            True conversion rate for control group
        treatment_rate : float
            True conversion rate for treatment group
        random_seed : int
            Random seed for reproducibility
            
        Returns:
        --------
        dict: Experiment results including conversions and raw data
        """
        
        np.random.seed(random_seed)
        
        # Simulate control group
        control = np.random.binomial(1, baseline_rate, n_per_group)
        
        # Simulate treatment group
        treatment = np.random.binomial(1, treatment_rate, n_per_group)
        
        # Calculate metrics
        control_conversions = control.sum()
        treatment_conversions = treatment.sum()
        
        control_rate = control_conversions / n_per_group
        treatment_rate_observed = treatment_conversions / n_per_group
        
        absolute_difference = treatment_rate_observed - control_rate
        relative_improvement = absolute_difference / control_rate if control_rate > 0 else 0
        
        # Store results
        experiment_data = {
            'n_per_group': n_per_group,
            'control': control,
            'treatment': treatment,
            'control_conversions': control_conversions,
            'treatment_conversions': treatment_conversions,
            'control_rate': control_rate,
            'treatment_rate': treatment_rate_observed,
            'absolute_difference': absolute_difference,
            'relative_improvement': relative_improvement
        }
        
        self.results['experiment_data'] = experiment_data
        return experiment_data
    
    def analyze_results(self, alpha=0.05):
        """
        Perform statistical analysis on experiment results
        
        Parameters:
        -----------
        alpha : float
            Significance level for confidence intervals
            
        Returns:
        --------
        dict: Statistical test results
        """
        
        if 'experiment_data' not in self.results:
            print("No experiment data found. Run simulate_experiment() first.")
            return
            
        d = self.results['experiment_data']
        
        # Extract data
        control = d['control']
        treatment = d['treatment']
        n_control = len(control)
        n_treatment = len(treatment)
        
        # Calculate conversion counts
        x_control = d['control_conversions']
        x_treatment = d['treatment_conversions']
        
        # Conversion rates
        p_control = x_control / n_control
        p_treatment = x_treatment / n_treatment
        
        # Pooled proportion for standard error
        p_pooled = (x_control + x_treatment) / (n_control + n_treatment)
        
        # Standard error
        se = math.sqrt(p_pooled * (1 - p_pooled) * (1/n_control + 1/n_treatment))
        
        # Z-statistic
        z_stat = (p_treatment - p_control) / se if se > 0 else 0
        
        # P-value (two-tailed)
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        
        # Confidence interval for difference
        z_critical = stats.norm.ppf(1 - alpha/2)
        me = z_critical * se
        ci_lower = (p_treatment - p_control) - me
        ci_upper = (p_treatment - p_control) + me
        
        # Chi-square test (alternative method)
        contingency_table = np.array([[x_control, n_control - x_control],
                                      [x_treatment, n_treatment - x_treatment]])
        chi2, p_value_chi2, _, _ = stats.chi2_contingency(contingency_table, correction=False)
        
        # Determine if result is statistically significant
        is_significant = p_value < alpha
        
        # Power calculation for observed effect
        # This is the post-hoc power
        effect_size = abs(p_treatment - p_control) / math.sqrt(p_pooled * (1 - p_pooled))
        observed_power = self._calculate_power(effect_size, n_control, n_treatment, alpha)
        
        # Store analysis results
        analysis = {
            'control_rate': p_control,
            'treatment_rate': p_treatment,
            'difference': p_treatment - p_control,
            'relative_improvement': (p_treatment - p_control) / p_control if p_control > 0 else 0,
            'standard_error': se,
            'z_statistic': z_stat,
            'p_value': p_value,
            'p_value_chi2': p_value_chi2,
            'is_significant': is_significant,
            'confidence_level': 1 - alpha,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'observed_power': observed_power,
            'alpha': alpha
        }
        
        self.results['analysis'] = analysis
        return analysis
    
    def _calculate_power(self, effect_size, n1, n2, alpha):
        """Calculate statistical power for given parameters"""
        # Approximate power calculation
        n = (n1 + n2) / 2
        se = math.sqrt(2 / n)  # Simplified
        z_alpha = stats.norm.ppf(1 - alpha/2)
        z_beta = effect_size / se - z_alpha
        power = stats.norm.cdf(z_beta)
        return max(0, min(1, power))  # Clamp between 0 and 1
    
    def print_results_summary(self):
        """Print formatted experiment results"""
        if 'analysis' not in self.results:
            print("No analysis found. Run analyze_results() first.")
            return
            
        a = self.results['analysis']
        d = self.results.get('experiment_data', {})
        
        print("\n" + "="*60)
        print(f"EXPERIMENT RESULTS: {self.experiment_name}")
        print("="*60)
        print(f"\n📊 CONVERSION RATES:")
        print(f"   Control group:    {a['control_rate']:.2%} ({d.get('control_conversions', 0)} / {d.get('n_per_group', 0)})")
        print(f"   Treatment group:  {a['treatment_rate']:.2%} ({d.get('treatment_conversions', 0)} / {d.get('n_per_group', 0)})")
        print(f"\n📈 EFFECT SIZE:")
        print(f"   Absolute difference:  {a['difference']:+.2%}")
        print(f"   Relative improvement: {a['relative_improvement']:+.2%}")
        print(f"\n🔬 STATISTICAL SIGNIFICANCE:")
        print(f"   Z-statistic:     {a['z_statistic']:.3f}")
        print(f"   P-value:         {a['p_value']:.4f}")
        print(f"   Significant at α={a['alpha']}: {a['is_significant']}")
        print(f"\n📏 CONFIDENCE INTERVAL ({a['confidence_level']:.0%}):")
        print(f"   [{a['ci_lower']:.2%}, {a['ci_upper']:.2%}]")
        print(f"\n⚡ OBSERVED POWER: {a['observed_power']:.1%}")
        print("="*60)
        
        # Recommendation
        print("\n💡 RECOMMENDATION:")
        if a['is_significant'] and a['difference'] > 0:
            print("   ✅ The treatment performs BETTER than control. Consider implementing.")
        elif a['is_significant'] and a['difference'] < 0:
            print("   ❌ The treatment performs WORSE than control. Do not implement.")
        elif not a['is_significant'] and a['difference'] > 0:
            print("   ⚠️  Positive trend but NOT statistically significant. Consider running longer or increasing sample size.")
        else:
            print("   ℹ️  No significant difference detected. Keep current version.")
        print("="*60)
    
    def plot_results(self, save_path=None):
        """Create visualizations of experiment results"""
        
        if 'analysis' not in self.results:
            print("No analysis found. Run analyze_results() first.")
            return
        
        a = self.results['analysis']
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. Conversion rates bar chart
        ax1 = axes[0, 0]
        groups = ['Control', 'Treatment']
        rates = [a['control_rate'], a['treatment_rate']]
        colors = ['#3498db', '#2ecc71']
        bars = ax1.bar(groups, rates, color=colors, alpha=0.7, edgecolor='black', linewidth=1)
        ax1.set_ylabel('Conversion Rate', fontsize=12)
        ax1.set_title('Conversion Rates by Group', fontsize=14, fontweight='bold')
        ax1.set_ylim(0, max(rates) * 1.2)
        
        # Add value labels on bars
        for bar, rate in zip(bars, rates):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                    f'{rate:.2%}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # 2. Difference with confidence interval
        ax2 = axes[0, 1]
        diff = a['difference']
        ci_lower = a['ci_lower']
        ci_upper = a['ci_upper']
        
        ax2.errorbar(0, diff, yerr=[[diff - ci_lower], [ci_upper - diff]], 
                    fmt='o', color='#e74c3c', capsize=10, markersize=10, markeredgecolor='black')
        ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.7)
        ax2.set_xlim(-1, 1)
        ax2.set_xticks([])
        ax2.set_ylabel('Difference in Conversion Rate', fontsize=12)
        ax2.set_title('Treatment Effect with 95% CI', fontsize=14, fontweight='bold')
        
        # Color the confidence interval based on significance
        if a['is_significant'] and diff > 0:
            ax2.text(0, diff + 0.01, '✅ Significant Positive', ha='center', fontsize=12, color='green')
        elif a['is_significant'] and diff < 0:
            ax2.text(0, diff - 0.01, '❌ Significant Negative', ha='center', fontsize=12, color='red')
        else:
            ax2.text(0, diff + 0.01, '⚪ Not Significant', ha='center', fontsize=12, color='gray')
        
        # 3. Distribution comparison
        ax3 = axes[1, 0]
        if 'experiment_data' in self.results:
            d = self.results['experiment_data']
            
            # Create data for histogram (conversion as 0/1)
            control_data = d['control']
            treatment_data = d['treatment']
            
            # Add jitter for better visualization
            control_jitter = control_data + np.random.normal(0, 0.05, len(control_data))
            treatment_jitter = treatment_data + np.random.normal(0, 0.05, len(treatment_data))
            
            # Strip plot
            ax3.scatter(control_jitter, [1]*len(control_jitter), alpha=0.3, color='#3498db', label='Control', s=30)
            ax3.scatter(treatment_jitter, [2]*len(treatment_jitter), alpha=0.3, color='#2ecc71', label='Treatment', s=30)
            
            ax3.set_yticks([1, 2])
            ax3.set_yticklabels(['Control', 'Treatment'])
            ax3.set_xlabel('Conversion (0 = No, 1 = Yes)', fontsize=12)
            ax3.set_title('Individual Conversions by Group', fontsize=14, fontweight='bold')
            ax3.set_xlim(-0.2, 1.2)
            ax3.legend()
        
        # 4. Power analysis curve
        ax4 = axes[1, 1]
        
        # Generate power curve
        effect_sizes = np.linspace(0, 0.15, 50)
        powers = []
        n_per_group = len(self.results['experiment_data']['control']) if 'experiment_data' in self.results else 1000
        
        for es in effect_sizes:
            if 'experiment_data' in self.results:
                # Approximate power calculation
                se = math.sqrt(2 * 0.1 * 0.9 / n_per_group)  # Rough estimate
                z_alpha = stats.norm.ppf(1 - 0.05/2)
                z_beta = es / se - z_alpha
                power = stats.norm.cdf(z_beta)
                powers.append(power)
        
        ax4.plot(effect_sizes * 100, powers, linewidth=3, color='#9b59b6')
        ax4.axhline(y=0.8, color='gray', linestyle='--', alpha=0.7, label='80% Power')
        ax4.axvline(x=abs(a['difference']) * 100, color='red', linestyle='--', alpha=0.7, 
                   label=f'Observed Effect: {abs(a["difference"]):.2%}')
        ax4.set_xlabel('Effect Size (%)', fontsize=12)
        ax4.set_ylabel('Statistical Power', fontsize=12)
        ax4.set_title('Power Analysis Curve', fontsize=14, fontweight='bold')
        ax4.set_ylim(0, 1)
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=100, bbox_inches='tight')
            print(f"Plot saved to: {save_path}")
        
        plt.show()
        return fig
    
    def export_report(self, filename="ab_test_report.csv"):
        """Export results to CSV"""
        
        if 'analysis' not in self.results:
            print("No analysis found. Run analyze_results() first.")
            return
        
        a = self.results['analysis']
        d = self.results.get('experiment_data', {})
        
        report_data = {
            'Metric': [
                'Experiment Name',
                'Control Conversions',
                'Treatment Conversions',
                'Control Rate',
                'Treatment Rate',
                'Absolute Difference',
                'Relative Improvement',
                'P-Value',
                'Statistically Significant',
                'Confidence Level',
                'CI Lower',
                'CI Upper',
                'Observed Power'
            ],
            'Value': [
                self.experiment_name,
                d.get('control_conversions', 0),
                d.get('treatment_conversions', 0),
                f"{a['control_rate']:.2%}",
                f"{a['treatment_rate']:.2%}",
                f"{a['difference']:+.2%}",
                f"{a['relative_improvement']:+.2%}",
                f"{a['p_value']:.4f}",
                'Yes' if a['is_significant'] else 'No',
                f"{a['confidence_level']:.0%}",
                f"{a['ci_lower']:.2%}",
                f"{a['ci_upper']:.2%}",
                f"{a['observed_power']:.1%}"
            ]
        }
        
        df = pd.DataFrame(report_data)
        df.to_csv(f"../results/{filename}", index=False)
        print(f"Report exported to results/{filename}")
        return df


# ======================================================
# EXAMPLE USAGE
# ======================================================

def run_ab_test_example():
    """Run a complete A/B testing example"""
    
    print("\n" + "🚀"*30)
    print("🚀  A/B TESTING SIMULATION EXAMPLE")
    print("🚀"*30 + "\n")
    
    # Initialize simulator
    ab_test = ABTestingSimulator("Website Redesign Test")
    
    # Step 1: Calculate required sample size
    print("\n📐 STEP 1: CALCULATE SAMPLE SIZE")
    print("-" * 40)
    
    baseline = 0.12  # 12% current conversion
    mde = 0.15       # Want to detect 15% improvement
    
    sample_size = ab_test.calculate_sample_size(
        baseline_rate=baseline,
        minimum_detectable_effect=mde,
        alpha=0.05,
        power=0.8
    )
    
    ab_test.print_sample_size_summary()
    
    # Step 2: Run the experiment
    print("\n\n🧪 STEP 2: RUN EXPERIMENT")
    print("-" * 40)
    
    # Treatment rate (15% improvement)
    treatment_rate = baseline * (1 + mde)
    
    experiment_data = ab_test.simulate_experiment(
        n_per_group=sample_size['n_per_group'],
        baseline_rate=baseline,
        treatment_rate=treatment_rate,
        random_seed=42
    )
    
    print(f"✓ Experiment completed with {sample_size['n_per_group']:,} users per group")
    
    # Step 3: Analyze results
    print("\n📊 STEP 3: STATISTICAL ANALYSIS")
    print("-" * 40)
    
    analysis = ab_test.analyze_results(alpha=0.05)
    
    ab_test.print_results_summary()
    
    # Step 4: Visualize
    print("\n📈 STEP 4: VISUALIZATION")
    print("-" * 40)
    
    ab_test.plot_results(save_path="../results/ab_test_visualization.png")
    
    # Step 5: Export report
    print("\n📁 STEP 5: EXPORT REPORT")
    print("-" * 40)
    
    ab_test.export_report("ab_test_results.csv")
    
    print("\n" + "✅"*30)
    print("✅  A/B TESTING EXAMPLE COMPLETE")
    print("✅"*30 + "\n")
    
    return ab_test


# ======================================================
# MULTIPLE SCENARIO SIMULATION
# ======================================================

def simulate_multiple_scenarios():
    """Run multiple A/B test scenarios to demonstrate different outcomes"""
    
    scenarios = [
        {"name": "Strong Positive", "baseline": 0.10, "effect": 0.30, "n": 5000},
        {"name": "Moderate Positive", "baseline": 0.10, "effect": 0.15, "n": 5000},
        {"name": "No Effect", "baseline": 0.10, "effect": 0.00, "n": 5000},
        {"name": "Negative Effect", "baseline": 0.10, "effect": -0.10, "n": 5000},
        {"name": "Underpowered", "baseline": 0.05, "effect": 0.10, "n": 1000},
    ]
    
    results = []
    
    for scenario in scenarios:
        print(f"\n📊 Testing: {scenario['name']}")
        
        test = ABTestingSimulator(scenario['name'])
        
        # Calculate treatment rate
        treatment_rate = scenario['baseline'] * (1 + scenario['effect'])
        
        # Run experiment
        test.simulate_experiment(
            n_per_group=scenario['n'],
            baseline_rate=scenario['baseline'],
            treatment_rate=treatment_rate,
            random_seed=42
        )
        
        # Analyze
        analysis = test.analyze_results()
        
        # Store results
        results.append({
            'Scenario': scenario['name'],
            'True Effect': f"{scenario['effect']:+.1%}",
            'Control Rate': f"{analysis['control_rate']:.2%}",
            'Treatment Rate': f"{analysis['treatment_rate']:.2%}",
            'Observed Effect': f"{analysis['difference']:+.2%}",
            'P-Value': f"{analysis['p_value']:.4f}",
            'Significant': '✅' if analysis['is_significant'] else '❌',
            'Sample Size': scenario['n']
        })
    
    # Create results dataframe
    df_results = pd.DataFrame(results)
    df_results.to_csv('../results/multiple_scenarios.csv', index=False)
    
    print("\n" + "="*60)
    print("MULTIPLE SCENARIO RESULTS")
    print("="*60)
    print(df_results.to_string(index=False))
    print("="*60)
    
    return df_results


# ======================================================
# MAIN EXECUTION
# ======================================================

if __name__ == "__main__":
    
    # Run the main example
    result = run_ab_test_example()
    
    # Uncomment to run multiple scenarios
    # scenarios = simulate_multiple_scenarios()
    
    print("\n💡 TIPS FOR INTERPRETING RESULTS:")
    print("-" * 40)
    print("• P-value < 0.05 indicates statistical significance")
    print("• Confidence interval shows range of plausible effects")
    print("• Power > 80% means test was well-designed")
    print("• Consider practical significance, not just statistical")
    print("• Always validate assumptions (random assignment, independence)")