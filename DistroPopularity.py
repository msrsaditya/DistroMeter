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

distributions = ["chromeos", "archlinux", "Ubuntu", "Proxmox", "linuxmint", "Fedora", "Kalilinux", "tails", "debian", "pop_os", "ManjaroLinux", "truenas", "redhat", "NixOS", "openSUSE", "SteamOS", "Gentoo", "batocera", "EndeavourOS", "OpenMediaVault", "elementaryos", "Bazzite", "cachyos", "voidlinux", "Qubes", "CentOS", "Kubuntu", "AsahiLinux", "NobaraProject", "zorinos", "SolusProject", "Whonix", "RockyLinux", "MXLinux", "linuxfromscratch", "GarudaLinux", "AlmaLinux", "kdeneon", "3CX", "Lubuntu", "xubuntu", "recalbox", "slackware", "tuxedocomputers", "AlpineLinux", "ParrotOS", "libreELEC", "archcraft", "UbuntuMATE", "artixlinux", "GUIX", "deepin", "vyos", "Lakka", "dietpi", "Freedombox", "bedrocklinux", "CrunchBang", "BlackArchOfficial", "holoiso", "puppylinux", "crunchbangplusplus", "ArcoLinux", "vanillaos", "antergos", "raspbian", "devuan", "kisslinux", "BunsenLabs", "trisquel", "antiXLinux", "PeppermintOS", "UbuntuBudgie", "chimeralinux", "bodhilinux", "PikaOS", "Mageia", "Parabola", "RedStarOS", "yunohost", "windowmaker", "Armbian", "LinuxLite", "FerenOS", "ipfire", "tinycorelinux", "OfficialArchLabsLinux", "BlendOS", "UbuntuUnity", "Q4OS", "ubuntucinnamon", "rebornos", "rhinolinux", "OpenMandriva", "TurnkeyLinux", "OracleLinux", "regata_os", "ultramarine", "geckolinux", "sabayon", "MaboxLinux", "t2sde", "pureos", "RockStor", "Kicksecure", "BackBox", "archbang", "kinoite", "cruxlinux", "NethServer", "endlessos", "SpiralLinux", "exherbo", "obarun", "siduction", "SparkyLinuxOrg", "SliTaz", "kodachilinux", "solydxk", "zentyal", "AVLinux", "venomlinux", "AltLinux", "AnarchyLinux", "UbuntuKylin", "scientificlinux", "RedCore", "EliveLinux", "risiOS", "kaos", "rlxos_dev", "openKylin", "Linspire"]

popularity = [573995, 329105, 261270, 166766, 154710, 145379, 126753, 120877, 118254, 88445, 75502, 70146, 49982, 45421, 41763, 39164, 34809, 28479, 27345, 25577, 24118, 21455, 20922, 18123, 17674, 16802, 16714, 15346, 13899, 12420, 11576, 10845, 10149, 9299, 8472, 7592, 7502, 7099, 7064, 6864, 6576, 6314, 6107, 5986, 5931, 5060, 4655, 4428, 4380, 4341, 4188, 3814, 3265, 3248, 2763, 2128, 2039, 2039, 1973, 1931, 1867, 1651, 1633, 1588, 1415, 1345, 1125, 984, 941, 891, 842, 735, 705, 688, 686, 676, 656, 617, 570, 560, 550, 546, 535, 523, 475, 434, 397, 363, 354, 352, 344, 311, 307, 305, 274, 269, 254, 219, 207, 202, 196, 196, 195, 189, 184, 179, 169, 163, 162, 133, 126, 123, 121, 121, 94, 91, 86, 76, 71, 71, 67, 66, 63, 63, 61, 59, 55, 53, 44, 42, 40, 34, 17]

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
