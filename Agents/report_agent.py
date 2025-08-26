import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_report(df: pd.DataFrame, insights: str, recommendations: str, governance: str, output_dir: str):
    """
    Generates visualizations and compiles the final markdown report.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # --- Generate Visualizations ---
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # 1. Sales by Region
    plt.figure(figsize=(10, 6))
    # Ensure 'Region' and 'Sales' columns exist after renaming in data_analyst
    region_sales = df.groupby('Region')['sales'].sum().sort_values(ascending=False)
    sns.barplot(x=region_sales.index, y=region_sales.values, palette='viridis')
    plt.title('Total Sales by Region')
    plt.ylabel('Total Sales ($)')
    plt.xlabel('Region')
    plt.tight_layout()
    sales_by_region_path = os.path.join(output_dir, 'sales_by_region.png')
    plt.savefig(sales_by_region_path)
    plt.close()

    # 2. Sales by Category (REPLACED FROM PROFIT)
    plt.figure(figsize=(10, 6))
    category_sales = df.groupby('Category')['sales'].sum().sort_values(ascending=False)
    sns.barplot(x=category_sales.index, y=category_sales.values, palette='plasma')
    plt.title('Total Sales by Product Category')
    plt.ylabel('Total Sales ($)')
    plt.xlabel('Category')
    plt.tight_layout()
    sales_by_category_path = os.path.join(output_dir, 'sales_by_category.png')
    plt.savefig(sales_by_category_path)
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

### Sales by Region
![Sales by Region]({sales_by_region_path})

### Sales by Product Category
![Sales by Category]({sales_by_category_path})
"""

    report_path = os.path.join(output_dir, 'final_report.md')
    with open(report_path, 'w') as f:
        f.write(report_content)
        
    return report_path, [sales_by_region_path, sales_by_category_path]