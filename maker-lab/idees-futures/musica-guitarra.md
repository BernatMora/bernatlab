# Idees - Musica i guitarra

> Projectes relacionats amb la musica i la guitarra: pedals MIDI, metronoms, controladors de peu, entrenadors de ritme.

## Idees

### Metronom visual amb LEDs

- **Dificultat**: Baixa-mitjana
- **Cost**: ~15 EUR
- **Temps**: 3-4 h
- **Components**: ESP32 + tira de LEDs WS2812B (NeoPixels) + polsador + buzzer
- **Utilitat real**: Metronom amb indicacio visual (LEDs que es mouen) i sonora.
- **Coneixements**: PWM, NeoPixels, timers, audio basic.
- **Integracio**: Es pot connectar via MIDI USB per controlar-lo des del DAW.

### Controlador de peu MIDI

- **Dificultat**: Mitjana
- **Cost**: ~20 EUR
- **Temps**: 4-5 h
- **Components**: ESP32 + 4-6 polsadors + caixa impresa en 3D + USB MIDI
- **Utilitat real**: Controlar el DAW o efectes amb els peus mentre toques la guitarra.
- **Coneixements**: MIDI USB, entrada digital, debouncing.
- **Integracio**: Funciona amb qualsevol DAW (Reaper, Ableton, ...).

### Botonera programable per a Guitar Rig / amplitus virtuals

- **Dificultat**: Mitjana
- **Cost**: ~20 EUR
- **Temps**: 4-5 h
- **Components**: ESP32 + 6-8 polsadors + OLED 0,96" + caixa
- **Utilitat real**: Canviar de preset, activar/desactivar efectes, mostrar el nom del preset.
- **Coneixements**: MIDI, pantalles OLED, entrada digital.
- **Integracio**: Funciona amb qualsevol programa que accepti MIDI.

### Entrenador de ritme amb metrica i feedback visual

- **Dificultat**: Mitjana-alta
- **Cost**: ~30 EUR
- **Temps**: 6-8 h
- **Components**: ESP32 + accelerometre MPU6050 + buzzer + NeoPixels
- **Utilitat real**: Mesurar el tempo real mentre toques i mostrar si vas massa rapid o massa lent.
- **Coneixements**: I2C, sensors de moviment, processament de senyal, audio.
- **Integracio**: Es pot conectar a un mobil via BLE per veure la grafica.

### Analitzador simplistic de so amb FFT

- **Dificultat**: Alta
- **Cost**: ~30 EUR
- **Temps**: 8-10 h
- **Components**: ESP32 + microfon MAX4466 + OLED o tira de LEDs
- **Utilitat real**: Mostrar lespai frequencial del que toques.
- **Coneixements**: ADC, FFT, processament de senyal en temps real.
- **Integracio**: Es pot integrar amb un sistema mes gran danalisi musical.

### Generador de patrons ritmics aleatoris

- **Dificultat**: Mitjana
- **Cost**: ~15 EUR
- **Temps**: 4-5 h
- **Components**: ESP32 + buzzer + 2-3 polsadors + OLED
- **Utilitat real**: Generar patrons ritmics aleatoris per practicar.
- **Coneixements**: Aleatorietat, timers, audio.
- **Integracio**: Es pot connectar via MIDI per enviar els patrons a un DAW.
