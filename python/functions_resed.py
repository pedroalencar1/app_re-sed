from math import trunc, ceil
import numpy as np

# Global variables - table 2
MATRIX_P = ([80,60,40],
            [60,40,30],
            [70,50,40],
            [80,50,30],
            [120,80,40],
            [200,130,80],
            [15,12,10],
            [80,50,30],
            [80,50,30],
            [80,60,40],
            [60,40,20],
            [50,40,30],
            [90,60,40],
            [300,200,150],
            [70,50,40])


MATRIX_K = ([60,40,20],
            [40,30,20],
            [50,40,30],
            [40,30,20],
            [90,70,40],
            [160,100,60],
            [12,6,4],
            [30,20,10],
            [40,30,20],
            [60,40,20],
            [40,30,20],
            [40,30,20],
            [60,40,30],
            [300,200,100],
            [50,40,30])

VECT_N = (50, 50, 80, 15, 40, 90, 9, 20, 15, 60, 40, 70, 90, 190, 60)
# VECT_N = (50,80,40,20,40,70,90,60)

EXPANSION_FACTOR = 1.25

OPTIONS = ("Abóbora", 
           "Algodão Herbáceo (Sequeiro)", 
           "Algodão Herbáceo (Irrigado)",
           "Amendoim",
           "Batata doce",
           "Batatinha", 
           "Cebolinha ou Coentro", 
           "Feijão de corda", 
           "Feijão mulatinho (Sequeiro)", 
           "Mamona", 
           "Mandioca", 
           "Milho (Sequeiro)", 
           "Milho (Irrigado)",
           "Pimentão", 
           "Sorgo forrageiro")

CONVERSION = {
    "P -> P2O5": 2.2914,
    "P2O5 -> P2O5-18p":5.556,
    "K -> K2O":1.2046,
    "K2O -> KCl":1.667,
    "N -> Urea":2.222
    }


def check_sed(supplement,
              sed_n, soil_n,
              sed_p, soil_p,
              sed_k, soil_k):
    """checks if there is enough nutrients in the sediment to supplement soil

    Args:
        supplement (string): name of nutrient to be supplemented

    Returns:
        bool: if the ampount of nutrient in the sediment is lower than in the soil
    """
    
    if supplement == "Nitrogênio":
        check = sed_n <= soil_n
    elif supplement == "Fósforo":
        check = sed_p <= soil_p
    else:
        check = sed_k <= soil_k
    
    return check
    

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


def npk_to_kgm3(npk_gkg, dens):
    
    """get concentrations into kg/m3
    """
    
    # get all concentrations into g/kg
    n_kgm3 = npk_gkg["N"] * dens
    p_kgm3 = npk_gkg["P"] * dens
    k_kgm3 = npk_gkg["K"] * dens
    
    npk = {"N":n_kgm3,
           "P":p_kgm3,
           "K":k_kgm3}
    
    return npk


def demand_from_crop(soil_p, soil_k, dens, crop, depth):
    """  Function to get the amount of nutrients based on culture.
    
    Values extracted from Table 2 (get reference)

    Args:
        soil_p (float): concentration of P in mg/kg
        soil_k (float): concentration of K in cmolc/kg
        dens (float): soil density in kg/dm3
        crop (string): which crop (selected from list)
        depth (float): depth of mix in cm
        
    Returns: demans in kg/m3
    """
    
    soil_p_vol = conc_mass_to_vol(soil_p, dens, input_type=3)
    soil_k_vol = conc_mass_to_vol(soil_k, dens, input_type=1)
    
    id_crop = OPTIONS.index(crop)
    
    id_p = min(trunc(soil_p_vol/7.1),2)
    id_k = min(trunc(soil_k_vol/0.8),2)
    depth_ = 1/(10000*depth/100)
    
    npk = {"N": depth_*VECT_N[id_crop],
            "P": depth_*MATRIX_P[id_crop][id_p]/CONVERSION["P -> P2O5"],
            "K": depth_*MATRIX_K[id_crop][id_k]/CONVERSION["K -> K2O"]}
    
    return npk

def get_mix(npk_demand, npk_soil, npk_sed, depth, supplement):
    """get mix

    Args:
        npk_demand (dict): nutrient demand in kg/m3
        npk_soil (dict): nutrient content in kg/m3
        npk_sed (dict): nutrient content in kg/m3
        depth (float): depth of mix in cm
        supplement (string): name of nutrient to be supplemented
        
    Returns: depth of sediment in centimeter
    """
    nutrients = ("Nitrogênio", "Fósforo", "Potássio")
    
    id_sup = nutrients.index(supplement)
    
    demand = np.array(list(npk_demand.values()))
    soil_supply = np.array(list(npk_soil.values()))
    sed_supply = np.array(list(npk_sed.values()))
    
    sed_supply_exp = sed_supply/EXPANSION_FACTOR
        
    d_sed = depth*demand[id_sup]/(sed_supply_exp[id_sup] - soil_supply[id_sup])

    return d_sed
    
def persistent_deficit(d_sed, npk_demand, npk_soil, npk_sed, depth):
    """_summary_

    Args:
        d_sed (float): depth of sediment used
        npk_demand (dict): nutrient demand in kg/m3
        npk_soil (dict): nutrient content in kg/m3
        npk_sed (dict): nutrient content in kg/m3
        depth (float): depth of mix in cm

    Returns:
        deficit_new (array): [N,P,K] values of deficit in kg/m3
    """
    
    demand = np.array(list(npk_demand.values()))
    soil_supply = np.array(list(npk_soil.values()))
    sed_supply = np.array(list(npk_sed.values()))
    
    sed_supply_exp = sed_supply/EXPANSION_FACTOR
    
    supply_new = (d_sed*sed_supply_exp + (depth - d_sed)*soil_supply)/depth
    deficit_new = demand + soil_supply - supply_new
 
    deficit_new[deficit_new < 0.001] = 0 # remove rounding erros
    
    return deficit_new

def additional_supplements(deficit_new, depth, price_n, price_p, price_k):
    
    mass_n = deficit_new[0]*depth*100*CONVERSION["N -> Urea"]  #kg
    mass_p = deficit_new[1]*depth*100*CONVERSION["P -> P2O5"]*CONVERSION["P2O5 -> P2O5-18p"] #kg
    mass_k = deficit_new[2]*depth*100*CONVERSION["K -> K2O"]*CONVERSION["K2O -> KCl"]  #kg
    
    bag_n = ceil(mass_n/25)
    bag_p = ceil(mass_p/25)
    bag_k = ceil(mass_k/25)
    
    cost_n = ceil(mass_n)*price_n
    cost_p = ceil(mass_p)*price_p
    cost_k = ceil(mass_k)*price_k
    
    output = {"Mass N": mass_n,
              "Mass P": mass_p,
              "Mass K": mass_k,
              "Bag N": bag_n,
              "Bag P": bag_p,
              "Bag K": bag_k,
              "Cost N": cost_n,
              "Cost P": cost_p,
              "Cost K": cost_k,
              }
    
    return output
    
def soil_movement(d_sed):
    
    vol_truck = d_sed*100
    vol_excavation =vol_truck/EXPANSION_FACTOR 
    
    vols = {"Vol of transport": vol_truck,
            "Vol of excavation": vol_excavation}

    return vols

def cost_no_sed(npk_demand, depth, price_n, price_p, price_k):
    
    # prices = np.array([price_n, price_p, price_k])
    # demand_cost = np.array(list(npk_demand.values()))
    
    
    mass_n = npk_demand["N"]*depth*100*CONVERSION["N -> Urea"]  #kg
    mass_p = npk_demand["P"]*depth*100*CONVERSION["P -> P2O5"]*CONVERSION["P2O5 -> P2O5-18p"] #kg
    mass_k = npk_demand["K"]*depth*100*CONVERSION["K -> K2O"]*CONVERSION["K2O -> KCl"]  #kg
    
    cost_n = ceil(mass_n)*price_n
    cost_p = ceil(mass_p)*price_p
    cost_k = ceil(mass_k)*price_k
    
    # kgs = np.ceil(demand_cost*depth*100)

    output = {"Mass N": mass_n,
              "Mass P": mass_p,
              "Mass K": mass_k,
              "Cost N": cost_n,
              "Cost P": cost_p,
              "Cost K": cost_k,
              }
    
    return output
    
    
    
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
        "N":trunc(sup_com["N"]),
        "P":trunc(sup_com["P"]),
        "K":trunc(sup_com["K"])}
    
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
