# GitHub Assistant - Trabalho de Agentes de IA

## 📋 Descrição

Este projeto implementa um **Assistente de IA para repositórios GitHub** usando LangChain e Azure OpenAI.

**Desenvolvido para:** Trabalho de Tópicos Especiais - 8º período  
**Professor:** Me. Alexandre Alves  
**Data:** 28/11/2025

## 🎯 Funcionalidades

O agente pode:
- ✅ Buscar issues em repositórios GitHub
- ✅ Obter detalhes de issues específicas
- ✅ Listar pull requests (abertos, fechados ou todos)
- ✅ Comentar em issues
- ✅ Responder perguntas sobre commits e informações do repositório
- ✅ **Rastrear uso de tokens** (requisito obrigatório)

## 🛠️ Tecnologias Utilizadas

- **LangChain**: Framework para desenvolvimento de agentes de IA
- **LiteLLM**: Integração unificada com diversos provedores de LLM
- **Azure OpenAI**: Provedor do modelo GPT-4o-mini
- **PyGithub**: Biblioteca para interação com a API do GitHub
- **Python-dotenv**: Gerenciamento de variáveis de ambiente

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/TrabalhoAgents-TopicosEspeciais.git
cd TrabalhoAgents-TopicosEspeciais
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # Linux/Mac
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
copy .env.example .env  # Windows
# ou
cp .env.example .env  # Linux/Mac
```

Edite o arquivo `.env` e configure:

#### **Azure OpenAI** (já configurado)
- `AZURE_API_KEY`: Chave da API do Azure OpenAI
- `AZURE_API_BASE`: URL base do serviço Azure OpenAI
- `AZURE_API_VERSION`: Versão da API

#### **GitHub Token** (você precisa criar)

1. Acesse: https://github.com/settings/tokens
2. Clique em "Generate new token (classic)"
3. Dê um nome ao token (ex: "GitHub Assistant")
4. Selecione as seguintes permissões:
   - ✅ `repo` (acesso completo a repositórios privados)
   - ✅ `read:org` (leitura de organizações)
   - ✅ `read:user` (leitura de perfil de usuário)
   - ✅ `read:discussion` (leitura de discussões)
5. Clique em "Generate token"
6. **IMPORTANTE:** Copie o token imediatamente (você não poderá vê-lo novamente!)
7. Cole o token no arquivo `.env` na variável `GITHUB_APP_ID`

Exemplo do `.env`:
```env
AZURE_API_KEY=
AZURE_API_BASE=https://seu-recurso.openai.azure.com/
AZURE_API_VERSION=2024-08-01-preview

GITHUB_APP_ID=
GITHUB_REPOSITORY=seu-usuario/seu-repositorio
```

## 🚀 Como Usar

Execute o assistente:

```bash
python main.py
```

### Comandos Disponíveis

- Digite perguntas sobre o repositório GitHub
- `tokens`: Mostra estatísticas de uso de tokens
- `limpar`: Reseta as estatísticas de tokens
- `sair` ou `exit`: Encerra o programa

### Exemplos de Perguntas

```
💬 Você: Quais são as issues abertas no repositório?
💬 Você: Me mostre detalhes da issue #5
💬 Você: Liste todos os pull requests fechados
💬 Você: Quais commits foram feitos recentemente?
```

## 📁 Estrutura do Projeto

```
TrabalhoAgents-TopicosEspeciais/
├── agents/
│   └── github_agent.py       # Agente principal
├── config/
│   └── settings.py            # Configurações e variáveis de ambiente
├── memory/
│   └── token_counter.py       # Rastreador de tokens
├── models/
│   └── llm_wrapper.py         # Wrapper do Azure OpenAI
├── tools/
│   └── github_tools.py        # Ferramentas do GitHub
├── .env                        # Variáveis de ambiente (não versionado)
├── .env.example                # Exemplo de configuração
├── .gitignore
├── main.py                     # Aplicação principal
├── requirements.txt            # Dependências
└── README.md                   # Este arquivo
```

## 🧪 Testando o Agente

Após configurar o GitHub token, teste se está funcionando:

```bash
python main.py
```

O assistente deve inicializar e você poderá fazer perguntas sobre seu repositório.

## 📊 Rastreamento de Tokens

O sistema rastreia automaticamente:
- Total de chamadas ao modelo
- Tokens de entrada (input)
- Tokens de saída (output)
- Total de tokens utilizados

Use o comando `tokens` durante a execução para ver as estatísticas.

## 🔍 Troubleshooting

### Erro: "GITHUB_APP_ID faltando"
- Verifique se você criou o token no GitHub
- Certifique-se de que copiou o token para o arquivo `.env`
- Confirme que a variável se chama `GITHUB_APP_ID` no `.env`

### Erro de autenticação do GitHub
- Verifique se o token tem as permissões corretas
- Tente gerar um novo token

### Erro do Azure OpenAI
- As credenciais do Azure já estão configuradas
- Se houver erro, verifique se o serviço está ativo no Azure

## 👥 Grupo

- [Nome do integrante 1]
- [Nome do integrante 2]
- [Nome do integrante 3]

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais.
