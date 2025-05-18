#!/bin/bash

distros=(
    "3CX"
    "AlmaLinux"
    "AlpineLinux"
    "AltLinux"
    "AnarchyLinux"
    "antergos"
    "antiXLinux"
    "archbang"
    "archcraft"
    "archlinux"
    "ArcoLinux"
    "Armbian"
    "artixlinux"
    "AsahiLinux"
    "AVLinux"
    "BackBox"
    "batocera"
    "Bazzite"
    "bedrocklinux"
    "BlackArchOfficial"
    "BlendOS"
    "bodhilinux"
    "BunsenLabs"
    "cachyos"
    "CentOS"
    "chimeralinux"
    "chromeos"
    "ClearLinux"
    "CrunchBang"
    "crunchbangplusplus"
    "cruxlinux"
    "debian"
    "deepin"
    "devuan"
    "dietpi"
    "elementaryos"
    "EliveLinux"
    "EndeavourOS"
    "endlessos"
    "exherbo"
    "Fedora"
    "FerenOS"
    "Freedombox"
    "GarudaLinux"
    "geckolinux"
    "Gentoo"
    "GUIX"
    "holoiso"
    "ipfire"
    "kaos"
    "Kalilinux"
    "kdeneon"
    "Kicksecure"
    "kinoite"
    "kisslinux"
    "kodachilinux"
    "Kubuntu"
    "Lakka"
    "Lubuntu"
    "libreELEC"
    "Linspire"
    "linuxfromscratch"
    "LinuxLite"
    "linuxmint"
    "MaboxLinux"
    "Mageia"
    "ManjaroLinux"
    "MXLinux"
    "NethServer"
    "NixOS"
    "NobaraProject"
    "obarun"
    "OfficialArchLabsLinux"
    "openKylin"
    "OpenMandriva"
    "OpenMediaVault"
    "openSUSE"
    "OracleLinux"
    "Parabola"
    "ParrotOS"
    "PeppermintOS"
    "PikaOS"
    "pop_os"
    "Proxmox"
    "puppylinux"
    "pureos"
    "Q4OS"
    "Qubes"
    "raspbian"
    "RedStarOS"
    "rebornos"
    "recalbox"
    "RedCore"
    "redhat"
    "regata_os"
    "rhinolinux"
    "rlxos_dev"
    "risiOS"
    "RockyLinux"
    "RockStor"
    "sabayon"
    "scientificlinux"
    "siduction"
    "slackware"
    "SliTaz"
    "SolusProject"
    "solydxk"
    "SparkyLinuxOrg"
    "SpiralLinux"
    "SteamOS"
    "t2sde"
    "tails"
    "tinycorelinux"
    "trisquel"
    "truenas"
    "TurnkeyLinux"
    "tuxedocomputers"
    "Ubuntu"
    "UbuntuBudgie"
    "ubuntucinnamon"
    "UbuntuKylin"
    "UbuntuMATE"
    "UbuntuUnity"
    "ultramarine"
    "vanillaos"
    "venomlinux"
    "voidlinux"
    "vyos"
    "Whonix"
    "windowmaker"
    "xubuntu"
    "yunohost"
    "zentyal"
    "zorinos"
)

printf "\n"
printf "Fetched "

for distro in "${distros[@]}"; do
    curl -s -o "$distro.html" "https://www.reddit.com/r/$distro/" \
        -H 'authority: www.reddit.com' \
        -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
        -H 'accept-language: en-US,en;q=0.9' \
        -H 'cache-control: max-age=0' \
        -H 'sec-ch-ua: "Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"' \
        -H 'sec-ch-ua-mobile: ?0' \
        -H 'sec-ch-ua-platform: "Windows"' \
        -H 'sec-fetch-dest: document' \
        -H 'sec-fetch-mode: navigate' \
        -H 'sec-fetch-site: none' \
        -H 'sec-fetch-user: ?1' \
        -H 'upgrade-insecure-requests: 1' \
        -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' \
        --compressed
    printf "%s, " "$distro"
done

printf "\n\nPopularity is as Follows:\n\n"

counts=()
for distro in "${distros[@]}"; do
    number=$(grep -m 1 '<faceplate-number number' "$distro.html" | awk -F'"' '{print $2}')
    counts+=("$number")
done

sorted=()
for i in "${!distros[@]}"; do
    sorted+=("${counts[i]}:::${distros[i]}")
done

IFS=$'\n'
sorted=($(printf "%s\n" "${sorted[@]}" | sort -t: -k1,1nr))
unset IFS

sorted_distros=()
sorted_counts=()
for entry in "${sorted[@]}"; do
    count=${entry%%::*}
    distro=${entry##*:::}
    sorted_counts+=("$count")
    sorted_distros+=("$distro")
done

printf "distributions=["
for i in "${!sorted_distros[@]}"; do
    printf "\"%s\"" "${sorted_distros[i]}"
    if [ $i -lt $(( ${#sorted_distros[@]} - 1 )) ]; then
        printf ", "
    fi
done
printf "]\n"

printf "popularity=["
for i in "${!sorted_counts[@]}"; do
    printf "%s" "${sorted_counts[i]}"
    if [ $i -lt $(( ${#sorted_counts[@]} - 1 )) ]; then
        printf ", "
    fi
done
printf "]\n\n"

rm -rf *.html
