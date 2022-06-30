#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 00:59:31 2022

@author: rodd369
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.keys import Keys
import os
import time
#import cutie
import glob
import shutil
import json
from pathlib import Path

def main():
    with open('config.json') as config_file:
        config = json.load(config_file)
    
    def clear_screen():
        os.system("clear||cls")
        
    def timeout(start_time, default=300):
        wait_time = default
        
        if time.time() > start_time + wait_time:
            return True
        return False
    
    os.path.exists(Path('.temp')) and shutil.rmtree(Path('.temp'))    
    os.mkdir(Path('.temp'), 0o777)
    
    servico = Service(ChromeDriverManager().install())
    option = webdriver.chrome.options.Options()
    option.add_argument('start-maximized')
    option.add_argument('--window-size=1920, 1080')
    option.add_argument('log-level=3')
    option.add_experimental_option("prefs", {
      "download.default_directory": os.getcwd() + r"\.temp",
      "plugins.always_open_pdf_externally": True,
      "download.prompt_for_download": False,
      "download.directory_upgrade": True,
      "safebrowsing_for_trusted_sources_enabled": False,
      "safebrowing.enabled": False
      })
    option.headless = False
    navegador = webdriver.Chrome(service=servico, options=option)
    
    clear_screen()
    
    class Colors:
        """ANSI Escape codes for the console output with colors and rich text.
    
        How to use: print(f"Total errors this run: {Cores.Red if a > 0 else Cores.Green}{a}")
        Read more also: 
            * https://en.wikipedia.org/wiki/ANSI_escape_code
            * https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
            * https://gist.github.com/arlm/f624561b2cd3f53cb26112f3e48f97cd
            * https://www.ecma-international.org/publications-and-standards/standards/ecma-48/
    
        Attributes:
            Reset (str): Reset colors.
            Bold (str): Makes text bold.
            Underline (str): Underlines text.
            Red (str): Red foreground text.
            Green (str): Green foreground text.
            Yellow (str): Yellow foreground text.
            Blue (str): Blue foreground text.
            Magenta (str): Magenta foreground text.
            Cyan (str): Cyan foreground text.
            bgRed (str): Red background.
            bgGreen (str): Green background.
            bgYellow (str): Yellow background.
            bgBlue (str): Blue background.
            bgMagenta (str): Magenta background.
            bgCyan (str): Cyan background.
            bgWhite (str): White background.
        """
        
        Reset = '\u001b[0m'
        """Reset colors ANSI Escape code.
        """
        Bold = '\u001b[1m'
        """Makes text bold ANSI Escape code.
        """
        Underline = '\u001b[4m'
        """Underlines text ANSI Escape code.
        """
    
        Red = '\u001b[31m'
        """Red foreground text ANSI Escape code.
        """
        Green = '\u001b[32m'
        """Green foreground text ANSI Escape code.
        """
        Yellow = '\u001b[33m'
        """Yellow foreground text ANSI Escape code.
        """
        Blue = '\u001b[34m'
        """Blue foreground text ANSI Escape code.
        """
        Magenta = '\u001b[35m'
        """Magenta foreground text ANSI Escape code.
        """
        Cyan = '\u001b[36m'
        """Cyan foreground text ANSI Escape code.
        """
    
        bgRed = '\u001b[41m'
        """Red background ANSI Escape code.
        """
        bgGreen = '\u001b[42m'
        """Green background ANSI Escape code.
        """
        bgYellow = '\u001b[43m'
        """Yellow background ANSI Escape code.
        """
        bgBlue = '\u001b[44m'
        """Blue background ANSI Escape code.
        """
        bgMagenta = '\u001b[45m'
        """Magenta background ANSI Escape code.
        """
        bgCyan = '\u001b[46m'
        """Cyan background ANSI Escape code.
        """
        bgWhite = '\u001b[47m'
        """White background ANSI Escape code.
        """
    
    login_url = 'https://perfil.estrategia.com/login?source=legado-polvo&target=https%3A%2F%2Fwww.estrategiaconcursos.com.br%2Faccounts%2Flogin%2F%3Fgoto%3D'
    
    navegador.get(login_url)
    #navegador.maximize_window()
    navegador.implicitly_wait(20)
    
    user_email = input('Informe seu login: ')
    user_senha = input('Informe sua senha: ')
    
    print('Aguarde enquanto carregamos os dados')
    
    login_input = navegador.find_element(By.NAME, 'loginField')
    login_input.send_keys(user_email)
    
    login_password = navegador.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/div/span/form/div[3]/span/div/div/div[1]/div[1]/input')
    login_password.send_keys(user_senha)
    
    submit_btn = navegador.find_element(By.TAG_NAME, 'button')
    submit_btn.click()
    
    
    wait = WebDriverWait(navegador, 50)
    wait.until(lambda driver: driver.current_url == 'https://www.estrategiaconcursos.com.br/app/dashboard/renovacao-2022')
    
    #time.sleep(15)
    dashboard = 'https://www.estrategiaconcursos.com.br/app/dashboard/assinaturas'
    # navegador.get(dashboard)
    
    menu = navegador.find_elements(By.CLASS_NAME, 'MenuButton')
    
    
    while navegador.current_url != dashboard:
        time.sleep(5)
        
        for m in menu:
            if 'Catálogo de Cursos' in m.text:
                m.click()
                
        #navegador.get(dashboard)
       
    
    lista_cursos = navegador.find_elements(By.CLASS_NAME, 'Section')
    
    list_links = []
    curso_titulos = []
    
    for curso in lista_cursos:
        fullstring = curso.text
        
        if fullstring != None and 'desmatricular'.upper() in fullstring:
            link_cursos = curso.find_elements(By.CLASS_NAME, 'Link')
            
            for i in range(len(link_cursos)):
                opt = "{0}[{1}{2}{3}{4}{5}]{6}".format(Colors.Red, Colors.Reset, Colors.Green, i, Colors.Reset, Colors.Red, Colors.Reset)
                print(opt, Colors.Underline + Colors.Cyan + link_cursos[i].text.split(' - ')[0] + Colors.Reset + Colors.Reset +'\n')
                list_links.append(link_cursos[i].get_attribute('href'))
                curso_titulos.append(link_cursos[i].text.split(' - ')[0])
                
                
    # print(Colors.Underline + Colors.Cyan + 'Selecione o curso desejado: \n' + Colors.Reset)            
    # curso_selecionar = cutie.select(curso_titulos)
    # curso_escolha = curso_titulos[curso_selecionar]
    
    # curso_titulos[curso_selecionar] in config or config.update({curso_escolha:{}})
    # print(f'\n{config}\n')
    
    # clear_screen()
    # print("Processando...")
    # root_dir_nome = curso_escolha
    # navegador.get(list_links[curso_selecionar])
    # clear_screen()
                
    #print(list_links)
    
    while True:
        curso_index = int(input("Digite o número do curso que deseja baixar: "))
        
        if curso_index >= 0 and curso_index <= len(list_links) -1:
            link_cursos[curso_index].click()
            #navegador.get(list_links[curso_index])
            clear_screen()
            break
    
    curso_escolha = curso_titulos[curso_index]
    curso_titulos[curso_index] in config or config.update({curso_escolha:{}})
    root_dir_nome = curso_escolha        
    listar_materias = navegador.find_elements(By.CLASS_NAME, 'boxCurso')
    materias_url = navegador.current_url
    titulo_materias = []
    
    for i in range(len(listar_materias)):
        titulo_materias.append(listar_materias[i].text)
        print(Colors.Underline + Colors.Red +'[' + Colors.Green + str(i) + Colors.Red + '] ' + Colors.Blue + listar_materias[i].text + Colors.Reset + '\n')
    
    #cap_prefix = Colors.Underline + Colors.Cyan + 'Selecione [tecla espaço] a(s) matéria(s) que deseja baixar: \n' + Colors.Reset
    materias_selecionar = titulo_materias
    
    os.path.exists(root_dir_nome) or os.mkdir(root_dir_nome, 0o777)
    # navegador.implicitly_wait(20)
    #is_clickable_waiter = WebDriverWait(navegador, 20)
    
    for m in range(len(materias_selecionar)):
        #listar_materias = navegador.find_elements(By.XPATH, '//*[@id="boxConteudo"]/div[2]/div/a')
        listar_materias = navegador.find_elements(By.CLASS_NAME, 'boxCurso')
        materia_dir_nome = listar_materias[m].text
        materia_dir_nome in config[curso_escolha] or config[curso_escolha].update({materia_dir_nome: {}})
        os.path.exists(root_dir_nome + '/' + materia_dir_nome) or os.mkdir(root_dir_nome + '/' + materia_dir_nome, 0o777)
        #navegador.get(listar_materias[m].get_attribute('href'))
        
        
        navegador.execute_script(f"window.scrollTo(0, {listar_materias[m].location['y']} / 2);")
        listar_materias[m].click()
        
        aulas_lista = navegador.find_elements(By.CLASS_NAME, 'Collapse-header')
        
        # for aula in aulas_lista:
        #     aula_nome = aula.text.split('\n')[0]
            
        
        for a in aulas_lista:
            print(a.text.split('\n')[0])
            aula_dir_nome = a.text.split('\n')[0]
            aula_dir_nome in config[curso_escolha][materia_dir_nome] or config[curso_escolha][materia_dir_nome].update({aula_dir_nome: {'start_video' : 0}})
            os.path.exists(root_dir_nome + '/' + materia_dir_nome + '/' + aula_dir_nome) or os.mkdir(root_dir_nome + '/' + materia_dir_nome + '/' + aula_dir_nome, 0o777)
            
            navegador.execute_script(f"window.scrollTo(0, {a.location['y']} / 2);")
            a.send_keys('\n')
            
            WebDriverWait(navegador, 60).until(
                EC.presence_of_element_located(
                        (By.CLASS_NAME, 'Collapse-header-container'),
                        
                    )
            )
            
            video_contents = navegador.find_elements(By.CLASS_NAME, 'ListVideos-items-video')
            
            if video_contents:
                for v in video_contents[config[curso_escolha][materia_dir_nome][aula_dir_nome]['start_video']:]:
                    video_dir_nome = v.find_element(By.TAG_NAME, 'a').text.split('\n')[0]
                    video_path = root_dir_nome + '/' + materia_dir_nome + '/' + aula_dir_nome + '/' + video_dir_nome
                    os.path.exists(video_path) or os.mkdir(video_path, 0o777)
                    #video_link = v.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    
                    video_link = v.find_element(By.TAG_NAME, 'a')
                    navegador.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center'})", video_link)
                    video_link.click()
                    
                    #navegador.execute_script("window.open('');")
                    #navegador.switch_to.window(navegador.window_handles[1])
                    #navegador.get(video_link)
                    
                    list_is_opened = navegador.find_elements(By.CSS_SELECTOR, 'div.Collapse-header-arrow.isOpened')
                    
                    if not list_is_opened:
                        player = navegador.find_element(By.CLASS_NAME, "icon-angle-down")
                        navegador.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center'})", player)
                        player.click()
                    
                    mp4 = navegador.find_elements(By.CLASS_NAME, 'Button')[1]
                    #time.sleep(10)
                    navegador.execute_script("arguments[0].scrollIntoView({behavior:'auto', block:'center', inline:'center'})", mp4)
                    #time.sleep(1)
                    mp4.click()
                    #print(mp4.get_attribute('src'), flush=True)
                    #cookies = navegador.get_cookies()
                    #print(cookies)
                    print('Baixando Vídeo...')
                    video_downloaded = False
                    
                    start_time = time.time()
                    
                    while not video_downloaded:
                        if Path('.temp').glob('*.mp4') and len(list((Path('.temp').glob('*.mp4')))) == 1:
                            f = list(Path('.temp').glob('*.mp4'))
                            os.rename(f[0], Path.cwd() / '.temp' / (video_dir_nome.lower() + '.mp4'))
                            video_to_be_moved = list(Path('.temp').glob('*.mp4'))[0]
                            print('Vídeo Baixado com Sucesso!')
                            video_downloaded = True
                        
                        if timeout(start_time, 600):
                            raise Exception("Tempo de download excedido. Verifique sua internet e tente novamente.")
                        time.sleep(2) #last changed ***********************************************************************************
                    
                    print('++++++++++++++++++++++')
                    print(f'+\n+\n+\n+{video_path}+\n+\n+\n+')
                    print('++++++++++++++++++++++')
                    
                    #f = f[0].split('/')[-1]
                    f = list(f)[0].resolve()
                    #print('Movendo o arquivo para a pasta de destino...')
                    
                    #print(f'========={Path(video_path + "/" + f).is_file()}==========')
                    #print(f'========={video_path}=========')
                    #print(f'========={f}=========')
                    
                    if not Path(Path(video_path) / video_to_be_moved.name).exists():
                        print('Movendo o Arquivo para a Pasta de Destino')
                        shutil.move(video_to_be_moved, video_path)
                        #f = f.with_stem()
                    #    os.system(f'move "{f}" "{Path(video_path).resolve()}"')
                    else:
                        print('ARQUIVO JÁ EXISTE')
                        video_to_be_moved.unlink()
                    
                    #if not Path(video_path + '/' + f).is_file():
                    #    print('Movendo o Arquivo para a Pasta de Destino...')
                    #    shutil.move(Path('.temp/' + f), video_path)
                    #else:
                    #    print('Arquivo já Existe')
                    #    os.remove('.temp\\' + f)
                    
                    #config[curso_escolha][materia_dir_nome][aula_dir_nome]['start_video'] += 1
                    
                    
                    material_extra = navegador.find_elements(By.CLASS_NAME, 'LessonButton')
                    
                    
                    for i, e in enumerate(material_extra):
                        file_link = material_extra[i].get_attribute('href')
                        if 'pdf' in file_link:
                            navegador.execute_script("window.open('');")
                            navegador.switch_to.window(navegador.window_handles[1])
                            navegador.get(file_link)
                            
                            #pdf = navegador.find_element(By.ID, 'icon')
                            #pdf.click()
                            print("Baixando Arquivo PDF...")
                            
                            file_downloaded = False
                            
                            start_time = time.time()
                            
                            while not file_downloaded:
                                if glob.glob(os.getcwd() + '/.temp/*.pdf') and len(glob.glob(os.getcwd() + '/.temp/*.pdf')) == 1:
                                    a = glob.glob(os.getcwd() + '/.temp/*.pdf')
                                    print('PDF Baixado com Sucesso!')
                                    file_downloaded = True
                                if timeout(start_time):
                                    raise Exception("Tempo de download excedido. Verifique sua internet e tente novamente.")
                                time.sleep(2)
                                
                            a = a[0].split('\\')[-1]    
                            # print('Movendo o arquivo para a pasta de destino...')
                            
                           
                            # shutil.move('.temp' / Path(a), video_path)
                            
                            if not Path(video_path + '/' + a).is_file():
                                print('Movendo o Arquivo para a Pasta de Destino...')
                                shutil.move('.temp\\' + a, video_path)
                            else:
                                print('Arquivo já existe')
                                os.remove('.temp\\' + a)
                                
                                
                                    
                            navegador.close()
                            navegador.switch_to.window(navegador.window_handles[0])
                        #print(e.text)
                        pass
                    
                    config[curso_escolha][materia_dir_nome][aula_dir_nome]['start_video'] += 1
                    
                    #navegador.close()
                    #navegador.switch_to.window(navegador.window_handles[0])
                    
                    with open('config.json', 'w') as outfile:
                        json.dump(config, outfile, indent=4)
            
            else:
                material_extra = navegador.find_elements(By.CLASS_NAME, 'LessonButton')
                
                for j, e in enumerate(material_extra):
                    pdf_link = material_extra[j].get_attribute('href')
                    
                    if 'pdf' in pdf_link:
                        pdf_dir_nome = 'PDF'
                        pdf_path = root_dir_nome + '/' + materia_dir_nome + '/' + aula_dir_nome + '/' + pdf_dir_nome
                        os.path.exists(pdf_path) or os.mkdir(pdf_path, 0o777)
                    
                        navegador.execute_script("window.open('');")
                        navegador.switch_to.window(navegador.window_handles[1])
                        navegador.get(pdf_link)
                        
                        #pdf = navegador.find_element(By.ID, 'icon')
                        #pdf.click()
                        print("Baixando Arquivo PDF...")
                        
                        file_downloaded = False
                        
                        start_time = time.time()
                        
                        while not file_downloaded:
                            if glob.glob(os.getcwd() + '/.temp/*.pdf') and len(glob.glob(os.getcwd() + '/.temp/*.pdf')) == 1:
                                a = glob.glob(os.getcwd() + '/.temp/*.pdf')
                                print('PDF Baixado com Sucesso!')
                                file_downloaded = True
                            if timeout(start_time):
                                raise Exception("Tempo de download excedido. Verifique sua internet e tente novamente.")
                            time.sleep(2)
                            
                        a = a[0].split('\\')[-1]    
                        #print('Movendo o arquivo para a pasta de destino...')
                        
                        
                        #shutil.move('.temp' / Path(a), pdf_path)
                        
                        if not Path(pdf_path + '/' + a).is_file():
                            print('Movendo o Arquivo para a Pasta de Destino...')
                            shutil.move('.temp\\' + a, pdf_path)
                        else:
                            print('Arquivo já existe na pasta')
                            os.remove('.temp\\' + a)
                            
                        
                        #config[curso_escolha][materia_dir_nome][aula_dir_nome]['start_video'] += 1
                        navegador.close()
                        navegador.switch_to.window(navegador.window_handles[0])
                        
                    config[curso_escolha][materia_dir_nome][aula_dir_nome]['start_video'] += 1
            
                    with open('config.json', 'w') as outfile:
                        json.dump(config, outfile, indent=4)
        
        #navegador.get(materias_url)
        
        menu = navegador.find_elements(By.CLASS_NAME, 'MenuButton')
    
    
        #while navegador.current_url != dashboard:
        #time.sleep(5)
        
        for m in menu:
            if 'Catálogo de Cursos' in m.text:
                m.click()
        
        time.sleep(20)
        link_cursos = navegador.find_elements(By.CLASS_NAME, 'Link')
            
        link_cursos[curso_index].click()

if __name__ == '__main__':
    main()
