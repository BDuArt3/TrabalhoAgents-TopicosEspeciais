"""
Contador de tokens para rastreamento de uso
"""
from datetime import datetime
import json


class TokenCounter:
    """Classe para contar e rastrear tokens"""
    
    def __init__(self):
        """Inicializa o contador de tokens"""
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_calls = 0
        self.start_time = datetime.now()
    
    def add_tokens(self, input_tokens: int, output_tokens: int):
        """
        Adiciona tokens ao contador
        
        Args:
            input_tokens: Número de tokens de entrada
            output_tokens: Número de tokens de saída
        """
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_calls += 1
    
    def get_stats(self) -> dict:
        """
        Retorna estatísticas de tokens
        
        Returns:
            Dicionário com estatísticas
        """
        total_tokens = self.total_input_tokens + self.total_output_tokens
        elapsed_time = (datetime.now() - self.start_time).total_seconds()
        
        return {
            "total_calls": self.total_calls,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": total_tokens,
            "elapsed_seconds": elapsed_time,
            "avg_tokens_per_call": total_tokens / self.total_calls if self.total_calls > 0 else 0
        }
    
    def reset(self):
        """Reseta todos os contadores"""
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_calls = 0
        self.start_time = datetime.now()
    
    def print_stats(self):
        """Imprime as estatísticas de forma formatada"""
        stats = self.get_stats()
        print("\n" + "="*50)
        print("📊 ESTATÍSTICAS DE TOKENS")
        print("="*50)
        print(f"Total de chamadas: {stats['total_calls']}")
        print(f"Tokens de entrada: {stats['total_input_tokens']}")
        print(f"Tokens de saída: {stats['total_output_tokens']}")
        print(f"Total de tokens: {stats['total_tokens']}")
        print(f"Tempo decorrido: {stats['elapsed_seconds']:.2f}s")
        print(f"Média tokens/chamada: {stats['avg_tokens_per_call']:.2f}")
        print("="*50 + "\n")
