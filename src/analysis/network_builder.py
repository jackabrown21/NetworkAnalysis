import os
from matplotlib import pyplot as plt
import pandas as pd
import networkx as nx
import matplotlib.cm as cm
import json


def main():
    # Specify your base directory
    input_base_dir = 'data/processed'

    full_G = nx.Graph()

    investments_dict = {}

    for company_name in os.listdir(input_base_dir):
        input_company_dir = os.path.join(input_base_dir, company_name)

        if not os.path.isdir(input_company_dir):
            continue

        for file_name in os.listdir(input_company_dir):
            if file_name.endswith('.csv'):
                file_path = os.path.join(input_company_dir, file_name)

                df = pd.read_csv(file_path)

                full_G.add_node(company_name)

                for index, row in df.iterrows():
                    invested_company = row['Name of Issuer'].lower()  
                    if invested_company not in full_G.nodes:  
                        full_G.add_node(invested_company)
                    full_G.add_edge(company_name, invested_company)
                    investments_dict[invested_company] = investments_dict.get(invested_company, [])
                    investments_dict[invested_company].append(company_name)

                break

    G = nx.Graph()

    for node in full_G.nodes:
        neighbors = list(full_G.neighbors(node))
        if len(neighbors) > 1 or node in os.listdir(input_base_dir):
            G.add_node(node)
            for neighbor in neighbors:
                G.add_edge(node, neighbor)

    colors = []
    # Put the number of investing companies
    max_investing_companies = 12 

    for node in G.nodes:
        if node in os.listdir(input_base_dir): 
            colors.append("green")  # Investing companies will have a fixed green color (or whatever color you want)
        else:
            investing_companies_connected = sum(neighbor in os.listdir(input_base_dir)
                                                for neighbor in G.neighbors(node))
            if investing_companies_connected == 1:
                colors.append("grey")
            else:
                normalized_value = 0.5 + (investing_companies_connected - 2) / (2 * (max_investing_companies - 2))
                colors.append(cm.Reds(normalized_value))  # Use the Reds colormap to color nodes (or whatever colormap you want)

    nx.draw(G, with_labels=True, node_color=colors, font_size=7)
    plt.show()

    nodes = [{'id': node, 'color': color} for node, color in zip(G.nodes(), colors)]
    links = [{'source': u, 'target': v} for u, v in G.edges()]

    # Create JSON data and write to file
    json_data = json.dumps({'nodes': nodes, 'links': links}, indent=4)
    with open('src/visualization/jsonnetworks/graph.json', 'w') as f:
        f.write(json_data)

if __name__ == "__main__":
    main()
