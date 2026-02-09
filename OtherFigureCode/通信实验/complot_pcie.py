import matplotlib.pyplot as plt
import numpy as np

font_size_xticks = 24
font_size_yticks = 24
font_xlabel = {'family' : 'serif',
'weight' : 'bold',
'size'   : 24,
}
font_ylabel = {'family' : 'serif',
'weight' : 'bold',
'size'   : 24,
}
font_lengend = {'family' : 'serif',
'weight' : 'bold',
'size'   : 24,
}

LINE_WIDTH = 2

# 1. Data Preparation
sm_counts = np.array([10, 15, 20, 25, 30])
total_sm = 82

# Baseline (Average)
baseline_raw = np.array([5997.45, 5993.42, 6010.96, 5997.20, 5995.42])
baseline_raw = baseline_raw / 1000  # Convert to seconds
avg_baseline = np.mean(baseline_raw)  # Already in seconds
baseline_latency = np.full_like(sm_counts, avg_baseline, dtype=float)
baseline_latency = baseline_latency.astype(float)

# Measured Data (Interference)
interference_latency = np.array([6811.05, 7404.77, 8125.54, 9172.89, 10331.18]) / 1000  # Convert to seconds

# Theoretical Calculation
theoretical_latency = avg_baseline * (total_sm / (total_sm - sm_counts))  # Already in seconds
print("Theoretical Latency (s):", theoretical_latency)
# Calculate Percentages
actual_increase_pct = (interference_latency - avg_baseline) / avg_baseline * 100
theo_increase_pct = (theoretical_latency - avg_baseline) / avg_baseline * 100

# 2. Setup Plot Style (Academic)    
fig, ax = plt.subplots(figsize=(11, 8))

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True

# Colors
color_measure = '#D62728'  # Red
color_theory = '#1F77B4'   # Blue
color_base = '#2CA02C'     # Green

# 3. Plotting Lines

# A. Baseline
plt.plot(sm_counts, baseline_latency, linestyle='--', color=color_base, linewidth=LINE_WIDTH,
         label='Baseline (Full SMs)')
plt.plot(sm_counts, theoretical_latency, marker='^', markersize=9, linestyle='-.',
         color=color_theory, linewidth=LINE_WIDTH, label='Theoretical (Reduced Parallelism Only)')

# C. Measured
plt.plot(sm_counts, interference_latency, marker='s', markersize=9, linestyle='-',
         color=color_measure, linewidth=LINE_WIDTH, label='Measured (With Comm. Interference)')
# 4. Fill Between (Visual only, no legend)
# Note: label is omitted so it doesn't appear in the legend
# plt.fill_between(sm_counts, theoretical_latency, interference_latency,
#                  color='orange', alpha=0.15, hatch='//', edgecolor='orange')

plt.fill_between(sm_counts, theoretical_latency, interference_latency,
                 color='#D62728', alpha=0.15, hatch='//', edgecolor='none')
# 添加文字说明
plt.text(25.7, 9, 
         "Resource Contention", ha='center', va='center', fontsize=font_xlabel['size'], color='black', alpha=0.8,
         family='serif', weight='bold',
         rotation=26)

# Region A: Parallelism Loss (Green Baseline -> Blue Theoretical)
# 这一块展示的是：仅仅因为 SM 变少导致的必然延时增加
plt.fill_between(sm_counts, baseline_latency, theoretical_latency,
                 color='#1F77B4', alpha=0.1, hatch='\\', edgecolor='none')
# 添加文字说明 (可选，如果图比较挤可以在图例里说明，或者用箭头)
plt.text(21, 7, 
         "Parallelism Loss",
          ha='center',
          va='center',
          fontsize=font_xlabel['size'],
          color='black', alpha=0.8,
          family='serif', weight='bold')

# 5. Annotations (Dual Labeling)

for i in range(len(sm_counts)):
    # 5.1 Measured Annotation (Above the red point)
    # Using bold font to emphasize the experimental result
    plt.text(sm_counts[i], interference_latency[i] + 0.15,
             f"+{actual_increase_pct[i]:.1f}%",
             ha='center', va='bottom', fontsize=font_size_xticks-4,
             color=color_measure, fontweight='bold')

    # 5.2 Theoretical Annotation (Below the blue point)
    # Using a slightly smaller font and "Theory" prefix for clarity
    # Added negative offset (-300) to push text down
    plt.text(sm_counts[i], theoretical_latency[i] - 0.3,
             f"+{theo_increase_pct[i]:.1f}%",
             ha='center', va='top', fontsize=font_size_xticks-4,
             color=color_theory, fontweight='bold')

# 6. Axes and Layout
# plt.xlabel('Number of Dedicated Communication SMs(Total SMs: 82)', fontsize=12)
plt.xlabel('# Reserved SMs for Communication (Total SMs: 82)', fontdict=font_xlabel)

plt.ylabel('Computation Latency (Second)', fontdict=font_ylabel)
# plt.title('The Impact of SM Binding for Communication on Compute Performance(PCIe )', fontsize=13, weight='bold', pad=15)

plt.xticks( sm_counts, fontsize=font_size_xticks)
plt.yticks([6, 8, 10], ['6', '8', '10'], fontsize=font_size_yticks)
# Y-axis limit adjusted slightly to make room for bottom labels if needed
plt.ylim(5.5, 11)
plt.grid(True, linestyle=':', alpha=0.6)

# Legend (Clean, only 3 entries)
# plt.legend(frameon=True, fancybox=False, edgecolor='black', framealpha=1, fontsize=10, loc='upper left')
plt.legend(prop=font_lengend, loc='upper center', bbox_to_anchor=(0.39, 1), ncol=1, edgecolor='black')

plt.tight_layout()
# plt.savefig('pcie.png', dpi=300, bbox_inches='tight')
dst_path = r'E:/Turbo-Plot-Github-SIGCOMM-2026-0204/turbo/Figures/comm-influence-pcie-without-fixed-freq.pdf'
plt.savefig(dst_path, bbox_inches='tight')
plt.show()