```javascript
// api/generate.js

export default async function handler(req, res) {
    // Hanya menerima request POST
    if (req.method !== 'POST') {
        return res.status(405).json({ message: 'Metode Tidak Diizinkan' });
    }

    const { url, name, email, logoBase64 } = req.body;

    // Validasi data input sederhana
    if (!url || !name || !email || !logoBase64) {
        return res.status(400).json({ message: 'Semua kolom formulir wajib diisi!' });
    }

    try {
        // Berdasarkan screenshot repositori kamu:
        const GITHUB_USERNAME = "nadia24021986-ship-it";
        const GITHUB_REPO = "-.Apk-Generator"; 

        // Mengirim permintaan (Repository Dispatch) ke GitHub Actions
        const githubResponse = await fetch(`https://api.github.com/repos/${GITHUB_USERNAME}/${GITHUB_REPO}/dispatches`, {
            method: 'POST',
            headers: {
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': `Bearer ${process.env.GITHUB_PAT}`, // Diambil dari variabel lingkungan Vercel nanti
                'Content-Type': 'application/json',
                'User-Agent': 'Vercel-Serverless-App'
            },
            body: JSON.stringify({
                event_type: "build_apk", // Event pemicu workflow
                client_payload: {
                    url: url,
                    app_name: name,
                    email: email,
                    logo: logoBase64
                }
            })
        });

        if (githubResponse.ok) {
            return res.status(200).json({ message: 'Proses build berhasil dipicu di GitHub Actions!' });
        } else {
            const errorText = await githubResponse.text();
            return res.status(500).json({ 
                message: 'Gagal memicu GitHub API. Pastikan GITHUB_PAT Anda valid.',
                error: errorText 
            });
        }
    } catch (error) {
        return res.status(500).json({ message: 'Kesalahan internal server', error: error.message });
    }
}

```
