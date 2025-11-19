import google.generativeai as genai
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from question import perguntas, alternativas, gabarito
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()  # Carrega tudo do .env

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


genai.configure(api_key="AIzaSyD9NcvEF9ES9rLk4lGUQmayjUFRerCxNmE")
model = genai.GenerativeModel("gemini-2.0-flash")

bot = "Bozzbot"


#abrir o whatzapp web
driver = driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
driver.get("https://web.whatsapp.com")          

#Verificar se foi feito o login
checkt = input(str('feito? Y/n ').lower().replace(" ", ""))
if checkt == "y":

    #selecionar a conversa
    time.sleep(10)
    pyautogui.press('tab', presses=4, interval=0.5)
    time.sleep(1)

    #selecionar a conversa
    pyautogui.write(bot, interval=0.3)
    pyautogui.press("enter")
    time.sleep(1)


    #Lista de todas as mensagens
    def ler_ultima_mensagem(driver):
        mensagens = driver.find_elements(By.CSS_SELECTOR, "div.message-in, div.message-out")

        #Retorno da função caso não haja mensagens
        if not mensagens:
            return None, None

        #Ultima mensagem lida
        ultima = mensagens[-1]
        # Descobre se a ultima mensagem é recebida ou enviada
        tipo = "Recebida" if "message-in" in ultima.get_attribute("class") else "Enviada"

        # Extrai o texto da mensagem
        try:
            texto = ultima.find_element(By.CSS_SELECTOR, "span.selectable-text").text.lower().replace(" ", "")
        except:
            texto = ultima.text or "<sem texto>" # Caso a mensagem seja só emoji, áudio ou arquivo

        return tipo, texto

    def questoes(driver):
        global acertos, respostas
        respostas = []
        acertos = 0
        for i in range(len(perguntas)):
            pergunta = perguntas[i]

            pyautogui.write(pergunta, interval=0.005)
            pyautogui.press("enter")

            resposta_usuario = ""
            while True:

                tipo, texto = ler_ultima_mensagem(driver)

                if tipo == "Recebida" and texto != resposta_usuario:
                    resposta_usuario = texto.lower().strip()

                    if resposta_usuario in alternativas:   # usa a lista do question.py

                        # SALVA a resposta corretamente
                        respostas.append(resposta_usuario)

                        print(f"✔ Resposta valida: {resposta_usuario}")
                        break
                    else:
                        print(f"❌ Resposta invalida: {resposta_usuario}")
                        pyautogui.write("Nao entendi, responda com apenas as letras A, B, C ou D.", interval=0.05)
                        pyautogui.press("enter")

                time.sleep(0.3)
        
        for i in range(len(gabarito)):
            if respostas[i] == gabarito[i]:
                acertos += 1

        return acertos

    def ia(pergunta):

        sintese = pergunta + ', explique de forma simples e resumida.'
        resposta = model.generate_content(sintese)
        pyautogui.write(resposta.text)
        pyautogui.press("enter")
        time.sleep(1)


    # Loop para detectar mensagens novas
    def monitorar(driver):

        ultima_lida = ""

        print("\n📡 Monitorando mensagens...")

        while True:
            tipo, texto = ler_ultima_mensagem(driver)

            # Detecta nova mensagem
            if texto and texto != ultima_lida:
                print(f"\n💬 Nova mensagem ({tipo}): {texto}")
                ultima_lida = texto

            # Inicia a conversa ao ler a ultima menasgem
            time.sleep(1)

            #dectar e mandar a primeira mensagem
            if tipo == "Recebida" and texto and 'duvida' not in texto and 'aprender' not in texto and 'não' not in texto and 'nao' not in texto:
                pyautogui.write('Oi, Sou o BozzBot!\n' 
                                'Como posso te ajudar hoje ?\n'
                                'Gostaria de tirar alguma duvida ou aprender mais\n', interval=0.03)
        

            #direciona para fazer o curso
            elif tipo == "Recebida" and 'aprender' in texto:
                pyautogui.write('Ok, vou te enviar uma serie de perguntas para entender seu nivel de concimento, sobre informatica. Respoda apenas com letras das questoes: [a] [b] [c] ou [d] \n', interval=0.1 )
                pyautogui.write('Gostaria de tirar alguma duvida \n')
                
                
                nota = questoes(driver)
                if nota <= 7:
                    pyautogui.write('Seu nivel e o BASICO, aqui esta um link de um curso para aprimorar mais o seu conhecimento para que possa chegar ao nivel intermediario: https://www.geeksforgeeks.org/computer-science-fundamentals/computer-fundamentals-tutorial/ \n')
                    pyautogui.write('Gostaria de tirar alguma duvida \n')

                elif nota >= 8 and nota <= 13:
                    pyautogui.write('Seu nivel e o INTERMEDIARIO, aqui esta um link de um curso para aprimorar mais o seu conhecimento para que possa chegar ao nivel avancado: https://www.geeksforgeeks.org/computer-science-fundamentals/computer-fundamentals-tutorial/ \n')
                    pyautogui.write('Gostaria de tirar alguma duvida \n')
                        
                elif nota >= 13:
                    pyautogui.write('Seu nivel e o Avancado \n')
                    pyautogui.write('Gostaria de tirar alguma duvida \n')
 

            #direciona para tirar duvida  
            elif tipo == "Recebida" and 'duvida' in texto or 'dúvida' in texto:
                pyautogui.write('qual seria a sua duvida \n', interval=0.05 )

                time.sleep(1)
 
                modo_duvida = True
                pergunta = None

                while modo_duvida:
                    tipo2, texto2 = ler_ultima_mensagem(driver)
                    pergunta = texto2

                    texto2 = texto2.lower().strip()

                    if tipo2 == "Recebida" and texto2 in ["nao", "não"]:
                        pyautogui.write(
                            "Entendido! Como posso te ajudar agora? Quer aprender mais ou tirar outra dúvida?",
                            interval=0.05
                        )
                        pyautogui.press("enter")
                        modo_duvida = False
                        break

                    # Caso o usuário responda algo que não seja "duvida"
                    elif tipo2 == "Recebida" and texto2 not in ["duvida", "dúvida"]:
                        pergunta = texto2

                        sintese = pergunta + ', explique de forma simples e resumida.'
                        resposta = model.generate_content(sintese)
                        pyautogui.write(resposta.text)
                        pyautogui.press("enter")

                        pyautogui.write("Teria mais alguma duvida? Se nao tiver, digite 'nao'.", interval=0.05)
                        pyautogui.press("enter")
                        time.sleep(0.05)


                    
                        continue

                    # Se o usuário disser "não", encerra o modo dúvida corretamente
                    

                
                    
                    
                    # Pergunta se quer continuar
                    
            elif tipo == 'Recebida' and 'não' in texto or 'nao' in texto:
                pyautogui.write('Ok, qualquer coisa estou aqui') 
                time.sleep(1)
                pyautogui.press('enter') 
                
                


    monitorar(driver)
    


