// ===== RENDER ADMIN =====
function updateStats() {
    document.getElementById('stat-pontos').textContent = data.pontos.length;
    document.getElementById('stat-praias').textContent = data.praias.length;
    document.getElementById('stat-imagens').textContent = data.pontos.length * 2 + data.praias.length;
    document.getElementById('stat-feedbacks').textContent = data.feedbacks.length;
}

function renderFeedbacks() {
    const tbody = document.getElementById('feedbacks-table');
    if (data.feedbacks.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" style="text-align:center;color:var(--muted-fg);padding:2rem;">Nenhum feedback recebido</td></tr>';
        return;
    }
    tbody.innerHTML = data.feedbacks.map(f => `<tr><td>${f.nome}</td><td>${f.mensagem}</td><td>${f.data}</td></tr>`).join('');
}

function renderPontos() {
    document.getElementById('pontos-table').innerHTML = data.pontos.map(p => `
      <tr>
        <td><strong>${p.nome}</strong></td>
        <td>${p.contacto || '—'}</td>
        <td>${p.hotel.nome || '—'}</td>
        <td>
          <button class="btn btn-danger btn-sm" onclick="deletePonto(${p.id})"><i class="fas fa-trash"></i></button>
        </td>
      </tr>
    `).join('');
}

function renderPraias() {
    const tbody = document.getElementById('praias-table');
    if (data.praias.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" style="text-align:center;color:var(--muted-fg);padding:2rem;">Nenhuma praia adicionada</td></tr>';
        return;
    }
    tbody.innerHTML = data.praias.map(p => `
      <tr>
        <td><strong>${p.nome}</strong></td>
        <td>${p.local}</td>
        <td><button class="btn btn-danger btn-sm" onclick="deletePraia(${p.id})"><i class="fas fa-trash"></i></button></td>
      </tr>
    `).join('');
}

function renderUsuarios() {
    document.getElementById('usuarios-table').innerHTML = data.usuarios.map(u => `
      <tr>
        <td>${u.nome}</td>
        <td>${u.email}</td>
        <td><span class="badge ${u.role === 'super_admin' ? 'badge-gold' : 'badge-green'}">${u.role === 'super_admin' ? 'Super Admin' : 'Admin'}</span></td>
        <td><button class="btn btn-danger btn-sm" onclick="deleteUsuario(${u.id})"><i class="fas fa-trash"></i></button></td>
      </tr>
    `).join('');
}

function renderAllAdmin() {
    updateStats();
    renderFeedbacks();
    renderPontos();
    renderPraias();
    renderUsuarios();
}

// Init
renderSpots();
renderAllAdmin();