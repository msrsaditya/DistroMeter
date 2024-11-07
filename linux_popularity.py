import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Linux Distributions' Popularity")

# Define Distributions And Popularity Data
distributions = [
    "ChromeOS", "Arch Linux", "Ubuntu", "Tails", "Fedora", "Kali Linux", "Linux Mint", 
    "Debian", "Pop!_OS", "Manjaro Linux", "Red Hat", "openSUSE", "Gentoo", "NixOS", 
    "elementary OS", "SteamOS", "CentOS", "Qubes OS", "Void Linux", "EndeavourOS", 
    "Kubuntu", "Solus Project", "Whonix", "Asahi Linux", "Rocky Linux", "Zorin OS", 
    "MX Linux", "KDE neon", "Linux from Scratch", "Nobara Project", "Lubuntu", 
    "AlmaLinux", "Xubuntu", "Garuda Linux", "Slackware", "Parrot OS", "deepin", 
    "Alpine Linux", "Guix", "CrunchBang", "Bedrock Linux", "HoloISO", "ArcoLinux", 
    "Antergos", "CrunchBangplusplus", "Puppy Linux", "Raspbian", "BlackArch Official", 
    "Clear Linux", "VanillaOS", "KISS Linux", "CachyOS", "Peppermint OS", "Mageia", 
    "Parabola", "antiX Linux", "Bodhi Linux", "Feren OS", "Linux Lite", 
    "Official Arch Labs Linux", "RedStar OS", "Tiny Core Linux", "GeckoLinux", 
    "Sabayon", "Q4OS", "RhinoLinux", "BackBox", "ArchBang", "Oracle Linux", 
    "OpenMandriva", "Crux Linux", "Exherbo", "Kinoite", "Scientific Linux", 
    "Venom Linux", "Anarchy Linux", "RLXOS Dev", "KaOS", "Alt Linux"
]

popularity = [
    573991, 272553, 234021, 107725, 106591, 103750, 103511, 86717, 75524, 70938, 
    40351, 33896, 29258, 27160, 23213, 19747, 16644, 15487, 15161, 14256, 
    12733, 11296, 10335, 9590, 8772, 8434, 7914, 7600, 6675, 6654, 
    5899, 5804, 5726, 5626, 5289, 4589, 3822, 3547, 3458, 2039, 
    1956, 1937, 1927, 1606, 1511, 1466, 1462, 1383, 1270, 1247, 
    1060, 972, 672, 616, 615, 584, 575, 520, 457, 437, 
    383, 326, 212, 210, 202, 185, 180, 166, 162, 160, 
    146, 107, 106, 59, 55, 44, 36, 31, 26
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
