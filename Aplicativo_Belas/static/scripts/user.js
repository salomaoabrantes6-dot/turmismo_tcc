//alert('testando a funcionalidade');
const btn_abrir_add_user = document.querySelector('.btn_open_modal');

btn_abrir_add_user.addEventListener('click', () => {
    const modal_user = document.querySelector('.modal-overlay');
    modal_user.classList.add('open');
})

const btn_close_modal = document.querySelector('.btn_close_modal');
btn_close_modal.addEventListener('click', () => {
    const close_modal_user = document.querySelector('.modal-overlay');
    close_modal_user.classList.remove('open');
})

document.querySelectorAll('form[action]').forEach(form => {
    form.addEventListener('submit', function(e) {
        const action = this.querySelector('input[name="action"]').value;
        if (action === 'delete') {
            if (!confirm('Tem certeza que deseja excluir este usuário?')) {
                e.preventDefault();
            }
        }
    });
});

// ===== FUNÇÕES PRINCIPAIS =====

// Verificar o tema ao carregar a página
function checkAndApplyTheme() {
    const savedTheme = localStorage.getItem('theme');

    // Se existir tema salvo como 'dark', aplica a classe
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }
}

// Toggle Sidebar (Mobile)
function toggleSidebar() {
    const sidebar = document.getElementById('admin-sidebar');
    const overlay = document.getElementById('sidebar-overlay');

    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');

    // Prevenir scroll quando sidebar está aberta
    document.body.style.overflow = sidebar.classList.contains('active') ? 'hidden' : '';
}

// Modal functions
function openModal() {
    const modal = document.getElementById('modal-usuario');
    modal.classList.add('open');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    const modal = document.getElementById('modal-usuario');
    modal.classList.remove('open');
    document.body.style.overflow = '';
}

// Fechar modal clicando fora
document.addEventListener('click', function (e) {
    const modal = document.getElementById('modal-usuario');
    if (e.target === modal) {
        closeModal();
    }
});

// Fechar modal com ESC
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
        closeModal();
    }
});

// Fechar sidebar ao redimensionar para desktop
window.addEventListener('resize', function () {
    if (window.innerWidth > 768) {
        const sidebar = document.getElementById('admin-sidebar');
        const overlay = document.getElementById('sidebar-overlay');

        sidebar.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// Inicializar
document.addEventListener('DOMContentLoaded', function () {
    // Aplicar tema baseado no localStorage
    checkAndApplyTheme();

    // Configurar botões de abrir/fechar modal
    const openButtons = document.querySelectorAll('.btn_open_modal');
    const closeButtons = document.querySelectorAll('.btn_close_modal');

    openButtons.forEach(btn => {
        btn.addEventListener('click', openModal);
    });

    closeButtons.forEach(btn => {
        btn.addEventListener('click', closeModal);
    });

    // Marcar link ativo na sidebar
    const currentPath = window.location.pathname;
    const sidebarLinks = document.querySelectorAll('.sidebar-nav a');

    sidebarLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            sidebarLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        }
    });

    // Observer para detectar mudanças no tema (caso seja alterado em outra aba)
    window.addEventListener('storage', function (e) {
        if (e.key === 'theme') {
            checkAndApplyTheme();
        }
    });
});