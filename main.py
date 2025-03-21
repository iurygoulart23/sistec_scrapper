from selenium.webdriver.common.by import By
from time import sleep
from myFunctions.navegador import navegador_firefox

driver = navegador_firefox(headless=False)
driver.get("https://sistec.mec.gov.br/consultapublicaunidadeensino")
 
sleep(3)
 
driver.execute_script(""" document.querySelector("#map > area:nth-child(22)").click()""")
 
driver.execute_script("""document.querySelector("#alertMensagemErro_closeButton").click()""")
 
div_cidades = driver.find_element(By.ID, 'containnerConteudo')
sleep(5)

for n in range(50):
    
    sleep(1.5)
    
    try:
        cidade_class = f"conteudo_SistecAccordion_{n}_titulo"
        cidade_Id = f"conteudo_SistecAccordion_{n}"
       
        # abre a cidade
        cidade_atual = div_cidades.find_element(By.CLASS_NAME, cidade_class)
        cidade_atual.click()
        sleep(1)  # Pequena pausa para garantir que o conteúdo seja carregado
       
        # Lê o arquivo JavaScript
        with open('./assets/lista_cidades.js', 'rb') as f:
            lista_cidades = f.read().decode('utf-8')  # Decodifica bytes para string
       
        # Execute o script no driver (não no WebElement)
        cidades = driver.execute_async_script(lista_cidades)
        print(cidades)
        
        
        # fecha a cidade
        cidade_atual.click()
        sleep(1)  # Pausa para garantir que o fechamento foi concluído
        
    except Exception as e:
        print(f"Erro ao processar cidade {n}: {str(e)}")
        # Continua para a próxima cidade em caso de erro
        continue

sleep(30)
driver.quit()