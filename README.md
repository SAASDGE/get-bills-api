# Download de Faturas pela API
Esse código faz o download das faturas por meio da API da Digital Grid.

# Requisitos
* Python 3.8+
* Token da API válido
* Mês e ano de emissão

# Como rodar o código
* Instalar o python 3.8+
* Criar um ambiente virtual e ativá-lo
* Instalar as dependências com o comando "python -m pip install -r requirements.txt"
* Criar um arquivo chamado .env na raiz do projeto
* Copiar e preencher as variáveis do arquivo "contrib/env_sample" para esse novo arquivo
* Executar o comando "python main.py" na raiz do projeto

# Resultado
As faturas serão baixadas no caminho especificado na variável PATH_TO_DOWNLOAD e serão organizados por
agente, ano e mês. Somente serão baixadas faturas que possuam data de emissão.