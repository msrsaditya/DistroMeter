import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Linux Distributions' Popularity", layout="wide")

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

distributions = ["chromeos", "archlinux", "Ubuntu", "Proxmox", "linuxmint", "Fedora", "Kalilinux", "tails", "debian", "pop_os", "ManjaroLinux", "truenas", "redhat", "NixOS", "openSUSE", "Gentoo", "SteamOS", "batocera", "OpenMediaVault", "elementaryos", "EndeavourOS", "Qubes", "CentOS", "voidlinux", "Kubuntu", "AsahiLinux", "Bazzite", "SolusProject", "NobaraProject", "zorinos", "Whonix", "RockyLinux", "MXLinux", "cachyos", "linuxfromscratch", "kdeneon", "AlmaLinux", "3CX", "GarudaLinux", "Lubuntu", "recalbox", "xubuntu", "slackware", "tuxedocomputers", "AlpineLinux", "ParrotOS", "libreELEC", "UbuntuMATE", "archcraft", "GUIX", "deepin", "artixlinux", "Lakka", "vyos", "dietpi", "Freedombox", "CrunchBang", "bedrocklinux", "holoiso", "BlackArchOfficial", "ArcoLinux", "puppylinux", "crunchbangplusplus", "vanillaos", "antergos", "raspbian", "ClearLinux", "devuan", "kisslinux", "BunsenLabs", "trisquel", "antiXLinux", "PeppermintOS", "UbuntuBudgie", "bodhilinux", "Mageia", "chimeralinux", "Parabola", "yunohost", "RedStarOS", "FerenOS", "LinuxLite", "Armbian", "windowmaker", "ipfire", "OfficialArchLabsLinux", "tinycorelinux", "BlendOS", "ubuntucinnamon", "UbuntuUnity", "rebornos", "rhinolinux", "Q4OS", "OpenMandriva", "TurnkeyLinux", "PikaOS", "regata_os", "OracleLinux", "geckolinux", "sabayon", "pureos", "RockStor", "MaboxLinux", "ultramarine", "BackBox", "archbang", "cruxlinux", "t2sde", "Kicksecure", "kinoite", "NethServer", "endlessos", "obarun", "SpiralLinux", "exherbo", "siduction", "SliTaz", "zentyal", "kodachilinux", "SparkyLinuxOrg", "solydxk", "AVLinux", "UbuntuKylin", "venomlinux", "AnarchyLinux", "scientificlinux", "AltLinux", "EliveLinux", "RedCore", "risiOS", "kaos", "rlxos_dev", "openKylin", "Linspire"]

popularity = [574121, 302925, 250039, 146851, 132985, 129171, 119332, 115474, 104680, 83240, 73378, 60193, 46085, 39290, 38792, 30971, 29497, 25526, 23982, 23819, 22052, 16696, 16672, 16542, 14905, 14008, 12116, 11436, 11423, 10311, 10255, 9550, 8690, 7613, 7578, 6877, 6708, 6652, 6568, 6168, 6153, 6039, 5619, 5244, 5072, 4938, 4330, 4234, 3921, 3889, 3654, 3321, 3196, 2990, 2496, 2115, 2030, 1989, 1948, 1708, 1671, 1613, 1578, 1542, 1436, 1308, 1119, 997, 979, 900, 898, 751, 719, 685, 644, 634, 582, 582, 538, 517, 511, 507, 486, 464, 435, 394, 394, 342, 326, 318, 314, 291, 285, 279, 269, 252, 239, 230, 208, 205, 193, 191, 187, 184, 172, 171, 157, 155, 154, 142, 131, 124, 123, 117, 115, 91, 83, 73, 72, 66, 65, 63, 62, 62, 59, 59, 53, 51, 48, 43, 40, 39, 37, 15]

INDEPENDENT = ["debian", "Fedora", "openSUSE", "NixOS", "SolusProject", "OpenMandriva", "AlpineLinux", "puppylinux", "slackware", "AltLinux", "Mageia", "chimeralinux", "Gentoo", "kaos", "archlinux", "tinycorelinux", "voidlinux", "cruxlinux", "venomlinux", "ClearLinux", "ipfire", "linuxfromscratch", "SliTaz", "batocera", "GUIX", "libreELEC", "bedrocklinux", "exherbo", "recalbox", "rlxos_dev"]

@st.cache_data
def load_data():
    df = pd.DataFrame({'Distribution': distributions, 'Popularity': popularity})
    return df.sort_values(by='Popularity', ascending=False)

data = load_data()

st.sidebar.title("Explore Linux Distributions")

display_mode = st.sidebar.selectbox("Distribution Type", ["ALL","Independent","Derived"], index=0)

excluded_distributions = st.sidebar.multiselect(
    "Exclude Distributions", distributions,
    default=["batocera","chromeos","OpenMediaVault","Proxmox","truenas"]
)

min_members = st.sidebar.number_input("Minimum Popularity", min_value=0, step=1000, value=10000)

def filter_data(df, mode, excluded, min_pop):
    base = df[(~df['Distribution'].isin(excluded)) & (df['Popularity'] >= min_pop)]
    if mode == "Independent":
        return base[base['Distribution'].isin(INDEPENDENT)]
    elif mode == "Derived":
        return base[~base['Distribution'].isin(INDEPENDENT)]
    return base

filtered = filter_data(data, display_mode, excluded_distributions, min_members)

tab1, tab2, tab3 = st.tabs(["Explore","Visualizations","Insights"])

def plot_chart(kind, df, title, x_label="", y_label="", **kwargs):
    fig, ax = plt.subplots(figsize=kwargs.get("figsize",(10,6)))
    if kind=='pie':
        ax.pie(df['Popularity'], labels=df['Distribution'], autopct='%1.1f%%', startangle=140)
        ax.axis('equal')
    elif kind=='barh':
        ax.barh(df['Distribution'], df['Popularity'], color=kwargs.get("color",'skyblue'))
        ax.set_xlabel(x_label); ax.set_ylabel(y_label)
    elif kind=='hist':
        ax.hist(df['Popularity'], bins=kwargs.get("bins",20), edgecolor='black', color=kwargs.get("color",'lightgreen'))
        ax.set_xlabel(x_label); ax.set_ylabel(y_label)
    elif kind=='box':
        ax.boxplot(df['Popularity'], vert=False, patch_artist=True, boxprops=dict(facecolor='skyblue'))
        ax.set_xlabel(y_label)
    elif kind=='scatter':
        ax.scatter(df['Distribution'], df['Popularity'], color='blue')
        ax.set_xlabel(x_label); ax.set_ylabel(y_label)
    ax.set_title(title)
    plt.tight_layout()
    return fig

with tab1:
    st.header("Distribution Rankings")
    ranked = filtered.reset_index(drop=True)
    ranked.index = ranked.index + 1
    st.dataframe(ranked, use_container_width=True, hide_index=False)

with tab2:
    if not filtered.empty:
        prefix = f"{display_mode} Distributions"
        fig = plot_chart('pie', filtered, title=f"{prefix} — Share of Total Members", figsize=(8,8))
        st.pyplot(fig)
        fig = plot_chart('barh', filtered, title=f"{prefix} — Subscriber Counts", x_label="Number of Members", y_label="Linux Distributions")
        st.pyplot(fig)
        fig = plot_chart('hist', filtered, title=f"{prefix} — Member Count Distribution", x_label="Number of Members", y_label="Frequency", bins=20)
        st.pyplot(fig)
        fig = plot_chart('box', filtered, title=f"{prefix} — Popularity Box Plot", y_label="Popularity")
        st.pyplot(fig)
        fig = plot_chart('scatter', filtered, title=f"{prefix} — Scatter of Popularity", x_label="Linux Distributions", y_label="Popularity")
        st.pyplot(fig)
    else:
        st.write("No data available for the current filters.")

with tab3:
    st.header("Key Insights")
    st.subheader("Distribution Concentration")
    st.markdown("""
    The top 13 distributions (10% of all listed distributions) account for nearly 80% of users. This aligns very well with the Pareto Principle.
    """)
    st.subheader("Major Distributions")
    st.markdown("""
    All of these (top 13) distributions have 30,000+ subreddit members. The distributions in this list are:
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
    - NixOS
    - OpenSUSE
    - Gentoo
    
    The top 10 distributions, though, have 46,000+ subreddit members. The top 9 have 73,000+, the top 8 have 83,000+, and the top 2 have 250,000+. The topmost distribution (archlinux) has 300,000+ subreddit members.

    There are some distributions excluded by default (in ALL type). These are "technically" called Linux distributions but are not for general purpose use and people don't refer to them when they're talking about Linux on the "desktop". For example, Proxmox is a server, True NAS and Open Media Vault are NAS's and Batocera is a retro gaming emulator. You can choose to include these if you want but my point still stands.
    """)
    st.subheader("Parent Distributions")
    st.markdown("""
    Among these, 5 distributions serve as the parent distribution for all others, these are:
    
    - Arch Linux
    - Debian
    - Fedora
    - NixOS
    - SUSE Linux
    - Gentoo

    If we consider only the top 10 list, all of them use either Arch Linux, Debian or Fedora as their parent distribution. This means 74% of users use these 3 as their parent distributions.
    """)
    st.subheader("Desktop Environment Usage")
    st.markdown("""
    There are 26 distributions with more than 10,000 members (which I think is the minimum to call a subreddit serious) in their subreddits. Out of these 26 distributions:
    
    ###### GNOME is used by:
    - CentOS
    - Debian
    - Fedora
    - NixOS
    - RHEL
    - Tails
    - Ubuntu
    - Zorin

    ###### KDE Plasma is used by:
    - Asahi Linux
    - Bazzite
    - Kubuntu
    - NobaraProject
    - OpenSUSE
    - SteamOS
    
    ###### Xfce is used by:
    - EndeavourOS
    - Kali Linux
    - Manjaro Linux
    - Qubes OS
    - Void Linux
    - Whonix
    
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

    ###### Usage Distribution:
    - **GNOME**: 8/26
    - **KDE Plasma**: 6/26
    - **Xfce**: 6/26
    - **None**: 2/26
    - **Cinnamon**: 1/26
    - **COSMIC**: 1/26
    - **Pantheon**: 1/26
    - **Budgie**: 1/26


    This clearly shows the "tripoly" of GNOME, KDE and Xfce with duopoly of GTK and QT toolkits.
    """)
    st.subheader("Conclusion and Opinion")
    st.markdown("""
    Linux Fragmentation is really overblown for no (good) reason. The overwhelming number of distros and desktops creates a paradox of choice for new users.

    Most people that ever use Linux (seriously) only either use **Arch, Debian or Fedora** with **GNOME, KDE or Xfce**.

    Derivative distros these days are just changing themes and calling it a new operating system (with exceptions like Linux Mint with Cinnamon DE).
    
    Use FAD (Fedora, Arch, Debian) with KNOX (Kde, gNOme, Xfce) [atleast as your parent distribution] - This should be the default mantra for beginners as it simplifies their Linux journey to a great extent.
    """)
