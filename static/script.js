document.getElementById('signup-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('http://localhost:3001/auth/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();
    document.getElementById('signup-message').innerText = data.message;
});

document.getElementById('login-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    const response = await fetch('http://localhost:3001/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();
    document.getElementById('login-message').innerText = data.message;

    if (data.token) {
        localStorage.setItem('token', data.token);
        window.location.href = '/recommendations.html';
    }
});

document.getElementById('recommendation-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const skills = document.getElementById('skills').value.split(',');

    const response = await fetch('http://localhost:3001/recommend/get_recommendations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ skills })
    });

    const data = await response.json();
    document.getElementById('recommendations-message').innerText = data.recommendations || "No recommendations found.";
});


