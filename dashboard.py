from urllib.request import urlopen
import json
import pandas as pd

import streamlit as st
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
        """The REMEDi4ALL consortium brings together a unique combination of expertise to address the complexities of drug repurposing. Under the leadership of EATRIS, the European infrastructure for translational medicine, 24 organisations in the fields of clinical and translational research, clinical operations, patient engagement and education, regulatory framework, funding, governance, Health Technology Assessment (HTA) and pricing and reimbursement will closely collaborate to make drug repurposing mainstream. Please check out our website for more information: https://remedi4all.org/"""
    )

tab1, tab2 = st.tabs(
    [
        "Project Information",
        "KG Drug Discovery ",
    ]
)

# Main content on R4A project
with tab1:
    st.write(
        """The [REMEDi4ALL consortium] 
        The vast majority of the over 7000 known diseases are without effective treatments—there is thus an urgent need to make better use of the medicines that we already have in hand. These include medicines that have already been approved for human use, as well as experimental medicines still in clinical trials already showing good pharmaceutical properties and human safety. In fact, most approved drugs intrinsically have the potential to treat many more diseases than they were originally approved for, even diseases seemingly unrelated to those for which they are currently being prescribed.
        
        [REMEDi4ALL](https://remedi4all.org/) is an EU-funded initiative (HORIZON EUROPE) whose key mission is to make it easier and more reliable to find new medical uses for drugs we already know are safe and effective. We also aim to show that in many cases such “repurposed” medicines can be taken all the way into clinic faster and at the fraction of the cost of developing a completely new drug from scratch. 
        
        But with hundreds or even thousands of opportunities to repurpose approved and experimental medicines—for the thousands of diseases that remain without any approved treatments at all—REMEDi4ALL must also help to transform the very landscape of drug repurposing. This needs to encompass not only the scientific, clinical research and patient communities, but regulatory, policy and commercial drug and investment sectors as well, so that all researchers will face fewer barriers and be able to bring much needed treatments to patients faster and more effectively—to “float all boats” in the drug repurposing ecosystem."""
    )

    st.header(
        "REMEDi4ALL structure and partners",
        divider="gray",
        help="This section allows you know more about the REMEDi4ALL project and see the basic information surrounding the project in the KG.",
    )

    # st.subheader("Drug repurposing stakeholder around the globe")

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
        f"REMEDi4ALL project is composed of :red[{total_people}] from :red[{total_partners}] partner organisations from :red[{total_countries}] countries that bring together a unique combination of expertise to address the complexities of drug repurposing with a patient-centric approach. At our core is a patient-centric drug repurposing platform designed to encompass the complete value chain supporting high impact projects initiating at any phase of development through to market entry and patient access."
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

    st.markdown(
        f"""REMEDi4ALL was designed with four imbedded drug repurposing projects at various stages of discovery and development to serve as “Demonstrator” projects with which our core platform could be put into practice from the start. In turn, experiences and lessons learned from designing and implementing project plans for these four Demonstrator have already been key in helping to validate, identify gaps and improve the structure of and resources/expertise contained in our core platform. These projects four Demonstrator focus on different indications, namely metastatic pancreatic cancer (mPDAC), pandemic preparedness, osteogenesis imperfecta (OI), and multiple sulfatase deficiency (MSD). The demonstrator portfolio covers different phases of the development path and represents the diverse nature of repurposing projects we are likely to work on in the future. 
        
        In the coming year, REMEDi4ALL will begin processes to expand its project portfolio by bringing on additional “User” projects to be supported by our core drug repurposing platform.
        
        The work distribution among REMEDi4ALL partner institutions is delineated through the allocation of work packages, each representing a distinct set of tasks or objectives. There are :red[{len(wp_data)}] work packages in REMEDi4ALL, which serve as the building blocks of collaboration between partners."""
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
            f""":red[{selected_wp}] is led by :red[{selected_wp_lead}] and has :red[{selected_wp_organizations}] contributing partners and a total of :red[{selected_wp_individuals}] individuals working on it."""
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
                """WP12 focuses on mapping the drug repurposing landscape, establishing connections with key stakeholders, and engaging with international consortia and repurposing initiatives. This grants significant presence of REMEDi4ALL at both global and EU levels, facilitates alignment of international agendas, and prevents fragmentation within the field. WP12 is led by EATRIS with X contributing partners and a total of 3 individuals working on it."""
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
        st.dataframe(
            people_with_skill_filtered, hide_index=True, use_container_width=True
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
                xaxis_title="Individuals",
                yaxis_title="Skills",
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
            st.image(wordcloud.to_image(), use_column_width=True)
        else:
            st.write("No information found in KG.")
