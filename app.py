import os
import requests
import re
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cotacaoEuro import get_euro_dollar_exchange_rate

# Configurações do navegador
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executa sem interface gráfica
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Gera a data e hora atuais
data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# Verificação do robots.txt
def check_robots(url):
    try:
        response = requests.get(url + 'robots.txt')
        if response.status_code == 200:
            disallowed_rules = [
                "/product", "/search", "/page", "/keyword", "/?gclid", "/utm_",
                "/amp", "/Taxonomy", "/tag", "/cdn-cgi"
            ]
            for rule in disallowed_rules:
                if rule in response.text:
                    print(f"Automação não permitida para regra: {rule}")
                    return False
            return True
        return False
    except Exception as e:
        print(f"Erro ao verificar robots.txt: {e}")
        return False

# Função para acessar a página e obter informações
def getInfo(url):
    driver.get(url)

    try:
        # Obtem o titulo do ETF a investir
        title = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//h1[@class='text-xl font-bold bp:text-2xl']"))
        )
        title = title.text.strip()

        # Obtém o valor da ação unitária
        valor_acao = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class ='text-4xl font-bold inline-block']"))
        )
        valor_acao = valor_acao.text.strip()
        valor_acao = re.sub(r'[^\d.]', '', valor_acao)
        valor_acao_atual = float(valor_acao)

        # Obtém o valor do dividendo anual
        dividendo_anual = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='mt-0.5 text-lg font-semibold bp:text-xl sm:mt-1.5 sm:text-2xl']"))
        )
        dividendo_anual = dividendo_anual.text.strip()
        valor_dividendo_anual = float(dividendo_anual.replace('%', '')) / 100

        # Mostra os resultados com a data e hora atuais
        print(f"\n{data_hora_atual}")
        print("-" * 60)
        print(f"{title}")
        print(f"Valor por unidade: {valor_acao_atual:.2f} USD")
        print(f"Dividendo anual: {valor_dividendo_anual:.2%}")
        print("-" * 60)

        # Retorna os valores obtidos
        return title, valor_acao_atual, valor_dividendo_anual
    except Exception as e:
        print(f"Erro ao obter informações: {e}")
        return None, None, None

def getGanhoMensal(valor_acao_atual):
    cotacao_atual = (valor_acao_atual * get_euro_dollar_exchange_rate())
    if cotacao_atual is None:
        print("Erro ao obter cotação. Encerrando cálculo.")
        return

    while True:
        try:
            # Solicitar o valor de investimento mensal convertendo-o para float
            ganho_mensal = float(input("Indique quanto quer ganhar por mês em dividendos (€): "))

            # Verificar se o valor é positivo
            if ganho_mensal <= 0:
                print("O valor deve ser maior que zero. Tente novamente.")
                continue

            # Solicitar o valor de investimento mensal convertendo-o para float
            aporte_mensal = float(input("Indique quanto quer investir por mês em (€): "))

            # Verificar se o valor é positivo
            if aporte_mensal <= 0:
                print("O valor deve ser maior que zero. Tente novamente.")
            elif aporte_mensal < cotacao_atual:
                print(f"O valor a investir é insuficiente. O valor por ação é de {cotacao_atual:.2f}€.")
                continue

            return ganho_mensal, aporte_mensal
        except ValueError:
            print("Valor inválido! Por favor, insira um número válido.")

# Converte meses para anos e meses
def getAnosMeses(total_meses):
    anos = total_meses // 12  # Divide por 12 para obter os anos completos
    meses = total_meses % 12  # Resto da divisão para obter os meses restantes
    resposta = ''

    if anos == 0:
        resposta = f"{meses} meses"
    elif anos == 1 and meses == 0:
        resposta = f"{anos} ano"
    elif anos == 1 and meses == 1:
        resposta = f"{anos} ano e {meses} mês"
    elif anos > 1 and meses == 0:
        resposta = f"{anos} anos"
    elif anos == 1 and meses > 1:
        resposta = f"{anos} ano e {meses} meses"
    elif anos > 1 and meses > 1:
        resposta = f"{anos} anos e {meses} meses"
    elif anos > 1 and meses == 1:
        resposta = f"{anos} anos e {meses} mês"

    return resposta

# Função para calcular o tempo e valores necessários
def getTempoNecessario(valor_dividendo_anual, ganho_mensal_pretendido, valor_acao_atual, aporte_mensal):
    # Obtém a cotação atual (em euros)
    taxa_cambio = get_euro_dollar_exchange_rate()
    if taxa_cambio is None:
        print("Erro ao obter a taxa de câmbio. Encerrando cálculo.")
        return

    cotacao_atual = valor_acao_atual * taxa_cambio

    novo_valor_acoes = valor_acao_atual * taxa_cambio

    # Validação de cotação
    if cotacao_atual <= 0:
        print("Cotação inválida. Encerrando cálculo.")
        return

    # Define as ações adquiridas com o valor do aporte mensal
    acoes_adquiridas = aporte_mensal // cotacao_atual  # Divisão inteira para evitar frações de ações

    # Define o investimento excedente
    investimento_excedente = aporte_mensal - (acoes_adquiridas * cotacao_atual)

    # Verifica se o número de ações adquiridas precisa ser ajustado
    if (acoes_adquiridas * cotacao_atual) < 0:
        acoes_adquiridas = max(acoes_adquiridas - 1, 0)  # Garante que o número de ações não fique negativo

    print("-" * 60)
    print(f"Valor da acao em euros: {novo_valor_acoes:.2f}€")
    print(f"Ações adquiridas por mês: {acoes_adquiridas:.0f}")
    print(f"Investimento excedente mensal: {investimento_excedente:.2f}€")

    # Exemplo adicional: Simulação de tempo necessário para atingir o objetivo (opcional)
    meses_necessarios = 0
    dividendo_acumulado = 0

    while dividendo_acumulado < ganho_mensal_pretendido:
        meses_necessarios += 1
        # Incrementa o dividendo acumulado com base no valor de dividendo anual
        dividendo_acumulado += (acoes_adquiridas * (valor_dividendo_anual / 12))

        # Simula a compra de mais ações a cada mês com o aporte mensal
        novas_acoes = aporte_mensal // cotacao_atual
        acoes_adquiridas += novas_acoes

        # Recalcula o excedente
        investimento_excedente += aporte_mensal - (novas_acoes * cotacao_atual)

    print(f"Tempo necessário para atingir o objetivo: {getAnosMeses(meses_necessarios)}")
    print(f"Dividendo acumulado: {dividendo_acumulado:.2f}€")
    print(f"Total excedente poupado: {investimento_excedente:.2f}€")
    print(f"Total de ações adquiridas: {acoes_adquiridas:.0f}")
    print(f"Total aporte: {(acoes_adquiridas * novo_valor_acoes):.2f}€")
    print("-" * 60)

def getPlano(base_url): # Implementar uma solução para evitar bloqueios de solicitações!!!
    # Captura infrmações atualizadas do ETFs/Ação desejada
    title, valor_acao_atual, valor_dividendo_anual = getInfo(base_url)

    # Conversão de dólar para euro e cálculos para o plano de investimento
    ganho_mensal_pretendido, aporte_mensal = getGanhoMensal(valor_acao_atual)

    # Processar e exibir o plano de investimento
    getTempoNecessario(valor_dividendo_anual, ganho_mensal_pretendido, valor_acao_atual, aporte_mensal)

# Execução
if __name__ == "__main__":
    try:
        base_url = 'https://stockanalysis.com/'
        if check_robots(base_url):
            getPlano('https://stockanalysis.com/etf/aaa/dividend/')
    finally:
        driver.quit()