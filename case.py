import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer
import speech_recognition as sr
from brain import pensar
from mouth import falar
import winsound # <-- Biblioteca nativa do Windows para emitir bipes

# ==========================================
# SEU MICROFONE (Mantenha o seu ID)
ID_MICROFONE = 3  
# ==========================================

if not os.path.exists("model"):
    print("\n[ERRO CRÍTICO] Pasta 'model' não encontrada.")
    exit(1)

print("Iniciando módulos do assistente em modo de baixa latência...")
modelo_vosk = Model("model")
vocabulario_restrito = '["robson", "robinson", "hobby som", "[unk]"]'
recognizer_vosk = KaldiRecognizer(modelo_vosk, 16000, vocabulario_restrito)
pa = pyaudio.PyAudio()

def escutar_comando_principal():
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=ID_MICROFONE) as source:
        print("\n[Ouvindo o seu comando principal...]")
        
        # Bipe 1 (Agudo): Avisa que abriu os ouvidos e você pode falar
        winsound.Beep(800, 150) 
        
        # Escuta o comando
        # timeout = espera até 10 segundos para você começar a falar
        # phrase_time_limit = permite que você fale ininterruptamente por até 15 segundos
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
        
        # Bipe 2 (Grave): Avisa que você parou de falar e ele está processando
        winsound.Beep(400, 150) 
        print("[Robson pensando...]")
        
    try:
        texto = recognizer.recognize_google(audio, language="pt-BR")
        print(f"[Você]: {texto}")
        return texto
    except:
        return None

def iniciar_sistema():
    falar("Protocolos de latência minimizados. Estou pronto.")
    print(f"\nUsando Microfone ID [{ID_MICROFONE}]. Diga 'Robson' para interagir.\n")

    gatilhos = ["robson", "robinson", "hobby som"]

    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000, input_device_index=ID_MICROFONE)
    stream.start_stream()

    try:
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            
            if recognizer_vosk.AcceptWaveform(data):
                resultado = json.loads(recognizer_vosk.Result())
                texto_detectado = resultado.get("text", "")
                
                if texto_detectado.strip() and texto_detectado != "[unk]":
                    print(f"[RAIO-X]: '{texto_detectado}'")
                
                if any(gatilho in texto_detectado.lower() for gatilho in gatilhos):
                    print("\n[Gatilho Detectado]")
                    
                    stream.stop_stream()
                    stream.close()
                    
                    # OTIMIZAÇÃO 5: Removido o falar("Sim?").
                    # Agora ele pula direto para escutar, emitindo apenas o bipe instantâneo.
                    comando = escutar_comando_principal()
                    
                    if comando:
                        resposta = pensar(comando)
                        falar(resposta)
                        
                    print("\n[Voltando ao modo de vigília...]")
                    
                    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000, input_device_index=ID_MICROFONE)
                    stream.start_stream()
                    
    except KeyboardInterrupt:
        falar("Encerrando operações do sistema.")
    finally:
        if 'stream' in locals() and stream.is_active():
            stream.stop_stream()
            stream.close()
        pa.terminate()

if __name__ == "__main__":
    iniciar_sistema()