import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import matplotlib.ticker as ticker

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 28,
    'axes.labelsize': 21,
    'axes.titlesize': 22,
    'xtick.labelsize': 21,
    'ytick.labelsize': 21,
    'legend.fontsize': 18,
})

m1_labels = np.array([3, 4, 5, 6, 7, 8])
m2_labels = np.array([8, 7, 6, 5])

# #llama的数据
# raw_data_input = np.array([
#     [0.004209, 0.004209, 0.004209, 0.004768, 0.01356, 0.060459],
#     [0.003436, 0.003447, 0.003429, 0.003766, 0.015904, 0.063513],
#     [0.009897, 0.00994, 0.009473, 0.007418, 0.018025, 0.06893],
#     [0.696359, 0.696359, 0.694132, 0.596996, 0.188634, 0.179552],
# ])

#gpt的数据
# '''
raw_data_input = np.array([
    [0.000067, 0.000067, 0.000067, 0.000072, 0.06236, 0.162255],
    [0.000129, 0.000129, 0.000124, 0.000129, 0.067755, 0.161227],
    [0.000464, 0.000464, 0.000447, 0.000444, 0.059672, 0.243838],
    [0.00238, 0.00238, 0.002403, 0.002936, 0.046286, 0.200164],
])
# '''
#qwen的数据
'''
raw_data_input = np.array([
    [0.005711, 0.005711, 0.005711, 0.005711, 0.005707, 0.005704],
    [0.008178, 0.008178, 0.008178, 0.008176, 0.007958, 0.006689],
    [0.028762, 0.028762, 0.028304, 0.029816, 0.026506, 0.019834],
    [0.809622, 0.809622, 0.81335, 0.858694, 0.634436, 0.278914]
])
'''

raw_data = raw_data_input[:, ::-1]

x_indices = np.arange(len(m1_labels))
y_indices = np.arange(len(m2_labels))
x_mesh, y_mesh = np.meshgrid(x_indices, y_indices)

x = x_mesh.flatten()
y = y_mesh.flatten()
values = raw_data.flatten()
mask = ~np.isnan(values)
x, y, values = x[mask], y[mask], values[mask]

log_values = np.log10(values)
z_base = -5
z = np.full_like(log_values, z_base)
dz = log_values - z_base
dx = 0.4
dy = 0.4


fig = plt.figure(figsize=(6, 5))
ax = fig.add_subplot(111, projection='3d')

norm = plt.Normalize(log_values.min(), log_values.max())
colors = cm.Wistia(norm(log_values))

ax.bar3d(x, y, z, dx, dy, dz, color=colors, shade=True, linewidth=0.5, edgecolor='gray')

ax.set_xlabel(r'$m_1$', labelpad=15)
ax.set_xticks(x_indices + dx / 2)
ax.set_xticklabels(m1_labels)

ax.set_ylabel(r'$m_2$', labelpad=15)
ax.set_yticks(y_indices + dy / 2)
ax.set_yticklabels(m2_labels)

z_tick_locations = np.array([-5, -4, -3, -2, -1, 0])
ax.set_zticks(z_tick_locations)
def log_tick_formatter(val, pos=None):
    return f"${{{int(val)}}}$"
ax.zaxis.set_major_formatter(ticker.FuncFormatter(log_tick_formatter))

ax.set_zlabel('KL Divergence (Log)', labelpad=10, rotation=90)
#ax.set_title('GPT-2 Small')
ax.set_zlim(-5, 0)

ax.view_init(elev=25, azim=-60)

# ax.zaxis.set_rotate_label(False)
ax.set_box_aspect((1, 1, 0.6))

ax.dist = 7

# 删除这一行（它是问题根源之一）：
# plt.subplots_adjust(left=0.0, right=0.9, bottom=0.0, top=1.0)

# 在 plt.savefig 之前，添加：
# plt.tight_layout(rect=[0.02, 0.02, 0.98, 0.98])  # 可选微调
fig.subplots_adjust(left=0.0, bottom=0.0, right=0.85, top=1.0)
# fig.subplots_adjust(right=0.12)  # ← 关键！只为左侧留出空间给 z-label

# plt.subplots_adjust(left=0.0, right=0.9, bottom=0.0, top=1.0)

#plt.savefig('tablellama.png', dpi=300, bbox_inches='tight', pad_inches=0.6)
dst_path = r'E:/Turbo-SIGCOMM-2026-Github/Turbo-2026-0126/Figure/PCIe-vs-NvLink/Figures/m1m2-gpt-001.pdf'
plt.savefig(dst_path)
plt.show()