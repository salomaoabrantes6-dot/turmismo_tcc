//alert('Script funcinando');

// Abrir o form para a edição de Ponto Turísticos

const btn_add = document.querySelector('#adicionar');
const form_to_add = document.querySelector('.form_to_add_pontos');

btn_add.addEventListener('click', () =>{
    form_to_add.classList.add('active');
})

// Pra feichar o form

const btn_fechar = document.querySelector('#fechar');

btn_fechar.addEventListener('click', () =>{
    form_to_add.classList.remove('active');
})