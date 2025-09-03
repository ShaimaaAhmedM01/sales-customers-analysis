import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

# load the dataset 
df = pd.read_csv("train.csv")

# Remove spaces from column names
df.columns = df.columns.str.strip()

# Get the number of rows and columns 
print("Shape of dataset: ", df.shape)
# we have 18 columns and 9800 rows

# Remove dollar signs before conversion
df["Sales"] = df["Sales"].replace('[\$,]', '', regex=True).astype(float)

# Covert "Order Date" column to datetime, 'Sales' is numerical (float)
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
df["Row ID"] = df["Row ID"].astype(str)
df["Postal Code"] = df["Postal Code"].astype(str)

# Check data types of each column after change and before
print("\nData types:")
print(df.dtypes)

# Look at the first few rows
print(df.head())

# Check for missing values in each column
print("\nMissing values per column:")
print(df.isnull().sum())

# Summary statistics for numeric columns
print("\nSummary statistics:")
print(df.describe())

# Count unique values per column:
print("\nUnique values per column:")
for col in df.columns:
    print(f"{col}: {df[col].nunique()}")

# Look at distribution of Sales
plt.hist(df["Sales"], bins=50)
plt.title("Distribution of Sales")
plt.xlabel("Sales")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("outputs/Distribution_of_sales.png")
plt.show()

# Look at top 10 highest sales orders:
print("\nTop 10 highest sales orders:")
print(df.sort_values("Sales", ascending=False).head(10))

# Sales distribution
plt.figure(figsize=(8,5))
sns.histplot(df["Sales"], bins=50, kde=True)
plt.title("Sales Distribution with KDE")
plt.xlabel("Sales Amount")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("outputs/sales_distribution_with_KDE.png")
plt.show()

# Sales by Category / Sub-Category
plt.figure(figsize=(8,5))
df.groupby("Category")["Sales"].sum().plot(kind="bar")
plt.title("Total Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("outputs/total_sales_by_category.png")
plt.show()

plt.figure(figsize=(10,5))
df.groupby("Sub-Category")["Sales"].sum().plot(kind="bar")
plt.title("Total Sales by Sub-Category")
plt.xlabel("Sub-Category")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("outputs/total_sales_by_subcategory.png")
plt.show()

# Sales by Region / Segment
plt.figure(figsize=(8,5))
df.groupby("Region")["Sales"].sum().plot(kind="bar")
plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("outputs/total_sales_by_region.png")
plt.show()

plt.figure(figsize=(8,5))
df.groupby("Segment")["Sales"].mean().plot(kind="bar")
plt.title("Average Sales by Segment")
plt.xlabel("Segment")
plt.ylabel("Average Sales")
plt.tight_layout()
plt.savefig("outputs/avg_sales_by_segment.png")
plt.show()

# top 5 Customers by sales
top_customers = df.groupby("Customer Name")["Sales"].sum().sort_values(ascending=False).head(5)
print("\nTop Customers by Sales: ")
print(top_customers)
plt.figure(figsize=(8,5))
top_customers.plot(kind="bar", title="Top 5 Customers by Sales")
plt.xlabel("Customer")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("outputs/top5_customers_by_sales.png")
plt.show()

# Monthly Revenue Trend
df["YearMonth"] = df["Order Date"].dt.to_period("M")
monthly_revenue = df.groupby("YearMonth")["Sales"].sum()
print("\nMonthly Revenue:")
print(monthly_revenue.head())
monthly_revenue.plot(kind="line", figsize=(10,5), title="Monthly Revenue Trend", marker="o")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("outputs/monthly_revenue_trend.png")
plt.show()

# Products with Highest Profit Margin
if "Profit" in df.columns:
    df["Profit Margin"] = df["Profit"] / df["Sales"]
    top_margin_products = df.groupby("Product Name")["Profit Margin"].mean().sort_values(ascending=False).head(10)
    print("\nTop 10 Products by Profit Margin:")
    print(top_margin_products)
    top_margin_products.plot(kind="bar", figsize=(10,5), title="Top 10 Products by Profit Margin")
    plt.ylabel("Profit Margin")
    plt.tight_layout()
    plt.savefig("outputs/Top10_Products_by_Profit_Margin.png")
    plt.show()
else:
    print("\nNo 'Profit' column found. Showing Top 10 Products by Sales instead.")
    top_sales_products = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10)
    print(top_sales_products)
    top_sales_products.plot(kind="bar", figsize=(10,5), title="Top 10 Products by Sales")
    plt.ylabel("Total Sales")
    plt.tight_layout()
    plt.savefig("outputs/Top10_Products_by_Sales.png")
    plt.show()