#!/usr/bin/env python3
"""
convert_allmodes.py
Universal GSI -> flashable ZIP converter (Linux / Windows native / Windows via WSL)

Place this in the root of the gsi2zip repo (alongside template_arm64/, simg/, img2sdat/).
Requirements (varies by mode):
 - Python 3.8+
 - If using Linux or WSL: simg/img2simg & simg/simg2img binaries (linux build)
 - If using Windows native: simg/*.exe Windows builds for img2simg & simg2img
 - img2sdat/ folder (img2sdat.py and helpers)
 - Optional: brotli Python package (pip install brotli) OR external 'brotli' binary

Usage:
  python convert_allmodes.py /path/to/system.img [--mode windows|wsl|linux] [--arch arm64]
"""
import os, sys, shutil, tempfile, subprocess, struct, argparse, time
from pathlib import Path

# -- configuration
DEFAULT_ARCH = "arm64"
WORK_BASE = Path.cwd() / "tmp"  # avoid /tmp tmpfs issues
os.makedirs(WORK_BASE, exist_ok=True)

# ---------- helpers ----------
def is_exe(path):
    return Path(path).is_file() and os.access(path, os.X_OK)

def exe_name(name):
    return name + (".exe" if os.name == "nt" else "")

def find_simg_tools(mode):
    """
    Return paths for (img2simg, simg2img) according to mode:
    - mode == 'native' -> look in ./simg/*.exe or ./simg/* (platform)
    - mode == 'wsl' -> use wsl paths (we will call via 'wsl' command)
    """
    base = Path.cwd() / "simg"
    img2simg = base / exe_name("img2simg")
    simg2img = base / exe_name("simg2img")
    if is_exe(img2simg) and is_exe(simg2img):
        return str(img2simg), str(simg2img)
    return None, None

def detect_gsi_format(path):
    """Header-based detection: returns 'sparse'|'raw'|'xz'|'gz'"""
    with open(path, "rb") as f:
        h = f.read(16)
    if h.startswith(b'\xfd7zXZ\x00'):
        return "xz"
    if h.startswith(b'\x1f\x8b'):
        return "gz"
    if h.startswith(b'\x3a\xff\x26\xed'):
        return "sparse"
    # check ext magic at 1080
    try:
        with open(path, "rb") as f:
            f.seek(1080)
            s = f.read(2)
            if s == struct.pack("<H", 0xEF53):
                return "raw"
    except Exception:
        pass
    return "raw"

def run(cmd, check=True, shell=False):
    """Run command (list or str). Return CompletedProcess."""
    if isinstance(cmd, str) and not shell:
        cmd = cmd.split()
    try:
        cp = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
    except FileNotFoundError as e:
        return None
    if check and cp.returncode != 0:
        return cp
    return cp

def try_wsl_available():
    """Return True if wsl command exists and WSL is usable."""
    res = run(["wsl", "--version"], check=False)
    return res is not None and res.returncode == 0

def patch_img2sdat_imp(img2sdat_dir):
    """Fix `import imp` -> `import importlib as imp` inside img2sdat python files (in-place backup)"""
    patched = False
    for p in Path(img2sdat_dir).glob("*.py"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        if "import imp" in text:
            backup = p.with_suffix(p.suffix + ".bak")
            if not backup.exists():
                backup.write_bytes(p.read_bytes())
            text2 = text.replace("import imp", "import importlib as imp")
            p.write_text(text2, encoding="utf-8")
            patched = True
    return patched

def compress_brotli_py(src_path, out_path):
    try:
        import brotli
    except Exception:
        return False
    data = Path(src_path).read_bytes()
    comp = brotli.compress(data, quality=11)
    Path(out_path).write_bytes(comp)
    return True

# ---------- main conversion ----------
def convert(gsi_input, arch=DEFAULT_ARCH, forced_mode=None):
    # sanity
    gsi_input = Path(gsi_input).expanduser().resolve()
    if not gsi_input.exists():
        print("[-] Input file not found:", gsi_input)
        return None

    # create work dir
    gsi_dir = Path(tempfile.mkdtemp(dir=WORK_BASE))
    print("[+] Work dir:", gsi_dir)
    shutil.copy2(str(gsi_input), str(gsi_dir / gsi_input.name))
    gsi_file = gsi_input.name
    full_gsi = gsi_dir / gsi_file

    # detect
    fmt = detect_gsi_format(str(full_gsi))
    print("[+] Detected format:", fmt)

    # copy template
    template_src = Path.cwd() / f"template_{arch}"
    if not template_src.exists():
        print("[-] Missing template folder:", template_src)
        return None
    shutil.copytree(template_src, gsi_dir / "template")
    template_dir = gsi_dir / "template"

    # decompress if needed
    if fmt == "xz":
        print("[+] Decompressing XZ with python lzma")
        import lzma
        out = full_gsi.with_suffix("")  # remove .xz
        with lzma.open(full_gsi) as fin, open(out, "wb") as fout:
            shutil.copyfileobj(fin, fout)
        full_gsi = out
        gsi_file = full_gsi.name
        fmt = detect_gsi_format(str(full_gsi))
    elif fmt == "gz":
        print("[+] Decompressing GZ with python gzip")
        import gzip
        out = full_gsi.with_suffix("")  # remove .gz
        with gzip.open(full_gsi, "rb") as fin, open(out, "wb") as fout:
            shutil.copyfileobj(fin, fout)
        full_gsi = out
        gsi_file = full_gsi.name
        fmt = detect_gsi_format(str(full_gsi))

    # choose mode
    mode = None
    if forced_mode:
        if forced_mode.lower() in ("windows", "native"):
            mode = "native"
        elif forced_mode.lower() == "wsl":
            mode = "wsl"
        elif forced_mode.lower() == "linux":
            mode = "linux"
    else:
        # auto: prefer native if tools exist, else wsl if available, else linux
        img2simg_native, simg2img_native = find_simg_tools(None)
        if img2simg_native and simg2img_native:
            mode = "native"
        elif try_wsl_available():
            mode = "wsl"
        else:
            mode = "linux"

    print("[+] Chosen mode:", mode)

    # prepare img2sdat patch
    img2sdat_dir = Path.cwd() / "img2sdat"
    if img2sdat_dir.exists():
        patched = patch_img2sdat_imp(img2sdat_dir)
        if patched:
            print("[+] Patched img2sdat files for Python3 importlib compatibility (backups have .bak)")

    # If format is raw => convert raw -> sparse (img2simg)
    if fmt == "raw":
        print("[+] RAW image detected — converting to sparse (img2simg required)")
        raw_src = full_gsi
        sparse_dst = gsi_dir / gsi_file
        # if native mode and binary present:
        img2simg, simg2img = find_simg_tools(mode)
        if mode == "native" and img2simg:
            print("[+] Using native img2simg:", img2simg)
            cp = run([img2simg, str(raw_src), str(sparse_dst)], check=False)
            if cp is None or cp.returncode != 0:
                print("[-] img2simg failed natively. Return code:", None if cp is None else cp.returncode)
                # fallback to WSL if available
                if try_wsl_available():
                    mode = "wsl"
                else:
                    print("[-] No fallback available. Provide img2simg executable (Windows build) or use WSL.")
                    return None
        if mode == "wsl":
            print("[+] Using WSL img2simg (must be installed in WSL)")
            # copy file into WSL tmp area or call wsl tar? We'll call wsl with path translation:
            wsl_src = f"/mnt/{str(raw_src.drive).rstrip(':').lower()}{str(raw_src).replace(raw_src.drive, '')}"
            # simpler: use wsl to run linux img2simg reading from Windows path via /mnt/c/...
            cmd = f"wsl img2simg '{wsl_src}' '/tmp/{gsi_file}'"
            cp = run(cmd, check=False, shell=True)
            if cp is None or cp.returncode != 0:
                print("[-] wsl img2simg failed:", None if cp is None else cp.returncode)
                return None
            # copy result back from wsl /tmp to gsi_dir: use wsl path -> windows path via wsl cat
            # write file content:
            with open(sparse_dst, "wb") as outf:
                cp2 = run(f"wsl cat /tmp/{gsi_file}", check=False, shell=True)
                if cp2 is None or cp2.returncode != 0:
                    print("[-] Failed to fetch sparse output from WSL")
                    return None
                outf.write(cp2.stdout)
            # cleanup wsl tmp
            run(f"wsl rm /tmp/{gsi_file}", check=False, shell=True)
        if mode == "linux":
            print("[+] Expecting img2simg & simg2img available in PATH")
            cp = run(["img2simg", str(raw_src), str(sparse_dst)], check=False)
            if cp is None or cp.returncode != 0:
                print("[-] img2simg failed. Install simg tools or run under WSL.")
                return None
        # set full_gsi to the sparse file in gsi_dir
        full_gsi = sparse_dst
        fmt = "sparse"

    # if format is sparse -> leave as-is
    # move sparse/gsi into template/system.img for next stage
    shutil.move(str(full_gsi), str(template_dir / "system.img"))
    # Unsparse using simg2img -> create system.img.raw
    print("[+] Unsparse: simg2img -> system.img.raw (required)")
    simg2img = None
    img2simg_native, simg2img_native = find_simg_tools(None)
    if mode == "native" and simg2img_native:
        simg2img = simg2img_native
        cp = run([simg2img, str(template_dir / "system.img"), str(template_dir / "system.img.raw")], check=False)
        if cp is None or cp.returncode != 0:
            print("[-] simg2img failed (native).")
            if try_wsl_available():
                mode = "wsl"
            else:
                return None
    if mode == "wsl":
        # use wsl simg2img
        print("[+] Using WSL simg2img")
        # write template/system.img into a temp file accessible to WSL (/mnt/c/...)
        win_path = str(template_dir / "system.img")
        wsl_path = f"/mnt/{win_path[0].lower()}{win_path[2:].replace('\\\\','/')}"
        # call wsl simg2img and capture to /tmp then fetch
        cp = run(f"wsl simg2img '{wsl_path}' /tmp/system.img.raw", check=False, shell=True)
        if cp is None or cp.returncode != 0:
            print("[-] wsl simg2img failed")
            return None
        # fetch /tmp/system.img.raw via wsl cat
        with open(template_dir / "system.img.raw", "wb") as outf:
            cp2 = run("wsl cat /tmp/system.img.raw", check=False, shell=True)
            if cp2 is None or cp2.returncode != 0:
                print("[-] Failed to fetch raw image from WSL")
                return None
            outf.write(cp2.stdout)
        run("wsl rm /tmp/system.img.raw", check=False, shell=True)
    if mode == "linux" and simg2img is None:
        # assume simg2img in PATH
        cp = run(["simg2img", str(template_dir / "system.img"), str(template_dir / "system.img.raw")], check=False)
        if cp is None or cp.returncode != 0:
            print("[-] simg2img failed. Install simg2img in PATH.")
            return None

    raw_size = (template_dir / "system.img.raw").stat().st_size
    print("[+] Raw size:", raw_size)

    # replace raw_size in dynamic_partitions_op_list
    opfile = template_dir / "dynamic_partitions_op_list"
    if opfile.exists():
        txt = opfile.read_text(encoding="utf-8")
        txt = txt.replace("[raw_size]", str(raw_size))
        opfile.write_text(txt, encoding="utf-8")

    # replace [gsi_file] in updater-script
    updater = template_dir / "META-INF" / "com" / "google" / "android" / "updater-script"
    if updater.exists():
        up = updater.read_text(encoding="utf-8")
        up = up.replace("[gsi_file]", gsi_file)
        updater.write_text(up, encoding="utf-8")

    # run img2sdat -> produce system.new.dat and transfer list files
    img2sdat_py = Path.cwd() / "img2sdat" / "img2sdat.py"
    if not img2sdat_py.exists():
        print("[-] img2sdat.py not found under ./img2sdat/")
        return None
    print("[+] Running img2sdat (Python) ... this can take time")
    cp = run([sys.executable, str(img2sdat_py), "-v", "4", "-o", str(template_dir), str(template_dir / "system.img")], check=False)
    if cp is None or cp.returncode != 0:
        print("[-] img2sdat failed. stdout/stderr:")
        if cp:
            print(cp.stdout.decode('utf-8', errors='ignore'))
            print(cp.stderr.decode('utf-8', errors='ignore'))
        return None

    # ensure system.new.dat exists
    snew = template_dir / "system.new.dat"
    if not snew.exists():
        print("[-] system.new.dat missing - img2sdat likely failed")
        return None

    # compress with brotli (python or external)
    print("[+] Compressing system.new.dat -> system.new.dat.br")
    br = template_dir / "system.new.dat.br"
    compressed_ok = False
    try:
        compressed_ok = compress_brotli_py(snew, br)
    except Exception:
        compressed_ok = False
    if not compressed_ok:
        print("[+] Python brotli module not available or failed. Trying external brotli binary.")
        cp = run(["brotli", "-j1", str(snew)], check=False)
        if cp is None or cp.returncode != 0:
            print("[-] brotli compression failed. Install python brotli or external brotli.")
            return None
        # external brotli creates .br next to snew

    # Remove large leftover files before zipping
    for big in ("system.img", "system.img.raw", "system.new.dat"):
        p = template_dir / big
        if p.exists():
            try:
                p.unlink()
            except Exception:
                pass

    # Create zip using Python zipfile (store=no compression to match original behavior)
    print("[+] Creating flashable ZIP (no compression store)")
    out_zip_name = Path(gsi_file).stem + ".zip"
    out_zip_tmp = gsi_dir / out_zip_name
    import zipfile
    with zipfile.ZipFile(out_zip_tmp, "w", compression=zipfile.ZIP_STORED) as zf:
        for root, dirs, files in os.walk(template_dir):
            for f in files:
                full = Path(root) / f
                # relative path inside zip
                arcname = os.path.relpath(full, template_dir)
                zf.write(full, arcname)

    # move zip to CWD (handle cross-device)
    final_dest = Path.cwd() / out_zip_name
    try:
        shutil.move(str(out_zip_tmp), str(final_dest))
    except Exception:
        shutil.copy2(str(out_zip_tmp), str(final_dest))
        out_zip_tmp.unlink()

    print("[✓] Done! Output:", str(final_dest))

    # cleanup: remove template and workdir
    try:
        shutil.rmtree(template_dir)
    except Exception:
        pass
    # leave gsi_dir for debug for a short while
    print("[+] Temporary workdir kept for 60s at:", str(gsi_dir))
    time.sleep(60)
    try:
        shutil.rmtree(gsi_dir)
    except Exception:
        pass

    return str(final_dest)


# ---------- CLI ----------
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Universal GSI->ZIP converter (Windows native / WSL / Linux)")
    ap.add_argument("gsi", help="path to system.img (or .img.xz/.img.gz/etc)")
    ap.add_argument("--mode", choices=["windows", "wsl", "linux"], help="force mode (optional)")
    ap.add_argument("--arch", default=DEFAULT_ARCH, help="arch (default arm64)")
    args = ap.parse_args()
    res = convert(args.gsi, arch=args.arch, forced_mode=args.mode)
    if not res:
        sys.exit(1)
