import os
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri yükle
load_dotenv()

# Flask uygulamamızı oluşturuyoruz
app = Flask(__name__)

# API anahtarını .env dosyasından güvenli bir şekilde alıyoruz
API_KEY = os.getenv("OWM_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Anahtarın bulunup bulunmadığını kontrol ediyoruz
if not API_KEY:
    raise ValueError("API anahtarı bulunamadı. Lütfen .env dosyasını kontrol edin.")


@app.route('/')
def anasayfa():
    """Kullanıcı siteye ilk girdiğinde ana HTML sayfasını gösterir."""
    return render_template('index.html')


@app.route('/weather')
def hava_durumunu_getir():
    """Formdan gelen şehir bilgisiyle API'ye istek atar ve sonucu HTML'e gönderir."""
    sehir = request.args.get('city')

    weather_data = None
    error_message = None

    if sehir:
        request_url = f"{BASE_URL}?q={sehir}&appid={API_KEY}&units=metric&lang=tr"
        response = requests.get(request_url)

        if response.status_code == 200:
            veri = response.json()
            weather_data = {
                "sehir": sehir.capitalize(),
                "aciklama": veri['weather'][0]['description'].capitalize(),
                "sicaklik": f"{veri['main']['temp']:.1f}",
                "hissedilen": f"{veri['main']['feels_like']:.1f}",
                "icon": veri['weather'][0]['icon']
            }
        else:
            error_message = "Şehir bulunamadı veya bir hata oluştu."

    # HTML şablonuna veriyi veya hata mesajını göndererek sayfayı oluşturuyoruz
    return render_template('index.html', data=weather_data, error=error_message)


if __name__ == '__main__':
    # Uygulamayı yerel makinede test etmek için çalıştırır
    app.run(debug=True)