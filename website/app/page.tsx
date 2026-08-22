import Image from 'next/image';
import { Terminal, GraduationCap, Clock, Music, ArrowRight, Github } from 'lucide-react';

export default function Home() {
  const INVITE_LINK = "https://discord.com/oauth2/authorize?client_id=1540221236821364788&permissions=8&scope=bot%20applications.commands";

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
          
          <div className="relative mb-8 flex justify-center items-center">
            {/* Glow vermelho animado no fundo */}
            <div className="absolute inset-0 bg-primary/30 rounded-full blur-2xl animate-pulse scale-125"></div>
            {/* Container da Imagem */}
            <div className="relative w-48 h-48 md:w-56 md:h-56 rounded-full overflow-hidden border-4 border-primary shadow-[0_0_40px_rgba(200,34,69,0.8)] z-10">
              <Image 
                src="/tayama.jpg" 
                alt="Avatar da Tayama" 
                fill
                quality={100}
                className="object-cover"
                priority
              />
            </div>
          </div>
          
          <h1 className="text-4xl md:text-6xl font-bold mb-4 tracking-tight">
            Bem-vinda, Tayama.
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mb-10 relative z-10">
            Sua assistente acadêmica noturna e de produtividade. <br className="hidden md:block" /> 
            Organize suas notas, acompanhe faltas e faça pausas pro café com uma dose de sarcasmo.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4">
            <a 
              href={INVITE_LINK} 
              target="_blank"
              rel="noopener noreferrer"
              className="bg-primary text-primary-foreground hover:bg-primary/90 font-bold py-3 px-8 rounded-lg flex items-center justify-center gap-2 transition-all shadow-[0_0_20px_rgba(200,34,69,0.3)]"
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
                A faculdade cobra caro da sua sanidade. A Tayama automatiza a papelada para você poder focar no que importa.
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
                  Cálculo automático de notas mínimas para aprovação, acompanhamento inteligente de limites de faltas e alertas diários direto no chat.
                </p>
              </div>

              {/* Feature 2 */}
              <div className="bg-card border border-[#2a2a30] rounded-2xl p-8 hover:border-primary/50 transition-colors">
                <div className="text-primary mb-4">
                  <Clock size={32} />
                </div>
                <h3 className="text-xl font-bold mb-2">Gestão Ágil e Foco</h3>
                <p className="text-muted-foreground text-sm">
                  Registro focado de horas de estudo e metodologias para manter seus projetos integradores e trabalhos acadêmicos sob total controle.
                </p>
              </div>

              {/* Feature 3 */}
              <div className="bg-card border border-[#2a2a30] rounded-2xl p-8 hover:border-primary/50 transition-colors">
                <div className="text-primary mb-4">
                  <Music size={32} />
                </div>
                <h3 className="text-xl font-bold mb-2">Pausa pro Cigarro</h3>
                <p className="text-muted-foreground text-sm">
                  Cansou de debugar a vida? Use `/pausa` ou `/som` e deixe a Tayama indicar aquele post-punk ou dar dicas ácidas para você relaxar.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-24 px-6 text-center">
          <h2 className="text-3xl font-bold mb-4">Pronto para organizar o caos?</h2>
          <p className="text-muted-foreground max-w-xl mx-auto mb-10">
            Adicione a Tayama ao seu servidor e comece a controlar sua vida acadêmica com eficiência e estilo.
          </p>
          <a 
            href={INVITE_LINK} 
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center gap-2 bg-card border border-primary text-primary hover:bg-primary hover:text-primary-foreground font-bold py-3 px-8 rounded-lg transition-all"
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
          <a href="https://github.com/pedrohl45/tayama-fatec-bot" target="_blank" rel="noopener noreferrer" className="hover:text-foreground transition-colors">GitHub</a>
        </div>
      </footer>
    </>
  );
}
