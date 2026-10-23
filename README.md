# Kernel Galaxy A05 (a05m) + BakaSU + SUSFS

Kernel 6.6 untuk **Samsung Galaxy A05 (SM-A055F / a05m)** dengan root **BakaSU** (sebelumnya ReSukiSU) dan **SUSFS**. Dibuat untuk ROM custom yang memakai kernel `6.6.142-android15-8-g37e9c3855f2c-4k`.

> ⚠️ Kernel ini hanya untuk SM-A055F dengan ROM yang kernelnya sama seperti di atas. Flash di ROM atau firmware lain bisa membuat HP bootloop.

## Isi

| Komponen | Versi |
|---|---|
| Kernel | 6.6.142-4k (android15-6.6-lts) |
| Root | BakaSU v4.2.0-rc3 (driver `10cada74`, mode SUSFS inline hook) |
| SUSFS | v2.3.0 |
| Manager | BakaSU Manager v4.2.0-rc3 |

## Cek dulu sebelum flash

1. Buka **Pengaturan → Tentang ponsel → Informasi perangkat lunak → Versi kernel**, atau jalankan `uname -r`.
2. Hasilnya harus diawali `6.6.142`. Kalau berbeda, jangan flash.
3. Model HP harus **SM-A055F**.

## Cara pasang

1. **Backup** partisi `boot` dan `init_boot` lewat OrangeFox. Simpan juga `boot.img` dan `init_boot.img` dari file ROM kamu.
2. Unduh file `A05-BakaSU-....zip` dari menu **Releases**.
3. Flash zip itu di OrangeFox, lalu reboot ke sistem. Tidak perlu mencopot kernel sebelumnya, flash langsung menimpanya.
4. Pasang **BakaSU Manager v4.2.0-rc3**: https://github.com/Baka-SU/BakaSU/releases/tag/v4.2.0-rc3
5. Buka manager dan cek bahwa driver kernel terbaca dan SuSFS menampilkan v2.3.0.

## Kalau bootloop

Restore backup `boot` dan `init_boot` lewat OrangeFox. Kalau OrangeFox tidak bisa dimasuki, flash `boot.img` dan `init_boot.img` dari ROM lewat Odin.

## Catatan versi manager

Manager dan driver kernel berasal dari rilis yang sama (v4.2.0-rc3). Nomor build bisa berbeda sedikit (misalnya manager 35236 dan driver 35241) karena driver kernel dibuat dari branch `sync-susfs` yang lebih baru dari rilis manager. Itu normal dan tidak mengganggu.

## Status pengujian

- Sudah diuji: boot normal di SM-A055F, manager membaca driver kernel dan SuSFS v2.3.0.
- Belum diuji menyeluruh: aplikasi yang butuh root, modul, dan efektivitas fitur penyembunyian SUSFS. Hasilnya bisa berbeda per aplikasi.
- Dibangun dan diuji hanya pada satu ROM custom. Firmware Samsung bawaan belum dicoba.

## Fitur

- Root dengan BakaSU (App Profile, manajemen modul).
- SUSFS: sembunyikan path, mount, dan kstat tertentu, serta spoof uname.
- Kompatibel dengan modul vendor ROM: kernel dicek otomatis terhadap CRC simbol modul bawaan ROM sebelum zip dibuat, supaya modul tidak ditolak saat boot.

## Detail build (untuk yang ingin membangun sendiri)

- Source kernel: [rsuntk/android_kernel_samsung_a05m-6.6](https://github.com/rsuntk/android_kernel_samsung_a05m-6.6), branch `android15-6.6-lts`.
- Konfigurasi dasar: `gki_defconfig`, dengan `io_uring` dan `ublk` dimatikan agar sama dengan kernel ROM.
- Build lewat GitHub Actions (`.github/workflows/build.yml`). Hasilnya dipaketkan dengan AnyKernel3 ke partisi `boot`.
- `patch_hooks.py` dan `patch_susfs.py` menyesuaikan source dengan BakaSU dan SUSFS.
- Cek CRC memakai `tools/cekcrc.py` dan `tools/stock_modver.json`.

## Kredit

- [BakaSU](https://github.com/Baka-SU/BakaSU) dan KernelSU
- [SUSFS](https://gitlab.com/simonpunk/susfs4ksu) oleh simonpunk
- [rsuntk](https://github.com/rsuntk) untuk source kernel A05
- [AnyKernel3](https://github.com/osm0sis/AnyKernel3) oleh osm0sis

Kernel berlisensi GPL-2.0, sesuai source aslinya.

## Tanggung jawab

Flash dengan risiko sendiri. Selalu simpan backup sebelum mencoba, karena kernel yang salah bisa membuat HP tidak bisa boot.
