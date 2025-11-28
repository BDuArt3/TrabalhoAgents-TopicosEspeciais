"""
Ferramentas para interação com a API do GitHub
"""
from github import Github
import os
from typing import Optional, List, Dict, Any


class GitHubTools:
    """Classe para gerenciar ferramentas do GitHub"""
    
    def __init__(self, token: str, repo_name: str):
        """
        Inicializa o GitHubTools
        
        Args:
            token: Token de autenticação do GitHub
            repo_name: Nome do repositório (ex: owner/repo)
        """
        self.token = token
        self.repo_name = repo_name
        self.github = Github(token)
        self.repo = self.github.get_repo(repo_name)
    
    def get_issues(self, state: str = "open") -> List[Dict[str, Any]]:
        """
        Obtém issues do repositório
        
        Args:
            state: "open", "closed" ou "all"
        
        Returns:
            Lista de issues com informações relevantes
        """
        try:
            issues = self.repo.get_issues(state=state)
            result = []
            for issue in issues:
                result.append({
                    "id": issue.number,
                    "title": issue.title,
                    "state": issue.state,
                    "created_at": str(issue.created_at),
                    "body": issue.body[:200] if issue.body else "Sem descrição"
                })
            return result
        except Exception as e:
            return [{"error": str(e)}]
    
    def get_issue_details(self, issue_number: int) -> Dict[str, Any]:
        """
        Obtém detalhes de uma issue específica
        
        Args:
            issue_number: Número da issue
        
        Returns:
            Dicionário com detalhes da issue
        """
        try:
            issue = self.repo.get_issue(issue_number)
            return {
                "id": issue.number,
                "title": issue.title,
                "state": issue.state,
                "body": issue.body,
                "created_at": str(issue.created_at),
                "updated_at": str(issue.updated_at),
                "user": issue.user.login,
                "comments_count": issue.comments,
                "labels": [label.name for label in issue.labels]
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_pull_requests(self, state: str = "open") -> List[Dict[str, Any]]:
        """
        Obtém pull requests do repositório
        
        Args:
            state: "open", "closed" ou "all"
        
        Returns:
            Lista de pull requests
        """
        try:
            prs = self.repo.get_pulls(state=state)
            result = []
            for pr in prs:
                result.append({
                    "id": pr.number,
                    "title": pr.title,
                    "state": pr.state,
                    "created_at": str(pr.created_at),
                    "user": pr.user.login,
                    "body": pr.body[:200] if pr.body else "Sem descrição"
                })
            return result
        except Exception as e:
            return [{"error": str(e)}]
    
    def comment_on_issue(self, issue_number: int, comment: str) -> Dict[str, Any]:
        """
        Adiciona um comentário em uma issue
        
        Args:
            issue_number: Número da issue
            comment: Texto do comentário
        
        Returns:
            Resultado da operação
        """
        try:
            issue = self.repo.get_issue(issue_number)
            comment_obj = issue.create_comment(comment)
            return {
                "success": True,
                "comment_id": comment_obj.id,
                "message": f"Comentário adicionado à issue #{issue_number}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_commits(self, branch: str = "main", limit: int = 10) -> List[Dict[str, Any]]:
        """
        Obtém commits recentes do repositório
        
        Args:
            branch: Nome da branch
            limit: Número máximo de commits
        
        Returns:
            Lista de commits
        """
        try:
            commits = self.repo.get_commits(sha=branch)
            result = []
            for i, commit in enumerate(commits):
                if i >= limit:
                    break
                result.append({
                    "sha": commit.sha[:7],
                    "message": commit.commit.message.split('\n')[0],
                    "author": commit.commit.author.name,
                    "date": str(commit.commit.author.date),
                    "url": commit.html_url
                })
            return result
        except Exception as e:
            return [{"error": str(e)}]
    
    def get_repository_info(self) -> Dict[str, Any]:
        """
        Obtém informações gerais do repositório
        
        Returns:
            Dicionário com informações do repositório
        """
        try:
            return {
                "name": self.repo.name,
                "full_name": self.repo.full_name,
                "description": self.repo.description,
                "stars": self.repo.stargazers_count,
                "forks": self.repo.forks_count,
                "open_issues": self.repo.open_issues_count,
                "language": self.repo.language,
                "url": self.repo.html_url
            }
        except Exception as e:
            return {"error": str(e)}
