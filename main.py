import streamlit as st
import pandas as pd
import numpy as np
import warnings
from io import BytesIO


warnings.filterwarnings('ignore')


def load_data(file_path):
    data = pd.read_excel(file_path)
    data = data[['Company', 'Sales Person', 'Quote Value', 'Final Quote Value', 'Status', 'Job No']]
    return data

def update_final_quote(row):
    if row['Final Quote Value'] == 0:
        return row['Quote Value']
    return row['Final Quote Value']

def preprocess_data(data):
    data['Final Quote Value'] = data.apply(update_final_quote, axis=1)
    data.drop('Quote Value', axis=1, inplace=True)
    return data

def calculate_metrics(data):
    process_statuses = ["New Enquiry", "Pending Survey", "Pending Quotation", "Estimate"]
    won_statuses = ["Order Acknowledged", "Order Received"]

    result = data.groupby('Company').apply(lambda x: pd.Series({
        'Total Enquiry Value': x['Final Quote Value'].sum(),
        'Under Process': x.loc[x['Status'].isin(process_statuses), 'Final Quote Value'].sum(),
        'Process %': x.loc[x['Status'].isin(process_statuses), 'Final Quote Value'].sum() / x['Final Quote Value'].sum() * 100 if x['Final Quote Value'].sum() != 0 else 0,
        'Follow-up': x.loc[x['Status'] == 'Follow up', 'Final Quote Value'].sum(),
        'Follow-up %': x.loc[x['Status'] == 'Follow up', 'Final Quote Value'].sum() / x['Final Quote Value'].sum() * 100 if x['Final Quote Value'].sum() != 0 else 0,
        'Won': x.loc[x['Status'].isin(won_statuses) & x['Job No'].notna(), 'Final Quote Value'].sum(),
        'Won %': x.loc[x['Status'].isin(won_statuses) & x['Job No'].notna(), 'Final Quote Value'].sum() / x['Final Quote Value'].sum() * 100 if x['Final Quote Value'].sum() != 0 else 0,
        'Lost': x.loc[x['Status'] == 'Order Lost', 'Final Quote Value'].sum(),
        'Lost %': x.loc[x['Status'] == 'Order Lost', 'Final Quote Value'].sum() / x['Final Quote Value'].sum() * 100 if x['Final Quote Value'].sum() != 0 else 0
    })).fillna(0).reset_index()

    return result


def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Metrics')
    processed_data = output.getvalue()
    return processed_data

st.title("Client Wise Conversion")


uploaded_file = st.file_uploader("Choose an Excel File", type="xlsx")

if uploaded_file is not None:

    data = load_data(uploaded_file)
    

    processed_data = preprocess_data(data)
    

    metrics = calculate_metrics(processed_data)
    st.write("### Metrics", metrics)
    

    excel_data = convert_df_to_excel(metrics)
    

    st.download_button(
        label="Download metrics as Excel",
        data=excel_data,
        file_name='metrics.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
