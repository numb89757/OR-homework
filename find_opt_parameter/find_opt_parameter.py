# -*- coding: utf-8 -*-
"""
==============================================================================
PARAMETER STUDY
==============================================================================
DESCRIPTION
    This script defines the simulation execution pipeline and handlers for 
    sales and logistics operations.

CREATED
    3/25/2018
    last modified: 4/2/2018

COLLABORATORS
    R. Borela
    S. Hanumasagar
    F. Liu
    N. Roy 
"""
import sys
import parameters

# 获取参数
parameters.param_lambda = float(sys.argv[1])
import numpy as np
from application import *
import os
import shutil
#===================
# DEFINE CASE CLASS



class case:
    def __init__(self,n_trucks,interval,base_cost,cost_per_mile,max_stores,min_percent, tag):
        self.n_trucks = n_trucks
        self.interval = interval
        self.base_cost = base_cost
        self.cost_per_mile = cost_per_mile
        self.max_stores = max_stores
        self.min_percent = min_percent
        self.tag = tag

#==========
# BASELINE

# number of trucks
n_trucks = 4  #default = 4
# number of days between deliveries
interval = 1
# truck daily base cost
base_cost = 100
# truck cost per mile
cost_per_mile = 10
# maximum number of stores a truck can visit
max_stores = 3
# min percentage of stock before issuing warning
min_percent = .8  #default = .8

# create baseline case
# baseline = case(n_trucks,interval,base_cost,cost_per_mile,max_stores,min_percent,'baseline')

#====================
# EXECUTE SIMULATION

# start = time.time()
# sim=simulation(baseline)
# sim.advance_time(360)
# end = time.time()

# print('simulation took:',end-start)

#==================
# NUMBER OF TRUCKS

def study_trucks():
    n_truck_cases = []
    # loop over variables
    for n_t in range(1,11):
        # define case
        this_case = case(n_t, baseline.interval, baseline.base_cost, 
                         baseline.cost_per_mile, baseline.max_stores,
                         baseline.min_percent,'n_trucks')
        # generate sim case
        n_truck_cases.append(simulation(this_case))
    
    # loop over cases
    for n_t in n_truck_cases:
        # execute the sim case
        n_t.advance_time(360)
    
    # get useful information for plotting
    cum_revenue = [sim.cum_revenue for sim in n_truck_cases]
    cum_del_cost = [sim.cum_delivery_cost  for sim in n_truck_cases]
    cum_opp_cost =  [sim.cum_opp_cost for sim in n_truck_cases]
    cum_profit =  [sim.cum_profit for sim in n_truck_cases]
    
    # activate interactive mode
    #plt.ion()
    
    # generate plot
    n_trucks_finances_fig = plot_study_finances('# trucks', range(1,11), cum_revenue, cum_del_cost, cum_opp_cost)
    n_trucks_profit_fig = plot_study_profit('# trucks', range(1,11), cum_profit)
    n_trucks_finances_fig.savefig('study_n_trucks_finances.png')
    n_trucks_profit_fig.savefig('study_n_trucks_profit.png')

#============
# MAX STORES

def study_maxstores():
    n_maxstore_cases = []
    # loop over variables
    for n_ms in range(1,6):
        # define case
        this_case = case(baseline.n_trucks, baseline.interval, baseline.base_cost,baseline.cost_per_mile, n_ms,
                         baseline.min_percent,'max_stores')
        # generate sim case
        n_maxstore_cases.append(simulation(this_case))
    
    # loop over cases
    for n_ms in n_maxstore_cases:
        # execute the sim case
        n_ms.advance_time(360)
    
    # get useful information for plotting
    cum_revenue = [sim.cum_revenue for sim in n_maxstore_cases]
    cum_del_cost = [sim.cum_delivery_cost  for sim in n_maxstore_cases]
    cum_opp_cost =  [sim.cum_opp_cost for sim in n_maxstore_cases]
    cum_profit =  [sim.cum_profit for sim in n_maxstore_cases]
    
    # activate interactive mode
    #plt.ion()
    
    # generate plot
    n_maxstores_finances_fig = plot_study_finances('# maxstores', range(1,6), cum_revenue, cum_del_cost, cum_opp_cost)
    n_maxstores_profit_fig = plot_study_profit('# maxstores', range(1,6), cum_profit)
    n_maxstores_finances_fig.savefig('study_n_maxstores_finances.png')
    n_maxstores_profit_fig.savefig('study_n_maxstores_profit.png')

#================
# MIN PERCENTAGE

def study_min_percent():
    min_percent_cases = []
    # loop over variables
    for min_p in np.linspace(0,.9,10):
        # define case
        this_case = case(baseline.n_trucks, baseline.interval, baseline.base_cost, 
                         baseline.cost_per_mile, baseline.max_stores,
                         min_p,'min_percent')
        # generate sim case
        min_percent_cases.append(simulation(this_case))
        
    # loop over cases
    for min_p in min_percent_cases:
        # execute the sim case
        min_p.advance_time(360)

    # get useful information for plotting
    cum_revenue = [sim.cum_revenue for sim in min_percent_cases]
    cum_del_cost = [sim.cum_delivery_cost  for sim in min_percent_cases]
    cum_opp_cost =  [sim.cum_opp_cost for sim in min_percent_cases]
    cum_profit =  [sim.cum_profit for sim in min_percent_cases]
  
    # activate interactive mode
    #plt.ion()
    
    # generate plot
    min_percent_finances_fig = plot_study_finances('min percent', np.linspace(0,.9,10), cum_revenue, cum_del_cost, cum_opp_cost)
    min_percent_profit_fig = plot_study_profit('min percent', np.linspace(0,.9,10), cum_profit)
    min_percent_finances_fig.savefig('study_min_percent_finances.png')
    min_percent_profit_fig.savefig('study_min_percent_profit.png')



#================================= to find the optimal parameter =================================
best_truck, best_min_percent, best_profit, best_revenue, best_opp_cost, best_delivery = 0, 0, 0, 0, 0, 0
opt = -10000000
for truck in range(1,11):
    print("truck=",truck)
    for min_percent in [10,30,50,70,90]:
        print("min_percent=",min_percent)
        min_percent = min_percent / 100
        base = case(truck, interval, base_cost, cost_per_mile, max_stores, min_percent, '')
        sim = simulation(base)
        sim.advance_time(360)
        if sim.cum_profit > opt:
            opt = sim.cum_profit
            best_truck = truck
            best_min_percent = min_percent
            best_revenue = sim.cum_revenue
            best_profit = sim.cum_profit
            best_opp_cost = sim.cum_opp_cost
            best_delivery = sim.cum_delivery_cost

# print(parameters.param_lambda, best_truck, best_min_percent, best_profit, best_revenue, best_opp_cost, best_delivery)
concat_txt = 'lambda:' + str(parameters.param_lambda) + ' ' + 'best_truck:' +str(best_truck)+' ' + 'best_min_percent:' +str(best_min_percent)+' ' + 'best_profit:' +str(best_profit)+' ' + 'best_revenue:' +str(best_revenue)+' ' + 'best_opp_cost:' +str(best_opp_cost)+' ' + 'best_delivery:' +str(best_delivery)
print(concat_txt)
with open("result.txt", "a") as file:
    file.write(concat_txt)
    file.write("\n")  # 添加换行符

