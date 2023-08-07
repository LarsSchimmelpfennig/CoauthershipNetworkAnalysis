import os, csv
import pandas as pd
from gensim.models import Word2Vec
import numpy as np
from gensim import utils
import networkx as nx

model = Word2Vec.load("PATH_TO_MODEL"))

def cosine_similarity(vector1, vector2):
	return float(np.dot(vector1, vector2)/(np.linalg.norm(vector1)* np.linalg.norm(vector2)))

def sum_word_vectors(words):
    sub_words = utils.simple_preprocess(words)
    curr_topic_vector = 0
    for sub_word in sub_words:
        if sub_word in model.wv:
            curr_topic_vector += model.wv[sub_word]
        else:
            pass
    return curr_topic_vector 
	
def extract_largest_component(G):
	connected_components = list(nx.connected_components(G))
	largest_component = max(connected_components, key=len)
	
	edges_to_exclude = set()
	nodes_to_exclude = set()
	for edge in G.edges():
		u, v = edge
		if u not in largest_component or v not in largest_component:
			nodes_to_exclude.add(u)
			nodes_to_exclude.add(v)
			edges_to_exclude.add(edge)
	
	G.remove_edges_from(edges_to_exclude)
	G.remove_nodes_from(nodes_to_exclude)
	return G


def generate_network(topic):
    files = os.listdir('PATH_TO_FILES')
    d_author_vectors = {}
    G = nx.Graph()
    d_edge_years = {}

    for file in files:
        if f'{topic}_WOS_' not in file:
            continue
        print(file)
        df = pd.read_csv(file)
        df = df.sort_values(by='Publication Year', ascending=True)
        for authors, keywords, keywords_plus, title, abstract, year in zip(df['Authors'], df['Author Keywords'], df['Keywords Plus'], df['Article Title'], df['Abstract'], df['Publication Year']):
            word_vector = 0
            combined_keywords = ''
            for sub_keywords in [keywords, keywords_plus]:
                if type(sub_keywords) != float:
                    combined_keywords += sub_keywords + '; '
            if combined_keywords != '':
                word_vector += sum_word_vectors(combined_keywords)

            word_vector += sum_word_vectors(title)
            authors_names = []
            if type(authors) == float:
                continue
            for author in authors.split('; '):
                if author == '[Anonymous]' or ',' not in author or len(author.split(', ')) != 2:
                    continue
                last, first = author.split(', ')
                first = first[0]
                author_name = last+', '+first
                authors_names.append(author_name)
                
                if author_name not in d_author_vectors:
                    d_author_vectors[author_name] = word_vector
                else:
                    d_author_vectors[author_name] += word_vector

            if len(authors_names) > 1:
                for i in range(len(authors_names)):
                    for j in range(i + 1, len(authors_names)):
                        a1 = authors_names[i]
                        a2 = authors_names[j]

                        if ((a1, a2) in d_edge_years and d_edge_years[(a1, a2)] > year):
                            G.remove_edge(a1, a2)
                            G.add_edge(a1, a2, year=year)
                            d_edge_years[(a1, a2)] = int(year)
                            d_edge_years[(a2, a1)] = int(year)

                        if (a1 != a2 and (a1, a2) not in d_edge_years and (a2, a1) not in d_edge_years and (a1, a2) not in G.edges()):
                            G.add_edge(a1, a2, year=year)
                            d_edge_years[(a1, a2)] = int(year)
                            d_edge_years[(a2, a1)] = int(year)
                                      
    avg_author_vector = 0
    for vector in d_author_vectors.values():
        avg_author_vector += vector

    d_sim_to_avg = {}
    vals = []
    for author in d_author_vectors:
        sim_to_avg = cosine_similarity(d_author_vectors[author], avg_author_vector)
        d_sim_to_avg[author] = sim_to_avg
            
    nx.set_edge_attributes(G, d_edge_years, 'year')
    nx.set_node_attributes(G, d_sim_to_avg, 'value')
    G = extract_largest_component(G)

    to_remove = []
    for node in d_sim_to_avg:
        if node not in G.nodes():
            to_remove.append(node)

    for node in to_remove:
        del d_sim_to_avg[node]

    return G, d_sim_to_avg
            
