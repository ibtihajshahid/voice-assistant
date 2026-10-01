import sys
import io
# Force UTF-8 encoding for Windows console (fixes Urdu printing)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pywhatkit
import webbrowser
import speech_recognition as sr
import os
import pyautogui
import screen_brightness_control as sbc
import psutil
try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

# --- Voice Engine Setup (safe) ---
engine = None
if pyttsx3 is not None:
    try:
        engine = pyttsx3.init()
    except Exception:
        engine = None

# --- Boy & Professional Voice Configuration (safe) ---
if engine is not None:
    try:
        voices = engine.getProperty('voices')
        selected = False
        for voice in voices:
            name_l = (voice.name or "").lower()
            if "david" in name_l or "male" in name_l:
                engine.setProperty('voice', voice.id)
                selected = True
                break

        # اگر preferred voice نہ ملے تو crash نہ ہو
        if not selected and voices:
            engine.setProperty('voice', voices[0].id)

        # آواز کی رفتار
        engine.setProperty('rate', 175)
    except Exception:
        pass

def speak(text):
    print(f"Alexa (Male): {text}")
    if engine is None:
        return
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass

def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("\nListening...")
        audio = r.listen(source, phrase_time_limit=5)
    try:
        query = r.recognize_google(audio, language='ur-PK')
        if not query:
            return ""
        print(f"You said: {query}")
        return query.lower()
    except Exception:
        return ""

def alexa_assistant():
    # پروفیشنل اور بھاری میل آواز میں شروعات
    speak("جی باس، میں حاضر ہوں۔ حکم کریں، کیا کرنا ہے؟")
    
    while True:
        query = listen_command()
        if not query:
            continue

        # --- Keyword Fixing (Urdu Correction) ---
        if "الیگزی" in query or "ایگزیکٹیو" in query or "الیکسا" in query:
            query = query.replace("الیگزی", "alexa").replace("ایگزیکٹیو", "alexa").replace("الیکسا", "alexa")

        # 1. Laptop Shutdown & Restart
        if "شٹ ڈاؤن" in query or "shutdown" in query or "بند کرو لیپ ٹاپ" in query or "لیپ ٹاپ بند کرو" in query:
            speak("ٹھیک ہے باس، لیپ ٹاپ پندرہ سیکنڈ میں شٹ ڈاؤن ہو جائے گا۔ اپنا خیال رکھیے گا، اللہ حافظ۔")
            os.system("shutdown /s /t 15")
            break

        elif "ریسٹارٹ" in query or "restart" in query or "دوبارہ چلاؤ" in query:
            speak("ٹھیک ہے باس، سسٹم ری اسٹارٹ ہو رہا ہے۔ میں ابھی واپس آتا ہوں۔")
            os.system("shutdown /r /t 15")
            break

        # 2. YouTube & Music Play
        elif "چلاؤ" in query or "play" in query:
            song = (
                query.replace("alexa", "")
                .replace("چلاؤ", "")
                .replace("play", "")
                .strip()
            )
            if not song:
                speak("کس چیز کو چلاؤں باس؟")
                continue
            # --- UPDATED: Speaks "Ok" first ---
            speak(f"Ok boss, playing {song} on YouTube")
            pywhatkit.playonyt(song)

        # 3. Google Search
        elif "سرچ" in query or "search" in query:
            term = query.replace("alexa", "").replace("سرچ", "").replace("search", "").strip()
            # --- UPDATED: Speaks "Ok" first ---
            speak(f"Ok, searching for {term} on Google")
            pywhatkit.search(term)

        # 4. Volume Control
        elif "volume down" in query or "کم کرو" in query or "ڈیکریز" in query:
            pyautogui.press("volumedown", presses=10)
            speak("Ok, volume kam kar diya")

        elif "volume up" in query or "بڑھاؤ" in query or "انکریز" in query:
            pyautogui.press("volumeup", presses=10)
            speak("Ok boss, volume barha diya")

        # 5. Brightness
        elif "brightness" in query or "روشنی" in query:
            if "کم" in query or "down" in query:
                sbc.set_brightness('-30')
                speak("Ok, brightness kam ho gayi")
            else:
                sbc.set_brightness('+30')
                speak("Ok, brightness barh gayi")

        # 6. Universal Website Opener
        elif "open" in query or "کھولو" in query or "اوپن" in query:
            target = query.replace("alexa", "").replace("open", "").replace("کھولو", "").replace("اوپن", "").strip()

            if "یوٹیوب" in target or "youtube" in target:
                # --- UPDATED: Speaks "Ok" first ---
                speak("Ok, opening YouTube")
                webbrowser.open("https://youtube.com")
            elif "گوگل" in target or "google" in target:
                # --- UPDATED: Speaks "Ok" first ---
                speak("Ok, opening Google")
                webbrowser.open("https://google.com")
            elif "فیس بک" in target or "facebook" in target:
                # --- UPDATED: Speaks "Ok" first ---
                speak("Ok boss, opening Facebook")
                webbrowser.open("https://facebook.com")
            elif "واٹس ایپ" in target or "whatsapp" in target:
                # --- UPDATED: Speaks "Ok" first ---
                speak("Ok, opening WhatsApp")
                webbrowser.open("https://whatsapp.com")
            elif target != "":
                # unknown website: open google search instead of broken URL
                # --- UPDATED: Speaks "Ok" first ---
                speak(f"Ok, searching {target} on Google")
                webbrowser.open(f"https://www.google.com/search?q={target}")

        # 7. Close Program / Exit
        elif "بند" in query or "exit" in query or "اللہ حافظ" in query:
            speak("اللہ حافظ باس، پھر ملتے ہیں۔")
            break

if __name__ == "__main__":
    alexa_assistant()
