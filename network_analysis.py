import os, csv
import numpy as np
import networkx as nx

def calculate_average_neighbor_difference(graph, temp_d_sim_score):
    total_difference = 0
    total_neighbors = 0

    for node in graph.nodes():
        neighbors = graph.neighbors(node)
        if not neighbors:
            continue

        node_score = temp_d_sim_score[node]
        for neighbor in neighbors:
            neighbor_score = temp_d_sim_score[neighbor]
            difference = abs(node_score - neighbor_score)
            total_difference += difference
            total_neighbors += 1

    average_difference = total_difference / total_neighbors
    return average_difference


def network_stats_over_time(G, d_sim_to_avg):
      with open(os.path.join('PATH_TO_NEW_CSV'),'w') as temp_csv:
          writer=csv.writer(temp_csv, delimiter=',',lineterminator='\n')
          writer.writerow(['year', 'homophily', 'modularity', 'average distance from neighbors', 'stdev of word vectors', 'num_nodes', 'num_edges', 'density'])
          for year in reversed(range(2000, 2024)):
              #print(year)
              if len(temp_G.nodes()) <= 50:
                  print('STOPPED graph has less than 50 nodes')
                  break
  
              edges_to_remove = [(v1, v2) for v1, v2, data in temp_G.edges(data=True) if data['year'] > year]
              temp_G.remove_edges_from(edges_to_remove)
  
              temp_G = extract_largest_component(temp_G)
  
              current_nodes = set()
              to_remove = []
              for n1, n2 in temp_G.edges():
                  current_nodes.add(n1)
                  current_nodes.add(n2)
  
              for node in temp_d_sim_score:
                  if node not in current_nodes:
                      to_remove.append(node)
  
              for node in to_remove:
                  del temp_d_sim_score[node]
                  if node in temp_G.nodes():
                      temp_G.remove_node(node)
                      
              #GE = graph_general_euclidean_distance(temp_G, temp_d_sim_score)
              stdev = np.std(list(temp_d_sim_score.values()))
              average_distance = calculate_average_neighbor_difference(temp_G, temp_d_sim_score)
              homophily = graph_average_homophily(G, neighbor_threshold=.01)
              GE = 'NaN'
              modularity_score = modularity(temp_G)
              #print(year, GE, modularity_score)
              writer.writerow([year,	GE, homophily, modularity_score, average_distance, stdev, len(temp_G.nodes()), len(temp_G.edges()), len(temp_G.edges())/len(temp_G.nodes())])