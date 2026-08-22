// Inicializa os ícones do Lucide
lucide.createIcons();

// Navegação Single Page Application (SPA) com Rotas Virtuais
function showPage(pageId) {
    // Atualiza a URL sem recarregar a página
    const newPath = pageId === 'home' ? '/' : '/' + pageId;
    window.history.pushState({ pageId: pageId }, "", newPath);

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

// Lida com botões de voltar/avançar do navegador
window.addEventListener('popstate', function(e) {
    const pageId = e.state ? e.state.pageId : 'home';
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById('page-' + pageId).classList.add('active');
});

// Lê a URL atual ao carregar a página para abrir direto nos Termos ou Privacidade
window.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    if (path.includes('termos')) {
        showPage('termos');
    } else if (path.includes('privacidade')) {
        showPage('privacidade');
    } else {
        // Se for / ou qualquer outra coisa, exibe a home mas não dá pushState pra não bugar o histórico
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById('page-home').classList.add('active');
    }
});
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

