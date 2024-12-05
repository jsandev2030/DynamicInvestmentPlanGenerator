# Calculadora de Ganhos com Dividendos para Investidores

Este projeto é uma ferramenta automatizada desenvolvida em Python para calcular o tempo necessário para atingir um 
objetivo de ganho mensal com dividendos de ações. 

O script realiza a coleta de informações financeiras de ações de uma página da web e calcula os dividendos que o 
usuário receberia com base em aportes mensais. 

Além disso, é capaz de fornecer uma estimativa do tempo necessário para 
alcançar esse objetivo de ganho mensal, considerando a cotação das ações, dividendos anuais e aportes mensais.

## Funcionalidades

1. **Verificação de Permissões de Automação:** O script verifica se a automação é permitida no site da ação, através da análise do arquivo `robots.txt`.
2. **Coleta de Informações:** O script coleta informações sobre o preço da ação e o dividendo anual diretamente de uma página web.
3. **Cálculos de Ganho Mensal:** O usuário define quanto deseja ganhar por mês com dividendos e quanto deseja investir mensalmente. O script calcula quanto tempo será necessário para atingir esse objetivo.
4. **Conversão de Moeda:** O script converte os valores para euro (EUR) utilizando a taxa de câmbio atual entre o dólar (USD) e o euro.
5. **Exibição dos Resultados:** O tempo necessário para atingir o objetivo é exibido, juntamente com a quantidade de ações adquiridas e o investimento excedente.

## Tecnologias Utilizadas

- **Python** 3.x
- **Selenium:** Para automação de navegação na web.
- **Requests:** Para fazer requisições HTTP e acessar o arquivo `robots.txt` dos sites.
- **WebDriverManager:** Para gerenciar o driver do navegador (Chrome).
- **re (expressões regulares):** Para manipulação de strings.
- **datetime:** Para manipulação e exibição de datas e horários.

## Requisitos

Antes de rodar o script, certifique-se de ter os seguintes pacotes instalados:

1. Python 3.x
2. Bibliotecas Python necessárias (via `pip`):
   - `selenium`
   - `requests`
   - `webdriver-manager`
   
   Você pode instalar essas dependências utilizando o comando:
```bash
pip install selenium requests webdriver-manager
```

2. Executar o Script

Execute o script Python utilizando o seguinte comando:
```bash
python nome_do_arquivo.py
```

O script irá pedir que você insira os seguintes dados:

  - Valor que deseja ganhar por mês em dividendos (€): O valor que você deseja alcançar mensalmente com os dividendos das ações.
  - Aporte mensal (€): O valor que você irá investir a cada mês em ações.

O script então irá calcular o tempo necessário para atingir o objetivo de ganho mensal com dividendos e fornecer informações sobre o número de ações adquiridas, o valor excedente e o total investido.

3. Obter os Resultados
Após inserir os dados, o script exibirá:

   - O tempo necessário para alcançar o objetivo de dividendos.
   - A quantidade de ações que você adquirirá mensalmente com o aporte informado.
   - O investimento excedente mensal (se houver).
   - O total de ações adquiridas durante o processo.

### Exemplo de Saída
```bash
04/12/2024 10:30:15
------------------------------------------------------------
Ação: ABC Inc.
Valor por unidade: 150.00 USD
Dividendo anual: 5.00%
------------------------------------------------------------
Indique quanto quer ganhar por mês em dividendos (€): 100
Indique quanto quer investir por mês em (€): 500
------------------------------------------------------------
Valor da ação em euros: 135.00€
Ações adquiridas por mês: 3
Investimento excedente mensal: 15.00€
Tempo necessário para atingir o objetivo: 2 anos e 5 meses
Dividendo acumulado: 100.00€
Total excedente poupado: 180.00€
Total de ações adquiridas: 39
Total aporte: 5265.00€
------------------------------------------------------------
```

## Licença
Este projeto está licenciado sob a [MIT License](https://opensource.org/license/mit).


## Como Funciona
1. O script acessa o site de informações financeiras para obter o título da ação, seu valor atual e o dividendo anual.
2. O usuário fornece os valores de ganho mensal desejado e aporte mensal.
3. O script calcula o valor necessário de ações, o tempo necessário para atingir o objetivo e exibe as informações 
financeiras detalhadas.


## Autor
Este projeto foi desenvolvido por [Jonathan Alves](https://www.linkedin.com/in/jonathan-s-alves/). 

