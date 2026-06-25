```python
# scripts/build_prep.py
import os
import base64
import xml.etree.ElementTree as ET

def main():
    # 1. Mengambil data payload dari Environment Variables yang dikirim oleh GitHub Actions
    app_name = os.environ.get('APP_NAME', 'My WebApp')
    app_url = os.environ.get('APP_URL', 'https://google.com')
    app_logo_base64 = os.environ.get('APP_LOGO', '')

    print("--- MEMULAI PROSES PENYIAPAN TEMPLATE ANDROID ---")
    print(f"Nama Aplikasi Baru : {app_name}")
    print(f"Target URL Website : {app_url}")

    # 2. Update Strings XML (Tempat menyimpan Nama App dan URL Website)
    strings_path = 'android-template/app/src/main/res/values/strings.xml'
    
    # Pastikan file strings.xml ada
    if os.path.exists(strings_path):
        try:
            tree = ET.parse(strings_path)
            root = tree.getroot()
            
            updated_name = False
            updated_url = False
            
            for string_elem in root.findall('string'):
                name_attr = string_elem.get('name')
                if name_attr == 'app_name':
                    string_elem.text = app_name
                    updated_name = True
                elif name_attr == 'website_url':
                    string_elem.text = app_url
                    updated_url = True
            
            # Jika elemen belum ada, buat baru
            if not updated_name:
                new_name_elem = ET.SubElement(root, 'string', name='app_name')
                new_name_elem.text = app_name
            if not updated_url:
                new_url_elem = ET.SubElement(root, 'string', name='website_url')
                new_url_elem.text = app_url

            tree.write(strings_path, encoding='utf-8', xml_declaration=True)
            print("✅ Berhasil memperbarui file strings.xml!")
        except Exception as e:
            print(f"❌ Gagal memperbarui strings.xml: {str(e)}")
    else:
        print(f"⚠️ Peringatan: File {strings_path} tidak ditemukan!")

    # 3. Proses Logo / Ikon Aplikasi (Decode Base64 ke PNG)
    if app_logo_base64:
        try:
            # Decode string base64 kembali menjadi biner gambar
            image_data = base64.b64decode(app_logo_base64)
            
            # Tentukan folder-folder tempat ikon Android disimpan
            mipmap_folders = [
                'mipmap-mdpi',
                'mipmap-hdpi',
                'mipmap-xhdpi',
                'mipmap-xxhdpi',
                'mipmap-xxxhdpi'
            ]
            
            base_res_path = 'android-template/app/src/main/res'
            
            for folder in mipmap_folders:
                folder_path = os.path.join(base_res_path, folder)
                # Buat folder jika belum ada
                os.makedirs(folder_path, exist_ok=True)
                
                # Simpan gambar sebagai ic_launcher.png (Ikon default Android)
                icon_path = os.path.join(folder_path, 'ic_launcher.png')
                with open(icon_path, 'wb') as f:
                    f.write(image_data)
                    
            print("✅ Berhasil men-decode logo dan memperbarui ikon aplikasi di semua folder mipmap!")
        except Exception as e:
            print(f"❌ Gagal memproses logo base64: {str(e)}")
    else:
        print("⚠️ Ikon kustom tidak diunggah, menggunakan ikon bawaan template.")

if __name__ == '__main__':
    main()

```

