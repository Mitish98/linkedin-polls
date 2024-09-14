from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from poll_dashboard import PollDashboard

# Função para inicializar o driver
def initialize_driver():
    driver = webdriver.Chrome()
    return driver

# Função para fazer login no LinkedIn
def login_linkedin(driver):
    driver.get('https://www.linkedin.com/login')
    input("Faça o login manualmente e complete qualquer verificação, depois pressione Enter para continuar...")

# Função para acessar a página de atividades recentes
def access_activity_page(driver, url='https://www.linkedin.com/in/matheus-iotti/recent-activity/all/'):
    driver.get(url)
    time.sleep(10)  # Espera a página carregar completamente

# Função para rolar a página até o final
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Função para extrair enquetes
def extract_polls(driver):
    polls = driver.find_elements(By.CSS_SELECTOR, "div.overflow-hidden.update-components-poll.feed-shared-update-v2__content.feed-shared-update-v2__content--simplification")
    
    poll_data = []
    
    for poll in polls:
        try:
            title_element = poll.find_element(By.CSS_SELECTOR, "h3.t-sans.t-16.t-black.t-bold.mb1.break-words")
            title = title_element.text
            
            options_data = []
            options = poll.find_elements(By.CSS_SELECTOR, "div.update-components-poll-option.display-flex.mb2")
            
            for option in options:
                option_label = option.find_element(By.CSS_SELECTOR, "div[aria-label]").get_attribute('aria-label')
                option_percentage = option.find_element(By.CSS_SELECTOR, "div.update-components-poll-option__percentage").text
                options_data.append({'Option': option_label, 'Percentage': option_percentage})
            
            # Captura o link da postagem da enquete
            poll_link = poll.find_element(By.XPATH, "../../../../../..").get_attribute('href')  # Caminho para obter o link da postagem
            
            # Captura o total de votos da enquete
            total_votes_element = poll.find_element(By.CSS_SELECTOR, "button.update-components-poll-summary__option-button.t-bold.t-14")
            total_votes = total_votes_element.text  # Pega o texto que contém o total de votos
            
            poll_data.append({'Title': title, 'Options': options_data, 'Link': poll_link, 'Total Votes': total_votes})
        except Exception as e:
            print(f"Erro ao processar enquete: {e}")
    
    return poll_data

# Função principal
def main():
    driver = initialize_driver()
    login_linkedin(driver)
    access_activity_page(driver)
    scroll_to_bottom(driver)
    
    poll_data = extract_polls(driver)
    driver.quit()
    
    # Instanciando o dashboard e criando a visualização
    dashboard = PollDashboard(poll_data)
    dashboard.export_dataframe("poll_data.csv")  # Primeiro, exporta os dados para CSV
    # Criando o dashboard com base no arquivo CSV
    dashboard = PollDashboard(csv_file="poll_data.csv")
    dashboard.create_dashboard()  # Depois, cria o dashboard com base no arquivo CSV

if __name__ == "__main__":
    main()
