from urllib.request import urlopen
import json
import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st
import plotly.express as px
from plotly.graph_objs import Figure, Data
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from rdkit import Chem
from rdkit.Chem import Draw

import utils
import queries


st.set_page_config(layout="wide", page_title="Remedi4all Dashboard", page_icon=":pill:")

st.title(
    "REMEDi4ALL: Dashboard for R4A Experitse KG",
    anchor="center",
    help="This dashboard allows you to interact with the R4A KG and explore the data.",
)

# Connect to KG
graph = utils.connect_to_kg()
tx = graph.begin()


with st.expander("Don't know what REMEDi4ALL is?"):
    st.write(
        """The REMEDi4ALL consortium brings together a unique combination of expertise to address the complexities of drug repurposing. Under the leadership of EATRIS, the European infrastructure for translational medicine, 24 organisations in the fields of clinical and translational research, clinical operations, patient engagement and education, regulatory framework, funding, governance, Health Technology Assessment (HTA) and pricing and reimbursement will closely collaborate to make drug repurposing mainstream. Please check out our website for more information: https://remedi4all.org/"""
    )

tab1, tab2 = st.tabs(
    [
        "Project Information",
        "KG Drug Discovery ",
    ]
)

# Comparison between CVL fractions of positive control and other spectra
with tab1:
    st.write(
        """The [REMEDi4ALL consortium](https://remedi4all.org/) brings together a unique combination of expertise to address the complexities of drug repurposing. Under the leadership of EATRIS, the European infrastructure for translational medicine, 24 organisations in the fields of clinical and translational research, clinical operations, patient engagement and education, regulatory framework, funding, governance, Health Technology Assessment (HTA) and pricing and reimbursement will closely collaborate to make drug repurposing mainstream."""
    )

    st.header(
        "Project overview from the KG",
        divider="gray",
        help="This section allows you know more about the REMEDi4ALL project and see the basic information surrounding the project in the KG.",
    )

    st.subheader("Drug repurposing stakeholder around the globe")

    # Get map data
    with urlopen(
        "https://raw.githubusercontent.com/leakyMirror/map-of-europe/master/GeoJSON/europe.geojson"
    ) as response:
        counties = json.load(response)  # GeoJSON counties

    map_data = graph.run(queries.get_location()).to_data_frame()

    total_partners = map_data["Partner counts"].sum()
    total_countries = map_data.shape[0]

    st.markdown(
        f"The REMEDi4ALL project is a consortium of :red[{total_partners}] partners from :red[{total_countries}] countries."
    )

    # Geographic Map
    fig = px.choropleth_mapbox(
        map_data,
        geojson=counties,
        locations="Location",
        color="Partner counts",
        color_continuous_scale="Viridis",
        mapbox_style="open-street-map",
        zoom=3,
        center={"lat": 51.0057, "lon": 13.7274},
        opacity=0.5,
        labels={"Partner counts": "Institutions"},
        featureidkey="properties.ISO2",
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Individuals from each organization contributing towards the project")

    org_data = graph.run(queries.get_organization_info()).to_data_frame()
    org_data.sort_values(by="Individuals", ascending=False, inplace=True)
    total_people = org_data["Individuals"].sum()

    wp_data = graph.run(queries.get_wp_info()).to_data_frame()

    st.markdown(
        f"The project invovles :red[{total_people}] individuals working across countries to identify drug repositioning candidates for 4 indication areas, namely Pancreatic cancer, COVID-19, Osteogenesis imperfecta, and Multiple sulfatase deficiency. Collectively, they are working on :red[{len(wp_data)}] work packages (WP)."
    )

    col = st.columns((1.5, 1, 1.5), gap="medium")

    with col[0]:
        st.markdown(
            "<h3 style='text-align: center; color: #54c3c0;'>WP Overview</h1>",
            unsafe_allow_html=True,
        )
        fig = px.pie(
            wp_data, values="Individuals", names="WP", hover_name="WP", hole=0.3
        )
        fig.update_layout(
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col[1]:
        st.markdown(
            "<h3 style='text-align: center; color: #54c3c0;'>WP Information</h1>",
            unsafe_allow_html=True,
        )
        selected_wp = st.selectbox("Select WP", wp_data["id"], index=0)
        selected_wp_data = wp_data[wp_data["id"] == selected_wp]
        selected_wp_name = selected_wp_data["WP"].values[0]
        selected_wp_lead = selected_wp_data["lead"].values[0]
        selected_wp_individuals = selected_wp_data["Individuals"].values[0]

        container = st.container(border=True)
        container.write(
            f""":red[{selected_wp}] coordinated the activities related to :red[{selected_wp_name}].
            It is lead by :red[{selected_wp_lead}] and has :red[{selected_wp_individuals}] individuals working on it."""
        )

    with col[2]:
        st.markdown(
            "<h3 style='text-align: center; color: #54c3c0;'>Top 10 organizations</h1>",
            unsafe_allow_html=True,
        )
        org_data = org_data.head(10)
        fig = px.pie(
            org_data,
            values="Individuals",
            names="Partner",
            hover_name="Partner",
            hole=0.3,
        )
        fig.update_layout(
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Want to know more about our vision?"):
        st.write(
            "You can read more about the project vision in our [factsheet](https://remedi4all.org/wp-content/uploads/2023/05/REMEDi4ALL-Factsheet.pdf)"
        )

    st.header(
        "Understanding the REMEDi4ALL KG",
        divider="gray",
        help="This section allows you know more about a KG and its utility in the project.",
    )

    kg_node_count = graph.run(queries.get_node_counts()).to_data_frame().values[0][0]
    kg_edge_count = graph.run(queries.get_edge_counts()).to_data_frame().values[0][0]
    node_stats = graph.run(queries.get_node_stats()).to_data_frame()

    col = st.columns((1.5, 1.5), gap="medium")

    with col[0]:
        st.subheader("What is a Knowledge Graph (KG)?")
        st.write(
            """A knowledge graph is a database that uses a graph-structured data model to integrate data from various sources. It is designed to provide a representation of the knowledge domain and is used by a variety of applications for data integration, data sharing and querying. By linking data in KG form, analysts and users can better understand the underlying data and thus answer questions to complex questions in a systematic fashion. The REMEDi4ALL KG is a collection of expertise data from various organizations allowing for a better understanding stakeholders in the project and their contribution to drug repurposing efforts."""
        )

        st.write(
            """In KG terminology, each individual real-world entity (for e.g., Compound name, protein targets, individuals, etc.) is called a :red[node] and a node can be connected to other nodes with help of :red[edges]. To read more about KGs, check out the blogs from [Stanford AI](https://ai.stanford.edu/blog/introduction-to-knowledge-graphs/), [Ontotext](https://www.ontotext.com/knowledgehub/fundamentals/what-is-a-knowledge-graph/), and the [Alan Turing Institute](https://www.turing.ac.uk/research/interest-groups/knowledge-graphs)
            """
        )

        st.write(
            f"""In the REMEDi4ALL KG, one can find :red[{kg_node_count}] nodes and :red[{kg_edge_count}] edges connecting these nodes. These nodes cover :red[{node_stats.shape[0]}] different types of entities. The section below provides insights into this.
            """
        )

    with col[1]:
        st.image(
            "./data/kg_intro.png",
            use_column_width=True,
            caption="KG applications. Figure taken from Ontotext.",
            output_format="PNG",
        )

    fig = px.bar(
        node_stats,
        x="Nodes",
        y="Counts",
        labels={"Nodes": "Entity", "Counts": "Count"},
        color_discrete_sequence=["#54c3c0"],
        text_auto=True,
        hover_name="Nodes",
    )
    fig.update_layout(title="Node distribution in the KG", title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

    col = st.columns((1.5, 1.5), gap="medium")
    with col[0]:
        st.image(
            "./data/schema.png",
            use_column_width=True,
            caption="Schema of the Expertise KG.",
            output_format="PNG",
        )

    with col[1]:
        st.subheader("What can you do with the KG?")
        st.markdown(""":blue[One can ask **organizational** questions like:]""")
        st.markdown("- What are the top 10 organizations contributing to the project?")
        st.markdown("- How many individuals are working on each work package?")
        st.markdown("- What is the distribution of organization across countries?")

        st.write(
            """:blue[One can also ask question for surrounding the **drug respurposing research community** with questions like:]"""
        )
        st.markdown(
            "- What expertise does a given organization have in the context of drug repurposing?"
        )
        st.markdown("- Whom to contact for a specific expertise?")
        st.markdown(
            "- Which target classes are being researched on by an organization?"
        )
        st.markdown("- How big is the research community in an organization?")

        st.write(
            """**We are constantly updating the KG with new data. In the future versions, users would be able ask drug discovery based question in the context of COVID-19.**"""
        )
        # st.markdown("- What are the top 10 compounds being researched on?")
        # st.markdown("- What are the top 10 targets being researched on?")
        # st.markdown("- What are the top 10 indications being researched on?")
        # st.markdown("- What are the top 10 drug classes being researched on?")


with tab2:
    st.write(
        """
        Drug discovery involves the discovery and design of drugs or potential drug compounds. This includes methods that search compound collections, generate or analyse drug 3D conformations, identify drug targets with structural docking etc. Moreover, this encompass our preclinical, regulatory, clinical and other drug discovery aspects that are part of REMEDi4ALL.
        
        💡 In this section we look into potential stakeholder's in the project that can assist you in drug discovery domain."""
    )

    st.header(
        "Drug discovery and development",
        divider="gray",
        help="This section allows you know explore the drug discovery and development expertise across the project found in the KG.",
    )
