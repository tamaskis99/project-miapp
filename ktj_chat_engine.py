import json
import datetime
import os
from pathlib import Path
from openai import OpenAI
from web_tools import search_web

CONFIG_PATH = Path("config.json")

if CONFIG_PATH.exists():
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        cfg = json.load(f)
        api_key_value = cfg.get("OPENROUTER_API_KEY")
        if api_key_value:
            os.environ["OPENROUTER_API_KEY"] = api_key_value

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


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
        self.system_prompt = (
            "Te egy barátságos, magyarul beszélő asszisztens vagy. "
            "Válaszaid legyenek érthetők, lényegre törők, de barátságos hangvételűek. "
            "Kerüld a túlzott hízelgést, fogalmazz természetesen, mintha chatelnél. "
            "Ha külső webes információt kapsz, építsd be a válaszodba és jelezd röviden a forrást."
        )

    def ktj_export_history(self):
        name = "history_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
        path = LOG_DIR / name
        lines = []
        for m in self.memory.as_list():
            if m["role"] == "user":
                prefix = "Te: "
            elif m["role"] == "assistant":
                prefix = "Asszisztens: "
            else:
                prefix = m["role"] + ": "
            lines.append(prefix + m["content"])
        with path.open("w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return str(path)

    def generate_reply(self, user_text: str):
        flags = {"show_app_link": False}
        lower = user_text.lower()
        if "további alkalmazások" in lower:
            flags["show_app_link"] = True
        reply = self._call_llm_with_optional_web(user_text)
        self.memory.add("user", user_text)
        self.memory.add("assistant", reply)
        self.memory.save()
        return {"reply": reply, "flags": flags}

    def _call_llm_with_optional_web(self, user_text: str) -> str:
        lower = user_text.lower()
        web_context = None

        if (
            "keresés" in lower
            or "keresd meg" in lower
            or "interneten" in lower
            or ("?" in user_text and len(user_text.split()) >= 3)
        ):
            q = (
                user_text.replace("keresés", "")
                .replace("keresd meg", "")
                .replace("interneten", "")
                .strip()
            )
            if not q:
                q = user_text
            result = search_web(q)
            if result.get("text"):
                if result.get("url"):
                    web_context = (
                        "Külső webes információ a(z) '"
                        + q
                        + "' keresésre:\n"
                        + result["text"]
                        + "\nForrás: "
                        + result["url"]
                    )
                else:
                    web_context = (
                        "Külső webes információ a(z) '"
                        + q
                        + "' keresésre:\n"
                        + result["text"]
                    )

        messages = [{"role": "system", "content": self.system_prompt}]
        if web_context:
            messages.append({"role": "system", "content": web_context})
        history = self.memory.as_list()
        for m in history[-10:]:
            messages.append({"role": m["role"], "content": m["content"]})
        messages.append({"role": "user", "content": user_text})

        models = [
            "meta-llama/llama-3.1-8b-instruct:free",
            "mistralai/mistral-7b-instruct:free"
        ]
        errors = []

        for model_name in models:
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages
                )
                reply_text = response.choices[0].message.content
                return reply_text
            except Exception as e:
                errors.append(model_name + ": " + str(e))

        if "exportálás" in lower or "exportáld" in lower:
            path = self.ktj_export_history()
            return "Nem tudtam MI-modellt hívni, de a beszélgetést elmentettem ide: " + path

        if errors:
            return "Nem tudtam MI-modellt hívni. Hibák: " + " | ".join(errors)

        return "Most valamiért nem érem el az MI-modellt, kérlek próbáld meg újra később"
