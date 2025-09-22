import pandas as pd
import os
from ydata_profiling import ProfileReport

def analyze_data(csv_path: str, emails_dir: str):
    """
    Loads data, summarizes key figures based on Sales, extracts text from emails,
    and generates time-series features and a data profiling report.
    """
    # Load and preprocess sales data
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding='windows-1252')
    except FileNotFoundError:
        return None, f"Error: The file was not found at {csv_path}"
    
    # Standardize column names
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    # Ensure the required columns exist
    required_cols = ['order_date', 'sales']
    if not all(col in df.columns for col in required_cols):
        return None, "Error: CSV must contain the columns 'Order Date' and 'Sales'."

    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
    df.dropna(subset=['sales', 'order_date'], inplace=True)
    
    # --- Time-Series Feature Engineering ---
    df['order_date'] = pd.to_datetime(df['order_date'])
    df.set_index('order_date', inplace=True)
    df.sort_index(inplace=True)

    # Calculate Monthly Sales
    monthly_sales = df['sales'].resample('M').sum()

    # Calculate Rolling Average
    df['sales_rolling_avg_3m'] = monthly_sales.rolling(window=3).mean()

    # Calculate Year-over-Year Growth (YoY)
    monthly_sales_df = monthly_sales.reset_index()
    monthly_sales_df['yoy_growth'] = monthly_sales_df['sales'].pct_change(periods=12) * 100

    # Generate a quantitative summary based only on Sales
    total_sales = df['sales'].sum()
    average_sale_value = df['sales'].mean()
    
    summary = (
        f"Data Summary:\n"
        f"- Total Sales: ${total_sales:,.2f}\n"
        f"- Average Sale Value: ${average_sale_value:,.2f}\n"
    )
    
    # Read unstructured email data
    email_summaries = []
    try:
        for filename in os.listdir(emails_dir):
            if filename.endswith(".txt"):
                with open(os.path.join(emails_dir, filename), 'r') as f:
                    email_summaries.append(f.read())
    except FileNotFoundError:
        return None, f"Error: The email directory was not found at {emails_dir}"
    
    unstructured_summary = "\n\n".join(email_summaries)
    
    full_summary = f"{summary}\n\nUnstructured Email Summaries:\n{unstructured_summary}"
    
    # Add time-series insights
    time_summary = (
        f"\nTime-Series Summary:\n"
        f"- Latest Month Sales: ${monthly_sales.iloc[-1]:,.2f}\n"
        f"- Latest YoY Growth: {monthly_sales_df['yoy_growth'].iloc[-1]:.2f}%\n"
    )
    full_summary += time_summary

    # Rename columns for other agents
    df.rename(columns={'region': 'Region', 'category': 'Category'}, inplace=True)

    # --- Generate YData Profiling Report ---
    profile = ProfileReport(df, title="Sales Data Profile", explorative=True)

    # Return enriched dataframes, summaries, and profile
    return df.reset_index(), full_summary, monthly_sales_df, profile
