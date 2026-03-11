# RFM Customer Segmentation — Online Retail

Customer segmentation web app using RFM analysis on the Online Retail dataset. Clusters customers into 5 behavioral segments using KMeans, Hierarchical, and DBSCAN algorithms, with PCA and t-SNE visualizations. Includes an interactive Streamlit app for real-time customer classification.

---

## 📁 Project Structure

```
├── customer_segmentation.ipynb   # Full ML pipeline notebook
├── app.py                        # Streamlit web app
└── README.md
```

---

## 📊 Dataset

[Online Retail Dataset — Kaggle](https://www.kaggle.com/datasets/lakshmi25npathi/online-retail-dataset)

Transactions from a UK-based online retail store. Contains ~500K rows across 8 columns: `Invoice`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `Price`, `Customer ID`, `Country`.

---

## 🔬 ML Pipeline (`customer_segmentation.ipynb`)

| Stage | Details |
|-------|---------|
| Data Cleaning | Remove cancellations, missing Customer IDs, invalid rows |
| Feature Engineering | RFM — Recency, Frequency, Monetary |
| Outlier Handling | IQR method + log1p transformation |
| Scaling | RobustScaler |
| Clustering | KMeans, Agglomerative (Ward), DBSCAN |
| Evaluation | Silhouette Score, Davies-Bouldin Score, Elbow Method |
| Visualization | PCA, t-SNE, 3D scatter, boxplots |
| Profiling | Cluster mean RFM + persona assignment |

---

## 🧠 Customer Segments

| Segment | Behaviour | Strategy |
|---------|-----------|----------|
| 🏆 Champions | Recent, frequent, high spend | Loyalty rewards, early access |
| 💙 Loyal Customers | Regular buyers, solid spend | Upsell, referral programs |
| 🌱 Promising / New | Recent but few orders | Onboarding, welcome discounts |
| ⚠️ At Risk | Were active, now drifting | Win-back emails |
| 💤 Lost / Dormant | Long inactive | Reactivation campaigns |

---

## 🚀 Running the App

### 1. Install dependencies

```bash
pip install pandas numpy matplotlib seaborn scikit-learn scipy streamlit openpyxl
```

### 2. Get your RFM thresholds

Run this at the end of `customer_segmentation.ipynb`:

```python
print("R_MED =", rfm_clean['Recency'].median())
print("F_MED =", rfm_clean['Frequency'].median())
print("M_MED =", rfm_clean['Monetary'].median())
```

Paste the values into `app.py`:

```python
R_MED = ...   # Recency median
F_MED = ...   # Frequency median
M_MED = ...   # Monetary median
```

### 3. Launch the app

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 🛠 Tech Stack

- Python, Pandas, NumPy
- Scikit-learn (KMeans, DBSCAN, Agglomerative, PCA, t-SNE)
- Matplotlib, Seaborn
- Streamlit
