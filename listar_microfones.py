import pyaudio

p = pyaudio.PyAudio()
print("\n--- Entradas de Áudio Disponíveis no Windows ---")

for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    # Filtra apenas dispositivos que captam áudio (microfones)
    if info['maxInputChannels'] > 0:
        print(f"ID [{i}]: {info['name']}")

print("------------------------------------------------")
p.terminate()