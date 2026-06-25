export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method tidak diizinkan' });
  }

  const { url, name, email, logo } = req.body;
  const token = process.env.GITHUB_PAT;
  
  // Menyesuaikan dengan data dari screenshot 1000179785.jpg
  const owner = 'nadia24021986-ship-it';
  const repo = '.-Apk-Generator'; 

  if (!token) {
    return res.status(500).json({ error: 'Kunci GITHUB_PAT belum dipasang di Vercel' });
  }

  try {
    const response = await fetch(`https://api.github.com/repos/${owner}/${repo}/dispatches`, {
      method: 'POST',
      headers: {
        'Authorization': `token ${token}`,
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
        'User-Agent': 'Vercel-Backend'
      },
      body: JSON.stringify({
        event_type: 'build-apk',
        client_payload: { url, name, email, logo }
      })
    });

    if (response.ok) {
      return res.status(200).json({ success: true, message: 'Robot GitHub Actions berhasil dipicu!' });
    } else {
      const errorText = await response.text();
      return res.status(response.status).json({ error: errorText });
    }
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}
