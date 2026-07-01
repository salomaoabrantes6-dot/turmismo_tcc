//alert('testando a funcionalidade');

const btn_abrir_add_ponto = document.querySelector('.btn_open_modal');

btn_abrir_add_ponto.addEventListener('click', () => {
    const modal_ponto = document.querySelector('.modal-overlay');
    modal_ponto.classList.add('open');
})

const btn_close_modal = document.querySelector('.btn_close_modal');
btn_close_modal.addEventListener('click', () => {
    const close_modal_ponto = document.querySelector('.modal-overlay');
    close_modal_ponto.classList.remove('open');
})