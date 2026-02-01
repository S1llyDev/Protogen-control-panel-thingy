
        // Set defaults
fetchConfig()

        document.querySelectorAll('select').forEach(s => s.onchange = generateConfig);

    function getConfig() {
            return {
        mod_jaws: document.getElementById('mod_jaws').value,
    mod_eye: document.getElementById('mod_eye').value,
    mod_nose: document.getElementById('mod_nose').value,
    mod_owo: document.getElementById('mod_owo').value,
    mod_zloy: document.getElementById('mod_zloy').value,
    mod_kill: document.getElementById('mod_kill').value,
    alt_owo: document.getElementById('alt_owo').value,
    alt_ang: document.getElementById('alt_ang').value,
    alt_kill: document.getElementById('alt_kill').value
            };
        }

    function generateConfig() {
            const config = getConfig();
    document.getElementById('output').textContent =
                Object.entries(config).map(([k, v]) => `#define ${k} ${v}`).join('\n');
        }

    async function fetchConfig() {
            try {
                const res = await fetch('api?config', {
        method: 'POST',
    headers: {'Content-Type': 'application/json' },
    body: JSON.stringify({
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        // _fetch: "config"
                    })
                });
    const data = await res.json();
    if (data.success) {
        Object.entries(data.config).forEach(([k, v]) =>
            document.getElementById(k).value = v);
    generateConfig();
                } else {
        alert('Fetch failed: ' + data.error);
                }
            } catch (e) {console.log('Error: ' + e); }
        }

    async function saveConfig() {
            try {
                const res = await fetch('api!config', {
        method: 'POST',
        headers: {'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: document.getElementById('username').value,
            password: document.getElementById('password').value,
            config: getConfig()
        })
            });
const data = await res.json();
alert(data.success ? 'Saved!' : 'Save failed: ' + data.error);
        } catch (e) {alert('Error: ' + e); }
    }

generateConfig();