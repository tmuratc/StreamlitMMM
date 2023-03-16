import streamlit as st 
import pandas as pd 
import numpy as np 

"### HOW TO USE"
"""This page aims to explain the steps you should follow to get best out of the application.
You are expected to upload 3 files. Please read descriptions for details. Also, you can always 
check left side bar to track status of data compatability during your use. 
"""

with st.expander("Step 1: Upload Train Data"): 
    st.write("""Historical data contains observed input variables and target KPI.""")    
    baseSample = pd.DataFrame(np.random.uniform(0,10000, size=(100,4)), 
                                    columns=["column1", "column2", "column3", "target column"])    
    baseSample["date column"] = pd.date_range("01/01/2023", periods=100) 

    st.dataframe(baseSample.set_index("date column"))
    st.write("Data must contain a date column and any number of columns with numeric values.")

with st.expander("Step 2: Upload Parameters Data"): 
    st.write("""Linear and non-linear indicators for given train data.""")    
  
    inputSample = pd.DataFrame(np.random.uniform(-5,5, size = (3,4)),
                                    columns=["column1", "column2", "column3", "target column"],
                                    index=["Adstock Decay","Adstock Diminished","Coefficient"]) 
    st.dataframe(inputSample) 

    """Data must contain index(first column) values as above. Column names must match with train data.
    Since target KPI indicators won't be used you can assign any numeric or empty value for it."""    

with st.expander("Step 3: Upload Data to Forecast"): 
    st.write("""Once you provide train data and parameters as to be accepted, 
    you can upload data to see forecasts on target KPI for given scenarios.
     """)    
  











