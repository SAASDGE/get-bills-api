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
agente, ano e mês. 

As faturas pertencentes aos agentes 43 e 55 serão baixadas com base na data de emissão (registro do banco), conforme informada nas chaves ISSUED_AT_MONTH e ISSUED_AT_YEAR. Por exemplo, se as chaves ISSUED_AT_MONTH e ISSUED_AT_YEAR forem 8 e 2023, serão baixadas as faturas com data de emissão em 08/2023.

As faturas do agente 65 serão baixadas de acordo com a data de referência da distribuidora. Já que este agente ainda não tem conexão com o banco. Por exemplo, se o ISSUED_AT_MONTH e ISSUED_AT_YEAR forem 8 e 2023, respectivamente, serão baixadas faturas com o mês de referência de 08/2023.
