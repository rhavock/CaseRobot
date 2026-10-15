from brain import pensar
from mouth import falar

falar("Sistemas centrais conectados. Aguardando entrada manual de dados.")

while True:
    comando = input("\n[Você]: ")
    
    if comando.lower() in ['sair', 'desligar', 'encerrar']:
        falar("Encerrando operações. Até logo.")
        break
        
    # Envia o texto para o Groq (Cérebro)
    resposta = pensar(comando)
    
    # Envia a resposta do Cérebro para o Áudio (Boca)
    falar(resposta)