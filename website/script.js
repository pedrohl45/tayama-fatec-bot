// Inicializa os ícones do Lucide
lucide.createIcons();

// Navegação Single Page Application (SPA)
function showPage(pageId) {
    // Esconde todas as páginas
    document.querySelectorAll('.page').forEach(function(p) {
        p.classList.remove('active');
    });
    
    // Mostra a página selecionada
    const targetPage = document.getElementById('page-' + pageId);
    if (targetPage) {
        targetPage.classList.add('active');
    }
    
    // Rola para o topo
    window.scrollTo(0, 0);
}

// Lógica do Audio Player Contínuo
const audio = document.getElementById('bgAudio');
const btn = document.getElementById('audioBtn');
const icon = document.getElementById('audioIcon');
let isPlaying = false;

if (btn && audio && icon) {
    btn.addEventListener('click', function() {
        if (isPlaying) {
            audio.pause();
            btn.classList.remove('playing');
            icon.classList.remove('spin-icon');
        } else {
            audio.volume = 0.4;
            audio.play().catch(function(e) {
                console.log("Autoplay bloqueado pelo navegador", e);
            });
            btn.classList.add('playing');
            icon.classList.add('spin-icon');
        }
        isPlaying = !isPlaying;
    });
}

