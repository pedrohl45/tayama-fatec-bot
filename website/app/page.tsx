'use client';

import Image from 'next/image';
import Link from 'next/link';
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
        <section className="relative flex flex-col items-center justify-center text-center py-32 px-4 min-h-[85vh] overflow-hidden">
          
          {/* Fundo Supermercado */}
          <div className="absolute inset-0 z-0 bg-[url('/supermarket.jpg')] bg-cover bg-center opacity-40"></div>
          {/* Degradê sobre o fundo */}
          <div className="absolute inset-0 z-0 bg-gradient-to-t from-background via-background/80 to-background/30"></div>

          <div className="relative mb-8 flex justify-center items-center z-10">
            <div className="absolute inset-0 bg-primary/40 rounded-full blur-3xl animate-pulse scale-125"></div>
            <div className="relative w-56 h-56 md:w-64 md:h-64 rounded-full overflow-hidden border-4 border-primary shadow-[0_0_50px_rgba(200,34,69,0.7)]">
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
          
          <h1 className="text-5xl md:text-7xl font-bold mb-4 tracking-tight z-10 drop-shadow-lg">
            Bem-vinda, Tayama.
          </h1>
          <p className="text-lg md:text-2xl text-muted-foreground max-w-2xl mb-12 relative z-10 drop-shadow-md">
            Sua assistente acadêmica noturna e de produtividade. <br className="hidden md:block" /> 
            Organize suas notas, acompanhe faltas e faça pausas pro café com uma dose de sarcasmo.
          </p>
          
          <div className="relative z-10 flex flex-col sm:flex-row gap-4">
            <a 
              href={INVITE_LINK} 
              target="_blank"
              rel="noopener noreferrer"
              className="bg-primary text-primary-foreground hover:bg-primary/90 font-bold py-3 px-8 rounded-lg flex items-center justify-center gap-2 transition-all shadow-[0_0_20px_rgba(200,34,69,0.3)]"
            >
              Adicionar ao Discord
            </a>
            <a 
              href="#tutorial" 
              className="bg-card text-foreground hover:bg-card/80 border border-[#2a2a30] font-medium py-3 px-8 rounded-lg flex items-center justify-center transition-colors"
            >
              Como Começar
            </a>
          </div>
        </section>

        {/* Tutorial Section */}
        <section id="tutorial" className="py-24 px-6 border-t border-[#2a2a30]">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-4 text-primary tracking-tight">Manual de Sobrevivência</h2>
              <p className="text-muted-foreground text-lg">Leia se quiser. Se não ler, não chore quando reprovar por falta no final do semestre.</p>
            </div>

            <div className="space-y-12">
              <div className="flex flex-col md:flex-row gap-6 items-start group">
                <div className="w-14 h-14 shrink-0 bg-[#0a0a0c] text-primary rounded-xl flex items-center justify-center font-black text-2xl border border-[#2a2a30] group-hover:border-primary/50 group-hover:bg-primary/10 transition-all shadow-lg">1</div>
                <div>
                  <h3 className="text-2xl font-bold mb-3 text-foreground/90">A Burocracia Inicial</h3>
                  <p className="text-muted-foreground leading-relaxed">
                    A FATEC não vai adivinhar quem você é. Vá até o servidor, digite <code>/perfil_setup</code> e me deixe criar um espaço isolado no servidor para documentar os seus futuros fracassos (ou notas azuis, se você for do tipo estudioso). 
                    Depois rode <code>/materias</code> pra encarar de frente o tamanho do problema que é a sua grade desse semestre.
                  </p>
                </div>
              </div>

              <div className="flex flex-col md:flex-row gap-6 items-start group">
                <div className="w-14 h-14 shrink-0 bg-[#0a0a0c] text-primary rounded-xl flex items-center justify-center font-black text-2xl border border-[#2a2a30] group-hover:border-primary/50 group-hover:bg-primary/10 transition-all shadow-lg">2</div>
                <div>
                  <h3 className="text-2xl font-bold mb-3 text-foreground/90">Controle de Danos</h3>
                  <p className="text-muted-foreground leading-relaxed">
                    Decidiu ficar em casa dormindo em vez de ir pra aula de Engenharia de Software? A vida é sua. Mas tenha a decência de avisar o sistema rodando <code>/lancar_falta</code>. 
                    Pegou o resultado da prova? Registre com <code>/lancar_nota</code>. Quando o desespero bater forte em novembro, digite <code>/media_necessaria</code> e eu calculo matematicamente qual milagre você precisa realizar na P2.
                  </p>
                </div>
              </div>

              <div className="flex flex-col md:flex-row gap-6 items-start group">
                <div className="w-14 h-14 shrink-0 bg-[#0a0a0c] text-primary rounded-xl flex items-center justify-center font-black text-2xl border border-[#2a2a30] group-hover:border-primary/50 group-hover:bg-primary/10 transition-all shadow-lg">3</div>
                <div>
                  <h3 className="text-2xl font-bold mb-3 text-foreground/90">A Área de Fumantes</h3>
                  <p className="text-muted-foreground leading-relaxed">
                    Ninguém aguenta codar 12 horas seguidas num projeto integrador que nem o professor entende. 
                    Quando sua sanidade piscar na reserva, digite <code>/som</code> que eu te receito um Post-Punk absurdo para recuperar o foco, ou roda <code>/pausa</code> para ouvir umas verdades amargas enquanto seu café esfria.
                  </p>
                </div>
              </div>
            </div>
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
        <section className="py-24 px-6 text-center border-t border-[#2a2a30]">
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

      <footer className="border-t border-[#2a2a30] py-8 text-center text-sm text-muted-foreground bg-[#0a0a0a]">
        <p>TayamaBot © 2026 - Pega leve, ninguém é de ferro.</p>
        <div className="flex justify-center gap-4 mt-4">
          <Link href="/termos" className="hover:text-foreground transition-colors">Termos de Uso</Link>
          <a href="https://github.com/pedrohl45/tayama-fatec-bot" target="_blank" rel="noopener noreferrer" className="hover:text-foreground transition-colors">GitHub</a>
        </div>
      </footer>
    </>
  );
}
