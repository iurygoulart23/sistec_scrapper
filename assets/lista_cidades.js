function navigateAndClickExport() {
  // Busca todos os elementos com a tag 'h3'
  var h3Elements = document.getElementsByTagName('h3');
  var h3Array = Array.from(h3Elements);
 
  // Array para armazenar resultados/log
  var results = [];
 
  // Função para processar um elemento h3
  function processElement(index) {
    // Se todos os elementos foram processados, retorna os resultados
    if (index >= h3Array.length) {
      console.log("Processamento completo!");
      return results;
    }
   
    // Aguarda 1.5 segundos antes de começar a processar o elemento
    setTimeout(function() {
      var currentElement = h3Array[index];
      var elementInfo = {
        text: currentElement.textContent.trim(),
        id: currentElement.id,
        clicked: false,
        foundExportButton: false,
        exportClicked: false
      };
     
      // Tenta clicar no elemento h3
      try {
        console.log("Clicando em: " + elementInfo.text);
        currentElement.click();
        elementInfo.clicked = true;
       
        // Espera um pouco para o conteúdo ser carregado
        setTimeout(function() {
          // Verifica se existe o botão de exportar
          var exportButton = document.getElementById('botaoExportarExcel');
         
          if (exportButton) {
            elementInfo.foundExportButton = true;
            console.log("Botão de exportar encontrado em: " + elementInfo.text);
           
            // Clica no botão de exportar
            try {
              exportButton.click();
              elementInfo.exportClicked = true;
              console.log("Clicado no botão exportar");
            } catch (e) {
              console.log("Erro ao clicar no botão exportar: " + e.message);
            }
          } else {
            console.log("Botão de exportar NÃO encontrado em: " + elementInfo.text);
          }
         
          // Fecha o elemento clicando nele novamente
          setTimeout(function() {
            try {
              console.log("Tentando fechar o elemento: " + elementInfo.text);
              // Verifica se o elemento ainda existe no DOM antes de clicar
              if (document.body.contains(currentElement)) {
                currentElement.click();
                console.log("Elemento fechado com sucesso: " + elementInfo.text);
              } else {
                console.log("Elemento não está mais no DOM: " + elementInfo.text);
                // Tenta encontrar o elemento novamente pelo id se disponível
                if (currentElement.id) {
                  var refreshedElement = document.getElementById(currentElement.id);
                  if (refreshedElement) {
                    refreshedElement.click();
                    console.log("Elemento fechado usando ID: " + elementInfo.text);
                  }
                }
              }
            } catch (e) {
              console.log("Erro ao fechar elemento: " + e.message);
              // Tentativa alternativa de fechamento
              try {
                // Tenta usar o seletor para encontrar o elemento novamente
                var selector = "#" + currentElement.id;
                var refreshedElement = document.querySelector(selector);
                if (refreshedElement) {
                  refreshedElement.click();
                  console.log("Elemento fechado usando seletor: " + selector);
                }
              } catch (innerError) {
                console.log("Todas as tentativas de fechar o elemento falharam");
              }
            } finally {
              // Independentemente do resultado, registra o elemento e continua
              elementInfo.closed = true;
              results.push(elementInfo);
              
              // Verifica novamente se o elemento realmente foi fechado
              setTimeout(function() {
                // Adiciona uma verificação de fechamento
                var isElementStillExpanded = false;
                try {
                  // Tenta verificar se o painel associado ainda está visível
                  // (implementação depende da estrutura da página)
                  if (currentElement.getAttribute("aria-expanded") === "true") {
                    isElementStillExpanded = true;
                  }
                } catch (e) {
                  // Ignora erros nesta verificação
                }
                
                if (isElementStillExpanded) {
                  console.log("Elemento ainda está expandido, tentando fechar novamente");
                  try {
                    currentElement.click();
                  } catch (e) {
                    console.log("Falha na tentativa final de fechamento");
                  }
                }
                
                // Continua para o próximo elemento
                console.log("Continuando para o próximo elemento");
                processElement(index + 1);
              }, 500);
            }
          }, 1000);
        }, 1000);
      } catch (e) {
        console.log("Erro ao processar elemento: " + e.message);
        results.push(elementInfo);
       
        // Tenta o próximo elemento mesmo em caso de erro
        setTimeout(function() {
          processElement(index + 1);
        }, 500);
      }
    }, 1500); // Espera 1.5 segundos antes de começar a processar cada elemento
  }
 
  // Inicia o processamento com o primeiro elemento
  processElement(0);
 
  // Como a função é assíncrona e usa setTimeout, retornamos uma promise
  return new Promise(function(resolve) {
    // Verificamos a cada 1 segundo se o processamento foi concluído
    var checkInterval = setInterval(function() {
      if (results.length === h3Array.length) {
        clearInterval(checkInterval);
        console.log("Processamento concluído, verificando se todos elementos foram fechados");
        
        // Verificação final para garantir que todos os elementos foram fechados
        var openElements = Array.from(h3Elements).filter(function(el) {
          return el.getAttribute("aria-expanded") === "true";
        });
        
        if (openElements.length > 0) {
          console.log(`${openElements.length} elementos ainda estão abertos, tentando fechar...`);
          openElements.forEach(function(el) {
            try {
              el.click();
              console.log(`Fechado elemento remanescente: ${el.textContent.trim()}`);
            } catch (e) {
              console.log(`Erro ao fechar elemento remanescente: ${e.message}`);
            }
          });
        }
        
        resolve(results);
      }
    }, 1000);
   
    // Timeout de segurança (5 minutos)
    setTimeout(function() {
      clearInterval(checkInterval);
      resolve(results);
    }, 300000);
  });
}
// Executa a função e retorna a promise
return navigateAndClickExport();