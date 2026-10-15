import pyttsx3

print("Iniciando diagnóstico de áudio...")

try:
    # Força a inicialização com o motor do Windows
    engine = pyttsx3.init('sapi5') 
    voices = engine.getProperty('voices')
    
    print("\n--- Vozes Instaladas no seu Windows ---")
    for i, voice in enumerate(voices):
        print(f"[{i}] {voice.name}")
    print("---------------------------------------")
    
    print("\nTentando emitir som pelo alto-falante...")
    
    # Vamos forçar a leitura com a primeira voz da lista (mesmo que seja em inglês)
    if len(voices) > 0:
        engine.setProperty('voice', voices[0].id)
    
    engine.say("Testando o sistema de áudio do CASE.")
    engine.runAndWait()
    
    print("\n[Diagnóstico concluído] O comando de áudio foi enviado com sucesso.")

except Exception as e:
    print(f"\n[ERRO CRÍTICO] O motor de voz falhou: {e}")