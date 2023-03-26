"""
    Application to estimate usage of sediments from reservoir as fertilizer (NPK)


    Pedro Alencar
    11.03.2023
"""

#%% import libraries

import pandas as pd
import numpy as np
import streamlit as st

import python.functions_resed as rsd

st.set_page_config(layout="wide")

#%% app
coltitle, colempty1, colfig1 = st.columns([3,2,1])
with coltitle:
    st.title("REUSO DE SEDIMENTO ASSOREADO EM AÇUDES")
    st.subheader("Dosagem de sedimento e custos de fertilização")
    st.write("  ")
    st.write("  ")

with colfig1:
    st.image("figs/4_crop.png", use_column_width= True)   




# # create two columns of five text inputs
col1, col2, col3, col4=  st.columns([1,1,1,1])
with col1:
    # st.subheader("Propriedades do solo")
    st.write('<p style="font-size:24px"><b>Propriedades do <br>solo</b></p>',
                     unsafe_allow_html=True)
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
                                 value = 1.5,
                                 key = "soil_dens",
                              step=0.01,format="%.2f")

with col2:
    # st.subheader("Propriedades do sedimento")
    st.write('<p style="font-size:24px"><b>Propriedades do <br>sedimento</b></p>',
                     unsafe_allow_html=True)
    sed_n = st.number_input(label = "N (g/kg) ",
                             min_value=0.,
                             max_value= 10000.,
                             value = 5.,
                             key = "sed_n",
                              step=0.01,format="%.2f")
    sed_p = st.number_input(label = "P (mg/kg) ",
                             min_value=0.,
                             max_value= 10000., 
                             value = 5.,
                             key = "sed_p",
                              step=0.01,format="%.2f")
    sed_k = st.number_input(label = "K (cmolc/kg) ",
                             min_value=0.,
                             max_value= 10000.,
                             value = 5.,
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
    # st.subheader("Preços dos suplementos (R$/kg)")
    st.write('<p style="font-size:24px"><b>Preços dos suplementos (R$/kg)</b></p>',
                     unsafe_allow_html=True)
    price_n = st.number_input(label = "Uréia",
                              min_value=0.,
                              max_value= 10000.,
                              value = 5., 
                              key = "price_n",
                              step=0.01,format="%.2f")
    price_p = st.number_input(label = "Superfosfato simples",
                              min_value=0.,
                              max_value= 10000., 
                              value = 5.,
                              key = "price_p",
                              step=0.01,format="%.2f")
    price_k = st.number_input(label = "Cloreto de Potássio",
                              min_value=0.,
                              max_value= 10000.,
                              value = 5., 
                              key = "price_k",
                              step=0.01,format="%.2f")
   
with col4:
    # st.subheader("Manejo da cultura")
    st.write('<p style="font-size:24px"><b>Manejo da cultura e <br> dos sedimentos</b></p>',
                     unsafe_allow_html=True)
    crop = st.selectbox(label = "Cultura",
                        # options = ("Algodão (sequeiro)", "Algodão (irrigado)", "Batada doce",
                        # "Feijão de corda", "Mandioca", "Milho (sequeiro)",
                        # "Milho (irrigado)", "Sorgo forrageiro"),
                        options = ("Abóbora", "Algodão Herbáceo (Sequeiro)", "Algodão Herbáceo (Irrigado)",
                                 "Amendoim", "Batata doce", "Batatinha", "Cebolinha ou Coentro", 
                                 "Feijão de corda", "Feijão mulatinho (Sequeiro)", "Mamona", 
                                 "Mandioca", "Milho (Sequeiro)", "Milho (Irrigado)", "Pimentão", 
                                 "Sorgo forrageiro"),
                        key = "crop")
    
    

    sup = st.selectbox(label = "Nutriente suplementado por sedimentos",
                        options = ("Nitrogênio", "Fósforo", "Potássio"),
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
    
st.markdown("""---""")


st.subheader("Resultados:")
if st.button('CALCULAR'):
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
    else: # compute
        st.subheader("Considerando uma área de lavoura de 1 hectare:")

        demand_crop = rsd.demand_from_crop(soil_p, soil_k, soil_dens, crop, depth) # crop demand
            
         #convert units  
        npk_soil_gkg = rsd.npk_to_gkg(soil_n, soil_p, soil_k) # soil
        npk_soil_kgm3 = rsd.npk_to_kgm3(npk_soil_gkg, soil_dens) 
                    
        npk_sed_gkg = rsd.npk_to_gkg(sed_n, sed_p, sed_k) # sed
        npk_sed_kgm3 = rsd.npk_to_kgm3(npk_sed_gkg, sed_dens) 
        
        # get mixture    
        depth_sed = rsd.get_mix(demand_crop, npk_soil_kgm3, npk_sed_kgm3, depth, sup) 
        
        if depth_sed < 0:
            st.subheader(f"Não há suficiente {sup} no sedimento.")
            print_ = 0
                       
        deficit_new = rsd.persistent_deficit(depth_sed, demand_crop, npk_soil_kgm3, npk_sed_kgm3, depth)            
        add_sup = rsd.additional_supplements(deficit_new, depth, price_n, price_p, price_k)            
        vols = rsd.soil_movement(depth_sed)
        
        # get costs    
        cost_trans = vols["Vol of transport"]*(8.6 + 0.0026*dist) # equation estimated from SEINFRA (conta 2.4)
        all_costs = cost_trans + add_sup['Cost N'] + add_sup['Cost P'] + add_sup['Cost K']
        
        no_sed = rsd.cost_no_sed(demand_crop, depth, price_n, price_p, price_k)
        all_costs_no_sed = no_sed['Cost N'] + no_sed['Cost P'] + no_sed['Cost K']
        

    if print_ == 1:        
        col51, col52 = st.columns([3,2])
        
        with col51: 
            
            st.write('<p style="font-size:22px"><b>1) Quantidades de fertilização COM reuso de sedimento e suplementação</b></p>',
                     unsafe_allow_html=True)
            st.write(f"* Volume de escavação de sedimentos {vols['Vol of excavation']:,.2f} metros cúbicos")
            st.write(f"* Volume de transporde de sedimentos {vols['Vol of transport']:,.2f} metros cúbicos")
            st.write(f"* Massa de uréia: {add_sup['Mass N']:,.2f} kg")
            st.write(f"* Massa de superfosfato simples: {add_sup['Mass P']:,.2f} kg")
            st.write(f"* Massa de cloreto de potássio: {add_sup['Mass K']:,.2f} kg")
            
            
            st.write('<p style="font-size:22px"><b>2) Custos de fertilização COM reuso de sedimento e suplementação</b></p>',
                     unsafe_allow_html=True)
            st.write(f"* Custo com escavação e transporte de sedimento: R$ {cost_trans:,.2f}")
            st.write(f"* Custo com suplementação com uréia: R$ {add_sup['Cost N']:,.2f}")
            st.write(f"* Custo com suplementação com superfosfato simples: R$ {add_sup['Cost P']:,.2f}")
            st.write(f"* Custo com suplementação com cloreto de potássio: R$ {add_sup['Cost K']:,.2f}")
            st.write(f"* Custo total: <b><u>R$ {all_costs:,.2f}</u></b>",
                     unsafe_allow_html=True)
            
        with col52:
            
            st.write('<p style="font-size:22px"><b>1) Quantidades de fertilização SEM reuso de sedimento</b></p>',
                     unsafe_allow_html=True)
            st.write(f"* Volume de escavação de sedimentos 0.00 metros cúbicos")
            st.write(f"* Volume de transporde de sedimentos 0.00 metros cúbicos")
            st.write(f"* Massa de uréia: {no_sed['Mass N']:,.2f} kg")
            st.write(f"* Massa de superfosfato simples: {no_sed['Mass P']:,.2f} kg")
            st.write(f"* Massa de cloreto de potássio: {no_sed['Mass K']:,.2f} kg")
            
            
            st.write('<p style="font-size:22px"><b>2) Custos de fertilização SEM reuso de sedimento</b></p>',
                     unsafe_allow_html=True)

            st.write(f"* Custo com escavação e transporte de sedimento: R$ 0.00")
            st.write(f"* Custo com suplementação com uréia: R$ {no_sed['Cost N']:,.2f}")
            st.write(f"* Custo com suplementação com superfosfato simples: R$ {no_sed['Cost P']:,.2f}")
            st.write(f"* Custo com suplementação com cloreto de potássio: R$ {no_sed['Cost K']:,.2f}")
            st.write(f"* Custo total: <b><u>R$ {all_costs_no_sed:,.2f}</u></b>",
                     unsafe_allow_html=True)
else:
    st.write(" ")

st.write(" ")    
st.write(" ")    
st.write(" ")    
st.write("""<p style='color:#808080;'><i><u>Dica: Salve esta página como um relatório em pdf</u><br>
         &nbsp;&nbsp;&nbsp;&nbsp; 1) Clique com o botão direito do mouse em qualquer ponto da tela e escolha 'imprimir'.<br>
         &nbsp;&nbsp;&nbsp;&nbsp; 2) Escolha _layout_ paisagem para uma melhor visualização. <br>
         &nbsp;&nbsp;&nbsp;&nbsp; 3) Pressione salvar. <br>
         &nbsp;&nbsp;&nbsp;&nbsp; 4) Pronto. O arquivo será salvo automaticamente na sua pasta de downloads.
         </i></p>
         """,
         unsafe_allow_html=True)


    
#%% additional information

st.markdown("""---""")
st.subheader("Sobre o app")

st.write("O projeto RESED (Reuso de sedimento para conservação de solo e água) é desenvolvido por \
    pesquisadores/as do Instituto Federal de Educação, Ciência e Tecnologia do Ceará - IFCE e \
    pela Universidade Federal do Ceará - UFC. O desenvolvimento deste aplicativo foi financiado pelo \
    Programa Cientista-Chefe em Agricultura (Convênio 14/2022 SDE/ADECE/FUNCAP e Processo 08126425/2020/FUNCAP), \
    do Governo do Estado do Ceará")
st.write("**Equipe:**")
st.write("[MSc. Brennda Braga](http://lattes.cnpq.br/0982317513941443) (pesquisadora)")
st.write("[MSc. Gabriela Domingos](http://lattes.cnpq.br/7655326235323800) (pesquisadora)")
st.write("[Dr. Pedro Alencar](https://www.tu.berlin/oekohydro/team/pedro-alencar/) (desenvolvedor)")
st.write("[Prof. Dr. Pedro Medeiros](http://lattes.cnpq.br/4970091740105771) (coordenador)")

col71, col72, col73 = st.columns([1,2,1])
with col72:  
    st.image("figs/logos.png", use_column_width = True)
