import matplotlib.pyplot as plt
import numpy as np

font_size_xticks = 24
font_size_yticks = 24
font_xlabel = {'family' : 'serif',
'weight' : 'bold',
'size'   : 28,
}
font_ylabel = {'family' : 'serif',
'weight' : 'bold',
'size'   : 28,
}
font_lengend = {'family' : 'serif',
'weight' : 'bold',
'size'   : 24,
}

LINE_WIDTH = 2
MARKER_SIZE = 15

# 1. Data Preparation
sm_counts = np.array([10, 15, 20, 25, 30])
total_sm = 82

# Baseline (Average)
# baseline_raw = np.array([5997.45, 5993.42, 6010.96, 5997.20, 5995.42])
baseline_raw = np.array([6150, 6150, 6150, 6150, 6150])  # Fixed frequency baseline
baseline_raw = baseline_raw / 1000  # Convert to seconds
avg_baseline = np.mean(baseline_raw)  # Already in seconds
baseline_latency = np.full_like(sm_counts, avg_baseline, dtype=float)
baseline_latency = baseline_latency.astype(float)

# Measured Data (Interference)
interference_latency_increase_ratio = np.array([0.1492, 0.2492, 0.3669, 0.5493, 0.7837])
interference_latency = baseline_latency * (1 + interference_latency_increase_ratio)
# interference_latency = np.array([6811.05, 7404.77, 8125.54, 9172.89, 10331.18]) / 1000  # Convert to seconds

# Theoretical Calculation
theoretical_latency_increase_ratio = np.array([0.1378, 0.2248, 0.3185, 0.4359, 0.5675])
theoretical_latency = baseline_latency * (1 + theoretical_latency_increase_ratio)
# theoretical_latency = avg_baseline * (total_sm / (total_sm - sm_counts))  # Already in seconds
print("Theoretical Latency (s):", theoretical_latency)
# Calculate Percentages
actual_increase_pct = (interference_latency - avg_baseline) / avg_baseline * 100
theo_increase_pct = (theoretical_latency - avg_baseline) / avg_baseline * 100
base_increase_pct = (baseline_latency - avg_baseline) / avg_baseline * 100

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
# color_measure = '#D62728'  # Red
# color_theory = '#1F77B4'   # Blue
color_measure = '#FF6B6B'  # Lighter Red (Pastel Red 或者是更柔和一点的红色)
color_theory = '#4D96FF'   # Lighter Blue (Soft Blue)
color_base = '#2CA02C'     # Green

# 3. Plotting Lines

# A. Baseline
print("Baseline Increase Percentages (%):", base_increase_pct)
plt.plot(sm_counts, base_increase_pct, linestyle='--', color=color_base, linewidth=LINE_WIDTH,
         label='Baseline (Full SMs)')

# B. Idle Reserved (Parallelism Loss / Resource Occupancy)
plt.plot(sm_counts, theo_increase_pct, marker='^', markersize=MARKER_SIZE, linestyle='-.',
         color=color_theory, linewidth=LINE_WIDTH, label='Reserved SMs (Idle)')

# C. Comm Reserved (Parallelism Loss + Interference / Contention)
plt.plot(sm_counts, actual_increase_pct, marker='s', markersize=MARKER_SIZE, linestyle='-',
         color=color_measure, linewidth=LINE_WIDTH, label='Reserved SMs (Comm.)')
# 4. Fill Between (Visual only, no legend)
# Note: label is omitted so it doesn't appear in the legend
# plt.fill_between(sm_counts, theoretical_latency, interference_latency,
#                  color='orange', alpha=0.15, hatch='//', edgecolor='orange')

plt.fill_between(sm_counts, theo_increase_pct, actual_increase_pct,
                 color=color_measure, alpha=0.15, hatch='//', edgecolor='none')
# 添加文字说明
plt.text(25.7, 50.5, 
         "Resource Contention", ha='center', va='center',
          fontsize=font_xlabel['size']+5, color='black', alpha=0.8,
         family='serif', weight='bold',
         rotation=27,
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1))

# Region A: Parallelism Loss (Green Baseline -> Blue Theoretical)
# 这一块展示的是：仅仅因为 SM 变少导致的必然延时增加
plt.fill_between(sm_counts, base_increase_pct, theo_increase_pct,
                 color=color_theory, alpha=0.1, hatch='\\', edgecolor='none')
# 添加文字说明 (可选，如果图比较挤可以在图例里说明，或者用箭头)
plt.text(21, 13, 
         "Parallelism Loss",
          ha='center',
          va='center',
          fontsize=font_xlabel['size']+5,
          color='black', alpha=0.8,
          family='serif', weight='bold',
          bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1))

# 5. Annotations (Dual Labeling)

# for i in range(len(sm_counts)):
#     # 5.1 Measured Annotation (Above the red point)
#     # Using bold font to emphasize the experimental result
#     plt.text(sm_counts[i], interference_latency[i] + 0.15,
#              f"+{actual_increase_pct[i]:.1f}%",
#              ha='center', va='bottom', fontsize=font_size_xticks-4,
#              color=color_measure, fontweight='bold')

#     # 5.2 Theoretical Annotation (Below the blue point)
#     # Using a slightly smaller font and "Theory" prefix for clarity
#     # Added negative offset (-300) to push text down
#     plt.text(sm_counts[i], theoretical_latency[i] - 0.3,
#              f"+{theo_increase_pct[i]:.1f}%",
#              ha='center', va='top', fontsize=font_size_xticks-4,
#              color=color_theory, fontweight='bold')

# 6. Axes and Layout
# plt.xlabel('Number of Dedicated Communication SMs(Total SMs: 82)', fontsize=12)
plt.xlabel('# Reserved SMs for Communication (Total SMs: 82)', fontdict=font_xlabel)

plt.ylabel('Computation Latency Increase (%)', fontdict=font_ylabel)
# plt.title('The Impact of SM Binding for Communication on Compute Performance(PCIe )', fontsize=13, weight='bold', pad=15)

plt.xticks( sm_counts, fontsize=font_size_xticks)
plt.yticks([0, 20, 40, 60, 80], ['0', '20', '40', '60', '80'], fontsize=font_size_yticks)
# Y-axis limit adjusted slightly to make room for bottom labels if needed
# plt.ylim(5.8, 11.2)
plt.grid(True, linestyle=':', alpha=0.6)

# Legend (Clean, only 3 entries)
# plt.legend(frameon=True, fancybox=False, edgecolor='black', framealpha=1, fontsize=10, loc='upper left')
plt.legend(prop=font_lengend, loc='upper center', bbox_to_anchor=(0.3, 0.92), ncol=1, edgecolor='black')

plt.tight_layout()
# plt.savefig('pcie.png', dpi=300, bbox_inches='tight')
dst_path = r'E:/Turbo-SIGCOMM-2026-Github/Turbo-2026-0126/Figure/PCIe-vs-NvLink/Figures/comm-influence-pcie-with-fixed-freq.pdf'
plt.savefig(dst_path, bbox_inches='tight')
plt.show()