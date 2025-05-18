import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(
    page_title="Linux Distributions' Popularity",
    layout="wide"
)

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
        <div class="last-updated">Last Updated ⚡ May 18th, 2025</div>
    </div>
    """, unsafe_allow_html=True)

distributions = ["chromeos", "archlinux", "Ubuntu", "linuxmint", "Fedora", "Kalilinux", "tails", "debian", "pop_os", "ManjaroLinux", "redhat", "NixOS", "openSUSE", "Gentoo", "SteamOS", "elementaryos", "EndeavourOS", "Qubes", "CentOS", "voidlinux", "Kubuntu", "AsahiLinux", "SolusProject", "NobaraProject", "zorinos", "Whonix", "RockyLinux", "MXLinux", "cachyos", "linuxfromscratch", "kdeneon", "AlmaLinux", "GarudaLinux", "Lubuntu", "xubuntu", "slackware", "AlpineLinux", "ParrotOS", "UbuntuMATE", "GUIX", "deepin", "CrunchBang", "bedrocklinux", "holoiso", "BlackArchOfficial", "ArcoLinux", "puppylinux", "crunchbangplusplus", "vanillaos", "antergos", "raspbian", "ClearLinux", "kisslinux", "antiXLinux", "PeppermintOS", "bodhilinux", "Mageia", "Parabola", "RedStarOS", "FerenOS", "LinuxLite", "OfficialArchLabsLinux", "tinycorelinux", "rhinolinux", "Q4OS", "OpenMandriva", "OracleLinux", "geckolinux", "sabayon", "BackBox", "archbang", "cruxlinux", "kinoite", "exherbo", "venomlinux", "AnarchyLinux", "scientificlinux", "AltLinux", "kaos", "rlxos_dev"]

popularity = [574124, 302815, 249999, 132871, 129095, 119301, 115452, 104621, 83221, 73369, 46076, 39250, 38773, 30958, 29474, 23820, 22032, 16694, 16671, 16532, 14886, 13993, 11435, 11413, 10307, 10253, 9548, 8690, 7588, 7577, 6874, 6708, 6568, 6165, 6039, 5620, 5070, 4938, 4234, 3888, 3653, 2030, 1989, 1948, 1706, 1671, 1612, 1578, 1542, 1436, 1308, 1121, 979, 749, 719, 643, 634, 582, 516, 511, 507, 394, 394, 291, 285, 279, 229, 208, 205, 172, 171, 157, 142, 115, 62, 59, 59, 53, 40, 39]

@st.cache_data
def load_data():
    data = pd.DataFrame({'Distribution': distributions, 'Popularity': popularity})
    return data.sort_values(by='Popularity', ascending=False)

data = load_data()

st.sidebar.title("Explore Linux Distributions")
ALL_OPTION = "ALL"

selected_distributions = st.sidebar.multiselect(
    "Select Distributions To Display",
    [ALL_OPTION] + distributions,
    default=[ALL_OPTION]
)

excluded_distributions = st.sidebar.multiselect(
    "Exclude Distributions",
    distributions,
    default=["chromeos"]
)

min_members = st.sidebar.number_input(
    "Minimum Popularity",
    min_value=0,
    step=1000,
    value=10000
)

def filter_data(data, selected, excluded, min_popularity):
    if ALL_OPTION in selected:
        filtered_data = data[~data['Distribution'].isin(excluded) & (data['Popularity'] >= min_popularity)]
    else:
        filtered_data = data[data['Distribution'].isin(selected) & ~data['Distribution'].isin(excluded) & (data['Popularity'] >= min_popularity)]
    return filtered_data

filtered_data = filter_data(data, selected_distributions, excluded_distributions, min_members)

tab1, tab2, tab3 = st.tabs(["Explore", "Visualizations", "Insights"])

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
        ax.boxplot(data['Popularity'], vert=False, patch_artist=True, boxprops=dict(facecolor='skyblue'))
        ax.set_xlabel(y_label)
    elif plot_type == 'scatter':
        ax.scatter(data['Distribution'], data['Popularity'], color='blue')
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
    
    ax.set_title(title)
    plt.tight_layout()
    return fig

with tab1:
    st.header("Distribution Rankings")
    filtered_data_with_rank = filtered_data.reset_index(drop=True)
    filtered_data_with_rank.index = filtered_data_with_rank.index + 1
    st.dataframe(
        filtered_data_with_rank,
        use_container_width=True,
        hide_index=False,
    )

with tab2:
    if len(filtered_data) > 0:
        fig_pie = plot_chart('pie', filtered_data, 
                          title=f"Distribution of Popularity",
                          figsize=(8, 8))
        st.pyplot(fig_pie)

        fig_bar = plot_chart('barh', filtered_data, 
                          title=f"Top Distributions by Popularity",
                          x_label="Number of Members", 
                          y_label="Linux Distributions")
        st.pyplot(fig_bar)

        fig_hist = plot_chart('hist', filtered_data, 
                          title="Distribution of Member Counts",
                          x_label="Number of Members", 
                          y_label="Frequency",
                          bins=20)
        st.pyplot(fig_hist)

        fig_box = plot_chart('box', filtered_data, 
                             title="Popularity Distribution Box Plot", 
                             y_label="Popularity")
        st.pyplot(fig_box)

        fig_scatter = plot_chart('scatter', filtered_data, 
                                 title="Scatter Plot of Popularity vs Distribution",
                                 x_label="Linux Distributions", 
                                 y_label="Popularity")
        st.pyplot(fig_scatter)
    else:
        st.write("No data available for the current filters.")

with tab3:
    st.header("Key Insights")

    st.subheader("Distribution Concentration")
    st.markdown("""
    The top 10 distributions (12% of all listed distributions) account for nearly 82% of users. This aligns very well with the Pareto Principle or Power Law.
    """)

    st.subheader("Major Distributions")
    st.markdown("""
    All of these (top 10) distributions have 46,000+ subreddit members. The distributions in this list are:
    - Arch Linux
    - Ubuntu
    - Linux Mint
    - Fedora
    - Kali Linux
    - Tails
    - Debian
    - Pop!_OS
    - Manjaro Linux
    - Red Hat
    
    The top 9 distributions, though, have 73,000+ subreddit members. The top 8 have 83,000+, the top 7 have 100,000+, and the top 2 have 250,000+. The topmost distribution (archlinux) has 300,000+ subreddit members.
    """)

    st.subheader("Parent Distributions")
    st.markdown("""
    Among these, three distributions serve as the parent distribution for all others. 
    This indicates that there are only three Linux distributions that most people basically use, these are:
    
    - Arch Linux
    - Debian
    - Fedora
    """)

    st.subheader("Desktop Environment Usage")
    st.markdown("""
    There are 25 distributions with more than 10,000 members in their subreddits. Out of these 25 distributions:
    
    ###### GNOME is used by:
    - CentOS
    - Debian
    - Fedora
    - NixOS
    - RHEL
    - Tails
    - Ubuntu
    - Zorin
    
    ###### Xfce is used by:
    - EndeavourOS
    - Kali Linux
    - Manjaro Linux
    - Qubes OS
    - Void Linux
    - Whonix
    
    ###### KDE Plasma is used by:
    - Asahi Linux
    - Kubuntu
    - NobaraProject
    - OpenSUSE
    - SteamOS
    
    ###### Pantheon is used by:
    - Elementary OS
    
    ###### Cinnamon is used by:
    - Linux Mint
    
    ###### COSMIC is used by:
    - Pop OS
    
    ###### Budgie is used by:
    - Solus
    
    ###### None is used by:
    - Arch Linux
    - Gentoo

    Note that "used" here means used by default or are marketed as the "flagship" desktop environment on these distributions' main website.
    
    ###### Usage Distribution:
    - **GNOME**: 8/25
    - **Xfce**: 6/25
    - **KDE Plasma**: 5/25
    - **None**: 2/25
    - **Cinnamon**: 1/25
    - **COSMIC**: 1/25
    - **Pantheon**: 1/25
    - **Budgie**: 1/25
    
   This clearly shows the "tripoly" of GNOME, KDE, and Xfce, as well as the duopoly of GTK and Qt GUI toolkits. This also shows that most distros are using **GNOME** with **GTK**, and almost no distro is using desktop environments like **Cufefish**, **Deepin**, **Enlightenment**, **LXDE**, **LXQt**, **Lumina**, **MATE**, **Unity**, etc. as their default or flagship desktops.
    """)

    st.subheader("Conclusion and Opinion")
    st.markdown("""
    Linux Fragmentation is really overblown for no (good) reason. The overwhelming number of distros and desktops creates a paradox of choice for new users.

    Most people that ever use Linux (seriously) only either use **Arch, Debian or Fedora** with **GNOME, KDE or Xfce**.

    Derivative distros these days are just changing themes and calling it a new operating system (with exceptions like Linux Mint with Cinnamon DE).
    Use FAD (Fedora, Arch, Debian) with KNOX (Kde, gNOme, Xfce) - This should be the default mantra for beginners as it simplifies their Linux journey to a great extent.
    """)
