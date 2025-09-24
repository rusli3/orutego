# 🧭 orutego - Demo & Testing Guide

## 🚀 Quick Demo

Setelah aplikasi berjalan di `http://localhost:5000`, ikuti langkah-langkah berikut:

### 1. Setup API Key
1. Masukkan Google Maps API Key Anda di kolom "Google Maps API Key"
2. Klik tombol "Save" - tombol akan berubah menjadi hijau dan menampilkan "Saved"
3. Google Maps akan otomatis dimuat di latar belakang

### 2. Test Perhitungan Rute
Coba dengan alamat-alamat berikut untuk testing:

#### Contoh 1: Rute dalam kota (Indonesia)
- **Origin**: `Jl. Gajah Mada No.1, Pontianak, Kalimantan Barat`
- **Destination**: `Jl. Ahmad Yani, Pontianak, Kalimantan Barat`
- **Travel Mode**: Driving
- **Expected**: Jarak sekitar 2-3 km, waktu 5-10 menit

#### Contoh 2: Rute antar kota
- **Origin**: `Jakarta Pusat, DKI Jakarta`
- **Destination**: `Bandung, Jawa Barat`
- **Travel Mode**: Driving
- **Expected**: Jarak sekitar 150 km, waktu 3-4 jam

#### Contoh 3: Rute internasional
- **Origin**: `Kuala Lumpur, Malaysia`
- **Destination**: `Singapore`
- **Travel Mode**: Driving
- **Expected**: Jarak sekitar 350 km, waktu 4-5 jam

### 3. Fitur yang Dapat Ditest

#### ✅ Address Input & Validation
- Coba kosongkan salah satu field → akan muncul error
- Masukkan alamat yang tidak valid → akan ada error handling

#### ✅ Address Swap
- Isi origin dan destination
- Klik tombol panah ↕️ di tengah
- Alamat akan bertukar posisi dengan animasi

#### ✅ Travel Mode Selection
- Coba semua mode: Driving, Walking, Cycling, Transit
- Perhatikan perubahan hasil perhitungan

#### ✅ Interactive Google Maps
- **Zoom & Pan**: Gunakan mouse wheel dan drag
- **Markers**: Klik marker A (origin) dan B (destination) untuk info
- **Route**: Akan menampilkan rute sebenarnya dari Google
- **Auto-fit**: Map otomatis menyesuaikan untuk menampilkan seluruh rute

#### ✅ Results Display
- **Distance**: Dalam kilometer
- **Time**: Format HH:MM dan desimal hours
- **Coordinates**: Data CSV format dengan presisi 6 decimal
- **Copy to Clipboard**: Klik tombol copy (📋) untuk menyalin coordinate data

#### ✅ Copy to Clipboard Feature
- Klik tombol hijau dengan icon copy di sebelah coordinate data
- Data akan tersalin ke clipboard dalam format CSV
- Feedback visual: icon berubah jadi ✓ dan pesan konfirmasi
- Kompatibel dengan semua browser modern

## 🔧 Troubleshooting

### Google Maps tidak muncul?
1. Pastikan API key sudah disimpan
2. Check console browser (F12) untuk error
3. Pastikan Maps JavaScript API sudah diaktifkan
4. Cek quota dan billing di Google Cloud Console

### Calculation failed?
1. Pastikan semua 4 APIs sudah diaktifkan:
   - Geocoding API
   - Distance Matrix API
   - Directions API
   - Maps JavaScript API
2. Cek apakah API key memiliki restrictions yang terlalu ketat

### Network Error?
1. Pastikan koneksi internet stabil
2. Cek apakah ada firewall yang memblokir Google APIs
3. Restart aplikasi Flask

## 🌟 Advanced Testing

### Test Multiple Calculations
1. Lakukan beberapa perhitungan berturut-turut
2. Perhatikan caching - hasil tersimpan di session
3. Refresh browser - data terakhir tetap ada (localStorage)

### Test Responsive Design
1. Resize window browser
2. Test di mobile view (F12 → Device simulation)
3. Semua elemen harus tetap accessible

### Test Error Handling
1. Matikan koneksi internet → harus ada error message
2. Gunakan API key yang salah → error handling
3. Input alamat yang tidak ada → graceful failure

## 📱 Production Checklist

Sebelum deploy ke production:

- [ ] Ganti `app.secret_key` dengan key yang aman
- [ ] Set `debug=False` di `app.run()`
- [ ] Restrict API key dengan domain yang benar
- [ ] Setup proper web server (nginx + gunicorn)
- [ ] Enable HTTPS
- [ ] Monitor API usage & costs
- [ ] Setup error logging
- [ ] Test dengan load testing tools

## 🎯 Expected Results Format

Output coordinate data harus dalam format:
```
lat_origin,lng_origin,lat_destination,lng_destination,distance_km,HH:MM,decimal_hours
```

Contoh:
```
-0.026700,109.342100,-0.114200,109.406500,12.84,01:30,1.50
```

Aplikasi sekarang sudah menggunakan **Google Maps JavaScript API** yang memberikan:
- ✅ Peta interaktif yang sesungguhnya
- ✅ Rute yang akurat sesuai kondisi jalan
- ✅ Zoom, pan, dan navigasi map
- ✅ Info windows dengan detail koordinat
- ✅ Marker custom dengan label A dan B
- ✅ Automatic bounds fitting untuk menampilkan seluruh rute