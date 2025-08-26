import pandas as pd
import os

def analyze_data(csv_path: str, emails_dir: str):
    """
    Loads data, summarizes key figures based on Sales, and extracts text from emails.
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
    
    # Rename columns for other agents
    df.rename(columns={'region': 'Region', 'category': 'Category'}, inplace=True)

    return df, full_summary