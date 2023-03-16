import streamlit as st  


"### Marketing Mix Modelling (MMM)"
with st.expander("What is MMM ?"):

    body1 = """<p> 
        <a href="https://en.wikipedia.org/wiki/Marketing_mix_modeling">Market Mix Modeling (MMM)</a> 
        is a technique which helps in quantifying the impact of several marketing inputs 
        on target KPI such as sales or Market Share. The purpose of using MMM is to understand how much each 
        marketing input contributes to sales, and how much to spend on each marketing input.
        </p>"""
    
    st.markdown(body=body1, unsafe_allow_html=True) 


with st.expander("Components"): 

    body2 = """<p>
Marketing-mix models decompose total sales into two components;

Base sales: This is the natural demand for the product driven by economic factors like pricing, 
long-term trends, seasonality, and also qualitative factors like brand awareness and brand loyalty.

Incremental sales: Incremental sales are the component of sales driven by marketing and promotional activities. 
    </p>""" 
    st.markdown(body=body2, unsafe_allow_html=True)  


with st.expander("Technical Summary"): 
    body3 = """<p>
Marketing-Mix analyses are typically carried out using
<a href="https://en.wikipedia.org/wiki/Linear_regression">linear regression</a> modeling. 
Nonlinear and lagged effects are included using techniques like advertising 
<a href="https://en.wikipedia.org/wiki/Advertising_adstock"> adstock transformations.</a>
<p/> """
    st.markdown(body=body3, unsafe_allow_html=True)