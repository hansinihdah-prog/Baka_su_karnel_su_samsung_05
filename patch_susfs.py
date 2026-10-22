#!/usr/bin/env python3
"""Pasang SUSFS (gki-android15-6.6) ke source kernel A05.
Pakai: python3 patch_susfs.py <source-kernel> <repo-susfs4ksu>
Patch resmi gagal di 1 tempat (fs/namespace.c, karena kode Samsung PROC_STLOG di antara include),
bagian itu dipasang manual di sini. Berhenti dengan error kalau ada yang tidak cocok."""
import sys, pathlib, shutil, subprocess

k = pathlib.Path(sys.argv[1]); r = pathlib.Path(sys.argv[2]) / "kernel_patches"
shutil.copy(r / "fs/susfs.c", k / "fs/susfs.c")
for h in (r / "include/linux").iterdir():
    shutil.copy(h, k / "include/linux" / h.name)

res = subprocess.run(["patch", "-p1", "--no-backup-if-mismatch", "-i", str(r / "50_add_susfs_in_gki-android15-6.6.patch")],
                     cwd=k, capture_output=True, text=True)
print(res.stdout[-1500:])
rej = sorted(str(p.relative_to(k)) for p in k.rglob("*.rej"))
if rej != ["fs/namespace.c.rej"]:
    sys.exit(f"[GAGAL] hasil patch tidak sesuai harapan. Reject: {rej}\n{res.stderr}")

p = k / "fs/namespace.c"; s = p.read_text()
a_old = "#include <linux/mnt_idmapping.h>\n\n#include \"pnode.h\""
a_new = ("#include <linux/mnt_idmapping.h>\n#ifdef CONFIG_KSU_SUSFS\n#include <linux/susfs_def.h>\n"
         "#endif // #ifdef CONFIG_KSU_SUSFS\n\n#include \"pnode.h\"")
b_old = "#ifdef CONFIG_PROC_STLOG\n#include <linux/fslog.h>\n#endif\n\n"
b_new = b_old + ("#ifdef CONFIG_KSU_SUSFS_SUS_MOUNT\nextern bool susfs_is_current_ksu_domain(void);\n"
                 "extern struct static_key_true susfs_is_sdcard_android_data_not_decrypted;\n\n"
                 "#define CL_COPY_MNT_NS BIT(25) /* used by copy_mnt_ns() */\n#endif // #ifdef CONFIG_KSU_SUSFS_SUS_MOUNT\n\n")
for n, o in (("a", a_old), ("b", b_old)):
    if s.count(o) != 1:
        sys.exit(f"[GAGAL] fs/namespace.c: anchor {n} ditemukan {s.count(o)}x")
s = s.replace(a_old, a_new).replace(b_old, b_new)
p.write_text(s)
(k / "fs/namespace.c.rej").unlink()
print("[ok] SUSFS terpasang (fs/namespace.c disesuaikan manual)")
