⚡ gsi2zip-project ⚡                                                                                                                                            


<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Orbitron&size=27&duration=2800&color=00F7FF&center=true&vCenter=true&width=750&lines=gsi2zip-project+by+KimTrixx07;Convert+ANY+GSI+into+Flashable+ZIP;Supports+Windows%2C+WSL%2C+Linux;Project+Still+Early+Stage;Feedback+and+Contributions+Welcome!" />
</p>

---

<p align="center">
  <img src="https://img.shields.io/github/stars/hakimz07/gsi2zip-project?style=for-the-badge&color=yellow">
  <img src="https://img.shields.io/badge/Version-1.0.0-purple?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-Early%20Stage-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Python-3.9%2B-00d7ff?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Platforms-Windows%20%7C%20WSL%20%7C%20Linux-00ff88?style=for-the-badge">
</p>

---

# ⚡ gsi2zip-project

A universal, cross-platform conversion tool that transforms **ANY GSI** into a **flashable ZIP** for Android dynamic-partition devices.

This project is still in **early stage** — I am still learning,  
so **any feedback, suggestions, criticism, or pull requests are highly appreciated.**

---

## ✨ Features

```
| ✔ Convert RAW / SPARSE / XZ / GZ images     │
│ ✔ Auto-detect GSI format                    │
│ ✔ 3 modes: Windows Native, WSL, Linux       │
│ ✔ RAW → SPARSE → DAT → BR transformation    │
│ ✔ Auto-fix updater-script & op_list         │
│ ✔ Auto patch Python3.13 img2sdat issues     │
│ ✔ Prevents 10GB ZIP bug                     │
│ ✔ Cleans all leftover files automatically   │
```

---

## 🖥 Platform Support

| Platform        | Status | Notes |
|----------------|--------|-------|
| **Linux**      | 🟢 Full | Native tools recommended |
| **WSL (Ubuntu)** | 🟢 Best/Partially | Easiest & most stable |
| **Windows Native** | 🟡 Unsupported Yet | Requires `.exe` simg tools |

---

## Notice

Currently this script only working fine in linux environtment...
so if u dont have linux on u machine..u need to figure it out
unless...you like to thinker around in windows...

Good News...We are currently working for the windows app
## 📦 Installation

### Linux / WSL
```bash
sudo apt update
sudo apt install android-sdk-libsparse-utils brotli python3-pip
```
---

## 🚀 Usage

### Auto Mode (Recommended)
```bash
python convert.py system.img
```

## ⚠ Important Notes
- Flash ZIP using **TWRP / OFOX / Custom Recovery**
- Device must support **Project Treble + Dynamic Partitions (A/B)**
- Some GSIs need patched **vbmeta**
- JoyUI / MIUI GSI sometimes require extra vendor patches

---

## 🧰 Troubleshooting

### ZIP becomes 10GB
This version automatically cleans raw images.

### WSL error: “command not found” (exit 127)
Install tools inside WSL.

---

## 🤝 Contributions

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Orbitron&size=22&duration=3000&color=FF74F7&center=true&vCenter=true&width=850&lines=This+project+is+still+early-stage...;I'm+still+learning!;Your+feedback+helps+me+grow!;Pull+Requests+are+Highly+Appreciated!" />
</p>

---

## ❤️ Credits
- Community GSI tools (inspiration) thanks to notmyst33d
- Full rewrite & cross-platform system by **Kimtrixx**
- Script logic & debugging improved with A.I
- Everyone Open to tests & contributes!

---

## ⭐ Support the Project
If this tool helps you, please ⭐ the repo ✨

<p align="center">
  <a href="https://github.com/hakimz07/gsi2zip-project">
    <img src="https://img.shields.io/github/stars/hakimz07/gsi2zip-project?style=social" width="150">
  </a>
</p>
