# MI-alapú Chat Asszisztens – Tkinter alkalmazással és mini appokkal  
**Készítette:** Kis Tamás József (KTJ)  
**Neptun-kód:** LPGJPZ

---

A `config.json` fájlban az "API KULCS HELYE" (2. sor a programban) részre a két idézőjel közé be kell másolni az API kulcsot, amely a következő: 
- `sk-or-v1-c9ccab9a4c e8a4cc51fdcc7d015b6 a25d88c605176f4b76 298e0426bdd1019ec`
FONTOS! A SZÓKÖZÖKET TÁVOLÍTSUK EL!

---

## Projekt rövid leírása

A projekt célja egy olyan komplex Python alkalmazás létrehozása, amely:

- grafikus felületen (Tkinter) keresztül fut,
- mesterséges intelligenciát (OpenRouter API – Llama / Mistral modellek) használ,
- emlékszik a beszélgetés előzményeire (memória modul),
- képes interneten keresztül információt gyűjteni (DuckDuckGo + Wikipedia API),
- mini alkalmazásokat is tartalmaz (költségfigyelő, jegyzetelő, időzítő, naptár),
- minden programrészt külön modulban tárol a jobb átláthatóság érdekében,
- betartja a tantárgyi előírásokat: saját modul, saját osztály, saját függvény – **KTJ monogrammal**.

Az alkalmazás teljes mértékben Python 3 kompatibilis, külső könyvtárak minimális használatával.

---

## Mesterséges intelligencia működése

A rendszer az **OpenRouter API** használja és hív meg ingyenesen elérhető modelleket:

- `meta-llama/llama-3.1-8b-instruct:free`
- `mistralai/mistral-7b-instruct:free`

A beszélgetés teljes kontextusa (system prompt + korábbi 10 üzenet) átadásra kerül a MI-modellnek, valamint opcionálisan webes információ is bekerülhet, ha a felhasználó keresést kezdeményez.

Az MI részért a `KTJChatEngine` osztály felel.

---
## 📁 Fájlstruktúra
```
project-miapp/
│
├── main.py # Főprogram – Tkinter GUI indítása
├── ktj_chat_engine.py # KTJ monogramos MI-motor modul
├── web_tools.py # Internetes keresőmodul
├── config.json # API kulcs helye (`Email-ben továbbítva`)
├── logs/ # Chat-naplózás
│
├── apps/
│ ├── ktj_costs.py # Költség elemző mini app
│ ├── ktj_notes.py # Jegyzetelő mini app
│ ├── ktj_timer.py # Időzítő mini app
│ └── ktj_calendar.py # Naptár mini app
│
└── README.md
```
---

## 🧩 Modulok és funkciók (a tantárgyi követelmények szerint)

### Tanult modulok
- `tkinter`
- `json`
- `os`
- `datetime`
- `requests`

### Bemutatandó modul
- `openai` (Az OpenAI által létrehozott OpenRouter API használata)

### Saját modul
- `ktj_chat_engine.py`  
  - KTJ monogrammal ellátott fejlesztés

### Saját osztály:  
- `KTJChatEngine`  
  – a teljes MI működésért, memóriakezelésért és webes keresések integrálásáért felel

### Saját függvény:
- `ktj_export_history()`  
  – KTJ monogramos beszélgetés-exportáló

### Grafikai modul és eseménykezelés
- Tkinter gombok, beviteli mezők, új ablak megnyitása (mini appok)

---

## Internetes keresés működése

A `web_tools.py` modulokból:

1. DuckDuckGo JSON API (`AbstractText`, `RelatedTopics`)
2. Magyar Wikipédia (ha működik)
3. Angol Wikipédia (fallback)

A text + URL visszakerül a chatmotorba, amely ezt hozzáadja a modell kontextusához.

### Fontos kihangsúlyozni, hogy ezt a módszert csak akkor használja, ha MI-modell nem elérhető valamiért.

---

## Telepítés és futtatás

### 1. Szükséges csomagok telepítése:
```
pip install openai requests
```
