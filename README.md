# Client Wise Conversion Metrics

This Streamlit application calculates and displays client-wise conversion metrics from an uploaded Excel file. The application allows users to upload an Excel file containing sales data, processes the data to calculate various metrics, and then provides an option to download the results as an Excel file.

## Features

- Upload an Excel file with sales data
- Process the data to calculate client-wise metrics
- Display the calculated metrics in the app
- Download the metrics as an Excel file

## Installation

To run this application locally, follow these steps:

1. **Clone the repository:**
   
   ```bash
   git clone https://github.com/StagMindVRithul/client_wise_conversion.git
   cd client_wise_conversion

3. **Install the required dependencies:**
   
   ```bash
   pip install -r requirements.txt

## Usage

1. **Run the Streamlit app:**

    ```bash
    streamlit run app.py


2. **Upload an Excel file:**

    The file should have the following columns: Company, Sales Person, Quote Value, Final Quote Value, Status, Job No.

3. **View the metrics:**

    The app will display the calculated metrics based on the uploaded data.

4. **Download the metrics:**

    Click the "Download metrics as Excel" button to download the processed metrics as an Excel file.
