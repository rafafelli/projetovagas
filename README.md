# Projeto

## Tecnologias Utilizadas

- **Python 3.9**
- **Django 3.2**

## Inicialização do Projeto

### Requisitos

- Python 3.9
- Pip (gerenciador de pacotes do Python)

### Instalação e Configuração

1. **Crie o ambiente virtual**: `python3 -m venv venv`
2. **Instale as Dependências**: `pip install -r requirements.txt`
3. **Configure o Banco de Dados**: `python manage.py makemigrations`
4. **Migre o Banco de Dados**: `python manage.py migrate`
5. **Execute o Servidor de Desenvolvimento**: `python manage.py runserver`
6. **Acesse a Aplicação**: Abra o navegador e acesse `http://localhost:8000/.`.

Agora, o projeto deve estar em execução em seu ambiente de desenvolvimento local.

### Funcionalidades

Agora, basta criar uma conta do tipo Empresa para criar as Vagas dentro do sistema. E após utilizar das funções nas duas perspectivas de cadastro (Candidato e Empresa):

#### Perspectiva do Candidato

- **Buscar Vagas**: É possível filtrar vagas de acordo com os requisitos, e visualizar as vagas de todas as empresas.
- **Aplicar-se**: É possível aplicar a todas as vagas, independente do perfil do candidato.
- **Visualizar Vagas Aplicadas**: Possibilidade de visualizar somente as vagas apliacadas, assim como cancelar a aplicação nas mesmas.

#### Perspectiva da Empresa

- **Publicar Vagas**: Criação de Vagas.
- **Editar Vagas**: Possibilidade de editar as vagas.
- **Excluir Vagas**: Possibilidade de excluir as vagas.
- **Visualizar**: Visualizar vagas criadas.
- **Pontuação de Candidato**: Dentro de cada vaga, é possível visualizar uma pontuação do candidato baseando-se em informações de pretensão salarial e escolaridade mínima.
- **Relatório**: Relatórios de Vagas Criadas Por Mês e Candidatos Recebidos Por Mês.

