// ===== ABRIR E FECHAR MODAL DE EXPLORAR =====

document.addEventListener('DOMContentLoaded', function () {

  // Todos os botões "Explorar"
  const btnsAbrir = document.querySelectorAll('.btn_open_explorar');
  // Todos os modais (nav.esplorar)
  const modais = document.querySelectorAll('nav.esplorar');

  // Abrir: cada botão abre o modal irmão dentro do mesmo .spot-card ou bloco
  btnsAbrir.forEach(function (btn) {
    btn.addEventListener('click', function () {
      // Procura o nav.esplorar mais próximo (irmão do .organiza)
      const card = btn.closest('.spot-card') || btn.closest('.organiza');
      if (!card) return;

      const modal = card.querySelector('nav.esplorar')
                  || card.parentElement.querySelector('nav.esplorar');
      if (!modal) return;

      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
    });
  });

  // Fechar: botão "Visto" / "sair_do_saber_mais"
  document.querySelectorAll('.sair_do_saber_mais').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const modal = btn.closest('nav.esplorar');
      if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  });

  // Fechar: botão X (se existir)
  document.querySelectorAll('.modal-close-x').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const modal = btn.closest('nav.esplorar');
      if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  });

  // Fechar ao clicar no fundo (overlay)
  modais.forEach(function (modal) {
    modal.addEventListener('click', function (e) {
      if (e.target === modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  });

  // Fechar com tecla Escape
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      modais.forEach(function (modal) {
        modal.classList.remove('active');
      });
      document.body.style.overflow = '';
    }
  });

});
