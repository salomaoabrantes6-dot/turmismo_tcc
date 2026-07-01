const tack_imgs = document.querySelector('.body_index');
const all_imgs = tack_imgs.querySelectorAll('img');
const total_imgs = all_imgs.length;
console.log(total_imgs);

if (total_imgs) {
    const inserir = document.querySelector('#inserir');
    inserir.textContent = `
        ${total_imgs}
    ` ; 
}