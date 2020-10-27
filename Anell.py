#Primeiramente faço a importação das bibliotecas que são usadas durante o processo
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time as time
import pandas as pd

#Neste momento eu crio a variavel que vai interar no while
num_est = 12
num_mun = 0

#Aqui eu crio o df_prin que irá ser o dataFrame principal usuado, onde ele vai receber todos os dados
df_prin = pd.DataFrame({"Distribuidora": [""],
                           "Conjunto": [""],
                           "Periodo de Referencia": [""],
                           "Unidades Consumidoras": [""],
                           "DEC³": [""],
                           "DEC Limite⁴": [""],
                           "FEC³": [""],
                           "FEC Limite⁴": [""],
                           "Compensações pagas no período": [""],
                           "Estado": [""],
                           "Muninicio": [""]
                        })

#Com isso eu pego o tempo inicial que começou a rodar o programa
inicio = time.time()

#Logo em seguida eu seto o drive do chrome para poder fazer essa automação, e passo a URL que desejo fazer a raspagem de dados
browser = webdriver.Chrome("C:\chromedriver.exe")
browser.get("http://www2.aneel.gov.br/relatoriosrig/(S(w2m3txjdfkjnfgurokoorfvg))/relatorio.aspx?folder=sfe&report=PainelMunicipio")

#Quando entramos no site da Aneel, podemos observar que dentro existe alguns problemas de para se fazer direto a raspagem de dados que é temos que selecionar qual estado, qual municipio e data queremos os dados, então para isso usei algumas bibliotecas do selenium, e outro problema era que quando se seta esses valores ele tem um tempo de carregamentos da informações então coloquei o time.sleep() para dar tempo de carregar os dados
try:
    while True:
        num_est += 1
        est = str(num_est)
        select_estado = Select(browser.find_element_by_id('ReportViewer1_ctl04_ctl03_ddValue')) #Select de estado
        select_estado.select_by_value(est) #Aqui eu to passando qual valor eu vou setar no select
        nome_estado = select_estado.first_selected_option.get_attribute("text") # Recupero o nome do estado

        time.sleep(20)

        try:
            while True:
                num_mun += 1
                mun = str(num_mun)

                select_municipio = Select(browser.find_element_by_id('ReportViewer1_ctl04_ctl05_ddValue')) #Select de município
                select_municipio.select_by_value(mun) #Aqui eu to passando qual valor eu vou setar no select
                nome_municipio = select_municipio.first_selected_option.get_attribute("text") # Recupero o nome do municipio

                time.sleep(30)

                select = Select(browser.find_element_by_id('ReportViewer1_ctl04_ctl07_ddValue')) #Select de Período de referência
                select.select_by_visible_text('2019') #Aqui eu to passando qual valor eu vou setar no select

                time.sleep(5)
                btn_more = browser.find_element(By.ID, 'ReportViewer1_ctl04_ctl00') #procuro o ID do botão
                btn_more.click() #Faço ele apertar o botão.

                time.sleep(25)

                # Aqui eu crio os vetores que serão utilizados para guardar os dados e futuramente fazer o DataFrame()
                Distribuidora = []
                Conjunto = []
                Periodo_Referencia = []
                Unidades_Consumidores = []
                DEC3 = []
                Dec_Limite = []
                FEC3 = []
                FEC_Limite = []
                Compensacoes_Pagas = []
                i = 3

                try:
                    while True:
                        """
                        Para poder pegar os dados eu percebi que todos dados da mesma coluna tem o xpath iguais a unica coisa que muda entre eles é um número que corresponde a qual coluna ele está, 
                        com isso eu criei um try e um while dentro para ele ficar rodando pegando todos dados dessas tabelas, então quando ele der erro é porque acabou os dados
                        """
                        Distribuidora.append(browser.find_element_by_xpath(f"/html/body/form/div[3]/div/div/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td[3]/table/tbody/tr[{i}]/td[2]/div").text)
                        Conjunto.append(browser.find_element_by_xpath(f"/html/body/form/div[3]/div/div/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td[3]/table/tbody/tr[{i}]/td[3]/div").text)
                        Periodo_Referencia.append(browser.find_element_by_xpath(f"/html/body/form/div[3]/div/div/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td[3]/table/tbody/tr[{i}]/td[4]").text)
                        Unidades_Consumidores.append(browser.find_element_by_xpath(f"/html/body/form/div[3]/div/div/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td[3]/table/tbody/tr[{i}]/td[5]").text)
                        DEC3.append(browser.find_element_by_xpath(f"/html/body/form/div[3]/div/div/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td[3]/table/tbody/tr[{i}]/td[6]/div").text)
                        Dec_Limite.append(browser.find_element_by_xpath(f"/html/body/form/div[3]/div/div/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td[3]/table/tbody/tr[{i}]/td[7]/div").text)
                        FEC3.append(browser.find_element_by_xpath(f"/html/body/form/div[3]/div/div/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td[3]/table/tbody/tr[{i}]/td[8]/div").text)
                        FEC_Limite.append(browser.find_element_by_xpath(f"/html/body/form/div[3]/div/div/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td[3]/table/tbody/tr[{i}]/td[9]/div").text)
                        Compensacoes_Pagas.append(browser.find_element_by_xpath(f"/html/body/form/div[3]/div/div/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td[3]/table/tbody/tr[{i}]/td[10]/div").text)
                        i += 1

                except:
                    if len(Distribuidora) != len(Conjunto):
                        Distribuidora.pop()
                        # Neste momento eu faço uma verificação se o tamanho do vetor da Distribuidora e do conjunto são diferentes, se for diferente eu faço o .pop() para retirar o ultimo dado da distribuidora

                # Depois de ter pegados esses dados e colocados em um vetor, eu crio um DataFrame contendo todas informações e seus vetores com as devidas informações
                df_aux = pd.DataFrame({"Distribuidora": Distribuidora,
                                   "Conjunto": Conjunto,
                                   "Periodo de Referencia": Periodo_Referencia,
                                   "Unidades Consumidoras": Unidades_Consumidores,
                                   "DEC³": DEC3,
                                   "DEC Limite⁴": Dec_Limite,
                                   "FEC³": FEC3,
                                   "FEC Limite⁴": FEC_Limite,
                                   "Compensações pagas no período": Compensacoes_Pagas,
                                   "Estado": nome_estado,
                                   "Muninicio": nome_municipio})

                # Neste momento eu pego o dataFrame e concato ele com o df_aux, pata termos um dataFrame com todos os dados
                df_prin = pd.concat([df_prin, df_aux])
                # Sempre que ele faz uma atualização nos dados eu salvo no computador esse arquivo para caso o computador desligar ou a internet cair ainda sim iremos ter os dados que coletamos até tal momento
                # e com isso podemos continuar da onde paramos.
                csv = df_prin.to_csv(r"C:\Users\Bright Cities 02\Desktop\Dados\todosDados4.csv")
                print(df_prin)
        except:
            # Neste momento é quando ele já pegou todos dados de um determinado Estado e vai para um novo estado então ele zera o num_mun para pegar desde o primerio municipio
            num_mun = 0
except:
    print()

# Neste momento já coletamos todos os dados de todos estados
#Pego o tempo que a aplicação acabou
print(df_prin)
fim = time.time()
#faço uma pequena conta para saber quanto tempo meu programa rodou
print(f"O tempo que levou para gerar todos os dados foi de: {fim - inicio}")
#e por fim, salvo a tabela
csv = df_prin.to_csv(r"C:\Users\Bright Cities 02\Desktop\Dados\todosDados4.csv")