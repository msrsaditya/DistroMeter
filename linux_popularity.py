import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

distributions = [
    "ChromeOS", "Arch Linux", "Ubuntu", "Tails", "Fedora", 
    "Kali Linux", "Linux Mint", "Debian", "Pop!_OS", "Manjaro Linux",
    "Red Hat", "openSUSE", "Gentoo", "NixOS", "elementary OS", 
    "SteamOS", "CentOS", "Qubes OS", "Void Linux", "EndeavourOS", 
    "Kubuntu", "Solus Project", "Whonix", "Asahi Linux", "Rocky Linux",
    "Zorin OS", "MX Linux", "KDE neon", "Linux from Scratch", 
    "Nobara Project", "Lubuntu", "AlmaLinux", "Xubuntu", "Garuda Linux",
    "Slackware", "Parrot OS", "deepin", "Alpine Linux", "Guix",
    "CrunchBang", "Bedrock Linux", "HoloISO", "ArcoLinux", "Antergos",
    "CrunchBangplusplus", "Puppy Linux", "Raspbian", "BlackArch Official",
    "Clear Linux", "VanillaOS", "KISS Linux", "CachyOS", "Peppermint OS",
    "Mageia", "Parabola", "antiX Linux", "Bodhi Linux", "Feren OS",
    "Linux Lite", "Official Arch Labs Linux", "RedStar OS", "Tiny Core Linux",
    "GeckoLinux", "Sabayon", "Q4OS", "RhinoLinux", "BackBox", "ArchBang",
    "Oracle Linux", "OpenMandriva", "Crux Linux", "Exherbo", "Kinoite",
    "Scientific Linux", "Venom Linux", "Anarchy Linux", "RLXOS Dev",
    "KaOS", "Alt Linux"
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

st.set_page_config(page_title="Linux Distributions' Popularity")
st.title("Linux Distributions' Popularity")

st.sidebar.title("Explore Linux Distributions")
all_option = "ALL"
exclude_option = "Exclude"
selected_distributions = st.sidebar.multiselect("Select distributions to display", [all_option] + distributions, default=[all_option])
excluded_distributions = st.sidebar.multiselect("Exclude distributions", distributions, default=[])
sort_by = st.sidebar.selectbox("Sort by", ["Popularity", "Alphabetical"])

if all_option in selected_distributions:
    selected_distributions = [d for d in distributions if d not in excluded_distributions]
else:
    selected_distributions = [d for d in selected_distributions if d != all_option and d not in excluded_distributions]

fig1, ax1 = plt.subplots(figsize=(12, 8))
ax1.barh(selected_distributions, [popularity[distributions.index(d)] for d in selected_distributions], color='skyblue')
ax1.set_xlabel('Popularity')
ax1.set_ylabel('Linux Distributions')
ax1.set_title('Popularity of Selected Linux Distributions')
plt.tight_layout()
st.pyplot(fig1)

fig2, ax2 = plt.subplots(figsize=(10, 10))
ax2.pie([popularity[distributions.index(d)] for d in selected_distributions], labels=selected_distributions, autopct='%1.1f%%', startangle=140)
ax2.axis('equal')
ax2.set_title('Distribution of Popularity Among Selected Distributions')
plt.tight_layout()
st.pyplot(fig2)

fig3, ax3 = plt.subplots(figsize=(10, 6))
ax3.hist([popularity[distributions.index(d)] for d in selected_distributions], bins=20, color='lightgreen', edgecolor='black')
ax3.set_xlabel('Popularity')
ax3.set_ylabel('Frequency')
ax3.set_title('Distribution of Popularity Scores for Selected Distributions')
plt.tight_layout()
st.pyplot(fig3)

data = pd.DataFrame({'Distribution': distributions, 'Popularity': popularity})
if sort_by == "Popularity":
    data = data.sort_values(by='Popularity', ascending=False)
else:
    data = data.sort_values(by='Distribution')

st.header("Ranking of Linux Distributions")
st.dataframe(data[['Distribution', 'Popularity']][data['Distribution'].isin(selected_distributions)], use_container_width=True)
