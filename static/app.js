// Função para carregar avisos dinamicamente (caso necessário)
function loadNotices() {
    fetch('/notices.json')
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('notices');
            container.innerHTML = data.map(n => `<p><strong>${n.title}</strong>: ${n.message}</p>`).join('');
        })
        .catch(() => {
            document.getElementById('notices').innerHTML = '<p>Erro ao carregar avisos.</p>';
        });
}

// Exemplo: Validação do formulário de login no frontend (opcional)
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', function(event) {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        if (username === '' || password === '') {
            alert('Por favor, insira tanto o nome de usuário quanto a senha.');
            event.preventDefault();  // Impede o envio do formulário
        }
    });
}
