# Importa as bibliotecas necessárias para automação de navegação no navegador com Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Função que obtém a taxa de câmbio do dólar para o euro (via Google Search)
def get_euro_dollar_exchange_rate():
    # Configurações do navegador para rodar de forma invisível (headless)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executa o navegador em modo sem interface gráfica
    chrome_options.add_argument("--disable-gpu")  # Desabilita aceleração de GPU, para evitar problemas com headless
    chrome_options.add_argument("--no-sandbox")  # Desabilita o sandboxing do Chrome, necessário para execução em algumas máquinas
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Impede a detecção de automação do Selenium

    # Inicializa o serviço do Chrome Driver e o navegador com as configurações especificadas
    service = Service(ChromeDriverManager().install())  # Instala o ChromeDriver necessário para o Selenium
    driver = webdriver.Chrome(service=service, options=chrome_options)  # Inicializa o navegador com as opções configuradas

    try:
        # URL do Google Search para procurar a cotação do dólar atual
        url = "https://www.google.com/search?q=valor+do+dolar+atual"
        driver.get(url)  # Navega até a URL

        # Aguarda até que o elemento com a cotação do dólar esteja visível na página (com tempo limite de 15 segundos)
        wait = WebDriverWait(driver, 15)
        cotacao_element = wait.until(
            EC.presence_of_element_located((By.XPATH, '//span[@class="DFlfde SwHCTb"]'))  # Localiza o elemento com a cotação usando XPath
        )

        # Obtém o valor da cotação do elemento encontrado, limpa o texto e converte para um número float
        cotacao_texto = cotacao_element.text.strip()  # Obtém o texto da cotação e remove espaços extras
        cotacao_texto = cotacao_texto.replace(",", "").strip()  # Remove qualquer vírgula e espaços extras
        cotacao_valor = float(cotacao_texto)  # Converte o texto para um valor numérico (float)

        # Caso a cotação seja maior que 10 (provavelmente porque o valor está em centavos), divide por 100 para ajustar
        if cotacao_valor > 10:
            cotacao_valor /= 100

        # Retorna o valor da cotação obtido
        return cotacao_valor

    except Exception as e:
        # Em caso de erro, imprime uma mensagem de erro e retorna None
        print(f"Erro ao obter a cotação: {e}")
        return None

    finally:
        # Fecha o navegador após o uso, independentemente de sucesso ou falha
        driver.quit()
