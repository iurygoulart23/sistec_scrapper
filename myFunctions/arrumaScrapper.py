def dir_download():
    '''Determina o diretório para salvar os arquivos de download.'''
    import os

    pasta_notebook = os.getcwd()
    pasta_projeto  = os.path.abspath(os.path.join(pasta_notebook, os.pardir))
    pasta_download = pasta_projeto + '/downloads'

    return pasta_download

def download_arq(url_download):
    import requests
    import os

    # Define the image URL and the desired local file path
    target_directory = dir_download()
    file_name = url_download.split('/')[-1].replace('%20', '_')

    # Create the target directory if it doesn't exist
    os.makedirs(target_directory, exist_ok= True)

    try:
        # Download the image data
        response = requests.get(url_download)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            with open(os.path.join(target_directory, file_name), 'wb') as f:
                f.write(response.content)
            print(f"Arquivo baixado e salvo em: {os.path.join(target_directory, file_name)}")
            return os.path.join(target_directory, file_name)
        else:
            print(f"Falhou em baixar o arquivo. Status code: {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"TimeoutError: Download falhou: {url_download}")
        dict_erro_download.append(url_download)

def download_wait(path_to_downloads):
    '''Função que fecha o navegador após a conclusão do 
    download OU até atingir o tempo máximo.'''
    import time
    import os

    seconds = 0
    dl_wait = True
    t_max =  60*10 #10 min
    
    while dl_wait and seconds < t_max:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.crdownload'):
                dl_wait = True
                print('\nEsperando download . . .')
        seconds += 1
    print('\nDownloads concluídos!')


def tempo_espera_aleatorio(low=1, high=5):
    '''Tempo de delay entre comandos para evitar 
    ser bloqueado pelo servidor.'''
    import numpy as np
    import time
    n_aleatorio = np.random.randint(low=low, high=high)
    time.sleep(n_aleatorio)


def get_links(driver):
    """Função que pega os links da pagina de pesquisa

    Args:
        driver (object): driver do selenium, ja com a pagina carregada

    Returns:
        LIST: retorna uma lista com os links das publicações
    """
    from bs4 import BeautifulSoup
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tabela-resultado"))
        )
    except TimeoutException:
        print("Timeout waiting for results table to load.")
        driver.quit()
        return []

    # Get the HTML content of the page
    html = driver.page_source

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find all links to the individual petition pages
    links = []
    for row in soup.find("table", id="tabela-resultado").find_all("tr")[1:]:
        link = row.find("a", href=True)["href"]
        links.append(link)
    
    return links

def save_page_source(response):
    """Função para salvar o html da pagina para fazer testes

    Args:
        response (_type_): _description_
    """
    with open('./assets/page_source.html', 'w') as f:
        f.write(response)
    
    print('Arquivo salvo com sucesso!')
    return
