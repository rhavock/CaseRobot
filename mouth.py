import os
import asyncio
import pygame
import edge_tts

# OTIMIZAÇÃO 1: Inicializa o mixer do sistema UMA ÚNICA VEZ globalmente
pygame.mixer.init()

def limpar_texto(texto):
    caracteres_proibidos = ['*', '#', '_', '`', '~', '"']
    for char in caracteres_proibidos:
        texto = texto.replace(char, '')
    return texto

async def gerar_e_falar(texto):
    texto_limpo = limpar_texto(texto)
    if not texto_limpo.strip():
        return
        
    print(f"\n[Robson falando]: {texto_limpo}")
    
    voz = "pt-BR-AntonioNeural" 
    communicate = edge_tts.Communicate(texto_limpo, voz, rate="+15%")
    
    arquivo_audio = "resposta_robson.mp3"
    await communicate.save(arquivo_audio)
    
    # OTIMIZAÇÃO 2: Pula a inicialização e vai direto para a execução
    pygame.mixer.music.load(arquivo_audio)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
    pygame.mixer.music.unload()
    os.remove(arquivo_audio)

def falar(texto):
    asyncio.run(gerar_e_falar(texto))

if __name__ == "__main__":
    falar("Módulo de voz neural carregado e otimizado para velocidade.")