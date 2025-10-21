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
        <div class="last-updated">Last Updated ⚡ Oct 21st, 2025</div>
    </div>
""", unsafe_allow_html=True)

distributions = ["chromeos", "archlinux", "Ubuntu", "Proxmox", "linuxmint", "Fedora", "Kalilinux", "tails", "debian", "pop_os", "ManjaroLinux", "truenas", "redhat", "NixOS", "openSUSE", "SteamOS", "Gentoo", "batocera", "EndeavourOS", "OpenMediaVault", "elementaryos", "Bazzite", "cachyos", "voidlinux", "Qubes", "Kubuntu", "CentOS", "AsahiLinux", "NobaraProject", "zorinos", "SolusProject", "Whonix", "RockyLinux", "MXLinux", "linuxfromscratch", "GarudaLinux", "AlmaLinux", "kdeneon", "3CX", "Lubuntu", "xubuntu", "recalbox", "slackware", "tuxedocomputers", "AlpineLinux", "ParrotOS", "libreELEC", "archcraft", "UbuntuMATE", "artixlinux", "GUIX", "deepin", "vyos", "Lakka", "dietpi", "Freedombox", "bedrocklinux", "CrunchBang", "BlackArchOfficial", "holoiso", "puppylinux", "crunchbangplusplus", "ArcoLinux", "vanillaos", "antergos", "raspbian", "devuan", "kisslinux", "BunsenLabs", "trisquel", "antiXLinux", "PeppermintOS", "UbuntuBudgie", "PikaOS", "chimeralinux", "bodhilinux", "Mageia", "Parabola", "RedStarOS", "yunohost", "windowmaker", "Armbian", "LinuxLite", "FerenOS", "ipfire", "tinycorelinux", "OfficialArchLabsLinux", "BlendOS", "instantos", "UbuntuUnity", "Q4OS", "ubuntucinnamon", "OpenMandriva", "rebornos", "rhinolinux", "TurnkeyLinux", "OracleLinux", "regata_os", "ultramarine", "geckolinux", "sabayon", "MaboxLinux", "pureos", "t2sde", "RockStor", "Kicksecure", "BackBox", "archbang", "cruxlinux", "kinoite", "NethServer", "endlessos", "exherbo", "obarun", "SpiralLinux", "siduction", "SparkyLinuxOrg", "SliTaz", "Crystal_Linux", "kodachilinux", "solydxk", "zentyal", "AVLinux", "venomlinux", "AltLinux", "AnarchyLinux", "UbuntuKylin", "scientificlinux", "RedCore", "EliveLinux", "risiOS", "kaos", "rlxos_dev", "openKylin", "Linspire"]

popularity = [574054, 330260, 262039, 167638, 156100, 146228, 127014, 121050, 118914, 88825, 75586, 70681, 50156, 45689, 41856, 39684, 35016, 28717, 27549, 25625, 24146, 22032, 21826, 18192, 17697, 16837, 16808, 15429, 14021, 12821, 11581, 10863, 10169, 9334, 8866, 7625, 7515, 7127, 7100, 6903, 6658, 6322, 6126, 6022, 6011, 5062, 4659, 4430, 4391, 4371, 4198, 3818, 3274, 3247, 2772, 2128, 2041, 2041, 1985, 1933, 1880, 1658, 1632, 1594, 1415, 1346, 1128, 985, 942, 892, 846, 739, 710, 703, 696, 690, 659, 619, 570, 560, 554, 546, 535, 524, 478, 434, 397, 366, 359, 357, 353, 348, 312, 311, 310, 274, 270, 255, 218, 206, 202, 197, 197, 196, 189, 188, 180, 170, 164, 161, 133, 126, 122, 122, 122, 94, 94, 85, 77, 76, 71, 71, 67, 66, 64, 64, 62, 59, 56, 54, 44, 43, 41, 35, 17]

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
    The top 10 distributions (7.5% of all listed distributions) account for nearly 80% of users. This aligns very well with the Pareto Principle (more so than the actual principle TBF)
    """)
    st.subheader("Major Distributions")
    st.markdown("""
    All of these (top 10) distributions have 50,000+ subreddit members. The distributions in this list are:
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
    
    The top 9 distributions, though, have 75,000+, the top 8 have 88,000+, and the top 2 have 260,000+. The topmost distribution (archlinux) has 330,000+ subreddit members.

    There are some distributions excluded by default (in ALL type). These are "technically" called Linux distributions but are not for general purpose use and people don't refer to them when they're talking about Linux on the "desktop". For example, Proxmox is a server, True NAS and Open Media Vault are NAS's and Batocera is a retro gaming emulator. You can choose to include these if you want but my point still stands.
    """)
    st.subheader("Parent Distributions")
    st.markdown("""
    Among these, 3 distributions serve as the parent distribution for all others, these are:
    
    - Arch Linux
    - Debian
    - Fedora

    This means >80% of users use these 3 as their parent distributions.
    """)
    st.subheader("Desktop Environment Usage")
    st.markdown("""
    There are 28 distributions with more than 10,000 members (which I think is the minimum to call a subreddit serious) in their subreddits. Out of these 28 distributions:
    
    ###### GNOME is used by:
    - CentOS
    - Debian
    - Fedora
    - RHEL
    - Rocky Linux
    - Tails
    - Ubuntu
    - Zorin

    ###### KDE Plasma is used by:
    - Asahi Linux
    - Bazzite
    - CachyOS
    - Kubuntu
    - NobaraProject
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

    Note that here, used means either used by default or offered as flagship desktop.

    ###### Usage Distribution:
    - **GNOME**: 8/26
    - **KDE Plasma**: 6/26
    - **Xfce**: 6/26
    - **Cinnamon**: 1/26
    - **COSMIC**: 1/26
    - **Pantheon**: 1/26
    - **Budgie**: 1/26
    - **None**: 1/26

    This clearly shows the "tripoly" of GNOME, KDE and Xfce with duopoly of GTK and QT toolkits. 
    """)
    st.subheader("Conclusion and Opinion")
    st.markdown("""
    Linux Fragmentation is really overblown for no (good) reason. The overwhelming number of distros and desktops creates a paradox of choice for new users.

    Most people that ever use Linux (seriously) only either use **Arch, Debian or Fedora** with **GNOME, KDE or Xfce**.

    Derivative distros these days are just changing themes and calling it a new operating system (with exceptions like Linux Mint with Cinnamon DE).
    
    Use FAD (Fedora, Arch, Debian) with KNOX (Kde, gNOme, Xfce) [atleast as your parent distribution] - This should be the default mantra for beginners as it simplifies their Linux journey to a great extent.
    """)
    
    st.subheader("NOTE")
    st.markdown("""
    All of the distros on distrowatch.com are accounted for here. The distros with no subreddits are listed in the "No Subreddits.txt" file in this project's repo. If there's a distro that's not present in DistroWatch but you wish it to be added here, it won't be, because if a distro is so niche that it's not even listed on DistroWatch, then it's not worth adding.

    This list of distributions is as comprehensive as possible. Every distro's subreddit presence is manually vetted and checked thoroughly, and ONLY when its absence is confirmed on Reddit (no subreddit of it exists) was it included in the "No Subreddits.txt" file.

    Also, some questions arise in users' minds, like how accurate is Reddit's member count for a distro's popularity? If we somehow solved that problem, then another problem that we need to account for no.of subreddits created for a particular distro and then how do we rank order the distros based on this and how many unique and non-overlpapping with these new subreddits accounts are there in each subreddit and how many of them are fake accounts or bots and then we need to account for multiple sources and give weights to how much accurate they are .... ANDDDD it becomes a research project! This is a never-ending thing.

    This does not necessarily reflect the true usage of these Linux distributions, but it can be considered a good, rough, educated "guess."
    
    All opinions expressed here are intended to be taken as such - opinions, and you are free to disregard them if you disagree, although I have endeavored to remain as objective as possible.
    """)
