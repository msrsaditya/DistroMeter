import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Linux Distributions' Popularity",
    layout="wide"
)

# Custom CSS for the title styling with reduced size
st.markdown("""
    <style>
    .title-container {
        text-align: center;
        padding: 1rem 0;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.3rem;
        white-space: nowrap;
    }
    .subtitle {
        font-size: 1.4rem;
        color: #666;
        margin-bottom: 0.3rem;
    }
    .last-updated {
        font-size: 1rem;
        color: #888;
        font-style: italic;
    }
    </style>
    
    <div class="title-container">
        <div class="main-title">Linux Distributions' Popularity</div>
        <div class="subtitle">Based on Subreddit Member Count</div>
        <div class="last-updated">Last Updated ⚡ November 18th, 2024</div>
    </div>
    """, unsafe_allow_html=True)

# New Distributions And Popularity Data
distributions = [
    "chromeos", "archlinux", "Ubuntu", "Fedora", "tails", "linuxmint", "Kalilinux", 
    "debian", "pop_os", "ManjaroLinux", "redhat", "openSUSE", "NixOS", "Gentoo", 
    "elementaryos", "SteamOS", "CentOS", "EndeavourOS", "Qubes", "voidlinux", 
    "Kubuntu", "SolusProject", "AsahiLinux", "Whonix", "RockyLinux", "zorinos", 
    "NobaraProject", "MXLinux", "linuxfromscratch", "kdeneon", "AlmaLinux", "GarudaLinux", 
    "Lubuntu", "xubuntu", "slackware", "ParrotOS", "AlpineLinux", "GUIX", "deepin", 
    "cachyos", "CrunchBang", "bedrocklinux", "holoiso", "ArcoLinux", "crunchbangplusplus", 
    "puppylinux", "antergos", "vanillaos", "BlackArchOfficial", "raspbian", "ClearLinux", 
    "kisslinux", "PeppermintOS", "antiXLinux", "Mageia", "bodhilinux", "Parabola", 
    "FerenOS", "LinuxLite", "RedStarOS", "OfficialArchLabsLinux", "tinycorelinux", 
    "Q4OS", "geckolinux", "sabayon", "OracleLinux", "rhinolinux", "BackBox", "archbang", 
    "OpenMandriva", "cruxlinux", "kinoite", "exherbo", "scientificlinux", "venomlinux", 
    "AnarchyLinux", "rlxos_dev", "kaos", "AltLinux"
]

numbers = [
    573969, 278307, 236710, 111505, 108157, 107805, 107515, 89603, 77042, 71334, 
    41424, 34675, 31089, 27758, 23262, 20217, 16666, 16083, 15708, 14620, 13191, 
    11348, 11270, 9837, 8982, 8731, 8055, 8049, 6806, 6724, 6139, 5961, 5797, 5697, 
    5356, 4683, 4058, 3603, 3566, 2583, 2038, 1946, 1939, 1636, 1532, 1487, 1458, 1441, 
    1345, 1262, 1078, 976, 673, 637, 618, 593, 578, 515, 468, 453, 390, 341, 220, 
    209, 205, 194, 190, 168, 166, 165, 149, 120, 108, 59, 58, 49, 37, 36, 32
]

# Load Data And Sort By Popularity
@st.cache_data
def load_data():
    data = pd.DataFrame({'Distribution': distributions, 'Popularity': numbers})
    return data.sort_values(by='Popularity', ascending=False)

data = load_data()

# Sidebar Controls
st.sidebar.title("Explore Linux Distributions")
ALL_OPTION = "ALL"

# Distribution Selection
selected_distributions = st.sidebar.multiselect(
    "Select Distributions To Display",
    [ALL_OPTION] + distributions,
    default=[ALL_OPTION]
)

# Exclusion Selection
excluded_distributions = st.sidebar.multiselect(
    "Exclude Distributions",
    distributions,
    default=["chromeos"]
)

# Minimum Members Filter
min_members = st.sidebar.number_input(
    "Minimum Popularity",
    min_value=0,
    step=1000,
    value=10000
)

# Filter Data Based On User Selections
def filter_data(data, selected, excluded, min_popularity):
    if ALL_OPTION in selected:
        filtered_data = data[~data['Distribution'].isin(excluded) & (data['Popularity'] >= min_popularity)]
    else:
        filtered_data = data[data['Distribution'].isin(selected) & ~data['Distribution'].isin(excluded) & (data['Popularity'] >= min_popularity)]
    return filtered_data

filtered_data = filter_data(data, selected_distributions, excluded_distributions, min_members)

# Create tabs
tab1, tab2, tab3 = st.tabs(["Explore", "Visualizations", "Insights"])

# Helper Function For Creating Plots
def plot_chart(plot_type, data, title, x_label="", y_label="", **kwargs):
    fig, ax = plt.subplots(figsize=(kwargs.get("figsize", (10, 6))))
    
    if plot_type == 'pie':
        ax.pie(data['Popularity'], labels=data['Distribution'], autopct='%1.1f%%', startangle=140)
        ax.axis('equal')
    elif plot_type == 'barh':
        ax.barh(data['Distribution'], data['Popularity'], color=kwargs.get("color", 'skyblue'))
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
    elif plot_type == 'hist':
        ax.hist(data['Popularity'], bins=kwargs.get("bins", 20), color=kwargs.get("color", 'lightgreen'), edgecolor='black')
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
    elif plot_type == 'box':
        # Create a box plot manually using matplotlib
        ax.boxplot(data['Popularity'], vert=False, patch_artist=True, boxprops=dict(facecolor='skyblue'))
        ax.set_xlabel(y_label)
    elif plot_type == 'scatter':
        # Create a scatter plot manually using matplotlib
        ax.scatter(data['Distribution'], data['Popularity'], color='blue')
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
    
    ax.set_title(title)
    plt.tight_layout()
    return fig

# Tab 1: Explore
with tab1:
    st.header("Distribution Rankings")
    # Add rank to the dataframe
    filtered_data_with_rank = filtered_data.reset_index(drop=True)
    filtered_data_with_rank.index = filtered_data_with_rank.index + 1
    st.dataframe(
        filtered_data_with_rank,
        use_container_width=True,
        hide_index=False,  # Show the index as rank
    )

# Tab 2: Visualizations
with tab2:
    # Ensure data is not empty
    if len(filtered_data) > 0:
        # Pie chart first
        fig_pie = plot_chart('pie', filtered_data, 
                          title=f"Distribution of Popularity",
                          figsize=(8, 8))
        st.pyplot(fig_pie)

        # Bar chart second
        fig_bar = plot_chart('barh', filtered_data, 
                          title=f"Top Distributions by Popularity",
                          x_label="Number of Members", 
                          y_label="Linux Distributions")
        st.pyplot(fig_bar)

        # Histogram third
        fig_hist = plot_chart('hist', filtered_data, 
                          title="Distribution of Member Counts",
                          x_label="Number of Members", 
                          y_label="Frequency",
                          bins=20)
        st.pyplot(fig_hist)

        # Box plot (updated)
        fig_box = plot_chart('box', filtered_data, 
                             title="Popularity Distribution Box Plot", 
                             y_label="Popularity")
        st.pyplot(fig_box)

        # Scatter plot (updated)
        fig_scatter = plot_chart('scatter', filtered_data, 
                                 title="Scatter Plot of Popularity vs Distribution",
                                 x_label="Linux Distributions", 
                                 y_label="Popularity")
        st.pyplot(fig_scatter)
    else:
        st.write("No data available for the current filters.")

# Tab 3: Insights
with tab3:
    st.header("Key Insights")

    # Distribution Concentration
    st.subheader("Distribution Concentration")
    st.markdown("""
    Approximately 15% of the total number of Linux distributions—aka the top 12 distributions—are used by around 81% of users. 
    This aligns with the Pareto Principle (Power Law).
    """)

    # Major Distributions
    st.subheader("Major Distributions")
    st.markdown("""
    These 80% market share distributions each have more than 30,000 subreddit members. 
    The distributions in this list are:
    
    - Arch Linux
    - Ubuntu
    - Fedora
    - Tails
    - Linux Mint
    - Kali Linux
    - Debian
    - Pop!_OS
    - Manjaro Linux
    - Red Hat
    - openSUSE
    - NixOS
    """)

    # Parent Distributions
    st.subheader("Parent Distributions")
    st.markdown("""
    Among these, five distributions serve as the parent distributions for all others:
    
    - Arch Linux
    - Debian
    - Fedora
    - openSUSE
    - NixOS
    """)

    # Core Usage
    st.subheader("Core Usage")
    st.markdown("""
    In practice, there are only four or five Linux distributions that most people actively use (as derivatives do not count). 
    The top three most popular are:
    
    - Arch Linux
    - Debian
    - Fedora
    """)

    # Top 12 Distributions Visualization
    st.subheader("Top 12 Distributions by Popularity")
    fig_top_12 = plot_chart('barh', filtered_data.head(12), 
                            title="Top 12 Distributions by Popularity",
                            x_label="Number of Members",
                            y_label="Linux Distributions")
    st.pyplot(fig_top_12)
