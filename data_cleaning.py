
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# 1. LOAD DATA

print("Loading dataset...")

df = pd.read_csv("ONINE_FOOD_DELIVERY_ANALYSIS.csv")

# Clean column names (VERY IMPORTANT)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

print("Dataset Loaded Successfully")
print("Columns in dataset:")
print(df.columns)
print("Initial Shape:", df.shape)


# 2. REMOVE DUPLICATES

df.drop_duplicates(inplace=True)


# 3. HANDLE MISSING VALUES


print("Handling missing values...")

# Numeric columns → median
for col in df.select_dtypes(include=np.number).columns:
    df[col] = df[col].fillna(df[col].median())

# Categorical columns → mode
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].fillna(df[col].mode()[0])
    


# 4. DATA VALIDATION & CLEANING


# Rating should not exceed 5
if "customer_rating" in df.columns:
    df = df[df["customer_rating"] <= 5]

# Remove negative profits
if "profit" in df.columns:
    df = df[df["profit"] >= 0]

# Remove extreme outliers in delivery_time
if "delivery_time" in df.columns:
    Q1 = df["delivery_time"].quantile(0.25)
    Q3 = df["delivery_time"].quantile(0.75)
    IQR = Q3 - Q1
    df = df[
        (df["delivery_time"] >= Q1 - 1.5 * IQR) &
        (df["delivery_time"] <= Q3 + 1.5 * IQR)
    ]

# Standardize text columns
if "city" in df.columns:
    df["city"] = df["city"].str.title().str.strip()

if "cuisine" in df.columns:
    df["cuisine"] = df["cuisine"].str.title().str.strip()


# 5. FEATURE ENGINEERING


print("Creating derived features...")

# Date conversion
if "order_date" in df.columns:
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    df["order_month"] = df["order_date"].dt.month
    df["day_name"] = df["order_date"].dt.day_name()
    df["order_hour"] = df["order_date"].dt.hour

    df["day_type"] = df["day_name"].apply(
        lambda x: "Weekend" if x in ["Saturday", "Sunday"] else "Weekday"
    )

    df["peak_hour"] = df["order_hour"].apply(
        lambda x: "Peak" if 18 <= x <= 22 else "Non-Peak"
    )

# Profit margin %
if "profit" in df.columns and "order_value" in df.columns:
    df["profit_margin_percent"] = (
        df["profit"] / df["order_value"]
    ) * 100

# Age group
if "customer_age" in df.columns:
    df["age_group"] = pd.cut(
        df["customer_age"],
        bins=[18, 25, 35, 50, 70],
        labels=["18-25", "26-35", "36-50", "50+"]
    )

print("Feature Engineering Completed")


# 6. BASIC EDA OUTPUTS


print("\n===== EDA RESULTS =====")

if "order_value" in df.columns:
    print("\nTotal Revenue:", df["order_value"].sum())
    print("Average Order Value:", df["order_value"].mean())

if "order_status" in df.columns:
    print("\nOrder Status Distribution:")
    print(df["order_status"].value_counts())

if "city" in df.columns and "order_value" in df.columns:
    print("\nTop 5 Cities by Revenue:")
    print(
        df.groupby("city")["order_value"]
        .sum()
        .sort_values(ascending=False)
        .head()
    )

# 7. SAVE CLEANED FILE


df.to_csv("cleaned_food_delivery_data.csv", index=False)
print("\nCleaned dataset saved as cleaned_food_delivery_data.csv")



# 8. UPLOAD TO MYSQL


from sqlalchemy import create_engine, text
from urllib.parse import quote_plus


password = quote_plus("Nithik@20")


engine = create_engine(
    f"mysql+pymysql://root:{password}@localhost:3306/"
)


with engine.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS food_delivery_db"))
    conn.commit()

# Connect to the created database
engine = create_engine(
    f"mysql+pymysql://root:{password}@localhost:3306/food_delivery_db"
)

# Step 4: Upload data
df.to_sql(
    "orders",
    engine,
    if_exists="replace",
    index=False
)

print("✅ Data uploaded successfully to MySQL table: orders")


