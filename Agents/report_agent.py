import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# The function definition is updated to accept 'monthly_sales_df'
def generate_report(df: pd.DataFrame, insights: str, recommendations: str, governance: str, monthly_sales_df: pd.DataFrame, output_dir: str):
    """
    Generates visualizations and compiles the final markdown report.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # --- Generate Visualizations ---
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # 1. Sales by Region
    plt.figure(figsize=(10, 6))
    region_sales = df.groupby('Region')['sales'].sum().sort_values(ascending=False)
    sns.barplot(x=region_sales.index, y=region_sales.values, hue=region_sales.index, palette='viridis', legend=False)
    plt.title('Total Sales by Region')
    plt.ylabel('Total Sales ($)')
    plt.xlabel('Region')
    plt.tight_layout()
    sales_by_region_path = os.path.join(output_dir, 'sales_by_region.png')
    plt.savefig(sales_by_region_path)
    plt.close()

    # 2. Sales by Category
    plt.figure(figsize=(10, 6))
    category_sales = df.groupby('Category')['sales'].sum().sort_values(ascending=False)
    sns.barplot(x=category_sales.index, y=category_sales.values, hue=category_sales.index, palette='plasma', legend=False)
    plt.title('Total Sales by Product Category')
    plt.ylabel('Total Sales ($)')
    plt.xlabel('Category')
    plt.tight_layout()
    sales_by_category_path = os.path.join(output_dir, 'sales_by_category.png')
    plt.savefig(sales_by_category_path)
    plt.close()

    # 3. Monthly Sales Trend (This chart now works)
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_sales_df['order_date'], monthly_sales_df['sales'], label='Monthly Sales', marker='o')
    plt.plot(monthly_sales_df['order_date'], monthly_sales_df['sales'].rolling(window=3).mean(), label='3-Month Rolling Avg', linestyle='--')
    plt.title('Monthly Sales Trend')
    plt.xlabel('Date')
    plt.ylabel('Sales ($)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    monthly_trend_path = os.path.join(output_dir, 'monthly_trend.png')
    plt.savefig(monthly_trend_path)
    plt.close()


    # --- Compile Markdown Report ---
    report_content = f"""
# Business Performance Report

## Executive Summary
This report provides an analysis of business performance based on sales data, email summaries, and company guidelines. It includes key insights, strategic recommendations, and governance validation.

{insights}

{recommendations}

{governance}

## Data Visualizations

### Monthly Sales Trend
![Monthly Sales Trend]({monthly_trend_path})

### Sales by Region
![Sales by Region]({sales_by_region_path})

### Sales by Product Category
![Sales by Category]({sales_by_category_path})
"""

    report_path = os.path.join(output_dir, 'final_report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

        
    # Return paths to all three images
    return report_path, [monthly_trend_path, sales_by_region_path, sales_by_category_path]