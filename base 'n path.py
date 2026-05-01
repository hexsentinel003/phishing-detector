import pandas as pd
df = pd.read_csv(r'C:\Users\Cypher\3D Objects\projects\Phishing\data\phishing_site_urls.csv')
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print("Label values:", df.iloc[:, -1].unique())
print(df.head(3))