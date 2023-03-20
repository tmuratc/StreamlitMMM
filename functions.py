import pandas as pd 
import numpy as np
import streamlit as st
import math 

###########################################################################
def displayDf(df:pd.DataFrame,widgetName:str):  
    forClick  = f"{widgetName}_next_click_count"  
    """
    click count continues from last value even data is changed 
    this should be fixed.  
    """
    def updateIndex(pageNum:int): 
        startIndex = pageNum*10
        endIndex =  (pageNum+1)*10
        return startIndex,endIndex

    def handleNextClick(): 
        if forClick not in st.session_state:  
            st.session_state[forClick] = 0 
        else: 
            st.session_state[forClick] += 1

    with st.expander('Click to see your data'): 
        
        st.button("Next", on_click=handleNextClick(),key=widgetName)  
        totalPages = math.ceil(len(df)/10) 
        modeOfClicks = st.session_state[forClick] % totalPages
        startIndex,endIndex = updateIndex(modeOfClicks)
        st.dataframe(df.iloc[startIndex:endIndex])  

########################################################################### 

def readFile(file,index_col=None): 
    try: return pd.read_csv(file,index_col=index_col) 
    except: return pd.read_excel(file,index_col=index_col)

########################################################################### 
########################################################################### 

def isOnlyOneDateColumn (df:pd.DataFrame) : 
    datetimeDf = df.select_dtypes(include="datetime") 
    return datetimeDf.shape[1] == 1 

########################################################################### 

def isAllNumericExceptDate (df:pd.DataFrame): 
    nonDatetimeDf = df.select_dtypes(exclude='datetime')
    numericDf = nonDatetimeDf.select_dtypes(include="number") 
    return numericDf.shape[1] == nonDatetimeDf.shape[1] 

########################################################################### 

########################################################################### 
###########################################################################  

def isAllNumeric(df:pd.DataFrame):
    dfNumeric = df.select_dtypes(include="number") 
    return df.shape[1] == dfNumeric.shape[1]  

###########################################################################  
###########################################################################  

def inputIndexCheck(df:pd.DataFrame): 
    needed = ["Adstock Decay", "Adstock Diminished", "Coefficient"]
    return set(list(df.index)) == set(needed)



#############################################################################  
#############################################################################  

def statusInfo (basedf=pd.DataFrame(),inputdf=pd.DataFrame()): 
    basecolumns = list(basedf.select_dtypes(exclude = "datetime").columns) 
    inputcolumns = list(inputdf.columns) 
    status_messages = []

    if not isAllNumeric(inputdf) and len(inputdf) != 0 : 
        status_messages.append("Parameters data contains non-numeric columns.") 
    
    if not inputIndexCheck(inputdf) and len(inputdf) != 0 : 
        status_messages.append("Parameters data index names doesn't match.") 
    
    if not isOnlyOneDateColumn(basedf) and len(basedf) != 0: 
        status_messages.append("Train data contains  more than one or no number of date columns.")
    
    if not isAllNumericExceptDate(basedf) and len(basedf) != 0: 
        status_messages.append("Train data contains non-numeric columns.") 

    if not set(inputcolumns) == set(basecolumns) and len(inputdf) != 0 and len(basedf) != 0:  
        unmathced_list = [i for i in basecolumns if i not in inputcolumns]
        for item in unmathced_list: 
            status_messages.append(f"Unmatched column : {item}")
    
    return status_messages

#############################################################################  
############################################################################# 

def statusInfo2(futuredf:pd.DataFrame, neededColumns:list): 
    status_messages = [] 
    if not isOnlyOneDateColumn(futuredf) : 
        status_messages.append("Data to forecast contains  more than one or no number of date columns.")

    if not isAllNumericExceptDate(futuredf) : 
        status_messages.append("Data to forecast contains non-numeric columns.") 
    
    if not set(neededColumns).issubset(set(futuredf.select_dtypes(include="number").columns)): 
        status_messages.append("Data to forecast column names don't match with base data.")

    return status_messages

############################################################################# 
############################################################################# 

def displayWarningSidebar(messages:list): 
    with st.sidebar:
        for message in messages: 
            st.warning(message,icon="⚠️") 

#############################################################################  
############################################################################# 

def decayTransform (arr:list or pd.Series, decVal:float or int) : 
    if decVal == 0 or pd.isna(decVal): 
        return arr 
        
    finalArr = [] 
    for index, item in enumerate(arr) : 
        if index == 0 : 
            finalArr.append(item)
            continue 
        newVal = item + (1-decVal)*finalArr[index-1]
        finalArr.append(newVal)
    return finalArr   

#################################################################################
################################################################################# 

def applyDecayAllDf(df:pd.DataFrame, paramDict:dict): 
    df_transformed = pd.DataFrame() 
    for col in df.columns: 
        df_transformed[col] = decayTransform(df[col],paramDict[col]) 
    
    return df_transformed 

#################################################################################
################################################################################# 

def diminishedTransform (arr:list or pd.Series, dimVal:float or int) :
    if dimVal == 0 or pd.isna(dimVal):
        return arr 
    finalArr = [] 
    for index, item in enumerate(arr) : 
        if index == 0 : 
            finalArr.append(item) 
            continue
        new_val = 1 - math.exp((-item/dimVal))
        finalArr.append(new_val)
    return finalArr        

#################################################################################
################################################################################# 

def applyDiminishedAllDf(df:pd.DataFrame, paramDict:dict): 
    df_transformed = pd.DataFrame() 
    for col in df.columns: 
        df_transformed[col] = diminishedTransform(df[col],paramDict[col]) 
    return df_transformed 

#################################################################################
################################################################################## 

def applyMultiply(df:pd.DataFrame, paramDict:dict) : 
    df_multiply = pd.DataFrame()
    for col in df.columns:  
        if pd.isna(paramDict[col]) : 
            df_multiply[col] = df[col] 
        else:
            df_multiply[col] = df[col]*paramDict[col]  

    df_multiply["results"] = df_multiply.copy().apply(lambda x: sum(x), axis = 1 )
    return df_multiply

#################################################################################
################################################################################## 

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

#################################################################################
################################################################################## 
