import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Linux Distributions' Popularity")

# Define Distributions And Popularity Data
distributions = [
    "chromeos", "archlinux", "Ubuntu", "Fedora", "tails", "linuxmint", 
    "Kalilinux", "debian", "pop_os", "ManjaroLinux", "redhat", "openSUSE", 
    "NixOS", "Gentoo", "elementaryos", "SteamOS", "CentOS", "EndeavourOS", 
    "Qubes", "voidlinux", "Kubuntu", "SolusProject", "AsahiLinux", 
    "Whonix", "RockyLinux", "zorinos", "MXLinux", "NobaraProject", 
    "linuxfromscratch", "kdeneon", "AlmaLinux", "GarudaLinux", "Lubuntu", 
    "xubuntu", "slackware", "ParrotOS", "AlpineLinux", "GUIX", "deepin", 
    "cachyos", "CrunchBang", "bedrocklinux", "holoiso", "ArcoLinux", 
    "crunchbangplusplus", "puppylinux", "antergos", "vanillaos", 
    "BlackArchOfficial", "raspbian", "ClearLinux", "kisslinux", 
    "PeppermintOS", "antiXLinux", "Mageia", "bodhilinux", "Parabola", 
    "FerenOS", "LinuxLite", "RedStarOS", "OfficialArchLabsLinux", 
    "tinycorelinux", "Q4OS", "geckolinux", "sabayon", "OracleLinux", 
    "rhinolinux", "BackBox", "archbang", "OpenMandriva", "cruxlinux", 
    "kinoite", "exherbo", "scientificlinux", "venomlinux", "AnarchyLinux", 
    "rlxos_dev", "kaos", "AltLinux"
]

popularity = [
    573984, 278234, 236683, 111454, 108128, 107717, 107467, 89550, 77018, 
    71334, 41411, 34646, 31053, 27750, 23262, 20177, 16667, 16053, 15706, 
    14613, 13187, 11346, 11255, 9833, 8979, 8734, 8045, 8042, 6803, 6722, 
    6132, 5962, 5796, 5695, 5355, 4683, 4043, 3602, 3564, 2572, 2038, 
    1945, 1939, 1635, 1532, 1487, 1459, 1442, 1343, 1262, 1078, 976, 673, 
    635, 618, 593, 579, 515, 468, 453, 390, 341, 219, 209, 205, 194, 189, 
    168, 166, 165, 149, 120, 108, 59, 58, 49, 37, 36, 32
]

# Load Data And Sort By Popularity
@st.cache_data
def load_data():
    data = pd.DataFrame({'Distribution': distributions, 'Popularity': popularity})
    return data.sort_values(by='Popularity', ascending=False)

data = load_data()

st.title("Linux Distributions' Popularity")

# Sidebar Controls
st.sidebar.title("Explore Linux Distributions")
ALL_OPTION = "ALL"
selected_distributions = st.sidebar.multiselect("Select Distributions To Display", [ALL_OPTION] + distributions, default=[ALL_OPTION])
excluded_distributions = st.sidebar.multiselect("Exclude Distributions", distributions)
min_members = st.sidebar.number_input("Minimum Popularity", min_value=0, step=1, value=0)

# Filter Data Based On User Selections
def filter_data(data, selected, excluded, min_popularity):
    if ALL_OPTION in selected:
        filtered_data = data[~data['Distribution'].isin(excluded) & (data['Popularity'] >= min_popularity)]
    else:
        filtered_data = data[data['Distribution'].isin(selected) & ~data['Distribution'].isin(excluded) & (data['Popularity'] >= min_popularity)]
    return filtered_data

filtered_data = filter_data(data, selected_distributions, excluded_distributions, min_members)

# Display Ranking
st.header("Ranking")
st.dataframe(filtered_data[['Distribution', 'Popularity']], use_container_width=True)

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
        
    ax.set_title(title)
    plt.tight_layout()
    st.pyplot(fig)

# Generate Visualizations
plot_chart('pie', filtered_data, title="Distribution Of Popularity Among Selected Distributions")
plot_chart('barh', filtered_data, title="Popularity Of Selected Linux Distributions", x_label="Popularity", y_label="Linux Distributions")
plot_chart('hist', filtered_data, title="Distribution Of Popularity Scores For Selected Distributions", x_label="Popularity", y_label="Frequency")
