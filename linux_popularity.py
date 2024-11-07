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

# Page configuration
st.set_page_config(page_title="Linux Distributions' Popularity")
st.title("Linux Distributions' Popularity")

# Sidebar controls
st.sidebar.title("Explore Linux Distributions")
ALL_OPTION = "ALL"
selected_distributions = st.sidebar.multiselect("Select Distributions to Display", [ALL_OPTION] + distributions, default=[ALL_OPTION])
excluded_distributions = st.sidebar.multiselect("Exclude Distributions", distributions)
min_members = st.sidebar.number_input("Minimum Popularity", min_value=0, step=1, value=0)

# Filter distributions based on selection
if ALL_OPTION in selected_distributions:
    selected_distributions = [d for d in distributions if d not in excluded_distributions and popularity[distributions.index(d)] >= min_members]
else:
    selected_distributions = [d for d in selected_distributions if d != ALL_OPTION and d not in excluded_distributions and popularity[distributions.index(d)] >= min_members]

# Create DataFrame and display ranking
data = pd.DataFrame({'Distribution': distributions, 'Popularity': popularity})
data = data.sort_values(by='Popularity', ascending=False)
st.header("Ranking")
st.dataframe(data[['Distribution', 'Popularity']][data['Distribution'].isin(selected_distributions)], use_container_width=True)

# Create visualizations
selected_popularity = [popularity[distributions.index(d)] for d in selected_distributions]

# Pie chart
fig_pie, ax_pie = plt.subplots(figsize=(10, 10))
ax_pie.pie(selected_popularity, labels=selected_distributions, autopct='%1.1f%%', startangle=140)
ax_pie.axis('equal')
ax_pie.set_title('Distribution of Popularity Among Selected Distributions')
plt.tight_layout()
st.pyplot(fig_pie)

# Horizontal bar chart
fig_bar, ax_bar = plt.subplots(figsize=(12, 8))
ax_bar.barh(selected_distributions, selected_popularity, color='skyblue')
ax_bar.set_xlabel('Popularity')
ax_bar.set_ylabel('Linux Distributions')
ax_bar.set_title('Popularity of Selected Linux Distributions')
plt.tight_layout()
st.pyplot(fig_bar)

# Histogram
fig_hist, ax_hist = plt.subplots(figsize=(10, 6))
ax_hist.hist(selected_popularity, bins=20, color='lightgreen', edgecolor='black')
ax_hist.set_xlabel('Popularity')
ax_hist.set_ylabel('Frequency')
ax_hist.set_title('Distribution of Popularity Scores for Selected Distributions')
plt.tight_layout()
st.pyplot(fig_hist)
