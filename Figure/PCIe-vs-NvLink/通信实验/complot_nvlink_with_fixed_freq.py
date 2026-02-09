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
# Sorted by SM count: 10, 15, 20, 25, 30
sm_counts = np.array([10, 15, 20, 25, 30])
total_sm = 108  # Updated for A100

# Baseline Data (from your input)
baseline_raw = np.array([2386, 2386, 2386, 2386, 2386])
baseline_raw = baseline_raw.astype(float) / 1000
avg_baseline = np.mean(baseline_raw)
baseline_latency = np.full_like(sm_counts, avg_baseline, dtype=float)
baseline_latency_pct = (baseline_latency - avg_baseline) / avg_baseline * 100
# Measured Data (Interference)
# interference_latency = np.array([416.49, 458.28, 507.69, 571.92, 699.43]) / 1000  # Convert to seconds
interference_latency_increase_ratio = np.array([0.1061, 0.1672, 0.2504, 0.4358, 0.8141])
interference_latency = baseline_latency * (1 + interference_latency_increase_ratio)

# Theoretical Calculation
# Formula: Time_theo = Time_base * (Total / (Total - Removed))
theoretical_latency_increase_ratio = np.array([0.1013, 0.1618, 0.2263, 0.3029, 0.3834])
# theoretical_latency = avg_baseline * (total_sm / (total_sm - sm_counts))
theoretical_latency = baseline_latency * (1 + theoretical_latency_increase_ratio)
theo_increase_pct = (theoretical_latency - avg_baseline) / avg_baseline * 100
print("Theoretical Latency (s):", theoretical_latency)              
# Calculate Percentages
actual_increase_pct = (interference_latency - avg_baseline) / avg_baseline * 100
theo_increase_pct = (theoretical_latency - avg_baseline) / avg_baseline * 100

# 2. Setup Plot Style (Academic)
# plt.figure(figsize=(9, 6), dpi=300)
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
plt.plot(sm_counts, baseline_latency_pct, linestyle='--', color=color_base, linewidth=LINE_WIDTH,
         label='Baseline (Full SMs)')
plt.plot(sm_counts, theo_increase_pct, marker='^', markersize=MARKER_SIZE, linestyle='-.',
         color=color_theory, linewidth=LINE_WIDTH, label='Reserved SMs (Idle)')

# # C. Measured
plt.plot(sm_counts, actual_increase_pct, marker='s', markersize=MARKER_SIZE, linestyle='-',
         color=color_measure, linewidth=LINE_WIDTH, label='Reserved SMs (Comm.)')
# # 4. Fill Between (Visual only, no legend)
# # Note: label is omitted so it doesn't appear in the legend
# plt.fill_between(sm_counts, theoretical_latency, interference_latency,
#                  color='orange', alpha=0.15, hatch='//')


# Region B: Interference Overhead (Blue Theoretical -> Red Measured)
# 这一块展示的是：通信带来的额外干扰
plt.fill_between(sm_counts, theo_increase_pct, actual_increase_pct,
                 color=color_measure, alpha=0.15, hatch='//', edgecolor='none')
# 添加文字说明
plt.text(26, 38.4, 
         "Resource Contention",
          ha='center',
          va='center',
          fontsize=font_xlabel['size']+5,
          color='black', alpha=1,
         family='serif', weight='bold',
         rotation=22,
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1))

# Region A: Parallelism Loss (Green Baseline -> Blue Theoretical)
# 这一块展示的是：仅仅因为 SM 变少导致的必然延时增加
plt.fill_between(sm_counts, baseline_latency_pct, theo_increase_pct,
                 color=color_theory, alpha=0.1, hatch='\\', edgecolor='none')
# 添加文字说明 (可选，如果图比较挤可以在图例里说明，或者用箭头)
plt.text(21, 11, 
         "Parallelism Loss",
          ha='center',
          va='center',
          fontsize=font_xlabel['size']+5,
          color='black', alpha=1,
          family='serif', weight='bold',
          bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1))

# 5. Annotations (Dual Labeling)
# Adjusted offsets for the new scale (approx 300ms - 700ms range)

# for i in range(len(sm_counts)):
#     # 5.1 Measured Annotation (Above the red point)
#     # Offset adjusted from 150 to 15 because the data scale is much smaller now
#     plt.text(sm_counts[i], interference_latency[i] + 0.005,
#              f"+{actual_increase_pct[i]:.1f}%",
#              ha='center', va='bottom', fontsize=font_size_xticks-4,
#              color=color_measure, fontweight='bold')

#     # 5.2 Theoretical Annotation (Below the blue point)
#     # Offset adjusted from 300 to 25
#     plt.text(sm_counts[i], theoretical_latency[i] - 0.01,
#              f"+{theo_increase_pct[i]:.1f}%",
#              ha='center', va='top', fontsize=font_size_xticks-4,
#              color=color_theory, fontweight='bold')

# 6. Axes and Layout
plt.xlabel('# Reserved SMs for Communication (Total SMs: 108)', fontdict=font_xlabel)
plt.ylabel('Computation Latency Increase (%)', fontdict=font_ylabel)
# plt.title('Impact of SM Binding for Communication on Compute Performance (NVLink)', fontsize=font_xlabel['size'], weight='bold', pad=15)

plt.xticks(sm_counts, fontsize = font_size_xticks)
plt.yticks([0, 20, 40, 60, 80], ['0', '20', '40', '60', '80'], fontsize=font_size_yticks)
# Adjusted Y-axis limit for the new data range (300ms to ~800ms)
# plt.ylim(0.38, 0.7)
plt.grid(True, linestyle=':', alpha=0.6)

# Legend
# plt.legend(frameon=True, fancybox=False, edgecolor='black', framealpha=1, fontsize=10, loc='upper left')
plt.legend(prop=font_lengend, loc='upper center', bbox_to_anchor=(0.3, 0.92), ncol=1, edgecolor='black')

plt.tight_layout()
dst_path = r'E:/Turbo-SIGCOMM-2026-Github/Turbo-2026-0126/Figure/PCIe-vs-NvLink/Figures/comm-influence-nvlink-with-fixed-freq.pdf'
plt.savefig(dst_path, bbox_inches='tight')
plt.show()