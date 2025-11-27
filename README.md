# gsi2zip-project
A universal tool that converts **any GSI (Generic System Image)** into a **flashable ZIP** for dynamic-partition Android devices.

This project is designed so **everyone** can convert any GSI easily — whether you’re on **Linux**, **Windows (native)**, or **Windows using WSL**.

---

## 🚀 Features
- Convert **raw**, **sparse**, **xz**, **gz** `.img` files  
- Supports **Linux**, **Windows native**, and **Windows WSL**  
- Auto-detects best mode (native/WSL/Linux)  
- Converts:
  - `system.img` → `system.img.raw`
  - `system.img.raw` → `system.new.dat`
  - `system.new.dat` → `system.new.dat.br`
- Automatically fixes:
  - dynamic partitions raw size  
  - updater-script GSI filename  
  - Python 3.13 `imp` removal (patches img2sdat automatically)  
- Handles Brotli compression (Python or external binary)  
- Avoids 10GB ZIP issue by cleaning leftover files  
- Creates a **flashable ZIP** compatible with most custom recoveries  
- Optimized to prevent “no space left on device” errors  

---

## 🖥 Supported Platforms
### ✔ Linux
Full support with native simg tools.

### ✔ Windows (WSL)
Best and most stable mode.  
Requires WSL + Ubuntu + simg tools installed.

### ✔ Windows Native (no WSL)
Requires Windows builds of:
- `img2simg.exe`
- `simg2img.exe`

_(If not present, tool will fallback to WSL automatically.)_

---

## 📦 Requirements

### Linux / WSL
Install required tools:

```bash
sudo apt update
sudo apt install android-sdk-libsparse-utils python3-pip brotli
