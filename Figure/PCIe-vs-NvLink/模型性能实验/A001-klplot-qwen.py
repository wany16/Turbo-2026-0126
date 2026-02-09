import matplotlib.pyplot as plt
import numpy as np

font_size_xticks = 30
font_size_yticks = 30
font_xlabel = {'family' : 'serif',
'weight' : 'bold',
'size'   : 32,
}
font_ylabel = {'family' : 'serif',
'weight' : 'bold',
'size'   : 32,
}
font_lengend = {'family' : 'serif',
'weight' : 'bold',
'size'   : 30,
}

LINE_WIDTH = 2

# #llama的数据
# tokens = ['512', '768', '1024', '1280', '1536', '1792', '2048']
# # tokens = ['512', '768, 1024, 1280, 1536, 1792, 2048]
# turbo_data = [0.004751, 0.004359, 0.004209, 0.003931, 0.004546, 0.004997, 0.005067]
# int8_data = [0.003955, 0.002925, 0.002762, 0.002877, 0.003168, 0.003407, 0.004514]

#gpt的数据
'''
tokens = ['512', '768', '1024']
turbo_data = [0.000132, 0.000087, 0.000067]
int8_data = [0.000232, 0.000159, 0.000122]
'''
#qwen的数据
# '''
tokens = ['512', '768', '1024', '1280', '1536', '1792', '2048']
turbo_data = [0.012496, 0.007767, 0.005711, 0.00501, 0.004933, 0.0052, 0.005898]
int8_data = [0.024954, 0.016498, 0.012746, 0.011167, 0.010572, 0.016689, 0.021613]
# '''
x = np.arange(len(tokens))
width = 0.35

plt.figure(figsize=(12, 7))

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True

rects2 = plt.bar(x - width/2, int8_data, width, hatch='\\', label='INT8 Quantization', color='#1f77b4', edgecolor='black')
rects1 = plt.bar(x + width/2, turbo_data, width, hatch='/', label='Turbo', color='none', edgecolor='red')


plt.axhline(y=0.05, color='green', linestyle='-.', linewidth=1.5, alpha=0.8, label='Negligible Loss Threshold')

plt.xlabel('Context Length', fontdict=font_xlabel)
plt.ylabel('KL Divergence', fontdict=font_ylabel)
#plt.title('Llama 2 7B', fontsize=32, fontweight='bold')
plt.xticks(x, tokens, fontsize=font_size_xticks)
plt.yticks(fontsize=font_size_yticks)
# plt.legend(loc='upper right', bbox_to_anchor=(1.0, 0.9), fontsize=30, frameon=True)
plt.legend(prop=font_lengend, loc='upper center', bbox_to_anchor=(0.35, 0.92), ncol=1, edgecolor='black')

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.annotate(f'{height:.4f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=font_size_yticks)

plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
dst_path = r'E:/Turbo-SIGCOMM-2026-Github/Turbo-2026-0126/Figure/PCIe-vs-NvLink/Figures/kl-qwen-001.pdf'
plt.savefig(dst_path, bbox_inches='tight')
plt.show()