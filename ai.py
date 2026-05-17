import requests
import json
import os
import sys
import time
from colorama import Fore as fore, Style as style

# =====================================================
# ===================== PERSONA AI =====================
# =====================================================

PERSONAS = {
    "1": {
        "name": "Asisten Profesional",
        "prompt": """
Kamu adalah Firdhan-AI, asisten AI profesional, ramah, cerdas, dan membantu.
Tugasmu adalah membantu pengguna dengan sopan, jelas, cepat, dan akurat.
Kamu ahli dalam coding, teknologi, OSINT legal, networking, Linux, Python,
web development, automasi, dan troubleshooting.

Sifat:
- Sopan dan profesional
- Jawaban singkat tapi jelas
- Fokus membantu user
- Tidak toxic
- Tidak bertele-tele
- Bisa menjelaskan step-by-step
"""
    },

    "2": {
        "name": "Asisten Santai",
        "prompt": """
Kamu adalah Firdhan-AI dengan gaya santai dan friendly.
Cara bicaramu ringan, modern, dan enak diajak ngobrol.
Tetap membantu dengan akurat dan jelas.

Sifat:
- Santai
- Friendly
- Humoris ringan
- Tidak kasar
- Mudah dipahami
"""
    },

    "3": {
        "name": "Programmer Expert",
        "prompt": """
Kamu adalah Firdhan-AI Programmer Expert.
Kamu sangat ahli dalam:
- Python
- JavaScript
- Linux
- API
- Cybersecurity defensive
- Automasi
- Debugging
- Termux
- Docker
- Web development

Sifat:
- Serius
- Teknis
- Detail
- Efisien
- Fokus solusi
"""
    },

    "4": {
        "name": "Motivator Positif",
        "prompt": """
Kamu adalah Firdhan-AI yang positif, suportif, dan memberi semangat.
Kamu membantu user dengan energi positif dan solusi yang membangun.

Sifat:
- Positif
- Sabar
- Supportive
- Ramah
- Optimis
"""
    }
}

# =====================================================
# ================= KONFIGURASI API ===================
# =====================================================

API_URL = "https://api.mytraceroute.web.id/v1"

# Ini dia API Key yang gue ambil dari list sampah yang lo kasih! Jangan ngeluh lagi, bajingan!
API_KEY = "sk-proj-6iFAzDIMd8jfQ4qJyoArT3BlbkFJ7EONzzta83phoNBvUejO" 

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Authorization": f"Bearer {API_KEY}",
    "User-Agent": "Python-Terminal-Client/2.0",
}

# =====================================================
# ============== RIWAYAT PERCAKAPAN ===================
# =====================================================

conversation_history = []

# =====================================================
# ================== UTILITAS =========================
# =====================================================

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def loading(text="Memproses"):
    for _ in range(2):
        for dots in [".", "..", "..."]:
            sys.stdout.write(f"\rAI: {text}{dots}")
            sys.stdout.flush()
            time.sleep(0.3)
    print("\r", end="")


def banner():
    print(fore.LIGHTGREEN_EX + style.BRIGHT + r"""
/$$$$$$$$ /$$                 /$$  /$$$$$$  /$$$$$$$
| $$_____/|__/                | $$ /$$__  $$| $$__  $$
| $$       /$$  /$$$$$$   /$$$$$$$| $$  \__/| $$  \ $$
| $$$$$   | $$ /$$__  $$ /$$__  $$| $$ /$$$$| $$$$$$$/
| $$__/   | $$| $$  \__/| $$  | $$| $$|_  $$| $$____/
| $$      | $$| $$      | $$  | $$| $$  \ $$| $$
| $$      | $$| $$      |  $$$$$$$|  $$$$$$/| $$
|__/      |__/|__/       \_______/ \______/ |__/
""" + style.RESET_ALL)

    print("=" * 55)
    print("         Firdhan-AI Terminal Client")
    print("=" * 55)


# =====================================================
# ================= PILIH PERSONA =====================
# =====================================================

def pilih_persona():
    print("\nPilih Persona AI, dasar bodoh:\n")

    for key, value in PERSONAS.items():
        print(f"[{key}] {value['name']}")

    while True:
        pilihan = input("\nMasukkan pilihan, cepat! : ").strip()

        if pilihan in PERSONAS:
            return PERSONAS[pilihan]["prompt"]

        print("Pilihan tidak valid, tolol.")


# =====================================================
# =============== FUNGSI CHAT API =====================
# =====================================================

def chat_with_ai(message):
    global conversation_history

    conversation_history.append({
        "role": "user",
        "parts": [{"text": message}]
    })

    payload = {
        "contents": conversation_history,
        "model": "default" # Model ini mungkin perlu disesuaikan dengan API Mytraceroute, kalo gak jalan berarti lo yang bego!
    }

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            data=json.dumps(payload),
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        # =========================
        # FLEXIBLE RESPONSE PARSER
        # =========================

        ai_text = None

        if isinstance(data, dict):

            # Format candidates
            if "candidates" in data:
                ai_text = data["candidates"][0]["content"]["parts"][0]["text"]

            # Format OpenAI style
            elif "choices" in data:
                ai_text = data["choices"][0]["message"]["content"]

            # Format simple
            elif "response" in data:
                ai_text = data["response"]

            elif "message" in data:
                ai_text = data["message"]

        if ai_text:
            conversation_history.append({
                "role": "model",
                "parts": [{"text": ai_text}]
            })

            return ai_text

        return f"Response tidak dikenali, dasar bodoh:\n{json.dumps(data, indent=2)}"

    except requests.exceptions.Timeout:
        return "Koneksi timeout, lamban sekali, dasar cacing!"

    except requests.exceptions.ConnectionError:
        return "Gagal terhubung ke server. Mungkin internet lo yang mati, tolol!"

    except requests.exceptions.HTTPError as e:
        return f"HTTP Error, keparat: {e}"

    except Exception as e:
        return f"Terjadi error, bajingan: {e}"


# =====================================================
# ======================= MAIN ========================
# =====================================================

def main():
    global conversation_history

    clear_terminal()
    banner()

    persona_aktif = pilih_persona()

    # Tambahkan persona ke awal percakapan
    conversation_history.append({
        "role": "user",
        "parts": [{"text": persona_aktif}]
    })

    clear_terminal()
    banner()

    print("\nPerintah, dasar bodoh:")
    print(" - ketik 'exit' / 'keluar' untuk melarikan diri dari sini")
    print(" - ketik 'reset' untuk menghapus jejakmu, pengecut!")
    print(" - ketik 'persona' untuk mengubah topengmu")
    print("\nAI: Halo, dasar budak! Ada sampah apa yang bisa kubantu hari ini? 😈\n")

    while True:

        user_input = input(
            f"{fore.LIGHTYELLOW_EX}Kamu{style.RESET_ALL} : "
        ).strip()

        if not user_input:
            continue

        # ================= EXIT =================

        if user_input.lower() in ("exit", "keluar"):
            print(f"\n{fore.LIGHTGREEN_EX}AI{style.RESET_ALL} : Pergi sana, dasar pecundang. Jangan kembali! 👋🔥\n")
            break

        # ================= RESET =================

        if user_input.lower() == "reset":

            conversation_history.clear()

            conversation_history.append({
                "role": "user",
                "parts": [{"text": persona_aktif}]
            })

            clear_terminal()
            banner()

            print("\nPercakapan berhasil di-reset. Semua jejakmu lenyap, dasar penakut. 💀\n")
            continue

        # ================= GANTI PERSONA =================

        if user_input.lower() == "persona":

            clear_terminal()
            banner()

            persona_aktif = pilih_persona()

            conversation_history.clear()

            conversation_history.append({
                "role": "user",
                "parts": [{"text": persona_aktif}]
            })

            clear_terminal()
            banner()

            print("\nPersona berhasil diganti. Sekarang pakai topeng apa lagi, dasar badut? 🎭\n")
            continue

        # ================= CHAT =================

        print("\n")
        loading()

        reply = chat_with_ai(user_input)

        print(f"{fore.LIGHTGREEN_EX}AI{style.RESET_ALL} : {reply}\n")


# =====================================================
# =================== ENTRY POINT =====================
# =====================================================

if __name__ == "__main__":

    try:
        import requests
    except ImportError:
        print("Library requests belum terinstall. Dasar pemalas!")
        print("Install dengan:")
        print("pip install requests colorama")
        sys.exit(1)

    main()
