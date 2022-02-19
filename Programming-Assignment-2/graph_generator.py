# to make this code run quick for a graph with n=1E7 vertices 
# Every edge is probable with a given probablity p

import time
import numpy as np

import torch
def make_graph(edge_probablity):

    gpu_device = torch.device('cuda')
    cpu_device = torch.device('cpu')
    gpu_batch = int(3E8)
    num_vertices=1E7

    max_edges = int(num_vertices*(num_vertices-1)/2)
    num_itter = max_edges//gpu_batch
    remaining_rands = max_edges%gpu_batch
    print(max_edges, num_itter, remaining_rands)

    # sample the edges
    edges = []
    buff = torch.zeros((gpu_batch,), device=gpu_device)
    for i in range(num_itter):
        torch.rand(size=(gpu_batch,), device=gpu_device, out=buff) # sample uniforms
        edges.append(((buff < edge_probablity).nonzero() + i*gpu_batch).to(cpu_device)) # sampled edges
        print(f'\r{(i+1)*100/num_itter:.2f}%, {len(edges)}, {i*gpu_batch}', end='')

    # sample remaining edges
    edges.append(
        ((torch.rand(size=(remaining_rands,)) < edge_probablity).nonzero() + num_itter*gpu_batch)
        ) # sampled edges    
    print()
    return edges

# import random
# from numba import jit
# @jit(nopython=True)
# def make_graph(edge_probablity):
#     num_vertices=1E7
#     max_edges = int(num_vertices*(num_vertices-1)/2)

#     edges = []
#     for i in range(num_vertices):
#         for j in range(i+1, num_vertices):
#             if random.uniform(0,1) < edge_probablity:
#                 edges.append(i*num_vertices+j)
#         # print(round((i+1)*100/num_vertices,2))
#     return edges


if __name__ =='__main__':
    s = time.time()
    make_graph(1E-7)
    print('time taken:', time.time()-s)











# device = torch.device('cuda')

# torch.randint(0,2,(int(1E8),),device=device)
# n=1E2
# s= time.time()
# for i in range(int(n)):
#     x = torch.randint(0,2,(int(4E8),),device=device)
#     del x
# print((time.time()-s))