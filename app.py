import streamlit as st
import pandas as pd
import os
from Agents import data_analyst, insights_agent, strategy_agent, governance_agent, report_agent
from streamlit_pandas_profiling import st_profile_report
import chatbot  # Import the chatbot module

st.set_page_config(layout="wide")

st.title("Multi-Agent GenAI Business Analyst System")

# --- 1. File Uploaders ---
st.sidebar.header("Upload Your Data")
sales_file = st.sidebar.file_uploader("Upload Sales CSV", type="csv")
email_files = st.sidebar.file_uploader("Upload Email Summaries (.txt)", type="txt", accept_multiple_files=True)
guidelines_file = st.sidebar.file_uploader("Upload Company Guidelines (.txt)", type="txt")

# Create temporary directories for uploaded files
if not os.path.exists('temp_data'):
    os.makedirs('temp_data')
if not os.path.exists('temp_data/emails'):
    os.makedirs('temp_data/emails')

# --- 2. Main Logic Trigger ---
if st.sidebar.button("Generate Business Report"):
    if sales_file and email_files and guidelines_file:
        with st.spinner("Processing data and generating report... Please wait."):
            # Save uploaded files to temp locations
            sales_path = os.path.join('temp_data', sales_file.name)
            with open(sales_path, "wb") as f:
                f.write(sales_file.getbuffer())

            emails_dir = 'temp_data/emails'
            for email in email_files:
                with open(os.path.join(emails_dir, email.name), "wb") as f:
                    f.write(email.getbuffer())

            guidelines_path = os.path.join('temp_data', guidelines_file.name)
            with open(guidelines_path, "wb") as f:
                f.write(guidelines_file.getbuffer())
                
            # --- Agent Pipeline ---
            st.info("Step 1: Data Analyst Agent is running...")
            df, summary, monthly_sales_df, profile = data_analyst.analyze_data(sales_path, emails_dir)
            
            if df is None:
                st.error(summary)  # Display error if CSV not found or invalid
            else:
                # Initialize the chatbot and store the chain in the session state
                st.session_state.conversation_chain = chatbot.initialize_chatbot(sales_path, emails_dir, guidelines_path)

                st.info("Step 2: Insights Agent is running...")
                insights = insights_agent.generate_insights(summary)
                
                st.info("Step 3: Strategy Agent is running...")
                recommendations = strategy_agent.generate_recommendations(insights)

                st.info("Step 4: Governance Agent is running...")
                governance_check = governance_agent.check_governance(recommendations, guidelines_path)
                
                st.info("Step 5: Report Agent is running...")
                output_dir = 'output'
                report_path, image_paths = report_agent.generate_report(
                    df, insights, recommendations, governance_check, monthly_sales_df, output_dir
                )
                
                st.success("Report generated successfully!")

                # --- 3. Display Results ---
                tab1, tab2, tab3 = st.tabs(["📊 Business Report", "📈 Data Profile", "🖼️ Visualizations"])

                with tab1:
                    with open(report_path, 'r') as f:
                        st.markdown(f.read(), unsafe_allow_html=True)

                with tab2:
                    st.header("Automated Data Profile")
                    st_profile_report(profile)

                with tab3:
                    st.header("Visual Charts")
                    for image_path in image_paths:
                        st.image(image_path)

                    # Placeholder for new time-series chart
                    st.header("Time Series Chart Placeholder")
                    # Example: Create a time-series chart using monthly_df if it exists
                    if 'monthly_df' in locals():
                        st.line_chart(monthly_df)

    else:
        st.sidebar.warning("Please upload all required files.")

# --- Chatbot Section ---
if st.sidebar.button("Go to Chatbot"):
    st.session_state.page = "chatbot"
if st.sidebar.button("Go to Report"):
    st.session_state.page = "report"

if st.session_state.get("page", "report") == "chatbot":
    chatbot.display_chat_interface()  # Show the chatbot interface
else:
    st.info("Please upload your sales data, email summaries, and company guidelines, then click 'Generate Business Report'.")
