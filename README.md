                                                                                                                                                        
                                                                                                                                                        
                                      ,----,                                                                                                    ___     
                         ,--,       .'   .' \              ,--,   ,-.----.          ,-.----.                                                  ,--.'|_   
                       ,--.'|     ,----,'    |     ,----,,--.'|   \    /  \         \    /  \   __  ,-.   ,---.      .--.                     |  | :,'  
  ,----._,.  .--.--.   |  |,      |    :  .  ;   .'   .`||  |,    |   :    |        |   :    |,' ,'/ /|  '   ,'\   .--,`|                     :  : ' :  
 /   /  ' / /  /    '  `--'_      ;    |.'  / .'   .'  .'`--'_    |   | .\ :        |   | .\ :'  | |' | /   /   |  |  |.    ,---.     ,---. .;__,'  /   
|   :     ||  :  /`./  ,' ,'|     `----'/  ;,---, '   ./ ,' ,'|   .   : |: |        .   : |: ||  |   ,'.   ; ,. :  '--`_   /     \   /     \|  |   |    
|   | .\  .|  :  ;_    '  | |       /  ;  / ;   | .'  /  '  | |   |   |  \ :        |   |  \ :'  :  /  '   | |: :  ,--,'| /    /  | /    / ':__,'| :    
.   ; ';  | \  \    `. |  | :      ;  /  /-,`---' /  ;--,|  | :   |   : .  |        |   : .  ||  | '   '   | .; :  |  | '.    ' / |.    ' /   '  : |__  
'   .   . |  `----.   \'  : |__   /  /  /.`|  /  /  / .`|'  : |__ :     |`-'        :     |`-';  : |   |   :    |  :  | |'   ;   /|'   ; :__  |  | '.'| 
 `---`-'| | /  /`--'  /|  | '.'|./__;      :./__;     .' |  | '.'|:   : :           :   : :   |  , ;    \   \  / __|  : ''   |  / |'   | '.'| ;  :    ; 
 .'__/\_: |'--'.     / ;  :    ;|   :    .' ;   |  .'    ;  :    ;|   | :           |   | :    ---'      `----'.'__/\_: ||   :    ||   :    : |  ,   /  
 |   :    :  `--'---'  |  ,   / ;   | .'    `---'        |  ,   / `---'.|           `---'.|                    |   :    : \   \  /  \   \  /   ---`-'   
  \   \  /              ---`-'  `---'                     ---`-'    `---`             `---`                     \   \  /   `----'    `----'             
   `--`-'                                                                                                        `--`-'                                 


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
| **WSL (Ubuntu)** | 🟢 Best | Easiest & most stable |
| **Windows Native** | 🟡 OK | Requires `.exe` simg tools |

---

## 📦 Installation

### Linux / WSL
```bash
sudo apt update
sudo apt install android-sdk-libsparse-utils brotli python3-pip
```

### Windows Native
Letak dalam folder `simg/`:
```
img2simg.exe
simg2img.exe
```

---

## 🚀 Usage

### Auto Mode (Recommended)
```bash
python convert.py system.img
```

### Force Mode
```bash
python convert.py system.img --mode windows
python convert.py system.img --mode wsl
python3 convert.py system.img --mode linux
```

---

## ⚠ Important Notes
- Flash ZIP using **TWRP / OFOX / Custom Recovery**
- Device must support **Project Treble + Dynamic Partitions (A/B)**
- Some GSIs need patched **vbmeta**
- JoyUI / MIUI GSI sometimes require extra vendor patches

---

## 🧰 Troubleshooting

### Missing `system.img.raw`
Install simg tools:
```bash
sudo apt install android-sdk-libsparse-utils
```

### ZIP becomes 10GB
This version automatically cleans raw images.

### Python error: `imp module not found`
Script auto-fixes img2sdat.

### WSL error: “command not found” (exit 127)
Install tools inside WSL.

---

## 🤝 Contributions

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Orbitron&size=22&duration=3000&color=FF74F7&center=true&vCenter=true&width=850&lines=This+project+is+still+early-stage...;I'm+still+learning!;Your+feedback+helps+me+grow!;Pull+Requests+are+Highly+Appreciated!" />
</p>

---

## ❤️ Credits
- Community GSI tools (inspiration)
- Full rewrite & cross-platform system by **hakimz07**
- Script logic & debugging improved with ChatGPT
- Everyone who tests & contributes!

---

## ⭐ Support the Project
If this tool helps you, please ⭐ the repo ✨

<p align="center">
  <a href="https://github.com/hakimz07/gsi2zip-project">
    <img src="https://img.shields.io/github/stars/hakimz07/gsi2zip-project?style=social" width="150">
  </a>
</p>
