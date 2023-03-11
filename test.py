
#%% import functions
import functions_resed as rsd
# %%
demand_crop = rsd.demand_from_crop(6, 0.24, 1.67, "Sorgo forrageiro")
demand_crop
# %%

npk_sed = rsd.npk_to_gkg(3.56, 210, 0.55)
individual_bal = rsd.sediment_balance_individual(demand_crop, npk_sed)
individual_bal
# %%

comb_bal = rsd.sediment_balance_combined(npk_balance = individual_bal, 
                                         npk_demand = demand_crop, 
                                         npk_sed = npk_sed)

comb_bal
# %%
bags = rsd.bags_supplement(comb_bal)
bags
# %%
prices_list = rsd.bag_price_as_list(100, 100, 197)

cost = rsd.cost_supplements(bags, prices_list)
cost
# %%
