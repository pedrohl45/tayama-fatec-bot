import { Terminal, GraduationCap, Clock, Music, ArrowRight, Github } from 'lucide-react';

export default function Home() {
  return (
    <>
      <header className="border-b border-[#2a2a30] py-4 px-6 flex items-center justify-between bg-background/80 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-2 text-primary font-bold text-xl">
          <Terminal size={24} />
          <span>TayamaBot</span>
        </div>
        <a 
          href="https://github.com/pedrohl45/tayama-fatec-bot" 
          target="_blank" 
          rel="noopener noreferrer"
          className="text-muted-foreground hover:text-foreground transition-colors"
        >
          <Github size={24} />
        </a>
      </header>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="flex flex-col items-center justify-center text-center py-24 px-4 min-h-[70vh]">
          <div className="w-20 h-20 bg-primary/20 rounded-full flex items-center justify-center mb-6 border border-primary/30">
            <Terminal size={40} className="text-primary" />
          </div>
          
          <h1 className="text-4xl md:text-6xl font-bold mb-4 tracking-tight">
            Bem-vinda, Tayama.
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mb-10">
            Sua assistente acadêmica noturna para a FATEC DSM. <br className="hidden md:block" /> 
            Organize suas notas, acompanhe faltas e faça pausas pro café com uma dose de sarcasmo.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4">
            <a 
              href="#" 
              className="bg-primary text-primary-foreground hover:bg-primary/90 font-bold py-3 px-8 rounded-lg flex items-center gap-2 transition-all shadow-[0_0_20px_rgba(225,29,72,0.3)]"
            >
              Adicionar ao Discord
            </a>
            <a 
              href="#features" 
              className="bg-card text-foreground hover:bg-card/80 border border-[#2a2a30] font-medium py-3 px-8 rounded-lg flex items-center justify-center transition-colors"
            >
              Conhecer Funcionalidades
            </a>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-24 px-6 bg-[#0f0f11] border-t border-[#2a2a30]">
          <div className="max-w-5xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold mb-4">Por que a Tayama?</h2>
              <p className="text-muted-foreground max-w-2xl mx-auto">
                A faculdade cobra caro da sua sanidade. A Tayama automatiza a papelada para você poder focar apenas no código que importa.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-6">
              {/* Feature 1 */}
              <div className="bg-card border border-[#2a2a30] rounded-2xl p-8 hover:border-primary/50 transition-colors">
                <div className="text-primary mb-4">
                  <GraduationCap size={32} />
                </div>
                <h3 className="text-xl font-bold mb-2">Controle Acadêmico</h3>
                <p className="text-muted-foreground text-sm">
                  Cálculo automático de notas mínimas para passar (cálculo FATEC DSM), avisos de limites de falta e grades diárias direto no chat.
                </p>
              </div>

              {/* Feature 2 */}
              <div className="bg-card border border-[#2a2a30] rounded-2xl p-8 hover:border-primary/50 transition-colors">
                <div className="text-primary mb-4">
                  <Clock size={32} />
                </div>
                <h3 className="text-xl font-bold mb-2">Gestão Ágil e Foco</h3>
                <p className="text-muted-foreground text-sm">
                  Registros de estudos, resumos por matéria e visualização de metas e Sprints para que o seu Projeto Integrador não vire um caos.
                </p>
              </div>

              {/* Feature 3 */}
              <div className="bg-card border border-[#2a2a30] rounded-2xl p-8 hover:border-primary/50 transition-colors">
                <div className="text-primary mb-4">
                  <Music size={32} />
                </div>
                <h3 className="text-xl font-bold mb-2">Pausa pro Cigarro</h3>
                <p className="text-muted-foreground text-sm">
                  O código quebrou? Use `/pausa` ou `/som` e deixe a Tayama indicar aquele post-punk ou dar dicas ácidas sobre a vida e a programação.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-24 px-6 text-center">
          <h2 className="text-3xl font-bold mb-4">Pronto para organizar o caos?</h2>
          <p className="text-muted-foreground max-w-xl mx-auto mb-10">
            Adicionar a Tayama ao seu servidor Discord é simples. Se você usa o repositório, faça o clone e ative os comandos de slash imediatamente.
          </p>
          <a 
            href="#" 
            className="inline-flex items-center gap-2 bg-card border border-primary text-primary hover:bg-primary hover:text-primary-foreground font-bold py-3 px-8 rounded-lg transition-all"
          >
            Convide a Tayama
            <ArrowRight size={18} />
          </a>
        </section>
      </main>

      <footer className="border-t border-[#2a2a30] py-8 text-center text-sm text-muted-foreground">
        <p>TayamaBot © 2026 - Pega leve, ninguém é de ferro.</p>
        <div className="flex justify-center gap-4 mt-4">
          <a href="#" className="hover:text-foreground transition-colors">Termos de Uso</a>
          <a href="#" className="hover:text-foreground transition-colors">GitHub</a>
        </div>
      </footer>
    </>
  );
}

