document.getElementById('login-form').addEventListener('submit', login);

async function login(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
    const response = await fetch('/admin/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    if (response.ok) {
        const query = new URLSearchParams(window.location.search);
        if (query.has('redirect')) {
            window.location.href = query.get('redirect');
        } else {
            window.location.href = '/admin';
        }
    } else {
        alert(result.message);
    }
}