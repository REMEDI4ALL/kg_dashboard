import os
from urllib.request import urlopen
import json
import pandas as pd

import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
from wordcloud import WordCloud


st.set_page_config(layout="wide", page_title="REMEDi4ALL Dashboard", page_icon=":pill:")

st.title(
    "Dashboard of REMEDi4ALL Expertise",
    anchor="center",
    help="This dashboard allows you to interact with the R4A KG and explore the data.",
)

with st.expander("Don't know what REMEDi4ALL is?"):
    st.write(
        """The REMEDi4ALL consortium brings together a unique combination of \
        expertise to address the complexities of drug repurposing. Under the \
        leadership of EATRIS, the European infrastructure for translational \
        medicine, 24 organisations in the fields of clinical and translational \
        research, clinical operations, patient engagement and education, \
        regulatory framework, funding, governance, Health Technology Assessment (HTA) \
        and pricing and reimbursement will closely collaborate to make drug repurposing \
        mainstream. Please check out our website for more information: https://remedi4all.org/"""
    )

st.markdown(
    """
        <style>
            .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {font-size:1rem;}
            .stExpander [data-testid="stMarkdownContainer"] p {font-size: 18px;}
        </style>
    """,
    unsafe_allow_html=True,
)  # .block-conatiner controls the padding of the page, .stTabs controls the font size of the text in the tabs


tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Project Information",
        "Drug Discovery Expertise",
        "Clinical Trials Expertise",
        "Standard Operating Expertise",
    ]
)

# Main content on R4A project
with tab1:
    st.write(
        "The vast majority of the over 7000 known diseases are without effective treatments—there is thus an urgent need to make better use of the medicines that we already have in hand. These include medicines that have already been approved for human use, as well as experimental medicines still in clinical trials already showing good pharmaceutical properties and human safety. In fact, most approved drugs intrinsically have the potential to treat many more diseases than they were originally approved for, even diseases seemingly unrelated to those for which they are currently being prescribed. \n"
    )

    st.write(
        "[REMEDi4ALL](https://remedi4all.org/) is an EU-funded initiative (HORIZON EUROPE) whose key mission is to make it easier and more reliable to find new medical uses for drugs we already know are safe and effective. We also aim to show that in many cases such “repurposed” medicines can be taken all the way into clinic faster and at the fraction of the cost of developing a completely new drug from scratch. \n"
    )

    st.write(
        "But with hundreds or even thousands of opportunities to repurpose approved and experimental medicines—for the thousands of diseases that remain without any approved treatments at all—REMEDi4ALL must also help to transform the very landscape of drug repurposing. This needs to encompass not only the scientific, clinical research and patient communities, but regulatory, policy and commercial drug and investment sectors as well, so that all researchers will face fewer barriers and be able to bring much needed treatments to patients faster and more effectively—to “float all boats” in the drug repurposing ecosystem. \n"
    )

    st.header(
        "REMEDi4ALL structure and partners",
        divider="gray",
        help="This section allows you know more about the REMEDi4ALL project and see the basic information surrounding the project in the KG.",
    )

    # Get map data
    with urlopen(
        "https://raw.githubusercontent.com/leakyMirror/map-of-europe/master/GeoJSON/europe.geojson"
    ) as response:
        counties = json.load(response)  # GeoJSON counties

    map_data = pd.read_csv("data/location.csv")
    total_partners = map_data["Partner counts"].sum()
    total_countries = map_data.shape[0]

    org_data = pd.read_csv("data/organization.csv")
    org_data.sort_values(by="Individuals", ascending=False, inplace=True)
    total_people = org_data["Individuals"].sum()

    st.markdown(
        f"REMEDi4ALL project is composed of :red[{total_people}] individuals from :red[{total_partners}] partner organisations working across :red[{total_countries}] countries that bring together a unique combination of expertise to address the complexities of drug repurposing with a patient-centric approach. At our core is a patient-centric drug repurposing platform designed to encompass the complete value chain supporting high impact projects initiating at any phase of development through to market entry and patient access."
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

    # st.subheader("Individuals from each organization contributing towards the project")

    wp_data = pd.read_csv("data/wp.csv")

    st.write(
        "REMEDi4ALL was designed with four imbedded drug repurposing projects at various stages of discovery and development to serve as “Demonstrator” projects with which our core platform could be put into practice from the start. In turn, experiences and lessons learned from designing and implementing project plans for these four Demonstrator have already been key in helping to validate, identify gaps and improve the structure of and resources/expertise contained in our core platform. These projects four Demonstrator focus on different indications, namely metastatic pancreatic cancer (mPDAC), pandemic preparedness, osteogenesis imperfecta (OI), and multiple sulfatase deficiency (MSD). The demonstrator portfolio covers different phases of the development path and represents the diverse nature of repurposing projects we are likely to work on in the future. \n"
    )

    st.write(
        "In the coming year, REMEDi4ALL will begin processes to expand its project portfolio by bringing on additional “User” projects to be supported by our core drug repurposing platform. \n"
    )

    st.markdown(
        f"""The work distribution among REMEDi4ALL partner institutions is delineated through the allocation of work packages, each representing a distinct set of tasks or objectives. There are :red[{len(wp_data)}] work packages in REMEDi4ALL, which serve as the building blocks of collaboration between partners."""
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
        selected_wp_organizations = selected_wp_data["Organizations"].values[0]

        container = st.container(border=True)
        container.write(
            f""":blue[{selected_wp_name}] (:red[{selected_wp}]) is led by :red[{selected_wp_lead}] and has :red[{selected_wp_organizations}] contributing partners and a total of :red[{selected_wp_individuals}] individuals working on it."""
        )

        if selected_wp == "WP1":
            container.write(
                """WP1 spearheads the "Patients-users co-creation" approach, ensuring patient engagement and partnership from project inception to medicine delivery. It drives the creation of the drug repurposing platform across all stages, from discovery to market access. WP1 is integral to Demonstrator and future User projects, collaborating with Research Development Teams and forming Patient Advocacy Groups. Initial efforts focus on engaging the patient community and implementing co-creation processes, with lessons learned informing the framework for future projects."""
            )

        elif selected_wp == "WP2":
            container.write(
                """WP2 focuses on developing and optimising development of a robust, operational model for the REMEDi4ALL drug repurposing platform. This operational model is being implemented for ongoing Demonstrator Projects and will also be used to support and manage future User Projects. In parallel, WP2 runs the REMEDi4ALL concierge , a portal that facilitates proactive engagement between REMEDi4ALL and a wide array of stakeholders, encompassing researchers, patients, clinicians, funders, investors, and companies involved in translational efforts across Europe, the UK, and beyond"""
            )

        elif selected_wp == "WP3":
            container.write(
                """WP3 focuses on training and education to strengthen the overall capacity within the drug repurposing ecosystem. REMEDi4ALL is dedicated to tackling the inherent challenges of drug repurposing by fostering collaboration among patients, researchers, and developers to refine therapeutic hypotheses and guide candidates through robust preclinical and clinical plans. Thus, an essential component of REMEDi4ALL's mission involves sharing insights and best practices with diverse stakeholders, including patients, researchers, funders, industry partners, and regulatory bodies."""
            )

        elif selected_wp == "WP4":
            container.write(
                """WP4 focuses on the initial phases of drug repurposing projects, with subsequent WPs addressing in vitro approaches and preclinical studies (WP5 and 6, respectively). WP4 is currently dedicated to organizing and assessing a diverse array of in silico resources. These resources support the development of therapeutic hypotheses and the establishment of critical paths for preclinical and clinical development, guided by Target Product Profiles (TPPs) specific to each repurposing project."""
            )

        elif selected_wp == "WP5":
            container.write(
                """WP5 focuses on in vitro biology discovery and screening and is the second of three WPs (WP4, 5, and 6) within REMEDi4ALL dedicated to the discovery and preclinical aspects of drug repurposing projects."""
            )

        elif selected_wp == "WP6":
            container.write(
                """WP6 is the final of the three WPs in REMEDi4ALL dedicated to preclinical discovery and development (WP4, 5, and 6). WP6 focuses on inventorying, systematizing, and applying preclinical resources and expertise across the platform."""
            )

        elif selected_wp == "WP7":
            container.write(
                """WP7 focuses on supporting the implementations of multinational trials, which are key in rare disease contexts."""
            )

        elif selected_wp == "WP8":
            container.write(
                """WP8 aims to improve the European policy environment for drug repurposing."""
            )

        elif selected_wp == "WP9":
            container.write(
                """WP9 aims to transform the drug repurposing ecosystem by actively engaging funders throughout the project lifecycle. By acquiring a deeper understanding of funders' perspectives and building a network encompassing public and private, non-profit, and commercial sectors, WP9 seeks to develop strategies to address market failures and improve conditions for successful drug repurposing."""
            )

        elif selected_wp == "WP10":
            container.write(
                """WP10 focuses on guiding and managing the four Demonstrator projects. These projects serve not only to address scientific and clinical needs but also to inform, optimize, and validate the operational framework of the platform. This hands-on approach fosters collaboration, trust-building, and skill development, positioning REMEDi4ALL to onboard new User projects, thus expanding its impact and sustainability."""
            )

        elif selected_wp == "WP11":
            container.write(
                """WP11 plays a pivotal role in ensuring the meaningful impact of REMEDi4ALL through effective communication, dissemination, and exploitation strategies aligned with project objectives."""
            )

        elif selected_wp == "WP12":
            container.write(
                """WP12 focuses on mapping the drug repurposing landscape, establishing connections with key stakeholders, and engaging with international consortia and repurposing initiatives. This grants significant presence of REMEDi4ALL at both global and EU levels, facilitates alignment of international agendas, and prevents fragmentation within the field."""
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
        "The REMEDi4ALL Knowledge Graph (KG)",
        divider="gray",
        help="This section allows you know more about a KG and its utility in the project.",
    )

    kg_node_count = pd.read_csv("data/nodes.csv").values[0][0]
    kg_edge_count = pd.read_csv("data/edges.csv").values[0][0]
    node_stats = pd.read_csv("data/node_stats.csv")

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
            use_container_width=True,
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
            use_container_width=True,
            caption="Schema of the Expertise KG.",
            output_format="PNG",
        )

    with col[1]:
        st.subheader("What can you do with the KG?")
        st.markdown(""":blue[One can ask **organisational** questions like:]""")
        st.markdown("- What are the top 10 organisations contributing to the project?")
        st.markdown("- How many individuals are working on each work package?")
        st.markdown("- What is the distribution of organisation across countries?")

        st.write(
            """:blue[One can also ask question for surrounding the **drug respurposing research community** with questions like:]"""
        )
        st.markdown(
            "- What expertise does a given organisation have in the context of drug repurposing?"
        )
        st.markdown("- Whom to contact for a specific expertise?")
        st.markdown(
            "- Which target classes are being researched on by an organisation?"
        )
        st.markdown("- How big is the research community in an organisation?")

        st.write(
            """**We are constantly updating the KG with new data. In the future versions, users would be able ask drug discovery based question in the context of COVID-19.**"""
        )


with tab2:
    st.write(
        """
        :blue-background[Drug discovery] involves the discovery and design of promising drug \
        candidates. This includes methods that search compound collections, \
        generate or analyse drug 3D conformations, identify drug targets with \
        structural docking etc.
        
        💡 In this section we look into potential stakeholder's in the project \
        that can assist you in drug discovery domain."""
    )

    st.header(
        "Skills relevant for drug discovery and development",
        divider="gray",
        help="This section allows you know explore the drug discovery and development expertise across the project found in the KG.",
    )

    col = st.columns((1.5, 1.5), gap="medium")
    with col[0]:
        skill_groups = pd.read_csv("data/skillgroups.csv")["SkillGroup"].values
        selected_skill = st.selectbox(
            "Select a skill group you would like to explore.", skill_groups, index=0
        )

        skill_distribution_percentage = pd.read_csv("data/skills.csv")
        m = skill_distribution_percentage["name"] == selected_skill
        skill_distribution_percentage = skill_distribution_percentage[m]
        fig = px.pie(
            skill_distribution_percentage,
            values="Individuals",
            names="skill_name",
            hover_name="skill_name",
            hole=0.5,
        )
        fig.update_layout(
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col[1]:
        skill_metadata = pd.read_csv("data/skills_metadata.csv")
        skill_metadata_subset = skill_metadata[
            skill_metadata["SkillGroup"] == selected_skill
        ]
        all_skills = skill_metadata_subset["Skill"].values

        selected_metadata = st.selectbox(
            "Select a skill to see description.", all_skills, index=0
        )

        skill_metadata_subset = skill_metadata_subset[
            skill_metadata_subset["Skill"] == selected_metadata
        ]
        curie = skill_metadata_subset["Curie"].values[0]
        description = skill_metadata_subset["description"].values[0]
        url = skill_metadata_subset["url"].values[0]

        st.write(f"**{selected_metadata}**")
        st.write(f"**Curie**: {curie}")
        st.write(f"**Description**: {description}")
        st.write(f"**More information**: {url}")

    st.header(
        "Stakeholders for drug development and discovery centric skill",
        divider="gray",
        help="This section allows you to identify stakeholders with the domain expertise.",
    )

    selected_metadata = st.selectbox(
        "Select a skill to see stakeholders.", skill_metadata["Skill"], index=0
    )

    col = st.columns((1.5, 1.5), gap="medium")
    with col[0]:
        people_with_skill = pd.read_csv("data/skills_info.csv")
        people_with_skill_filtered = people_with_skill[
            people_with_skill["Skill"] == selected_metadata
        ]
        people_with_skill_filtered = people_with_skill_filtered[
            ["Individual", "ORCID", "Affiliation"]
        ]
        st.write(
            f"Found :red[{people_with_skill_filtered.shape[0]}] individuals with this skill."
        )

        st.data_editor(
            people_with_skill_filtered,
            column_config={
                "ORCID": st.column_config.LinkColumn(
                    "Research profile",
                    help="The ORCID of the individual.",
                    validate=r"^https://orcid\.org/\d{4}-\d{4}-\d{4}-\d{3}[X0-9]$",
                    max_chars=100,
                    display_text=r"https://(.*?)\.streamlit\.app",
                ),
            },
            disabled=True,
            hide_index=True,
        )

    with col[1]:
        st.write("Visualizing the distribution of skills across individuals.")
        if people_with_skill_filtered.shape[0] > 0:
            people_in_filtered = people_with_skill_filtered["Individual"].unique()

            data_list = []
            for individual in people_in_filtered:
                tmp = people_with_skill[people_with_skill["Individual"] == individual]
                for skill in skill_groups:
                    skill_list = tmp[tmp["Group"] == skill]
                    if skill == "Communication and Project Management Group":
                        skill_name = "Communication"
                    elif skill == "Drug Development Group":
                        skill_name = "Drug Development"
                    elif skill == "Drug Discovery Group":
                        skill_name = "Drug Discovery"
                    else:
                        raise ValueError(f"Unknown skill group - {skill}")

                    data_list.append(
                        {
                            "individual": individual,
                            "skill": skill_name,
                            "count": skill_list.shape[0],
                        }
                    )

            data_df = pd.DataFrame(data_list)
            new_df = data_df.pivot(index="individual", columns="skill")["count"].fillna(
                0
            )

            fig = px.imshow(
                new_df,
                x=new_df.columns,
                y=new_df.index,
                color_continuous_scale="blues",
                text_auto=True,
                aspect="auto",
            )
            fig.update_layout(
                xaxis_title="Skills",
                yaxis_title="Individuals",
                margin=dict(l=20, r=20, t=20, b=20),
            )
            fig.update(
                data=[
                    {
                        "hovertemplate": "Individual: %{y}<br>Group: %{x}<br># Skills: %{z}"
                    }
                ],
            )
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No data to visualize.")

    st.header(
        "Technology stakeholders in drug repurposing",
        divider="gray",
        help="This section allows you to identify organization and individual stakeholders with the technological expertise in software, assay and target classes among others.",
    )

    with st.expander("Experimental stakeholders in drug repurposing"):
        all_assays = pd.read_csv("data/assays.csv")

        selected_assay = st.selectbox(
            "Select an assay to see stakeholders.", all_assays["Assay"], index=0
        )

        assay_data = pd.read_csv("data/assay_data.csv")
        assay_data = assay_data[assay_data["Name"] == selected_assay]
        assay_data = (
            assay_data.groupby("Partner")["info"]
            .count()
            .reset_index()
            .assign(Percentage=lambda x: round((x["info"] / x["info"].sum()) * 100, 2))
        )

        col = st.columns((1.5, 1.5), gap="medium")

        with col[0]:
            fig = px.pie(
                assay_data,
                values="Percentage",
                names="Partner",
                hover_name="Partner",
            )
            fig.update_layout(
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=20),
            )
            st.plotly_chart(fig, use_container_width=True)

        with col[1]:
            assay_metatadata = all_assays[all_assays["Assay"] == selected_assay]
            assay_curie = assay_metatadata["Curie"].values[0]
            assay_description = assay_metatadata["Definition"].values[0]

            st.write(f"**{selected_assay}**")
            st.write(f"**Curie**: {assay_curie}")
            st.write(f"**Description**: {assay_description}")
            st.write(
                f"Found :red[{assay_data.shape[0]}] organizations with expertise in :red[{selected_assay}]."
            )

    with st.expander(
        "In-silico tools and target class stakeholders in drug repurposing"
    ):
        col = st.columns((1.5, 1.5), gap="medium")

        with col[0]:
            all_software = pd.read_csv("data/software.csv")

            selected_software = st.selectbox(
                "Select a software/tool to see stakeholders.",
                all_software["Software"],
                index=0,
            )

            software_data = pd.read_csv("data/software_data.csv")
            software_data = software_data[software_data["Name"] == selected_software]
            software_data = (
                software_data.groupby("Partner")["info"]
                .count()
                .reset_index()
                .assign(
                    Percentage=lambda x: round((x["info"] / x["info"].sum()) * 100, 2)
                )
            )

            software_metatadata = all_software[
                all_software["Software"] == selected_software
            ]
            software_curie = software_metatadata["Curie"].values[0]

            st.write(
                f"Found :red[{software_data.shape[0]}] organizations with expertise in :red[{selected_software} ({software_curie})]"
            )

            fig = px.pie(
                software_data,
                values="Percentage",
                names="Partner",
                hover_name="Partner",
            )
            fig.update_layout(
                showlegend=False, margin=dict(l=20, r=20, t=20, b=20), autosize=False
            )
            st.plotly_chart(fig, use_container_width=True)

        with col[1]:
            all_target_classes = pd.read_csv("data/target_class.csv")

            selected_target_class = st.selectbox(
                "Select a target class to see stakeholders.",
                all_target_classes["Target"],
                index=0,
            )

            # TODO: Fix this part
            target_data = pd.read_csv("data/target_data.csv")
            target_data = target_data[target_data["Name"] == selected_target_class]
            target_data = (
                target_data.groupby("Partner")["info"]
                .count()
                .reset_index()
                .assign(
                    Percentage=lambda x: round((x["info"] / x["info"].sum()) * 100, 2)
                )
            )

            target_metatadata = all_target_classes[
                all_target_classes["Target"] == selected_target_class
            ]
            target_curie = target_metatadata["Curie"].values[0]

            st.write(
                f"Found :red[{target_data.shape[0]}] organizations with expertise in :red[{selected_target_class} ({target_curie})]"
            )

            fig = px.pie(
                target_data,
                values="Percentage",
                names="Partner",
                hover_name="Partner",
            )
            fig.update_layout(
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=20),
            )
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Organization and their expertise in drug repurposing")

    col = st.columns((1.5, 1.5), gap="medium")

    with col[0]:
        partners = pd.read_csv("data/partner_info.csv")
        selected_partner = st.selectbox(
            "Select a organization to see their expertise.", partners["Name"], index=0
        )

        partner_data = partners[partners["Name"] == selected_partner]
        all_indivudals = pd.read_csv("data/person_info.csv")
        indivudals_in_selected_partner = all_indivudals[
            all_indivudals["Partner"] == selected_partner
        ]
        if selected_partner == partner_data["acronym"].values[0]:
            st.write(
                f":red[**{selected_partner}**] has :red[{indivudals_in_selected_partner.shape[0]}] individuals working with them."
            )
        else:
            st.write(
                f":red[**{selected_partner}**], also known as :red[{partner_data['acronym'].values[0]}], has :red[{indivudals_in_selected_partner.shape[0]}] individuals working with them."
            )

        st.write(f"Find more about them [here]({partner_data['info_link'].values[0]})")
    with col[1]:
        all_partner_connections = pd.read_csv("data/partner_data.csv")

        all_partner_connections = all_partner_connections[
            all_partner_connections["Partner"] == selected_partner
        ]
        if all_partner_connections.shape[0] > 0:
            wordcloud = WordCloud(
                background_color="white", width=512, height=384
            ).generate(" ".join(all_partner_connections.Name))
            st.image(wordcloud.to_image(), use_container_width=True)
        else:
            st.write("No information found in KG.")


with tab3:
    st.write(
        """
        :blue-background[Clinical Trials] involves research study that \
        prospectively assigns human participants or groups of humans to one \
        or more health-related interventions to evaluate the effects on \
        health outcomes.

        💡 In this section we look into potential stakeholder's in the project \
        that can assist to managing various aspects of a clinical trial."""
    )

    st.header(
        "Skills relevant for clinical trials management",
        divider="gray",
        help="This section allows you know explore the clinical trial related expertise across the project.",
    )

    clincal_skills = pd.read_csv("data/clinical_expertise_info.tsv", sep="\t")

    selected_clin_skill = st.selectbox(
        "Select a clinical skill group you would like to explore.",
        clincal_skills,
        index=0,
    )

    # Add description
    tmp = clincal_skills[clincal_skills["Services"] == selected_clin_skill]

    st.write(f"**Description**: {tmp['Definition'].values[0]}\n")
    if pd.notna(tmp["Source link"].values[0]):
        st.markdown(
            f"**Source**: [{tmp['Source'].values[0]}]({tmp['Source link'].values[0]})\n"
        )
    else:
        st.markdown(f"**Source**: {tmp['Source'].values[0]}\n")

    # Display the stakeholders
    clincal_stakeholders = pd.read_csv(
        "data/clinical_expertise.tsv", sep="\t", index_col=0
    )
    clincal_stakeholders.fillna(0, inplace=True)
    clincal_stakeholders.replace("Available", 0.2, inplace=True)

    for col in clincal_stakeholders.columns:
        original_val = clincal_stakeholders.loc[selected_clin_skill, col]
        if original_val > 0:
            clincal_stakeholders.loc[selected_clin_skill, col] = 1

    fig = px.imshow(
        clincal_stakeholders,
        aspect="auto",
        width=800,
        height=1000,
        color_continuous_scale="PuBu",
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis=dict(tickfont=dict(size=18)),
        xaxis=dict(tickfont=dict(size=18)),
    )
    fig.update(
        data=[
            {
                "hovertemplate": "Skill: %{y}<br>Organization: %{x}<br> Availability: %{z}"
            }
        ],
    )
    st.plotly_chart(fig, use_container_width=True)


with tab4:
    so_data = pd.read_csv("data/standard_operations.tsv", sep="\t")
    so_sub = so_data[~so_data["ID"].str.contains("SOC", na=False)]
    so_display = so_sub[
        ["ID", "Category", "Title", "Type", "DOI", "Creator", "Reviewer"]
    ]

    all_socs = sorted(list(set(so_data["Category"].dropna())))
    all_keywords = sorted(
        list(
            set(
                kw.strip()
                for kws in so_data["Keywords"].dropna()
                for kw in kws.split(",")
            )
        )
    )
    all_creators = sorted(
        list(
            set(
                creator.strip()
                for creators in so_data["Creator"].dropna()
                for creator in creators.split(",")
            )
        )
    )
    all_reviewers = sorted(
        list(
            set(
                reviewer.strip()
                for reviewers in so_data["Reviewer"].dropna()
                for reviewer in reviewers.split(",")
            )
        )
    )
    all_types = [
        "Standard Operating Guideline (SOG)",
        "Standard Operating Protocol (SOP)",
        "SOG+SOP",
    ]
    all_names = list(set(all_creators + all_reviewers))

    st.write(
        """
        A :blue-background[Standard Operating procedure] is a set of instructions to help project members to carry out routine operation in a standardized way. Here we distinguish between :blue-background[Standard Operating Protocol (SOPs)] for detailed step-by-step manuals and :blue-background[Standard Operating Guidelines (SOGs)] for more general principles. 
        
        Our SOGs and SOPs are assigned to 4 distinct categories (:blue-background[Standard Operating Categories, SOCs]) whether they instruct on: (a) computational analysis, (b) data management and quality, (c) hit identification and validation or (d)d other procedures. On this page you can find and search all our published procedures and 
        find expertise on a SOG/SOP of interest"""
    )

    st.header(
        "Standard Operating Categories",
        divider="gray",
        help="This section allows you to explore the different categories standard operating protocols and guidelines are grouped in.",
    )

    col = st.columns((1, 1), gap="medium")

    with col[0]:
        st.markdown(
            """
            <div style="text-align: center; font-weight: bold;">
                Distribution of Standard Operating Protocols/Guidelines across Categories
            </div>
            """,
            unsafe_allow_html=True,
        )
        soc_stats = so_data["Category"].value_counts().reset_index()
        soc_stats["Count"] = soc_stats["count"] - 1

        fig = px.bar(
            soc_stats,
            x="Category",
            y="Count",
            color_discrete_sequence=["#54c3c0"],
            text_auto=True,
            hover_name="Category",
        )
        fig.update_traces(
            hovertemplate="Category: %{x}<br>Count: %{y}",
        )
        st.plotly_chart(fig, use_container_width=True)

        selected_soc = st.selectbox(
            "Select a standard operating category to see description.",
            all_socs,
            index=0,
        )
        id = so_data[
            (so_data["Category"] == selected_soc)
            & (so_data["ID"].str.contains("SOC", na=False))
        ]["ID"].iloc[0]
        description = so_data[
            (so_data["Category"] == selected_soc)
            & (so_data["ID"].str.contains("SOC", na=False))
        ]["Description"].iloc[0]

        st.write(f"**Category name**: {selected_soc}")
        st.write(f"**Description**: {description}")

    with col[1]:
        st.markdown(
            """
            <div style="text-align: center; font-weight: bold;">
                Distribution of Standard Operating Expertise across Categories
            </div>
            """,
            unsafe_allow_html=True,
        )
        ###Code to create the person/SOC heatmap data###

        # Initialize the result DataFrame with zero counts
        all_categories = list(set(so_sub["Category"].tolist()))
        expertise_hp = pd.DataFrame(0, index=all_names, columns=all_categories)
        so_sub["Creator"] = so_sub["Creator"].fillna("").astype(str)
        so_sub["Reviewer"] = so_sub["Reviewer"].fillna("").astype(str)

        # Populate the counts
        for _, row in so_sub.iterrows():
            category = row["Category"]
            # Split and clean Creator and Reviewer names
            creators = [name.strip() for name in row["Creator"].split(",")]
            reviewers = [name.strip() for name in row["Reviewer"].split(",")]
            # Combine creators and reviewers
            participants = set(creators + reviewers)
            # Increment counts in the result DataFrame
            for participant in participants:
                if not participant == "":
                    expertise_hp.loc[participant, category] += 1
        ###End: Code to create the person/SOC heatmap data###

        fig = px.imshow(
            expertise_hp,
            x=expertise_hp.columns,
            y=expertise_hp.index,
            color_continuous_scale="blues",
            text_auto=True,
            aspect="auto",
        )
        fig.update_layout(
            xaxis_title="Standard Operating Category",
            yaxis_title="Individuals",
            margin=dict(l=20, r=20, t=20, b=20),
        )
        fig.update(
            data=[{"hovertemplate": "Individual: %{y}<br>SOC: %{x}<br>#SOG/Ps: %{z}"}],
        )
        fig.update_coloraxes(showscale=False)

        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            **Interested in knowing more about the individuals above?** 
            
            Check out the [Expertise section](#stakeholders-for-drug-development-and-discovery-centric-skill) or download the information below."""
        )

        left, middle, right = st.columns(3)
        middle.write("")

        @st.cache_data
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode("utf-8")

        csv = convert_df(so_sub)

        if middle.download_button(
            label="Download Expertise data",
            data=csv,
            file_name="SOP_expertise.csv",
            mime="text/csv",
            use_container_width=True,
        ):
            st.write("Downloaded dataset")

    st.header(
        "Find a Standard Operating Protocol/Guideline",
        divider="gray",
        help="This section allows you to find specific SOG/Ps based on name, keywords, category, type, creators, reviewers etc.",
    )

    col2 = st.columns((1.5, 1), gap="large")

    with col2[0]:
        all_filters = [
            "SOG/Ps Name",
            "ID",
            "Category",
            "Keywords",
            "Type",
            "Creator",
            "Reviewer",
        ]
        selected_filter = st.selectbox(
            "Select a filter to search SOGs/SOPs.", all_filters, index=2
        )

    with col2[1]:
        if selected_filter == "Category":
            all_socs.insert(0, "All")
            selected_soc = st.selectbox(
                "Select a standard operating category to see all related SOG/Ps.",
                all_socs,
                index=0,
            )

        if selected_filter == "SOG/Ps Name":
            text_input = st.text_input(
                "Enter parts or the full name of the SOG/Ps you are looking for:",
            )
        if selected_filter == "ID":
            text_input = st.text_input(
                "Enter part of or the full ID of the SOG/Ps you are looking for:",
            )
        if selected_filter == "Type":
            all_types.insert(0, "All")
            selected_type = st.selectbox(
                "Select a standard operating type to see all related SOG/Ps.",
                all_types,
                index=0,
            )
        if selected_filter == "Creator":
            selected_creator = st.selectbox(
                "Select a creator to see all SOG/Ps they created.",
                all_creators,
                index=0,
            )
        if selected_filter == "Reviewer":
            selected_reviewer = st.selectbox(
                "Select a reviewer to see all SOG/Ps they reviewed.",
                all_reviewers,
                index=0,
            )
        if selected_filter == "Keywords":
            text_input2 = st.text_input(
                "Enter parts or the full name of keywords to filter (selection is case-sensitive):",
            )
            if text_input2 == "":
                selection_kw = st.pills(
                    "Keywords", all_keywords, selection_mode="multi"
                )
            else:
                filtered_kws = [
                    key for key in all_keywords if key.find(text_input2) != -1
                ]
                selection_kw = st.pills(
                    "Keywords", filtered_kws, selection_mode="multi"
                )
    st.write("")
    if selected_soc == "All":
        dataframe_subset = so_display
    elif selected_filter == "Category" and selected_soc != "All":
        dataframe_subset = so_display[so_sub["Category"] == selected_soc]
    elif selected_filter == "SOG/Ps Name" and selected_soc != "All":
        dataframe_subset = so_display[
            so_sub["Title"].str.contains(text_input, case=False, na=False)
        ]
    elif selected_filter == "ID" and selected_soc != "All":
        dataframe_subset = so_display[
            so_sub["ID"].str.contains(text_input, case=False, na=False)
        ]
    elif selected_filter == "Type":
        if selected_type == "All":
            dataframe_subset = so_display
        else:
            mapper = {
                "Standard Operating Guideline (SOG)": "SOG",
                "Standard Operating Protocol (SOP)": "SOP",
                "SOG+SOP": "SOP, SOG",
            }
            dataframe_subset = so_display[so_sub["Type"] == mapper[selected_type]]

    elif selected_filter == "Creator" and selected_soc != "All":
        dataframe_subset = so_display[
            so_sub["Creator"].str.contains(selected_creator, case=False, na=False)
        ]
    if selected_filter == "Reviewer" and selected_soc != "All":
        dataframe_subset = so_display[
            so_sub["Reviewer"].str.contains(selected_reviewer, case=False, na=False)
        ]
    if selected_filter == "Keywords" and selected_soc != "All":
        pattern = "|".join(selection_kw)
        dataframe_subset = so_display[
            so_sub["Keywords"].str.contains(pattern, case=False, na=False)
        ]

    dataframe_subset["DOI"] = dataframe_subset["DOI"].apply(
        lambda x: f"https://doi.org/{x}" if pd.notna(x) else x
    )

    st.data_editor(
        dataframe_subset,
        column_config={
            "DOI": st.column_config.LinkColumn(
                "Zenodo entry",
                help="The Zenodo entry for the SOP/SOG.",
                max_chars=100,
                display_text=r"https://(.*?)\.streamlit\.app",
            ),
        },
        disabled=True,
        hide_index=True,
    )
    st.write("")
    st.header(
        "Access a Standard Operating Protocol or Guideline",
        divider="gray",
        help="This section allows you to access a specific Standard Operating Protocol or Guideline with its ID.",
    )
    col4 = st.columns((1, 1.5), gap="medium")

    with col4[0]:
        access_so = st.selectbox(
            "Type the ID of the SOP/G you want to access", so_display["ID"], index=0
        )

        zenodo = so_sub[so_sub["ID"] == access_so]["DOI"].tolist()

    with col4[1]:
        st.write("")
        if zenodo:
            if len(zenodo) < 1 or pd.isna(zenodo[0]):
                st.warning(
                    f"No Zenodo entry for {access_so} found! Please check back later."
                )
            else:
                zenodo_id = zenodo[0].split(".")[-1]
                components.iframe(
                    f"https://zenodo.org/record/12700122", height=300
                )  # TODO: Still to fix this issue!

# Define your custom CSS
custom_css = """
<style>
.my-container {
background-color: #54c3c0;
padding: 20px;
border-radius: 5px;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

col = st.columns((0.08, 0.84, 0.08))
with col[0]:
    st.image("data/eu_logo.png", width=70)

with col[1]:
    st.markdown(
        '<div class="my-container"> The REMEDi4ALL project has received \
        funding from the European Union’s Horizon Europe Research & Innovation programme \
        under grant agreement No 101057442. </div>',
        unsafe_allow_html=True,
    )

with col[2]:
    st.image("data/Remedi4Alllogo.png", width=90)
