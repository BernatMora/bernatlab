# Qüestionari - Capitol 4: Prompt engineering

> 10 preguntes · ~15 min

## Pregunta 1

Que es un "prompt"?

- [ ] El nom d'un model d'IA
- [x] La pregunta o instruccio que dones a un LLM
- [ ] Un tipus de memoria RAM
- [ ] Un error del sistema

## Pregunta 2

Quina es la tecnica que consisteix a donar exemples dins del prompt per ensenyar el format esperat?

- [ ] Zero-shot prompting
- [x] Few-shot prompting
- [ ] Chain of thought
- [ ] Role prompting

## Pregunta 3

Quin es el millor prompt per demanar consells de seguretat per a una RPi?

- [ ] "Com millorar la seguretat?"
- [x] "Soc admin d'una RPi 4 amb SSH obert a Internet. Dona'm 5 consells concrets de seguretat ordenats per prioritat."
- [ ] "Seguretat"
- [ ] "Escriu sobre seguretat"

## Pregunta 4

Que es el "chain-of-thought prompting"?

- [ ] Pensar en veu alta davant del model
- [x] Demanar al model que raoni pas a pas abans de donar la resposta
- [ ] Encadenar multiples models
- [ ] Una cadena de text molt llarga

## Pregunta 5

Quin rol té el "system prompt" a l'API de xat d'Ollama?

- [ ] Es la primera pregunta de l'usuari
- [x] Conte instruccions permanents sobre el rol i estil del model
- [ ] Es el prompt de benvinguda
- [ ] No existeix a Ollama

## Pregunta 6

Per que es important usar delimitadors (com `[INSTRUCCIONS]`, `[DADES]`) en prompts llargs?

- [ ] Per estalviar memoria
- [x] Per ajudar el model a distingir les diferents parts del prompt
- [ ] Perque Ollama ho requereix
- [ ] No es important

## Pregunta 7

Quin es l'error mes comu en escriure prompts?

- [ ] Fer preguntes massa llargues
- [x] Fer preguntes massa obertes o vagues
- [ ] Usar angles en lloc de catala
- [ ] Posar exemples

## Pregunta 8

Quin es el format de sortida correcte per a un prompt que vol JSON?

- [ ] "Escriu la sortida en JSON"
- [x] "Respon nomes amb JSON valid, sense text adicional. Format: {...}"
- [ ] "Fes-ho estructurat"
- [ ] "Vull un objecte"

## Pregunta 9 (oberta)

Tens un log del sistema amb aquesta linia: `Mar 15 03:42:17 rpi sshd[1234]: Failed password for root from 185.143.223.47 port 44231 ssh2`. Escriu un prompt ben dissenyat per demanar al LLM que l'analitzi i suggereixi accions.

Pistes per respondre:
- Especifica el rol (expert en seguretat? administrador?).
- Dona el contexte (RPi 4 amb SSH obert).
- Indica el format de sortida (analisi + risc + accions).
- Demana un maxim de longitud.

## Pregunta 10 (oberta)

Explica amb les teves paraules la diferencia entre un prompt "zero-shot", "few-shot" i "chain-of-thought". Posa un exemple de cada un aplicat a una tasca del BernatLab (pot ser analitzar logs, generar scripts, etc.).

Pistes per respondre:
- Zero-shot: prompt directe, sense exemples.
- Few-shot: amb 1-3 exemples del que vols.
- Chain-of-thought: pas a pas, deixant "veure" el raonament.
- Tria una tasca realista: resumir logs, classificar correus, generar scripts.
