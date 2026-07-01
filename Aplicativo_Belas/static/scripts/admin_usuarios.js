const select = document.querySelectorAll('#selecionar');

select.forEach(selected => {
    const updatSelectStyle = () =>{
        selected.addEventListener('change', ()=>{
            const value = selected.value;
            console.log(value);
            
            if (selected.value === 'ativo') {
                const status = document.querySelector('.status');
                status.classList.remove('inativo');
                status.classList.toggle('ativo');
                //alert('ativo');
            }else{
                const status = document.querySelector('.status');
                status.classList.remove('ativo');
                status.classList.toggle('inativo');
                //alert('inativo');
            }

            
        });
    };

    updatSelectStyle();

});