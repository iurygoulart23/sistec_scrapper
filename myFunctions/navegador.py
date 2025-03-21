def navegador_firefox(headless=0, firefox_options=None) -> any:
    '''Função para abrir o navegador com todas config
    já configuradas'''

    import subprocess
    from selenium import webdriver
    from webdriver_manager.firefox import GeckoDriverManager
    from selenium.webdriver.firefox.service import Service as GeckoService

    from myFunctions.arrumaScrapper import dir_download
    
    print('\n###############################\n')
    print('         Bem vindo(a)!           ')
    print('\n###############################\n')
    print('Abrindo navegador..\n')

    firefox_binary_path = '/usr/bin/firefox'
    link_geckodriver = 'https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz' 

    # checa versão do seu firefox para baixar o geckodriver certo
    # firefox_version = subprocess.check_output('firefox --version', shell=True, stderr=subprocess.STDOUT).decode()
    # print(f'Voce está usando o firefox versão:\n{firefox_version[-8:-1]}\n')

    # MIME type for the file you want to download

    # if headless:
    #     firefox_options.add_argument('--headless')

    # firefox_options.add_argument('--disable-dev-shm-usage')
    # firefox_options.add_argument("disable-infobars")

    # create service to GECKODRIVER
    service = GeckoService(GeckoDriverManager(url = link_geckodriver,
                                              version='v0.34.0').install(),
                                              service_log_path = '../downloads/')

    # Creating the Firefox driver
    navegador = webdriver.Firefox(
        service = service,
        options = firefox_options
    )

    print('Navegador aberto.\n')

    return navegador

def navegador_chrome(headless=0) -> any:
    '''Função para abrir o navegador Chrome com todas configurações já configuradas'''

    import subprocess
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service as ChromeService

    print('\n###############################\n')
    print('         Bem vindo(a)!           ')
    print('\n###############################\n')
    print('Abrindo navegador Chrome..\n')

    # Configurando navegador Chrome
    chrome_options = webdriver.ChromeOptions()
    
    # Configure preferences for downloads
    download_directory = "./download/"
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    # MIME type for the file you want to download

    if headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')  # This make Chromium reachable
    chrome_options.add_argument('--disable-infobars')

    # create service to CHROMEDRIVER
    service = ChromeService(ChromeDriverManager().install())

    # Creating the Chrome driver
    navegador = webdriver.Chrome(
        service=service,
        options=chrome_options
    )

    print('Navegador Chrome aberto.\n')

    return navegador

def get_links(driver):
    """_summary_
    """
    
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By


    # Wait for the page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.col-md-3.col-12 select[name='base']")))

    # Find all links to ADCs
    adc_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='verPeticaoInicial.asp?base=ADC']")

    # Extract the href attribute from each link
    extracted_links = [link.get_attribute("href") for link in adc_links]

    # Close the browser
    driver.quit()

    return extracted_links
    
def get_files(soup:any):

    from bs4 import BeautifulSoup
    import requests

    # Send a GET request to the URL
    response = requests.get(url, verify=True)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract information
    data = {}

    # Find and extract the process number
    process_number_tag = soup.find("span", {"id": "lblNumeroProcesso"})
    data["process_number"] = process_number_tag.text.strip()

    # Find and extract the petitioner information
    petitioner_info_tag = soup.find("div", {"id": "divAutor"})
    petitioner_info = petitioner_info_tag.find_all("p")
    data["petitioner_name"] = petitioner_info[0].text.strip()
    data["petitioner_cpf_cnpj"] = petitioner_info[1].text.strip()

    # Find and extract the defendant information
    defendant_info_tag = soup.find("div", {"id": "divReu"})
    defendant_info = defendant_info_tag.find_all("p")
    data["defendant_name"] = defendant_info[0].text.strip()
    data["defendant_cpf_cnpj"] = defendant_info[1].text.strip()

    # Find and extract the petition text
    petition_text_tag = soup.find("div", {"id": "divTextoPeticao"})
    data["petition_text"] = petition_text_tag.text.strip()

    # Convert the extracted data to JSON
    json_data = json.dumps(data, indent=4)

    # Save the JSON data to a file
    with open("stf_petition_data.json", "w") as f:
        f.write(json_data)

    print("JSON data generated successfully!")