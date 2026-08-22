import Link from "next/link";
import { Terminal, ArrowLeft } from "lucide-react";

export default function Termos() {
  return (
    <div className="min-h-screen flex flex-col bg-background">
      <header className="border-b border-[#2a2a30] py-4 px-6 flex items-center justify-between bg-background/80 backdrop-blur-md sticky top-0 z-50">
        <Link href="/" className="flex items-center gap-2 text-primary font-bold text-xl hover:opacity-80 transition-opacity">
          <Terminal size={24} />
          <span>TayamaBot</span>
        </Link>
      </header>

      <main className="flex-1 max-w-3xl mx-auto py-16 px-6">
        <Link href="/" className="inline-flex items-center gap-2 text-muted-foreground hover:text-primary transition-colors mb-8 text-sm font-medium">
          <ArrowLeft size={16} /> Voltar para a página inicial
        </Link>

        <h1 className="text-4xl font-bold mb-8 tracking-tight">Termos de Uso</h1>
        
        <div className="space-y-8 text-muted-foreground leading-relaxed">
          
          <section>
            <h2 className="text-2xl font-bold text-foreground mb-4">1. Aceitação do Caos</h2>
            <p>
              Ao convidar a Tayama para o seu servidor e utilizar nossos comandos, você aceita de livre e espontânea vontade que a faculdade é difícil, o código eventualmente quebra e que a Tayama vai te lembrar disso de forma sarcástica. 
              Se você não concorda com isso, recomendamos usar uma agenda de papel.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-foreground mb-4">2. Seus Dados, Suas Lágrimas</h2>
            <p>
              A Tayama salva suas notas, faltas e horas de estudo em um banco de dados local hospedado nos servidores (ou no computador do dono do repositório). 
              Nós <strong>não vendemos seus dados</strong> para ninguém. A única coisa que fazemos com as suas informações é fazer os cálculos para te avisar se você vai rodar por falta ou não. 
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-foreground mb-4">3. Ausência de Garantias (O famoso "Na minha máquina funciona")</h2>
            <p>
              Este bot é fornecido "no estado em que se encontra", sem garantias de qualquer tipo. A Tayama vai calcular a sua média com matemática pura, mas a responsabilidade de ir lá e acertar as questões na prova da FATEC é exclusivamente sua. Não nos responsabilizamos por dependências, reprovações ou commits na sexta-feira.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-foreground mb-4">4. Restrições e Banimentos</h2>
            <p>
              Não tente quebrar o bot, injetar código no <code>/lancar_nota</code> ou floodar requisições. 
              Qualquer tentativa de abuso resultará em um ban permanente da API, e a Tayama vai bloquear o seu ID de usar as funções. Seja um universitário civilizado.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-foreground mb-4">5. Modificações nestes Termos</h2>
            <p>
              Podemos atualizar estas regras amargas sempre que a sanidade pedir. Recomendamos checar esta página ocasionalmente (se você realmente tiver tempo livre sobrando).
            </p>
          </section>

          <p className="pt-8 border-t border-[#2a2a30] text-sm text-center">
            Última atualização: 22 de Agosto de 2026. <br />
            Pega leve, ninguém é de ferro.
          </p>

        </div>
      </main>
    </div>
  );
}
