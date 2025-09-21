<h1 align="center">🔎 SkyHawk – Network & Port Scanner</h1>

<p align="center">
  <b>SkyHawk</b> is a powerful and lightweight tool for discovering devices and scanning open ports in local networks.  
  Built with Python, it provides fast multi-threaded scanning, detailed service detection, and optional web service verification.  
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20Windows-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/status-active-success" alt="Status">
</p>

---

## 📌 Overview

SkyHawk is designed for **network administrators, penetration testers, and security researchers** to quickly map devices and identify open services within a given network range.    

⚠️ **Disclaimer:** Use this tool **only** on networks you own or have explicit permission to test. The author assumes **no liability** for misuse.

---

## ✨ Features

- 🚀 **Fast Multi-threaded Scanning** – Efficient port checks with configurable threading.  
- 🌐 **Device Discovery** – ARP-based network scanning with hostname & MAC address resolution.  
- 🔍 **Service Mapping** – Maps ports to protocols/services using `ports.py`.  
- 🌎 **Web Service Verification** – Automatically detects HTTP/HTTPS responses & status codes.  
- 🎨 **Colorful CLI Output** – Clear and structured output with `colorama`.  
- 📝 **Logging Support** – Results are saved to `scan_results.log`.  
- 🔒 **Cross-Platform Support** – Works on Linux (root required) and Windows (admin required).  

---

## 📂 Project Structure

