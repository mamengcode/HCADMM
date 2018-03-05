# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 16:09:20 2018

@author: maxxx971

For in-network acceleration, but on RANDOM graphs.

"""

#%% import libraries
from Simulator import Simulator
#from Admm_simulator import Simulator
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

#%% simulation setting
# 1. graph: N, d
# 2. function: objective value, opt_value
# 3. penalty parameters
# 4. simulation: max_iter, epsilon, initial value


# 1. graph
n_nodes = 50     # number of nodes
d = 3            # dimension of variable at each node

# 2. function
# objective value
v = np.random.rand(n_nodes, d)
# optimal value
x_opt = v.mean()

# 3. simulation setting
graphs = [nx.lollipop_graph(n_nodes//2, n_nodes - n_nodes//2 ),
          nx.connected_caveman_graph(n_nodes//5, 5),
          Simulator.erdos_renyi(n_nodes, 0.1),
          Simulator.erdos_renyi(n_nodes, 0.05)]
graph_name = ['Lollipop', 'Caveman', 'ER(p=0.01)', 'ER(p=0.05)']
line_style = ['--rd', '-rd',
              '--c^', '-c^',
              '--bs', '-bs',
              '--go', '-go']
best_penalty = [{'D-CADMM': 5, 'H-CADMM': 5},
                {'D-CADMM': 5, 'H-CADMM': 5},
                {'D-CADMM': 5, 'H-CADMM': 5},
                {'D-CADMM': 5, 'H-CADMM': 5}]
all_mode = ['D-CADMM', 'H-CADMM']
max_iter = 500
epsilon = 1e-8
# start simulation
setting = {'penalty': -1, 'max_iter': max_iter, 'objective': v,
           'initial': 0 * np.random.randn(n_nodes, d),
           'random_hyperedge': [],
           'epsilon': epsilon,
           'n_FC': -1}

#title_str = '{}, Nodes: {}, Edges: {}'.format(graph_type, n_nodes,
#             g.number_of_edges())

#%% simulation
# centralized
#sim.mode = 'centralized'
#sim.simulation_setting['penalty'] = best_penalty[0]
#c_opt_gap, c_primal_residual, c_dual_residual = sim.run_least_squares()

sim_data = []
for G, name, rho in zip(graphs, graph_name, best_penalty):
    sim = Simulator(G, simulation_setting=setting)
    for mode in all_mode:
        data = {}
        sim.mode = mode
        sim.setting['penalty'] = rho[mode]
        opt_gap, primal_residual, dual_residual,_ = sim.run_least_squares()
        data['legend'] = name + ' ' + sim.mode
        data['opt_gap'] = opt_gap
        data['primal_residual'] = primal_residual
        data['dual_residual'] = dual_residual
        sim_data.append(data)

#%%
#plt.figure()
#plt.semilogy(sim_data[0]['opt_gap'], '--r', label='frist')
#plt.semilogy(sim_data[1]['opt_gap'], '-b', label='second')
#
#plt.legend()
#plt.show()
## decentralized ADMM
#   sim.mode = 'decentralized'
#   sim.simulation_setting['penalty'] = best_penalty[2]
#   d_opt_gap, d_primal_residual, d_dual_residual = sim.run_least_squares()


#%% plot
n_markers = 20
#marker_at = range(0, setting['max_iter'], setting['max_iter'] // n_markers)
marker_at = setting['max_iter'] // n_markers

# accuracy vs iteration
fig = plt.figure(1, figsize=(8, 6))
# fig = plt.figure()
for data, style in zip(sim_data, line_style):
    plt.semilogy(data['opt_gap'], style, label=data['legend'],
                 markevery=marker_at)

plt.ylabel('Accuracy')
plt.xlabel('Iterations')
# plt.title(title_str)
plt.ylim(ymin=epsilon)
plt.legend()


fig.tight_layout()
plt.show()