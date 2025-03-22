from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://script.google.com/macros/s/AKfycbywRYYUjvLXuKA0Ad2CUJta3lRDA6RTtHMzWMmFY9jaPzqa9WdWgO9iROHQxi_L9qqK/exec"

def get_zodiac_data():
    response = requests.get(API_URL)
    return response.json() if response.status_code == 200 else {}

@app.route('/', methods=['GET', 'POST'])
def home():
    data = get_zodiac_data()
    zodiac_info = None

    if request.method == 'POST':
        birth_date = request.form['birth_date']
        month, day = map(int, birth_date.split('-')[1:])  # Ambil bulan & hari
        zodiac = get_zodiac_sign(month, day)
        zodiac_info = {zodiac: data.get(zodiac, "Data tidak tersedia")}

    return render_template('index.html', data=data, zodiac_info=zodiac_info)

def get_zodiac_sign(month, day):
    zodiacs = {
        "aries": (3, 21, 4, 19), "taurus": (4, 20, 5, 20),
        "gemini": (5, 21, 6, 20), "cancer": (6, 21, 7, 22),
        "leo": (7, 23, 8, 22), "virgo": (8, 23, 9, 22),
        "libra": (9, 23, 10, 22), "scorpio": (10, 23, 11, 21),
        "sagittarius": (11, 22, 12, 21), "capricorn": (12, 22, 1, 19),
        "aquarius": (1, 20, 2, 18), "pisces": (2, 19, 3, 20)
    }

    for zodiac, (start_month, start_day, end_month, end_day) in zodiacs.items():
        if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
            return zodiac
    return "unknown"

if __name__ == '__main__':
    app.run(debug=True)
