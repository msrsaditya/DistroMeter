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
        <div class="last-updated">Last Updated ⚡ December 30th, 2024</div>
    </div>
    """, unsafe_allow_html=True)

distributions = [
    "chromeos", "archlinux", "Ubuntu", "Fedora", "linuxmint", "Kalilinux",
    "tails", "debian", "pop_os", "ManjaroLinux", "redhat", "openSUSE",
    "NixOS", "Gentoo", "elementaryos", "SteamOS", "EndeavourOS", "CentOS",
    "Qubes", "voidlinux", "Kubuntu", "AsahiLinux", "SolusProject", "Whonix",
    "RockyLinux", "zorinos", "NobaraProject", "MXLinux", "linuxfromscratch",
    "kdeneon", "AlmaLinux", "GarudaLinux", "Lubuntu", "xubuntu", "slackware",
    "ParrotOS", "AlpineLinux", "UbuntuMATE", "GUIX", "deepin", "cachyos",
    "CrunchBang", "holoiso", "bedrocklinux", "ArcoLinux", "crunchbangplusplus",
    "puppylinux", "vanillaos", "antergos", "BlackArchOfficial", "raspbian",
    "ClearLinux", "kisslinux", "PeppermintOS", "antiXLinux", "Mageia",
    "bodhilinux", "Parabola", "FerenOS", "LinuxLite", "RedStarOS",
    "OfficialArchLabsLinux", "tinycorelinux", "Q4OS", "geckolinux",
    "rhinolinux", "sabayon", "OracleLinux", "BackBox", "OpenMandriva",
    "archbang", "cruxlinux", "kinoite", "exherbo", "scientificlinux",
    "venomlinux", "AnarchyLinux", "kaos", "rlxos_dev", "AltLinux"
]

popularity = [
    574047, 283023, 238681, 114997, 112327, 109944, 109840, 92690, 78398,
    71675, 42428, 35469, 33123, 28708, 23573, 20998, 17422, 16672, 15884,
    14990, 13604, 11864, 11367, 9899, 9126, 9047, 8460, 8190, 6853, 6753,
    6300, 6053, 5858, 5806, 5406, 4746, 4281, 4170, 3665, 3563, 3186, 2032,
    1955, 1951, 1650, 1545, 1506, 1470, 1453, 1415, 1267, 1081, 979, 679,
    664, 615, 598, 579, 510, 472, 468, 388, 351, 228, 205, 205, 205, 199,
    170, 168, 168, 151, 126, 110, 59, 57, 50, 38, 37, 35
]

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
    Approximately 15% of the total number of Linux distributions—aka the top 12—are used by around 81% of users.
    Whereas the top 10 distributions (12%) account for nearly 77% of users. This aligns very well with the Pareto Principle or Power Law.
    """)

    st.subheader("Major Distributions")
    st.markdown("""
    These top 12 distributions have more than 30,000 subreddit members. The distributions in this list are:
    
    - Arch Linux
    - Ubuntu
    - Fedora
    - Linux Mint
    - Tails
    - Kali Linux
    - Debian
    - Pop!_OS
    - Manjaro Linux
    - Red Hat
    - openSUSE
    - NixOS

    The top 10 distributions though, have more than 40,000 subreddit members. The top 9 have >70,000, the top 6 have >100,000 and the top 2 have >200,000
    """)

    st.subheader("Parent Distributions")
    st.markdown("""
    Among these, five distributions serve as the parent distributions for all others. 
    This indicates that there are only four or five Linux distributions that most people actively use, which are:
    
    - Arch Linux
    - Debian
    - Fedora
    - openSUSE
    - NixOS
    """)

    st.subheader("Top 12 Distributions by Popularity")
    fig_top_12 = plot_chart('barh', filtered_data.head(12), 
                            title="Top 12 Distributions by Popularity",
                            x_label="Number of Members",
                            y_label="Linux Distributions")
    st.pyplot(fig_top_12)

    st.subheader("Core Usage")
    st.markdown("""
    Looking at the popularity bar graph, The top three most popular independent distributions (which are also used by the top 10 in the list) are:
    
    - Arch Linux
    - Debian
    - Fedora

    These are also the top 3 distributions with the most number of subreddit members of all time (coincidentally :p)
    """)

    st.subheader("Desktop Environment Usage")
    st.markdown("""
    There are 22 distributions with more than 10,000 members in their subreddits. Out of these 22 distributions:
    
    ###### GNOME is used by:
    - CentOS
    - Debian
    - Fedora
    - NixOS
    - RHEL
    - Tails
    - Ubuntu
    
    ###### Xfce is used by:
    - EndeavourOS
    - Kali Linux
    - Manjaro Linux
    - Qubes OS
    - Void Linux
    
    ###### KDE Plasma is used by:
    - Asahi Linux
    - Kubuntu
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
    
    All of these desktop environments are used by default or are marketed as the "flagship" desktop environment on all of these distributions' main website.
    
    ###### Usage Distribution:
    - **GNOME**: 7/22
    - **Xfce**: 5/22
    - **KDE Plasma**: 4/22
    - **None**: 2/22
    - **Cinnamon**: 1/22
    - **COSMIC**: 1/22
    - **Pantheon**: 1/22
    - **Budgie**: 1/22
    
    This clearly shows the "tripoly" of GNOME, KDE, and Xfce, and the duopoly of GTK and Qt GUI toolkits. This clearly shows that most users are using **GNOME** with **GTK**, and no one using desktop environments like **Cutefish**, **Deepin**, **Enlightenment**, **LXDE**, **LXQt**, **Lumina**, **MATE**, **Unity** etc. as their default or flagship desktops.
    """)

    st.subheader("Conclusion and Opinion")
    st.markdown("""
    Linux Fragmentation is really overblown and overhyped. The overwhelming number of distros and desktops create a paradox of choice for new users. 
    Most people that ever use Linux only either use **Arch, Debian or Fedora** with **GNOME, KDE or Xfce**, so why confuse the new user with all these useless choices?
    Derivative distros these days are just changing themes and calling it a new operating system (with exceptions like Linux Mint with Cinnamon DE). Don't fall for the hype. 
    Use FAD (Fedora, Arch, Debian) with KNOX (Kde, gNOme, Xfce) - This should be the default mantra for beginners. This is not my opinion, this is an objective assessment of the data.
    """)
