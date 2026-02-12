#!/usr/bin/env python3
import os, shutil, tempfile, asyncio
from subprocess import Popen, PIPE, call
import functools
import sys

# ======== async utils from web.py ==========
async def async_call(loop, args, stdout=PIPE, shell=True):
    return await loop.run_in_executor(None, functools.partial(call, args, stdout=stdout, shell=shell))

async def async_Popen(loop, args, stdout=PIPE):
    return await loop.run_in_executor(None, functools.partial(Popen, args, stdout=stdout))

async def async_communicate(loop, p):
    return await loop.run_in_executor(None, p.communicate)

# ======== main converter ==========
async def convert_gsi(gsi_file, arch="arm64"):
    loop = asyncio.get_running_loop()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_tmp = os.path.join(script_dir, "tmp")
    os.makedirs(base_tmp, exist_ok=True)
    gsi_dir = tempfile.mkdtemp(dir=base_tmp)

    print("[+] Working directory:", gsi_dir)
    shutil.copy(gsi_file, f"{gsi_dir}/{os.path.basename(gsi_file)}")

    gsi_file = os.path.basename(gsi_file)

    # detect format
    p = await async_Popen(loop, ["file", f"{gsi_dir}/{gsi_file}"])
    stdout, stderr = await async_communicate(loop, p)
    stdout = stdout.decode()

    if "Android sparse" in stdout:
        gsi_format = "sparse"
    elif "ext2 filesystem" in stdout:
        gsi_format = "raw"
    elif "XZ compressed" in stdout:
        gsi_format = "xz"
    elif "gzip compressed" in stdout:
        gsi_format = "gz"
    else:
        print("[-] Unsupported format:", stdout)
        return

    print("[+] Detected format:", gsi_format)

    # copy template
    shutil.copytree(f"template_{arch}", f"{gsi_dir}/template")

    # PROCESS SAME AS WEB.PY
    if gsi_format == "raw":
        shutil.move(f"{gsi_dir}/{gsi_file}", f"{gsi_dir}/{gsi_file}.raw")
        print("[+] Converting RAW → SPARSE")
        p = await async_Popen(loop, ["./simg/img2simg", f"{gsi_dir}/{gsi_file}.raw", f"{gsi_dir}/{gsi_file}"])
        await async_communicate(loop, p)

    if gsi_format == "xz":
        print("[+] Decompressing XZ")
        p = await async_Popen(loop, ["unxz", "-T", "0", f"{gsi_dir}/{gsi_file}"])
        await async_communicate(loop, p)
        gsi_file = gsi_file.replace(".xz", "")

    if gsi_format == "gz":
        print("[+] Decompressing GZ")
        p = await async_Popen(loop, ["gunzip", f"{gsi_dir}/{gsi_file}"])
        await async_communicate(loop, p)
        gsi_file = gsi_file.replace(".gz", "")

    print("[+] Unsparse system.img → system.img.raw")
    shutil.move(f"{gsi_dir}/{gsi_file}", f"{gsi_dir}/template/system.img")

    p = await async_Popen(loop, ["./simg/simg2img", f"{gsi_dir}/template/system.img", f"{gsi_dir}/template/system.img.raw"])
    await async_communicate(loop, p)

    raw_size = os.path.getsize(f"{gsi_dir}/template/system.img.raw")
    print("[+] RAW size:", raw_size)

    # replace raw size
    with open(f"{gsi_dir}/template/dynamic_partitions_op_list", "r") as f:
        data = f.read().replace("[raw_size]", str(raw_size))
    with open(f"{gsi_dir}/template/dynamic_partitions_op_list", "w") as f:
        f.write(data)

    # replace gsi filename
    with open(f"{gsi_dir}/template/META-INF/com/google/android/updater-script", "r") as f:
        data = f.read().replace("[gsi_file]", gsi_file)
    with open(f"{gsi_dir}/template/META-INF/com/google/android/updater-script", "w") as f:
        f.write(data)

    print("[+] Converting to system.new.dat")
    p = await async_Popen(loop, ["python3", "img2sdat/img2sdat.py", "-v", "4", "-o", f"{gsi_dir}/template", f"{gsi_dir}/template/system.img"])
    await async_communicate(loop, p)

    print("[+] Compressing with Brotli")
    p = await async_Popen(loop, ["brotli", "-j1", f"{gsi_dir}/template/system.new.dat"])
    await async_communicate(loop, p)

    # Delete leftover system.img and system.img.raw files
    print("[+] Deleting leftover files")
    try:
        os.remove(f"{gsi_dir}/template/system.img")
    except:
        pass
    try:
        os.remove(f"{gsi_dir}/template/system.img.raw")
    except:
        pass

    print("[+] Creating final ZIP")
    out_zip = gsi_file.replace(".img", ".zip")
    await async_call(loop, f"cd {gsi_dir}/template && zip -r0 ../{out_zip} *")

    shutil.move(f"{gsi_dir}/{out_zip}", f"./{out_zip}")
    print("[✓] Done! Output:", out_zip)

async def main():
    if len(sys.argv) < 2:
        print("Usage: python3 convert.py <system.img> [arm64]")
        return

    gsi_file = sys.argv[1]
    arch = "arm64"

    await convert_gsi(gsi_file, arch)

asyncio.run(main())
