import numpy as np
import matplotlib.pyplot as plt
#thanks chatgpt

file_path = 'data/PL.npz'
data = np.load(file_path)

boolean_matrix = data['matrix']
header = data['header']

plt.figure(figsize=(20, 10))
plt.imshow(boolean_matrix, aspect='auto', cmap='pink')

plt.colorbar(label='Boolean Value')
plt.title('PL heatmap')
plt.xlabel('Columns')
plt.ylabel('Rows')
plt.show()
