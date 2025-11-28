#!/usr/bin/env python3
"""
GitHub Assistant - Assistente de IA para repositórios GitHub
Desenvolvido para: Trabalho de Tópicos Especiais - 8º período
"""
import os
import sys
from dotenv import load_dotenv
from agents.github_agent import GitHubAgent

# Carregar variáveis de ambiente
load_dotenv()


def print_header():
    """Imprime o cabeçalho da aplicação"""
    print("\n" + "="*60)
    print("🤖 GITHUB ASSISTANT - Assistente de IA para GitHub")
    print("="*60)
    print("Desenvolvido para: Trabalho de Tópicos Especiais - 8º período")
    print("="*60 + "\n")


def print_help():
    """Imprime a mensagem de ajuda"""
    print("\n📋 COMANDOS DISPONÍVEIS:")
    print("-" * 60)
    print("  • Faça perguntas sobre o repositório GitHub")
    print("  • 'issues' ou 'issues abertas' - Lista issues abertas")
    print("  • 'issue #N' - Detalhes de uma issue específica")
    print("  • 'pull requests' - Lista PRs abertos")
    print("  • 'commits' - Mostra commits recentes")
    print("  • 'info' - Informações do repositório")
    print("  • 'tokens' - Mostra estatísticas de tokens")
    print("  • 'limpar' - Reseta estatísticas de tokens")
    print("  • 'ajuda' - Mostra esta mensagem")
    print("  • 'sair' ou 'exit' - Encerra o programa")
    print("-" * 60 + "\n")


def process_command(agent: GitHubAgent, user_input: str) -> bool:
    """
    Processa um comando do usuário
    
    Args:
        agent: Instância do agente GitHub
        user_input: Comando do usuário
    
    Returns:
        False se deve encerrar, True para continuar
    """
    user_input = user_input.strip().lower()
    
    if not user_input:
        return True
    
    # Comandos de controle
    if user_input in ["sair", "exit", "quit"]:
        print("\n👋 Encerrando. Até logo!")
        return False
    
    if user_input == "ajuda":
        print_help()
        return True
    
    if user_input == "tokens":
        stats = agent.get_token_stats()
        agent.token_counter.print_stats()
        return True
    
    if user_input == "limpar":
        agent.reset_token_counter()
        print("✅ Contador de tokens resetado!")
        return True
    
    # Processar queries com o agente
    print("\n🤔 Processando sua pergunta...")
    try:
        # Mapear comandos conhecidos para queries do agente
        if user_input in ["issues", "issues abertas"]:
            query = "Quais são as issues abertas no repositório?"
        elif user_input == "pull requests" or user_input == "prs":
            query = "Liste todos os pull requests abertos"
        elif user_input == "commits":
            query = "Quais foram os commits recentes?"
        elif user_input == "info":
            query = "Me dê informações gerais do repositório"
        elif user_input.startswith("issue #"):
            issue_num = user_input.replace("issue #", "").strip()
            query = f"Mostrar detalhes da issue número {issue_num}"
        else:
            query = user_input
        
        response = agent.process_query(query)
        print(f"\n✅ Resposta:\n{response}\n")
    except Exception as e:
        print(f"❌ Erro: {str(e)}\n")
    
    return True


def main():
    """Função principal"""
    print_header()
    
    # Validar configuração
    if not os.getenv("GITHUB_APP_ID"):
        print("❌ Erro: GITHUB_APP_ID não configurado no arquivo .env")
        print("📝 Por favor, configure seu GitHub token no arquivo .env")
        return
    
    if not os.getenv("GITHUB_REPOSITORY"):
        print("❌ Erro: GITHUB_REPOSITORY não configurado no arquivo .env")
        return
    
    # Testar conexão com Azure OpenAI
    print("🔗 Testando conexão com Azure OpenAI...")
    try:
        from litellm import completion
        response = completion(
            model="azure/gpt-5-mini",
            messages=[{"role": "user", "content": "Olá, você está funcionando?"}]
        )
        print("✅ Conexão com Azure OpenAI estabelecida!\n")
    except Exception as e:
        print(f"❌ Erro ao conectar com Azure OpenAI: {str(e)}\n")
        print("⚠️  Por favor, verifique suas credenciais do Azure no arquivo .env\n")
        return
    
    # Inicializar agente
    try:
        print("🚀 Inicializando agente GitHub...")
        agent = GitHubAgent()
        print("✅ Agente GitHub inicializado com sucesso!\n")
    except Exception as e:
        print(f"❌ Erro ao inicializar agente: {str(e)}\n")
        return
    
    # Loop interativo
    print_help()
    
    while True:
        try:
            user_input = input("💬 Você: ").strip()
            if not process_command(agent, user_input):
                break
        except KeyboardInterrupt:
            print("\n\n👋 Interrupção do usuário. Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {str(e)}\n")


if __name__ == "__main__":
    main()

