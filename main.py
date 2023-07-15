import os
import speech_recognition as sr
import tkinter as tk
from tkinter import filedialog, messagebox, IntVar
import re

def transcribe_file():
    file_path = filedialog.askopenfilename(title="Select File", filetypes=[("Video/Audio Files", "*.mp4;*.wav;*.mp3")])
    if not file_path:
        return

    # Ask for confirmation
    confirm = messagebox.askyesno("Confirmation", f"Transcribe the selected file?\n\nFile: {file_path}")
    if not confirm:
        return

    file_extension = os.path.splitext(file_path)[1]

    if file_extension.lower() == ".mp4":
        transcribe_video(file_path)
    elif file_extension.lower() == ".wav":
        transcribe_audio(file_path)
    elif file_extension.lower() == ".mp3":
        temp_wav_path = convert_mp3_to_wav(file_path)
        if temp_wav_path:
            transcribe_audio(temp_wav_path)
            if os.path.exists(temp_wav_path):
                os.remove(temp_wav_path)
        else:
            messagebox.showwarning("Conversion Error", "Failed to convert MP3 to WAV.")
    else:
        messagebox.showwarning("Unsupported File", "The selected file format is not supported.")

def transcribe_video(video_path):
    audio_path = os.path.join(os.getcwd(), "temp_audio.wav")
    os.system(f'ffmpeg -y -i "{video_path}" -vn -acodec pcm_s16le -ar 44100 -ac 2 "{audio_path}"')
    transcribe_audio(audio_path)
    if os.path.exists(audio_path):
        os.remove(audio_path)

def transcribe_audio(audio_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = r.record(source)
    language = get_selected_language()
    text = r.recognize_google(audio_data, language=language)
    formatted_text = format_text(text)
    save_path = filedialog.asksaveasfilename(title="Save Transcription", defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if save_path:
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(formatted_text)
        messagebox.showinfo("Transcription Saved", f"Transcription saved to {save_path}")

def convert_mp3_to_wav(mp3_path):
    wav_path = os.path.join(os.getcwd(), "temp_audio.wav")
    os.system(f'ffmpeg -y -i "{mp3_path}" -acodec pcm_s16le -ar 44100 -ac 2 "{wav_path}"')
    if os.path.isfile(wav_path):
        return wav_path
    else:
        return None

def format_text(text):
    text = " ".join(text.split())
    text = re.sub(r'\. ', '.\n', text)
    return text

def get_selected_language():
    selected_language = []
    if use_english.get():
        selected_language.append('en-US')
    if use_arabic.get():
        selected_language.append('ar-SA')
    if use_french.get():
        selected_language.append('fr-FR')
    if use_german.get():
        selected_language.append('de-DE')
    if selected_language:
        return ','.join(selected_language)
    else:
        return 'en-US'  # Default language is English

window = tk.Tk()
window.title("File Transcription")
window.geometry("400x350")

label = tk.Label(window, text="Click the button to transcribe a file")
label.pack(pady=10)

use_english = IntVar()
checkbox_english = tk.Checkbutton(window, text="English", variable=use_english)
checkbox_english.pack(pady=5)

use_arabic = IntVar()
checkbox_arabic = tk.Checkbutton(window, text="Arabic", variable=use_arabic)
checkbox_arabic.pack(pady=5)

use_french = IntVar()
checkbox_french = tk.Checkbutton(window, text="French", variable=use_french)
checkbox_french.pack(pady=5)

use_german = IntVar()
checkbox_german = tk.Checkbutton(window, text="German", variable=use_german)
checkbox_german.pack(pady=5)

button = tk.Button(window, text="Select File", command=transcribe_file)
button.pack(pady=10)

window.mainloop()
