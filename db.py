import streamlit as st 
import functions as f
import pandas as pd
import numpy as np
import plotly.graph_objects as go


st.set_page_config(page_title="MMM Simulation")

"# MMM Simulation" 

basedata = st.file_uploader('Train Data', type=["xlsx", "csv"]) 
inputdata = st.file_uploader('Parameters', type=["xlsx", "csv"]) 
#neededIndex = ["Adstock Decay", "Adstock Diminished", "Coefficient"]


################################################################################
################################################################################

if basedata is None and inputdata is None :  
    pass

################################################################################
################################################################################

if basedata is None and inputdata is not None : 

    inputdf = f.readFile(inputdata,index_col=0)
    inputcolumns = list(inputdf.columns) 
    inputIndex = list(inputdf.index) 

    if f.statusInfo(inputdf=inputdf) == [] :
        baseSampleDf = pd.DataFrame(np.random.uniform(0,100000, size=(10,len(inputcolumns))), 
                                    columns=inputcolumns) 
        baseSampleDf["(your date column)"] = pd.date_range("2022-01-01", periods=10,freq="D")
        
        """#### Parameters"""
        f.displayDf(inputdf,"case5")
    
    else:
        f.displayWarningSidebar(f.statusInfo(inputdf=inputdf))
        f.displayDf(inputdf, "case1") 
 
################################################################################
################################################################################

if basedata is not None and inputdata is None :
    basedf = f.readFile(basedata) 
    """#### Train Data"""
    f.displayDf(basedf,"case2")
  

    if f.statusInfo(basedf=basedf) == []:
        pass
    else :
        f.displayWarningSidebar(f.statusInfo(basedf=basedf))
        
################################################################################
################################################################################

if basedata is not None and inputdata is not None :  
    basedf = f.readFile(basedata) 
    inputdf = f.readFile(inputdata, index_col=0)
  
    """#### Train Data"""
    f.displayDf(basedf,"case3")

    """#### Parameters""" 
    f.displayDf(inputdf,"case4") 

    if f.statusInfo(basedf,inputdf) == []: 
        
        targetOptions = basedf.select_dtypes(include="number").columns
        with st.sidebar:   
            targetColumn = st.selectbox("Target Column", options=targetOptions)
        
        dateColumn = basedf.select_dtypes(include="datetime").columns[0]  
        inputcolumns = [i for i in basedf.columns if i != targetColumn and i != dateColumn]
        transformableDf = basedf[inputcolumns] 
        firstTransformDf = f.applyDecayAllDf(transformableDf,dict(inputdf.loc["Adstock Decay"]))
        secondTransformDf = f.applyDiminishedAllDf(firstTransformDf,dict(inputdf.loc["Adstock Diminished"]))
        finalDf = f.applyMultiply(secondTransformDf,dict(inputdf.loc["Coefficient"]))
        

        #fig = px.line(data_frame=basedf,x=dateColumn,y=targetColumn,)  
        fig = go.Figure() 
        fig.add_trace(go.Scatter(x=basedf[dateColumn], y = basedf[targetColumn], name = "actual"))
        fig.add_trace(go.Scatter(x = basedf[dateColumn], y = finalDf["results"], name = "MMM forecast"))  
         

        with st.container():  
            futurefile = st.file_uploader("future data")

            if futurefile is not None : 
                futuredf = f.readFile(futurefile) 
                if f.statusInfo2(futuredf, inputcolumns) == [] : 
                    futureDateColumn = futuredf.select_dtypes(include="datetime").columns[0] 
                    firstTransformFuture = f.applyDecayAllDf(futuredf[inputcolumns], dict(inputdf.loc["Adstock Decay"]))
                    secondTransformFuture = f.applyDiminishedAllDf(firstTransformFuture, dict(inputdf.loc["Adstock Diminished"])) 
                    finalFuture = f.applyMultiply(secondTransformFuture, dict(inputdf.loc["Coefficient"]))

                    fig.add_trace(go.Scatter(x=futuredf[futureDateColumn], y=finalFuture["results"], name ="MMM future forecast" ))


                    outputData = pd.DataFrame()
                    outputData["Date"] = basedf[dateColumn] 
                    outputData["Actual"] = basedf[targetColumn] 
                    outputData["Forecast"] = finalDf["results"]  
        
                    futureOutputData = pd.DataFrame()
                    futureOutputData["Date"] = futuredf[futureDateColumn]
                    futureOutputData["Actual"] = float("nan")
                    futureOutputData["Forecast"] = finalFuture["results"] 
                    
                    
                    outputData = pd.concat([outputData,futureOutputData])

                    csv = f.convert_df(outputData) 
                    st.download_button( label="Download data as CSV", data=csv,
                                        file_name='finaloutput.csv',mime='text/csv',)
                    
                    st.dataframe(outputData) 
        
                else : 
                    f.displayDf(futuredf,"future")
                    f.displayWarningSidebar(f.statusInfo2(futuredf, inputcolumns))


        st.plotly_chart(fig)


    else: 
        f.displayWarningSidebar(f.statusInfo(basedf,inputdf))





 





