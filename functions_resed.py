from math import trunc
import numpy as np

# Global variables - table 2
MATRIX_P = ([60,40,30],
           [70,50,40],
            [120,80,40],
            [80,50,30],
            [60,40,20],
            [50,40,30],
            [90,60,40],
            [70,50,40],)

MATRIX_K = ([40,30,20],
            [50,40,30],
            [90,70,40],
            [30,20,10],
            [40,30,20],
            [40,30,20],
            [60,40,30],
            [50,40,30],)

VECT_N = (50,80,40,20,40,70,90,60)

OPTIONS = ("Algodão (sequeiro)", 
           "Algodão (irrigado)",
           "Batada doce",
           "Feijão de corda", 
           "Mandioca", 
           "Milho (sequeiro)",
           "Milho (irrigado)",
           "Sorgo forrageiro")

CONVERSION = {
    "P -> P2O5": 2.2914,
    "P2O5 -> P2O5-18p":5.556,
    "K -> K2O":1.2046,
    "K2O -> KCl":1.667,
    "N -> Urea":2.222
    }



def conc_mass_to_vol(conc_mass, dens, input_type = 1):
    """Converts concentration values from cmolc/kg;g/kg;mg/kg to mmolc/dm3;mg/dm3 to 

    Args:
        conc_mass (float): value of concentration in cmolc/kg       
        dens (float): soil density in kg/dm3
        input_type (int): type of input. 
            1: cmolc/kg
            2: g/kg (only for N)
            3: mg/kg (only for P)
    """
    
    if input_type == 1:    
        conc_vol = conc_mass*10*dens
    elif input_type == 2:
        conc_vol = conc_mass*dens*1000
    elif input_type == 3:
        conc_vol = conc_mass*dens
    else:
        conc_vol = "NULL"
    
    return conc_vol

def npk_to_gkg(conc_n, conc_p, conc_k):
    
    """get concentrations into g/kg
    """
    
    # get all concentrations into g/kg
    sed_n_mass = conc_n
    sed_p_mass = conc_p/1000
    sed_k_mass = conc_k*39.1/100
    
    npk = {"N":sed_n_mass,
           "P":sed_p_mass,
           "K":sed_k_mass}
    
    return npk

def demand_from_crop(soil_p, soil_k, dens, crop):
    """  Function to get the amount of nutrients based on culture.
    
    Values extracted from Table 2 (get reference)

    Args:
        soil_p (float): concentration of P in mg/kg
        soil_k (float): concentration of K in cmolc/kg
        dens (float): soil density in kg/dm3
        crop (string): which crop (selected from list)
    """
    
    soil_p_vol = conc_mass_to_vol(soil_p, dens, input_type=3)
    soil_k_vol = conc_mass_to_vol(soil_k, dens, input_type=1)
    
    id_crop = OPTIONS.index(crop)
    
    id_p = min(trunc(soil_p_vol/7.1),2)
    id_k = min(trunc(soil_k_vol/0.8),2)
    
    npk = {"N": VECT_N[id_crop],
            "P": MATRIX_P[id_crop][id_p],
            "K": MATRIX_K[id_crop][id_k]}
    
    return npk
    
def sediment_balance_individual(npk_demand, npk_sed):
    """get balance of nutrients between sediment and demand.

    Args:
        npk_demand (list): output from `demand_from_crop()`
        sed_npk (list): output from `npk_to_gkg()` for sediment values
    """
    
    npk_balance = {"N": 0, "P": 0, "K": 0}
    
    # balange in kg/ha
    npk_balance["N"] = 1000*npk_demand["N"]/npk_sed["N"]
    npk_balance["P"] = 1000*npk_demand["P"]/npk_sed["P"]
    npk_balance["K"] = 1000*npk_demand["K"]/npk_sed["K"]
    
    return(npk_balance)
    
    
def sediment_balance_combined(npk_balance, npk_demand, npk_sed):
    
    ref = min(list(npk_balance.values()))
    
    npk_balance_comb = {
        "N": ref*npk_sed["N"]/1000,
        "P": ref*npk_sed["P"]/1000,
        "K": ref*npk_sed["K"]/1000}
    
    urea = npk_demand["N"] - npk_balance_comb["P"]*CONVERSION["N -> Urea"]
    p2o5 = npk_demand["P"] - npk_balance_comb["P"]*CONVERSION["P -> P2O5"]
    k2o = npk_demand["K"] - npk_balance_comb["K"]*CONVERSION["K -> K2O"]
    
    supplement = {
        "N":urea,
        "P":p2o5,
        "K":k2o}
    
    return supplement

def bags_supplement(supplement):
    
    sup_com = {
        "N":supplement["N"],
        "P":supplement["P"]*CONVERSION["P2O5 -> P2O5-18p"],
        "K":supplement["K"]*CONVERSION["K2O -> KCl"]}
    
    sup_bag = {
        "N":trunc(sup_com["N"]/25)+1,
        "P":trunc(sup_com["P"]/25)+1,
        "K":trunc(sup_com["K"]/25)+1}
    
    return sup_bag

def bag_price_as_list(price_n, price_p, price_k):
    
    price_sup = {"N": price_n,
                 "P": price_p, 
                 "K": price_k}
    
    return(price_sup)

def cost_supplements(bags, prices):
    
    cost_sup = {
        "N":bags["N"]*prices["N"],
        "P":bags["P"]*prices["P"],
        "K":bags["K"]*prices["K"]}
    
    return cost_sup

# estimate cost of transport
# def cost_transport():
