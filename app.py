"""
    Application to estimate usage of sediments from reservoir as fertilizer (NPK)


    Pedro Alencar
    11.03.2023
"""

#%% import libraries

import pandas as pd
import numpy as np
import streamlit as st

import functions_resed as rsd
#%% app
st.title("Aplicativo Re-Sed")

# # create two columns of five text inputs
col1, col2, col3=  st.columns([1,1,1])
with col1:
    st.subheader("Propriedades do solo")
    soil_ca_ = st.number_input(label = "Ca (cmolc/kg)",
                               min_value=0,
                               max_value= 10000,
                               key = "soil_ca")
    soil_na_ = st.number_input(label = "Na (cmolc/kg)",
                               min_value=0,
                               max_value= 10000, 
                               key = "soil_na")
    soil_mg_ = st.number_input(label = "Mg (cmolc/kg)", 
                               min_value=0,
                               max_value= 10000,
                               key = "soil_mg")
    soil_n_ = st.number_input(label = "N (g/kg)", 
                              min_value=0,
                              max_value= 10000, 
                              key = "soil_n")
    soil_p_ = st.number_input(label = "P (mg/kg)",
                              min_value=0,
                              max_value= 10000, 
                              key = "soil_p")
    soil_k_ = st.number_input(label = "K (cmolc/kg)", 
                              min_value=0,
                              max_value= 10000, 
                              key = "soil_k")
    soil_dens_ = st.number_input(label = "densidade (g/cm³ ou kg/dm³)", 
                                 min_value=0,
                                 max_value= 10000, 
                                 key = "soil_dens")


with col2:
    st.subheader("Prop. do sedimento")
    sed_ca_ = st.number_input(label = "Ca (cmolc/kg) ",
                              min_value=0,
                              max_value= 10000, 
                              key = "sed_ca")
    sed_na_ = st.number_input(label = "Na (cmolc/kg) ", 
                              min_value=0,
                              max_value= 10000,
                              key = "sec_na")
    sed_mg_ = st.number_input(label = "Mg (cmolc/kg) ", 
                              min_value=0
                              ,max_value= 10000, 
                              key = "sed_mg")
    sed_n_ = st.number_input(label = "N (g/kg) ",
                             min_value=0,
                             max_value= 10000,
                             key = "sed_n")
    sed_p_ = st.number_input(label = "P (mg/kg) ",
                             min_value=0,
                             max_value= 10000, 
                             key = "sed_p")
    sed_k_ = st.number_input(label = "K (cmolc/kg) ",
                             min_value=0,
                             max_value= 10000,
                             key = "sed_k")
    sed_dens_ = st.number_input(label = "densidade (g/cm³ ou kg/dm³) ", 
                                min_value=0,
                                max_value= 10000, 
                                key = "sed_dens")
with col3:
    st.subheader("Preços dos suplementos")
    price_n_ = st.number_input(label = "Uréia",
                              min_value=0,
                              max_value= 10000, 
                              key = "price_n")
    price_p_ = st.number_input(label = "Superfosfato simples",
                              min_value=0,
                              max_value= 10000, 
                              key = "price_p")
    price_k_ = st.number_input(label = "Cloreto de Potássio",
                              min_value=0,
                              max_value= 10000, 
                              key = "price_k")  
    st.subheader("Manejo dos sedimentos")
    dist_ = st.number_input(label = "Diatância",
                              min_value=0,
                              max_value= 5000, 
                              key = "dist")     
    machine_ = st.number_input(label = "Aluguel da retroescavadeira (R$/h)",
                              min_value=0,
                              max_value= 5000, 
                              key = "machine")      
    truck_ = st.number_input(label = "Aluguel da caçamba (R$/h)",
                              min_value=0,
                              max_value= 5000, 
                              key = "truc_") 
    


crop_ = st.selectbox(label = "Cultura",
                     options = ("Algodão (sequeiro)", "Algodão (irrigado)", "Batada doce",
                      "Feijão de corda", "Mandioca", "Milho (sequeiro)",
                      "Milho (irrigado)", "Sorgo forrageiro"),
                     key = "crop")

sup_ = st.selectbox(label = "Nutriente suplementado por sedimentps",
                     options = ("Nitrogênio", "Fósforo", "Potássio"),
                     key = "sup")



# # show the results in a row below
st.subheader("Results:")
st.write(f"Input 1: {soil_ca_}")
# st.write(f"Input 6: {input_6}, Input 7: {input_7}, Input 8: {input_8}, Input 9: {input_9}, Input 10: {input_10}")







# %%
