from streamlit_extras.dataframe_explorer import dataframe_explorer
import streamlit as st
import pandas as pd
from streamlit_extras.colored_header import colored_header
from st_pages import add_page_title
import matplotlib.pyplot as plt
import networkx as nx
import textwrap

add_page_title(layout="wide")


colored_header(
    label="Network Visualization",
    description="",
    color_name="violet-70",
)

all_selaras = pd.read_csv('assets/all_selaras.csv')

# Create a graph and add edges based on the similarities between 'Perundangan1' and 'Perundangan2'
G = nx.Graph()

with st.expander("Visualisasi Seluruh Klaster"):
    for idx, row in all_selaras.iterrows():
        G.add_edge(row['Perundangan1'], row['Perundangan2'])

    # Find connected components (topics) in the graph
    topics = list(nx.connected_components(G))

    # Convert the topics to a dictionary with keys as 'Topic1', 'Topic2', etc.
    topics_dict = {f"Klaster{i+1}": list(topic) for i, topic in enumerate(topics)}

    # Visualize the graph
    pos = nx.spring_layout(G, seed = 55)
    plt.figure(figsize=(20, 12))
    num_colors = len(topics_dict)
    colormap = plt.cm.get_cmap('tab20', num_colors)
    for i, topic in enumerate(topics):
        color = colormap(i)
        nx.draw_networkx_nodes(G, pos, nodelist=topic, node_color=color, label=f"Klaster {i+1}", node_size=1500)
    nx.draw_networkx_edges(G, pos, alpha=0.5)

    label_pos = {node: (x, y) for node, (x, y) in pos.items()}
    nx.draw_networkx_labels(G, label_pos, font_size=5, font_color='black', font_weight='bold')

    legend = plt.legend(markerscale=0.3, fontsize=10)
    legend.set_title("Pengelompokan", prop={"size": 12})
    legend._legend_box.align = "left"
    plt.axis('off')
    plt.title("Perundang-undangan yang Memiliki Keselarasan")
    plt.show()
    st.pyplot(plt) 

cluster_selection = st.selectbox("Select a cluster:", list(range(1, 17)), index=0)

selected_nodes = topics[cluster_selection - 1]
G_topic = G.subgraph(selected_nodes)

plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G_topic, seed=42, k=1.5)

num_colors = len(selected_nodes)

colormap = plt.cm.get_cmap('Pastel2', num_colors)
color = colormap(cluster_selection - 1)
node_colors = [color] * len(G_topic.nodes())
nx.draw_networkx_nodes(G_topic, pos, node_color=node_colors, node_size=3000, label=f"Cluster {cluster_selection}")

nx.draw_networkx_edges(G_topic, pos, width=1.5, alpha=0.7)
label_pos = {node: (x, y) for node, (x, y) in pos.items()}
wrapped_labels = {node: '\n'.join(textwrap.wrap(node, width=20)) for node in G_topic.nodes()}
nx.draw_networkx_labels(G_topic, label_pos, labels=wrapped_labels, font_size=5, font_color='black', font_weight='bold')

plt.axis('off')
plt.title(f"Hubungan Keselarasan pada Klaster {cluster_selection}")

st.pyplot(plt)