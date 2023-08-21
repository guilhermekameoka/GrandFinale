const comecePorAqui = document.getElementById('B1');
const closeButton = document.getElementById('close');
const modal = document.getElementById('modal');
const section1 = document.getElementById('s1');

comecePorAqui.addEventListener("click", function () {
    if (modal.style.display == 'none') {
        modal.style.display = 'block';
        setTimeout(function() { blurEvent(); }, 10)
    }

    else {
        modal.style.display = 'none';
    }
});

closeButton.addEventListener("click", function () {
    if (modal.style.display == 'block') {
        modal.style.display = 'none';
        uncheckBlur();
    } else {
        modal.style.display = 'none';
    }
});

function uncheckBlur() {
    if (section1.style.filter == 'blur(10px)')
        section1.style.filter = 'none'
}

function blurEvent() {
    if (section1.style.filter == 'none') {
        section1.style.filter = 'blur(10px)';
    }
    else {
        section1.style.filter = 'none'
    }
}