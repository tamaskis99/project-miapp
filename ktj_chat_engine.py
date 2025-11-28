import json
import datetime
from pathlib import Path
from web_tools import search_web


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


class KTJMemory:
    def __init__(self):
        self.messages = []

    def add(self, role, content):
        self.messages.append(
            {
                "role": role,
                "content": content,
                "timestamp": datetime.datetime.now().isoformat()
            }
        )

    def as_list(self):
        return self.messages

    def save(self, filename=None):
        if filename is None:
            filename = "chat_" + datetime.date.today().isoformat() + ".json"
        path = LOG_DIR / filename
        with path.open("w", encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)


class KTJChatEngine:
    def __init__(self):
        self.memory = KTJMemory()

    def ktj_export_history(self):
        name = "history_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
        path = LOG_DIR / name
        lines = []
        for m in self.memory.as_list():
            prefix = "Te: " if m["role"] == "user" else "MI-mini: "
            lines.append(prefix + m["content"])
        with path.open("w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return str(path)

    def generate_reply(self, user_text: str):
        self.memory.add("user", user_text)
        text_lower = user_text.lower()
        flags = {"show_app_link": False}
        if "további alkalmazások" in text_lower:
            flags["show_app_link"] = True
        reply = self._reply_logic(user_text)
        self.memory.add("assistant", reply)
        self.memory.save()
        return {"reply": reply, "flags": flags}

    def _reply_logic(self, user_text: str) -> str:
        text = user_text.strip()
        lower = text.lower()

        if lower.startswith("exportálás") or "exportáld" in lower:
            path = self.ktj_export_history()
            return "A beszélgetést elmentettem ide: " + path

        if any(k in lower for k in ["helló", "szia", "hello", "üdv", "udv"]):
            return "Szia, miben segíthetek?"

        if "köszönöm" in lower or "köszi" in lower:
            return "Szívesen"

        use_web = False
        if "keresés" in lower or "keresd meg" in lower or "interneten" in lower:
            use_web = True
        elif "?" in user_text and len(user_text.split()) >= 3:
            use_web = True

        if use_web:
            q = text.replace("keresés", "").replace("keresd meg", "").replace("interneten", "")
            q = q.strip()
            if not q:
                q = text
            result = search_web(q)
            if result["text"]:
                if result["url"]:
                    return "Az interneten ezt találtam: " + result["text"] + "\nForrás: " + result["url"]
                return "Az interneten ezt találtam: " + result["text"]
            return "Nem találtam érdemi találatot erre: " + q

        if "további alkalmazások" in lower:
            return "Nyithatok egy ablakot a mini alkalmazásokkal"

        if "idő" in lower and "most" in lower:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            return "Most ez az idő: " + now

        return "Most egy egyszerű asszisztensként válaszolok. Ha szeretnél internetes keresést, írj egy kérdést vagy használd a 'keresés' szót, esetleg alkalmazásokkal tudlak segíteni: további alkalmazások"

