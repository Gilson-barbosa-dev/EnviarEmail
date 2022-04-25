from http import server
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email.mime.base import MIMEBase
from email import encoders

import PySimpleGUI as sg

# SISTEMA BÁSICO DE ENVIO DE EMAIL 

'''
Bibliotecas a ser importadas

from http import server
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email.mime.base import MIMEBase
from email import encoders

import PySimpleGUI as sg
'''
# ==== Layout começa aqui ======

# Layout - campos de leitura botão e-mail e enviar
layout = [
    [sg.Text('Email'), sg.Input(key='email')],
    [sg.Button('Enviar')],
    [sg.Output(size=(50,30))] #Output de log
]

#Janela

janela = sg.Window('Enviar Email', layout) # Deseign da Janela - aqui você define o nome da janela

# Ler arquivos - Aqui lê o e-mail de destino que o usuário digitou

while True:
    eventos, valores = janela.read() # Lê os valores que o usuário digitou
    if eventos == sg.WINDOW_CLOSED: # caso o usuário feche a janela interrompemos o programa
        break
    nome = valores['email'] # Variável que passa o destinatário da e-mail
    print(nome)

# ==== Layout termina aqui ======

# ==== Programação começa aqui ======
    # Startar o servidor SMTP

    host    = "" # SMTP do servidor de e-mail 
    port    = "" # Porta do servidor
    login   = "" # E-mail de envio
    senha   = "" # Senha do email

    server = smtplib.SMTP(host,port)

    server.ehlo()
    server.starttls()
    server.login(login,senha)

    # Montando E-mail - Corpo do e-mail quebrar em base HTML

    corpo = "Mensagem do corpo do e-mail aqui você pode editar em formato HTML"

    email_msg = MIMEMultipart()
    email_msg['From']    = login # E-mail remetente o mesmo que configurado na conexão
    email_msg['To']      = nome #E-mail de destino digitado pelo usuário - digitado pela interfase
    email_msg['Subject'] = "" # Título do E-mail
    email_msg.attach(MIMEText(corpo,'html'))

    # caminho do arquivo que vai ser anexado

    cam_arquivo = ".arquivo" # Arquivo que vai ser enviado - ps precisa passar o caminho e nome do arquivo.
    attachment = open(cam_arquivo, 'rb')

    # Convertendo para base 64 padrão de envio de e-mail
    att = MIMEBase('application', 'octet-stream')
    att.set_payload(attachment.read())
    encoders.encode_base64(att)

    # Nome do arquivo anexado
    att.add_header('Content-Disposition', f'attachment; filename=nome do anexo')
    attachment.close()
    email_msg.attach(att)

    #Enviar o EMAIL
    server.sendmail(email_msg['From'], email_msg['To'],email_msg.as_string())
    #Fechar o Servidor de e-mail
    server.quit()

    print("== Email Enviado ==")
# ==== Programação termina aqui ======
