import requests
import hashlib
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime

URL = os.environ.get("https://www.pontagrossa.pr.gov.br/concursos/")
EMAIL_REMETENTE = os.environ.get("hugopurger@gmail.com")
SENHA_APP = os.environ.get("aoaz hpdm liwh ajyr")
EMAIL_DESTINO = os.environ.get("whainerlima@outlook.com.br")
ARQUIVO_HASH = "ultimo_hash.txt"

def obter_conteudo(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    resposta = requests.get(url, headers=headers, timeout=20)
    resposta.raise_for_status()
    return resposta.text

def calcular_hash(conteudo):
    return hashlib.sha256(conteudo.encode("utf-8")).hexdigest()

def carregar_hash():
    try:
        with open(ARQUIVO_HASH, "r") as f:
            return f.read().strip()
    except:
        return None

def salvar_hash(hash_atual):
    with open(ARQUIVO_HASH, "w") as f:
        f.write(hash_atual)

def enviar_email(assunto, mensagem):
    msg = MIMEText(mensagem)
    msg["Subject"] = assunto
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = EMAIL_DESTINO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(EMAIL_REMETENTE, SENHA_APP)
        servidor.send_message(msg)

def main():
    hash_anterior = carregar_hash()
    conteudo = obter_conteudo(URL)
    hash_atual = calcular_hash(conteudo)

    if hash_anterior is None:
        print("Primeira execução. Salvando hash inicial.")
        salvar_hash(hash_atual)
        return

    if hash_atual != hash_anterior:
        print("⚠️ Mudança detectada!")
        mensagem = f"""
Mudança detectada na página!

URL: {URL}
Horário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} UTC

Hash anterior: {hash_anterior}
Hash atual:   {hash_atual}
"""
        enviar_email("⚠️ Alteração detectada na página", mensagem)
        salvar_hash(hash_atual)
    else:
        print("Sem alterações.")

if __name__ == "__main__":
    main()