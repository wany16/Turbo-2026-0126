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
# Sorted by SM count: 10, 15, 20, 25, 30
sm_counts = np.array([10, 15, 20, 25, 30])
total_sm = 108  # Updated for A100

# Baseline Data (from your input)
baseline_raw = np.array([381.43, 381.69, 383.96, 379.40, 383.61])
baseline_raw = baseline_raw.astype(float) / 1000
avg_baseline = np.mean(baseline_raw)
baseline_latency = np.full_like(sm_counts, avg_baseline, dtype=float)

# Measured Data (Interference)
interference_latency = np.array([416.49, 458.28, 507.69, 571.92, 699.43]) / 1000  # Convert to seconds

# Theoretical Calculation
# Formula: Time_theo = Time_base * (Total / (Total - Removed))
theoretical_latency = avg_baseline * (total_sm / (total_sm - sm_counts))
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
color_measure = '#D62728'  # Red
color_theory = '#1F77B4'   # Blue
color_base = '#2CA02C'     # Green

# 3. Plotting Lines

# A. Baseline
plt.plot(sm_counts, baseline_latency, linestyle='--', color=color_base, linewidth=LINE_WIDTH,
         label='Baseline (Full SMs)')
plt.plot(sm_counts, theoretical_latency, marker='^', markersize=9, linestyle='-.',
         color=color_theory, linewidth=LINE_WIDTH, label='Theoretical (Reduced Parallelism Only)')

# # C. Measured
plt.plot(sm_counts, interference_latency, marker='s', markersize=9, linestyle='-',
         color=color_measure, linewidth=LINE_WIDTH, label='Measured (With Comm. Interference)')
# # 4. Fill Between (Visual only, no legend)
# # Note: label is omitted so it doesn't appear in the legend
# plt.fill_between(sm_counts, theoretical_latency, interference_latency,
#                  color='orange', alpha=0.15, hatch='//')


# Region B: Interference Overhead (Blue Theoretical -> Red Measured)
# 这一块展示的是：通信带来的额外干扰
plt.fill_between(sm_counts, theoretical_latency, interference_latency,
                 color='#D62728', alpha=0.15, hatch='//', edgecolor='none')
# 添加文字说明
plt.text(25.5, 0.545, 
         "Resource Contention", ha='center', va='center', fontsize=font_xlabel['size'], color='black', alpha=0.8,
         family='serif', weight='bold',
         rotation=30)

# Region A: Parallelism Loss (Green Baseline -> Blue Theoretical)
# 这一块展示的是：仅仅因为 SM 变少导致的必然延时增加
plt.fill_between(sm_counts, baseline_latency, theoretical_latency,
                 color='#1F77B4', alpha=0.1, hatch='\\', edgecolor='none')
# 添加文字说明 (可选，如果图比较挤可以在图例里说明，或者用箭头)
plt.text(21, 0.42, 
         "Parallelism Loss",
          ha='center',
          va='center',
          fontsize=font_xlabel['size'],
          color='black', alpha=0.8,
          family='serif', weight='bold')

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
plt.xlabel('# Reserved SMs for Communication (Total SMs: 108)', fontsize=font_xlabel['size'])
plt.ylabel('Computation Latency (s)', fontsize=font_ylabel['size'])
# plt.title('Impact of SM Binding for Communication on Compute Performance (NVLink)', fontsize=font_xlabel['size'], weight='bold', pad=15)

plt.xticks(sm_counts, fontsize = font_size_xticks)
plt.yticks([0.3, 0.4, 0.5, 0.6, 0.7], ['0.3', '0.4', '0.5', '0.6', '0.7'], fontsize=font_size_yticks)

# Adjusted Y-axis limit for the new data range (300ms to ~800ms)
# plt.ylim(300, 850)
plt.grid(True, linestyle=':', alpha=0.6)

# Legend
# plt.legend(frameon=True, fancybox=False, edgecolor='black', framealpha=1, fontsize=10, loc='upper left')
plt.legend(prop=font_lengend, loc='upper center', bbox_to_anchor=(0.37, 1), ncol=1, edgecolor='black')

plt.tight_layout()
dst_path = r'E:/Turbo-Plot-Github-SIGCOMM-2026-0204/turbo/Figures/comm-influence-nvlink.pdf'
plt.savefig(dst_path, bbox_inches='tight')
plt.show()