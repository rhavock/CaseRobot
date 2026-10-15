import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer
import speech_recognition as sr

if not os.path.exists("model"):
    print("\n[ERRO CRÍTICO] Pasta 'model' não encontrada.")
    exit(1)

print("Carregando sistema neural de audição (isso pode levar alguns segundos)...")
modelo_vosk = Model("model")
recognizer_vosk = KaldiRecognizer(modelo_vosk, 16000)

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000, input_device_index=3)
stream.start_stream()

def escutar_comando_principal():
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=3) as source:
        print("\n[CASE] Microfone principal aberto. Pode falar...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
        
    try:
        print("[CASE] Processando áudio principal...")
        texto = recognizer.recognize_google(audio, language="pt-BR")
        return texto
    except:
        return None

def iniciar_vigiia():
    print("\nSistema CASE online e vigiando.")
    print("Fale qualquer coisa para testarmos o que ele está ouvindo.\n")

    # Expandimos as possibilidades de como o modelo em português pode "escrever" a palavra CASE
    gatilhos = ["case", "keis", "queise", "keys", "quem é", "que ex", "que diz", "vez"]

    try:
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            
            if recognizer_vosk.AcceptWaveform(data):
                resultado = json.loads(recognizer_vosk.Result())
                texto_detectado = resultado.get("text", "")
                
                # MODO RAIO-X: Vai imprimir tudo o que ele achar que você disse
                if texto_detectado.strip():
                    print(f"[RAIO-X VOSK ouviu]: '{texto_detectado}'")
                
                # Checa se algum dos gatilhos foi falado
                if any(gatilho in texto_detectado.lower() for gatilho in gatilhos):
                    print("\n[CASE] Acordou!")
                    
                    # PAUSA O VOSK PARA LIBERAR O MICROFONE PRO GOOGLE
                    stream.stop_stream()
                    
                    comando = escutar_comando_principal()
                    if comando:
                        print(f"-> Comando capturado: '{comando}'")
                        
                    print("\nVoltando ao modo de vigília...")
                    
                    # REATIVA O VOSK
                    stream.start_stream()
                    
    except KeyboardInterrupt:
        print("\n[CASE] Encerrando módulos de escuta.")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()

if __name__ == "__main__":
    iniciar_vigiia()