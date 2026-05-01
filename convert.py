import os
import pandas as pd
from scipy.io import arff

# Load file
data, meta = arff.loadarff(r'C:\Users\Cypher\3D Objects\projects\zipped\phishing+websites\Training Dataset.arff')
df = pd.DataFrame(data)

# Decode bytes
for col in df.select_dtypes([object]):
    df[col] = df[col].apply(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)

# Output path
output_path = r'C:\Users\Cypher\3D Objects\projects\data\dataset.csv'

# 🔥 Create folder automatically
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save
df.to_csv(output_path, index=False)

print("Converted successfully! Shape:", df.shape)