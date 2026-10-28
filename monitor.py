import requests
import hashlib
import time
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# ==================== CONFIGURAÇÕES ====================

# Página que você quer monitorar
URL = "https://arede.info/Ultimas)"          # ← Coloque a URL aqui

# Intervalo entre verificações (em segundos)
INTERVALO = 300                             # 300 = 5 minutos

# Configurações do e-mail (Gmail recomendado)
EMAIL_REMETENTE = "hugopurger@gmail.com"      # ← Seu e-mail
SENHA_APP = "aoaz hpdm liwh ajyr"           # ← Senha de app do Gmail
EMAIL_DESTINO = "whainerlima@outlook.com.br"        # ← Para onde vai o alerta (pode ser o mesmo)

# Arquivo que guarda o último hash
ARQUIVO_HASH = "ultimo_hash.txt"

# =======================================================

def obter_conteudo(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36"
    }
    try:
        resposta = requests.get(url, headers=headers, timeout=20)
        resposta.raise_for_status()
        return resposta.text
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Erro ao acessar: {e}")
        return None

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
    try:
        msg = MIMEText(mensagem)
        msg["Subject"] = assunto
        msg["From"] = EMAIL_REMETENTE
        msg["To"] = EMAIL_DESTINO

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(EMAIL_REMETENTE, SENHA_APP)
            servidor.send_message(msg)

        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def monitorar():
    print(f"Monitorando: {URL}")
    print(f"Verificando a cada {INTERVALO} segundos...\n")

    hash_anterior = carregar_hash()

    while True:
        agora = datetime.now().strftime("%H:%M:%S")
        conteudo = obter_conteudo(URL)

        if conteudo is None:
            time.sleep(INTERVALO)
            continue

        hash_atual = calcular_hash(conteudo)

        if hash_anterior is None:
            print(f"[{agora}] Primeira verificação. Hash salvo.")
            salvar_hash(hash_atual)
            hash_anterior = hash_atual

        elif hash_atual != hash_anterior:
            print(f"\n⚠️  [{agora}] MUDANÇA DETECTADA!")
            
            mensagem = f"""
Mudança detectada na página!

URL: {URL}
Horário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

Hash anterior: {hash_anterior}
Hash atual:   {hash_atual}
"""
            enviar_email("⚠️ Alteração detectada na página", mensagem)
            
            salvar_hash(hash_atual)
            hash_anterior = hash_atual
        else:
            print(f"[{agora}] Sem alterações.")

        time.sleep(INTERVALO)

if __name__ == "__main__":
    monitorar()