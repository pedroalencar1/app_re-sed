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

st.set_page_config(layout="wide")

#%% app
st.title("Aplicativo Re-Sed")

# # create two columns of five text inputs
col1, col2, col3=  st.columns([1,1,1])
with col1:
    st.subheader("Propriedades do solo")
    # soil_ca = st.number_input(label = "Ca (cmolc/kg)",
    #                            min_value=0.,
    #                            max_value= 10000.,
    #                            key = "soil_ca")
    # soil_na = st.number_input(label = "Na (cmolc/kg)",
    #                            min_value=0.,
    #                            max_value= 10000., 
    #                            key = "soil_na")
    # soil_mg = st.number_input(label = "Mg (cmolc/kg)", 
    #                            min_value=0.,
    #                            max_value= 10000.,
    #                            key = "soil_mg")
    soil_n = st.number_input(label = "N (g/kg)", 
                              min_value=0.,
                              max_value= 10000., 
                              value = 1.,
                              key = "soil_n",
                              step=0.01,format="%.2f")
    soil_p = st.number_input(label = "P (mg/kg)",
                              min_value=0.,
                              max_value= 10000., 
                              value = 1.,
                              key = "soil_p",
                              step=0.01,format="%.2f")
    soil_k = st.number_input(label = "K (cmolc/kg)", 
                              min_value=0.,
                              max_value= 10000., 
                              value = 1.,
                              key = "soil_k",
                              step=0.01,format="%.2f")
    soil_ce = st.number_input(label = "C.E. (dS/m)",
                               min_value=0.,
                               max_value=10000.,
                               key = "soil_ce",
                              step=0.01,format="%.2f")
    soil_dens = st.number_input(label = "densidade (g/cm³ ou kg/dm³)", 
                                 min_value=0.,
                                 max_value= 10000., 
                                 value = 1.6,
                                 key = "soil_dens",
                              step=0.01,format="%.2f")

with col2:
    st.subheader("Prop. do sedimento")
    # sed_ca = st.number_input(label = "Ca (cmolc/kg) ",
    #                           min_value=0.,
    #                           max_value= 10000., 
    #                           key = "sed_ca")
    # sed_na = st.number_input(label = "Na (cmolc/kg) ", 
    #                           min_value=0.,
    #                           max_value= 10000.,
    #                           key = "sec_na")
    # sed_mg = st.number_input(label = "Mg (cmolc/kg) ", 
    #                           min_value=1
    #                           ,max_value= 10000., 
    #                           key = "sed_mg")
    sed_n = st.number_input(label = "N (g/kg) ",
                             min_value=0.,
                             max_value= 10000.,
                             value = 2.,
                             key = "sed_n",
                              step=0.01,format="%.2f")
    sed_p = st.number_input(label = "P (mg/kg) ",
                             min_value=0.,
                             max_value= 10000., 
                             value = 2.,
                             key = "sed_p",
                              step=0.01,format="%.2f")
    sed_k = st.number_input(label = "K (cmolc/kg) ",
                             min_value=0.,
                             max_value= 10000.,
                             value = 100.,
                             key = "sed_k",
                              step=0.01,format="%.2f")
    sed_ce = st.number_input(label = "C.E. (dS/m)",
                              min_value=0.,
                              max_value= 10000.,
                              key = "sed_ce",
                              step=0.01,format="%.2f")
    sed_dens = st.number_input(label = "densidade (g/cm³ ou kg/dm³) ", 
                                min_value=0.,
                                max_value= 10000., 
                                value = 1.1,
                                key = "sed_dens",
                              step=0.01,format="%.2f")
with col3:
    st.subheader("Preços dos suplementos")
    price_n = st.number_input(label = "Uréia",
                              min_value=0.,
                              max_value= 10000.,
                              value = 100., 
                              key = "price_n",
                              step=0.01,format="%.2f")
    price_p = st.number_input(label = "Superfosfato simples",
                              min_value=0.,
                              max_value= 10000., 
                              value = 200.,
                              key = "price_p",
                              step=0.01,format="%.2f")
    price_k = st.number_input(label = "Cloreto de Potássio",
                              min_value=0.,
                              max_value= 10000.,
                              value = 200., 
                              key = "price_k",
                              step=0.01,format="%.2f")
   
st.subheader("Manejo da cultura")
col4, col41, col42=  st.columns([1,1,1])
with col41:
    crop = st.selectbox(label = "Cultura",
                        options = ("Algodão (sequeiro)", "Algodão (irrigado)", "Batada doce",
                        "Feijão de corda", "Mandioca", "Milho (sequeiro)",
                        "Milho (irrigado)", "Sorgo forrageiro"),
                        # value = "Sorgo forrageiro",
                        key = "crop")

    sup = st.selectbox(label = "Nutriente suplementado por sedimentos",
                        options = ("Nitrogênio", "Fósforo", "Potássio"),
                        # value = "Fósforo",
                        key = "sup")

    dist = st.number_input(label = "Diatância de transporte (m)",
                        min_value=0.,
                        max_value= 10000., 
                        value = 1000.,
                        key = "dist",
                        step=0.01,format="%.2f")

    depth = st.number_input(label = "Profundidade de mistura (cm) ", 
                            min_value=0.,
                            max_value= 100., 
                            value = 20.,
                            key = "depth",
                            step=0.01,format="%.2f")
    



st.subheader("Resultados:")
col5, col61, col62, col63 = st.columns([2,1,1,1])
with col5:
    print_ = 1
    if soil_ce > 4:
        st.subheader("Solo salino - impróprio para cultivo.")
        print_ = 0
    elif sed_ce > 4:
        st.subheader("Sedimento salino - improprio para reúso.")
        print_ = 0
    elif rsd.check_sed(sup, sed_n, soil_n,sed_p, soil_p,sed_k, soil_k):
        st.subheader(f"Não há suficiente {sup} no sedimento.")
        print_ = 0

    # print results if process is valid    
    if print_ == 1:
        
        # compute!
        
        demand_crop = rsd.demand_from_crop(soil_p, soil_k, soil_dens, crop, depth)
        
        npk_soil_gkg = rsd.npk_to_gkg(soil_n, soil_p, soil_k)
        npk_soil_kgm3 = rsd.npk_to_kgm3(npk_soil_gkg, soil_dens) 
        
        npk_sed_gkg = rsd.npk_to_gkg(sed_n, sed_p, sed_k)
        npk_sed_kgm3 = rsd.npk_to_kgm3(npk_sed_gkg, sed_dens) 
        
        depth_sed = rsd.get_mix(demand_crop, npk_soil_kgm3, npk_sed_kgm3, depth, sup)
        
        deficit_new = rsd.persistent_deficit(depth_sed, demand_crop, npk_soil_kgm3, npk_sed_kgm3, depth)
        
        add_sup = rsd.additional_supplements(deficit_new, depth, price_n, price_p, price_k)
        
        vols = rsd.soil_movement(depth_sed)
        
        cost_trans = vols["Vol of transport"]*(8.6 + 0.0026*dist) # equation estimated from SEINFRA (conta 2.4)
        cost_sed = rsd.cost_no_sed(demand_crop, depth, price_n, price_p, price_k)
        
        st.subheader("Considerando uma area de lavoura de 1 hectare:")
        st.write(f"1) Para a suplementação de {sup} com sedimentos será necessária a escavação de {vols['Vol of excavation']:.1f} m3, \
            resultando em transporte de {vols['Vol of transport']:.1f} m3 de sedimento (apróx R$ {cost_trans:.2f})\n")
        
        st.write(f"2) Para suplementação adicional serão necessários:\n")
        st.write(f" 2.1) {add_sup['Mass N']:.2f} quilogramas de Uréia (apróx R$ {add_sup['Cost N']:.2f}); ")
        st.write(f" 2.2) {add_sup['Mass P']:.2f} quilogramas de Superfosfato simples (apróx R$ {add_sup['Cost P']:.2f});")
        st.write(f" 2.3) {add_sup['Mass N']:.2f} quilogramas de Cloreto de potássio (apróx R$ {add_sup['Cost K']:.2f})")
        st.write(f"O custo dos nutrientes repostos pelos sedimentos seria de aproximadamente R$ {cost_sed:.2f}")
    
with col61:
    st.write(" ")
with col63:
    st.write(" ")
with col62:
    st.image("figs/4.png", width = 600)
    
#%% additional information

st.subheader("Sobre o app")
st.write("O projeto Re-Sed, desenvolvido por MSc. Brenda Bragga, MSc. Gabriela Domingos e Prof. Dr. Pedro Medeiros faz parte do projeto\
    Cientista Chefe.......")
st.write("Contato: [phamedeiros@ifce.edu.br](phamedeiros@ifce.edu.br)")
st.write(" ")
st.write(" ")
st.write("Desenvolvido por: [Dr. Pedro Alencar](https://www.tu.berlin/oekohydro/team/pedro-alencar/)")