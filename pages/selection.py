from streamlit_extras.dataframe_explorer import dataframe_explorer
import streamlit as st
import pandas as pd
from streamlit_extras.colored_header import colored_header
from st_pages import add_page_title
from fuzzywuzzy import process
import networkx as nx
import matplotlib.pyplot as plt
import textwrap

add_page_title(layout="wide")

colored_header(
    label="Visualisasi Seleksi",
    description="",
    color_name="violet-70",
)

df = pd.read_csv('assets/inicsv.csv')
df['FileName'].head()

all_selaras = pd.read_csv('assets/all_selaras.csv')

# all_selaras = all_selaras.iloc[:, 1:3]
all_selaras.head()
st.dataframe(all_selaras, use_container_width=True)

# Search for the document based on df['FileName']
def get_suggestions(query, threshold=75, df=df, col='FileName'):
    suggestions = set()
    for value in df[col]:
        similarity = process.extractOne(query, [value])
        if similarity[1] >= threshold:
            suggestions.add(similarity[0])
    return suggestions

# Save the selected document from searching
def select_suggestions(change):
    global selected_data
    selected_data = [suggestion for suggestion, selected in zip(suggestions, checkbox_widgets) if selected.value]
    print(f"Selected data: {selected_data}")

# let user enter the query
# Display the selected document
query = ""
query = st.text_input("Cari Dokumen", query)
suggestions = get_suggestions(query)

selected_data = st.multiselect("Pilih Dokumen", list(suggestions), format_func=lambda x: x)

# checkbox_widgets = [st.checkbox(suggestion, key=suggestion) for suggestion in suggestions]

# st.write(f"Selected data: {selected_data}")
# Filter the rows
filtered_rows = all_selaras[all_selaras['Perundangan1'].isin(selected_data) | all_selaras['Perundangan2'].isin(selected_data)]
# filtered_rows

if filtered_rows.empty:
    pass
else:
    # print("Hasil:")
    st.write("Hasil:")
    for value in selected_data:
        if any(filtered_rows['Perundangan1'] == value) or any(filtered_rows['Perundangan2'] == value):
            # print(f'{value} memiliki keselarasan')
            st.write(f'{value} memiliki keselarasan')
        elif not any(filtered_rows['Perundangan1'] == value) and not any(filtered_rows['Perundangan2'] == value):
            # print(f'{value} tidak memiliki keselarasan')
            st.write(f'{value} tidak memiliki keselarasan')

    def make_graph(dataframe):
        # Create a graph and add edges based on the similarities between 'Perundangan1' and 'Perundangan2'
        G = nx.Graph()
        for idx, row in dataframe.iterrows():
            G.add_edge(row['Perundangan1'], row['Perundangan2'])

        # Find connected components (topics) in the graph
        topics = list(nx.connected_components(G))

        # Convert the topics to a dictionary with keys as 'Topic1', 'Topic2', etc.
        topics_dict = {f"Klaster{i + 1}": list(topic) for i, topic in enumerate(topics)}

        return G, topics, topics_dict

    G, topics, topics_dict = make_graph(filtered_rows)

    def plot_subgraph(G, topics, index, subplot_index, topics_dict):
        # Extract nodes for Topic
        topic = list(topics[index])

        # Create a subgraph containing only nodes from the topic
        G_topic = G.subgraph(topic)

        plt.subplot(4, 4, subplot_index)  # 3 rows and 4 columns, subplot_index specifies the position
        pos = nx.spring_layout(G_topic, seed=42, k=1.5)

        # Choose a colormap with x distinct colors and select the color for the topic
        num_colors = len(topics_dict)
        colormap = plt.cm.get_cmap('tab20', num_colors)
        color = colormap(index)
        nx.draw_networkx_nodes(G_topic, pos, node_color=color, node_size=3000, label=f"Topic {index}")

        nx.draw_networkx_edges(G_topic, pos, width=1.5, alpha=0.7)
        label_pos = {node: (x, y) for node, (x, y) in pos.items()}
        wrapped_labels = {node: '\n'.join(textwrap.wrap(node, width=20)) for node in G_topic.nodes()}
        nx.draw_networkx_labels(G_topic, label_pos, labels=wrapped_labels, font_size=7, font_color='black', font_weight='bold')
        plt.title(f"Hubungan Keselarasan pada Pilihan {index + 1}")

    # Topics list
    index = range(len(topics_dict))

    # Create subplots for each selected topic
    plt.figure(figsize=(25, 30))
    for k, i in enumerate(index):
        plot_subgraph(G, topics, k, k + 1, topics_dict)

    plt.tight_layout()
    plt.show()
    st.pyplot(plt)
