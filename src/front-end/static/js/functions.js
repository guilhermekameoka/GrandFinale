const comecePorAqui = document.getElementById('B1');
const closeButton = document.getElementById('close');
const modal = document.getElementById('modal');


comecePorAqui.addEventListener("click", function(){
    console.log('visibility');

    if (modal.style.display == 'none') {
        modal.style.display = 'block';
    } else{
        modal.style.display = 'none';
    }   
});

closeButton.addEventListener("click", function(){
    console.log('close');

    if (modal.style.display == 'block') {
        modal.style.display = 'none';
    } else{
        modal.style.display = 'none';
    }  
});