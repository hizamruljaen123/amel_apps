# Smartphone Sales Classification using BIRCH Algorithm

## Introduction
BIRCH (**Balanced Iterative Reducing and Clustering using Hierarchies**) is a clustering algorithm that is efficient for large datasets.  
It incrementally builds a **Clustering Feature (CF) tree**, making it suitable for analyzing sales data such as smartphone purchases.  

In the smartphone sales context, BIRCH can classify customers or sales patterns into groups, e.g.:
- High-value vs low-value buyers  
- Preference for brand/type  
- Buying frequency  

## How It Works
1. Build a **CF tree** to summarize the dataset.  
2. Incrementally insert data points (sales records) into the tree.  
3. Perform clustering on leaf nodes.  
4. Optionally, refine the clustering with another algorithm (e.g., K-Means).  

## Python Implementation (Simplified Example)

```python
import pandas as pd
from sklearn.cluster import Birch
from sklearn.preprocessing import StandardScaler

# Example dataset (toy data)
data = {
    "price": [300, 800, 1200, 250, 700, 1000, 1500, 400],
    "units_sold": [50, 30, 20, 80, 40, 25, 10, 60],
    "brand_popularity": [7, 9, 10, 5, 8, 9, 10, 6]
}
df = pd.DataFrame(data)

# Preprocessing
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

# BIRCH model
model = Birch(n_clusters=3)
labels = model.fit_predict(X_scaled)

df["Cluster"] = labels
print(df)
