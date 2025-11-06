import requests
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk 
import os
import sys

# --- CONFIGURATION & API SETUP ---
API_KEY = "e88520016d5e51be5ee3e00d4024db11" # Replace with your OpenWeatherMap API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# --- EMOJI & IMAGE MAPPING ---
WEATHER_EMOJI_MAP = {
    '01d': '☀️',  # Clear sky (day)
    '01n': '🌙',  # Clear sky (night)
    '02d': '⛅',  # Few clouds
    '02n': '☁️',  # Few clouds (night)
    '03d': '☁️',  # Scattered clouds
    '03n': '☁️',  # Scattered clouds
    '04d': '☁️',  # Broken clouds
    '04n': '☁️',  # Broken clouds
    '09d': '🌧️',  # Shower rain
    '09n': '🌧️',  # Shower rain
    '10d': '🌦️',  # Rain
    '10n': '🌦️',  # Rain
    '11d': '⛈️',  # Thunderstorm
    '11n': '⛈️',  # Thunderstorm
    '13d': '❄️',  # Snow
    '13n': '❄️',  # Snow
    '50d': '🌫️',  # Mist/Fog
    '50n': '🌫️',  # Mist/Fog
}

WEATHER_IMAGE_MAP = {
    '01d': 'sun.png',          # Clear sky (day)
    '01n': 'sun.png',          # Clear sky (night)
    '02d': 'clouds.png',       # Few clouds
    '02n': 'clouds.png',       
    '03d': 'clouds.png',       # Scattered clouds
    '03n': 'clouds.png',       
    '04d': 'clouds.png',       # Broken clouds
    '04n': 'clouds.png',       
    '09d': 'rain.png',         # Shower rain
    '09n': 'rain.png',         
    '10d': 'rain.png',         # Rain
    '10n': 'rain.png',         
    '11d': 'thunder.png',      # Thunderstorm
    '11n': 'thunder.png',      
    '13d': 'snow.png',         # Snow
    '13n': 'snow.png',         
    '50d': 'clouds.png',       # Mist/Fog
    '50n': 'clouds.png',       
}

DEFAULT_EMOJI = '🌍'
DEFAULT_IMAGE = 'background.png'

# --- CORE FUNCTIONALITY ---

def get_weather():
    """Fetches weather data and updates the UI."""
    city = city_entry.get().strip()
    
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name!")
        return

    if API_KEY == "YOUR_API_KEY_HERE":
         messagebox.showerror("Config Error", "Please replace 'YOUR_API_KEY_HERE' with your actual API key.")
         return

    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    
    result_label.configure(text="")
    details_label.configure(text="Searching...", text_color="gray")
    weather_icon_label.configure(image=None, text="⏳")
    emoji_label.configure(text="⏳")

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()

        if response.status_code != 200:
            error_message = data.get('message', 'Unknown error.')
            messagebox.showerror("Error", f"City not found or API error: {error_message.capitalize()}")
            details_label.configure(text="---", text_color="red")
            weather_icon_label.configure(image=None, text="❌")
            emoji_label.configure(text="❌")
            return

        # --- Data Extraction ---
        city_name = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"].capitalize()
        weather_main = data["weather"][0]["main"]
        icon_id = data["weather"][0]["icon"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        pressure = data["main"]["pressure"]
        feels_like = data["main"]["feels_like"]

        # --- Get Emoji ---
        weather_emoji = WEATHER_EMOJI_MAP.get(icon_id, DEFAULT_EMOJI)

        # --- Update Dynamic Image ---
        image_path = WEATHER_IMAGE_MAP.get(icon_id, DEFAULT_IMAGE)
        
        if not os.path.exists(image_path):
            image_path = DEFAULT_IMAGE
            print(f"Warning: Image '{image_path}' not found, falling back to '{DEFAULT_IMAGE}'")

        try:
            dynamic_img_data = Image.open(image_path)
            dynamic_img_data = dynamic_img_data.resize((120, 120))
            dynamic_photo = ctk.CTkImage(light_image=dynamic_img_data, dark_image=dynamic_img_data, size=(120, 120))
            
            weather_icon_label.configure(image=dynamic_photo, text="")
            weather_icon_label.image = dynamic_photo
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            weather_icon_label.configure(image=None, text="🖼️❌")

        # --- Update Emoji Display ---
        emoji_label.configure(text=weather_emoji)

        # --- Update Main Display ---
        result_label.configure(
            text=f"{city_name}, {country}\n{temp:.1f}°C\n{weather_desc}",
            text_color="#007acc"
        )
        
        # --- Update Details Panel ---
        details_text = (
            f"🌡️  Feels like: {feels_like:.1f}°C\n"
            f"💧  Humidity: {humidity}%\n"
            f"💨  Wind: {wind_speed:.1f} m/s\n"
            f"🔽  Pressure: {pressure} hPa"
        )
        details_label.configure(text=details_text, text_color=("gray10", "gray90"))

    except requests.exceptions.RequestException:
        messagebox.showerror("Connection Error", "Unable to connect to weather service. Check your Internet connection.")
        result_label.configure(text="---")
        details_label.configure(text="---", text_color="red")
        weather_icon_label.configure(image=None, text="🌐❌")
        emoji_label.configure(text="🌐❌")

# --- UI SETUP ---

# 1. Initialize CustomTkinter settings
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# 2. Create the main window
app = ctk.CTk()
app.title("Pro Weather Dashboard 🌤️")
app.geometry("420x750")  # Slightly increased width for better text fitting
app.resizable(False, False)

# --- Main Frame ---
main_frame = ctk.CTkFrame(app, corner_radius=20)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# --- Title with Emoji ---
title_label = ctk.CTkLabel(main_frame, text="🌤️ Weather Dashboard", font=("Roboto", 26, "bold"), text_color="#1f6aa5")
title_label.pack(pady=15)

# --- City Entry ---
city_entry = ctk.CTkEntry(
    main_frame, 
    placeholder_text="🏙️ Enter City Name (e.g., London)", 
    font=("Roboto", 16), 
    width=300,  # Increased width
    height=40,
    corner_radius=10
)
city_entry.pack(pady=(15, 10))
city_entry.bind('<Return>', lambda event=None: get_weather())
city_entry.focus()

# --- Search Button ---
search_btn = ctk.CTkButton(
    main_frame, 
    text="🔍 Check Weather", 
    command=get_weather, 
    font=("Roboto", 16, "bold"), 
    corner_radius=10, 
    fg_color="#1f6aa5",
    height=40,
    width=200
)
search_btn.pack(pady=15)

# --- Large Emoji Display ---
emoji_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
emoji_frame.pack(pady=10)

emoji_label = ctk.CTkLabel(
    emoji_frame, 
    text="🌍", 
    font=("Segoe UI Emoji", 48),
    text_color="#FFD700"
)
emoji_label.pack()

# --- Weather Icon Display ---
weather_icon_label = ctk.CTkLabel(main_frame, text="📁", font=("Roboto", 14))
weather_icon_label.pack(pady=5)

# --- Main Result Display ---
result_label = ctk.CTkLabel(
    main_frame, 
    text="---", 
    font=("Roboto", 22, "bold"),
    pady=15
)
result_label.pack(pady=10)

# --- Details Panel ---
details_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color=("gray85", "gray25"))
details_frame.pack(pady=20, padx=25, fill='x')  # Increased padding

# Fixed details label with proper alignment
details_label = ctk.CTkLabel(
    details_frame, 
    text="🔍 Search to view details...", 
    font=("Roboto", 16),
    justify='left',
    anchor='w'  # Left alignment
)
details_label.pack(pady=15, padx=20, fill='x')

# --- Footer ---
footer_label = ctk.CTkLabel(
    main_frame, 
    text="Made with ❤️ using Python", 
    font=("Roboto", 12),
    text_color="gray"
)
footer_label.pack(side="bottom", pady=10)

# --- Run the App ---
if __name__ == "__main__":
    app.mainloop()