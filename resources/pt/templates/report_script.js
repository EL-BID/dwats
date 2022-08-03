function onPageLoad() {
    try {
        // Se não ver mudanças ao mudar e compilar esse script, tente reiniciar o QGIS.
        let a4PaperHeight = 2480;
        let pages = document.querySelectorAll('.page');
        for (let i = 0; i < pages.length - 1; i++) {
            let page = pages[i];
            let margin = (a4PaperHeight - page.clientHeight);
            page.style.marginBottom = margin + "px";
        }
    } catch (e) {
        console.log(e);
    }
}

document.addEventListener('DOMContentLoaded', onPageLoad, false);
