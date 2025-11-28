"""
Agente GitHub usando LiteLLM
"""
from litellm import completion
import json
from tools.github_tools import GitHubTools
from memory.token_counter import TokenCounter
import os
from dotenv import load_dotenv

load_dotenv()


class GitHubAgent:
    """Agente de IA para interagir com GitHub"""
    
    def __init__(self):
        """Inicializa o agente GitHub"""
        self.github_token = os.getenv("GITHUB_APP_ID")
        self.repo_name = os.getenv("GITHUB_REPOSITORY")
        self.token_counter = TokenCounter()
        
        if not self.github_token or not self.repo_name:
            raise ValueError("GITHUB_APP_ID e GITHUB_REPOSITORY devem estar configurados no .env")
        
        self.github_tools = GitHubTools(self.github_token, self.repo_name)
    
    def _format_response(self, result):
        """Formata a resposta das ferramentas"""
        if isinstance(result, list):
            return json.dumps(result, ensure_ascii=False, indent=2)
        return str(result)
    
    def get_available_tools(self):
        """Retorna descrições das ferramentas disponíveis"""
        return {
            "get_issues": "Obtém issues do repositório. State pode ser 'open', 'closed' ou 'all'",
            "get_issue_details": "Obtém detalhes de uma issue específica. Requer o número da issue",
            "get_pull_requests": "Obtém pull requests do repositório",
            "get_commits": "Obtém commits recentes da branch especificada",
            "get_repository_info": "Obtém informações gerais do repositório",
            "comment_on_issue": "Adiciona um comentário em uma issue"
        }
    
    def _handle_github_request(self, request_type: str, **kwargs) -> str:
        """
        Processa requisições do GitHub
        
        Args:
            request_type: Tipo de requisição
            **kwargs: Argumentos específicos
        
        Returns:
            Resultado formatado
        """
        try:
            if request_type == "issues":
                state = kwargs.get("state", "open")
                result = self.github_tools.get_issues(state)
            elif request_type == "issue_details":
                issue_number = kwargs.get("issue_number", 0)
                result = self.github_tools.get_issue_details(issue_number)
            elif request_type == "pull_requests":
                state = kwargs.get("state", "open")
                result = self.github_tools.get_pull_requests(state)
            elif request_type == "commits":
                branch = kwargs.get("branch", "main")
                result = self.github_tools.get_commits(branch)
            elif request_type == "repository_info":
                result = self.github_tools.get_repository_info()
            else:
                result = {"error": "Tipo de requisição desconhecido"}
            
            return self._format_response(result)
        except Exception as e:
            return f"Erro ao processar requisição: {str(e)}"
    
    def process_query(self, query: str) -> str:
        """
        Processa uma consulta do usuário
        
        Args:
            query: Pergunta do usuário
        
        Returns:
            Resposta do agente
        """
        try:
            # Detectar tipo de query e buscar dados do GitHub
            query_lower = query.lower()
            
            context = ""
            if "issue" in query_lower and "#" in query_lower:
                # Extrair número da issue
                import re
                match = re.search(r'#(\d+)', query)
                if match:
                    issue_num = int(match.group(1))
                    context = f"\n\nDados da issue:\n{self._handle_github_request('issue_details', issue_number=issue_num)}"
            elif "issue" in query_lower or "problema" in query_lower:
                context = f"\n\nDados das issues:\n{self._handle_github_request('issues')}"
            elif "pull request" in query_lower or "pr" in query_lower or "merge" in query_lower:
                context = f"\n\nDados dos PRs:\n{self._handle_github_request('pull_requests')}"
            elif "commit" in query_lower:
                context = f"\n\nDados dos commits:\n{self._handle_github_request('commits')}"
            elif "repositório" in query_lower or "info" in query_lower:
                context = f"\n\nDados do repositório:\n{self._handle_github_request('repository_info')}"
            
            # Usar completion do litellm para processar a query
            system_prompt = """Você é um assistente para repositórios GitHub especializado em ajudar desenvolvedores.
            Você tem acesso a informações do repositório e pode analisar issues, pull requests e commits.
            Forneça respostas claras, bem formatadas e úteis em português."""
            
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"{query}{context}" if context else query
                }
            ]
            
            response = completion(
                model="azure/gpt-5-mini",
                messages=messages
            )
            
            # Contar tokens
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            self.token_counter.add_tokens(prompt_tokens, completion_tokens)
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Erro ao processar query: {str(e)}"
    
    def get_token_stats(self) -> dict:
        """Retorna estatísticas de uso de tokens"""
        return self.token_counter.get_stats()
    
    def reset_token_counter(self):
        """Reseta o contador de tokens"""
        self.token_counter.reset()
