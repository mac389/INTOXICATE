
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


data = pd.read_csv('synthetic_patients_1.csv')

fig, axes = plt.subplots(1, 3, figsize=(18, 5))


# Plot 1: Age
sns.histplot(data['age'], kde=True, color='teal', ax=axes[0])
axes[0].set_title('Distribution of Age')
axes[0].set_xlabel('Age')
axes[0].set_ylabel('Frequency')

# Plot 2: Heart Rate
sns.histplot(data['hr'], kde=True, color='orange', ax=axes[1])
axes[1].set_title('Distribution of Heart Rate')
axes[1].set_xlabel('Heart Rate')
axes[1].set_ylabel('Frequency')

# Plot 3: SBP
sns.histplot(data['sbp'], kde=True, color='orange', ax=axes[2])
axes[2].set_title('Distribution of Systolic BP')
axes[2].set_xlabel('SBP')
axes[2].set_ylabel('Frequency')

plt.tight_layout()
plt.savefig('results/multiple_histograms.png')  # Save to file
plt.show()







