```python
import os
import base64

def create_directory_structure():
    """Membuat seluruh folder yang dibutuhkan untuk project Android WebView"""
    dirs = [
        'android-template',
        'android-template/app',
        'android-template/app/src/main',
        'android-template/app/src/main/res',
        'android-template/app/src/main/res/values',
        'android-template/app/src/main/res/layout',
        'android-template/app/src/main/java/com/example/webapp',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("✅ Struktur folder Android berhasil dibuat!")

def write_file(path, content):
    """Fungsi pembantu untuk menulis file teks"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ File dibuat: {path}")

def main():
    # Mengambil data dari payload Vercel
    app_name = os.environ.get('APP_NAME', 'My WebApp')
    app_url = os.environ.get('APP_URL', 'https://google.com')
    app_logo_base64 = os.environ.get('APP_LOGO', '')

    print("--- MEMULAI GENERASI PROJECT ANDROID OTOMATIS ---")
    
    # 1. Buat folder-folder dasar
    create_directory_structure()

    # 2. Tulis settings.gradle
    settings_gradle = """
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "WebApp"
include ':app'
"""
    write_file('android-template/settings.gradle', settings_gradle)

    # 3. Tulis build.gradle (Project Level)
    project_gradle = """
plugins {
    id 'com.android.application' version '8.2.0' apply false
}
"""
    write_file('android-template/build.gradle', project_gradle)

    # 4. Tulis app/build.gradle (Module Level)
    app_gradle = """
plugins {
    id 'com.android.application'
}

android {
    namespace 'com.example.webapp'
    compileSdk 34

    defaultConfig {
        applicationId "com.nadia.webapp"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
}
"""
    write_file('android-template/app/build.gradle', app_gradle)

    # 5. Tulis strings.xml (isi nama aplikasi & URL web tujuan)
    strings_xml = f"""
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{app_name}</string>
    <string name="website_url">{app_url}</string>
</resources>
"""
    write_file('android-template/app/src/main/res/values/strings.xml', strings_xml)

    # 6. Tulis activity_main.xml (Layout WebView)
    layout_xml = """
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    <WebView
        android:id="@+id/webview"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />
</RelativeLayout>
"""
    write_file('android-template/app/src/main/res/layout/activity_main.xml', layout_xml)

    # 7. Tulis AndroidManifest.xml (Izin Internet)
    manifest_xml = """
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher"
        android:supportsRtl="true"
        android:theme="@style/Theme.AppCompat.Light.NoActionBar"
        android:usesCleartextTraffic="true">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    write_file('android-template/app/src/main/AndroidManifest.xml', manifest_xml)

    # 8. Tulis MainActivity.java (Logika WebView Android)
    main_activity_java = """
package com.example.webapp;

import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    private WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        webView = findViewById(R.id.webview);
        
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setDatabaseEnabled(true);
        webSettings.setAllowFileAccess(true);
        webSettings.setAllowContentAccess(true);

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                view.loadUrl(url);
                return true;
            }
        });

        String url = getString(R.string.website_url);
        webView.loadUrl(url);
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
"""
    write_file('android-template/app/src/main/java/com/example/webapp/MainActivity.java', main_activity_java)

    # 9. Decode Logo & pasang ke folder mipmap
    if app_logo_base64:
        try:
            image_data = base64.b64decode(app_logo_base64)
            mipmap_folders = [
                'mipmap-mdpi',
                'mipmap-hdpi',
                'mipmap-xhdpi',
                'mipmap-xxhdpi',
                'mipmap-xxxhdpi'
            ]
            for folder in mipmap_folders:
                folder_path = f'android-template/app/src/main/res/{folder}'
                os.makedirs(folder_path, exist_ok=True)
                with open(f'{folder_path}/ic_launcher.png', 'wb') as f:
                    f.write(image_data)
            print("✅ Logo kustom berhasil didecode & dipasang!")
        except Exception as e:
            print(f"❌ Gagal memproses logo: {str(e)}")

    print("--- PROSES GENERASI COMPLETED ---")

if __name__ == '__main__':
    main()

```
