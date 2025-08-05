# Import necessary libraries
import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QtMsgType

# Define the main Weather Application class
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        # UI components
        self.city_label = QLabel("Enter the City name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temprature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)

        # Initialize the UI
        self.initUI()

    # UI layout and styling setup
    def initUI(self):
        self.setWindowTitle("Weather App")

        # Vertical layout for all widgets
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temprature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)

        # Center align all text widgets
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temprature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        # Assign object names for styling
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temprature_label.setObjectName("temprature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # Apply stylesheet for styling widgets
        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: 'Segoe UI', Calibri, sans-serif;
                color: #f0f0f0;
            }

            QLabel#city_label {
                font-size: 42px;
                font-style: italic;
                color: #00bfff;
                padding-bottom: 10px;
                letter-spacing: 1px;
            }

            QLineEdit#city_input {
                font-size: 36px;
                padding: 15px 20px;
                border-radius: 15px;
                background-color: #ffffff;
                color: #1c1c1c;
                border: 2px solid #00bfff;
                selection-background-color: #cceeff;
                selection-color: #000000;
            }

            QPushButton#get_weather_button {
                font-size: 36px;
                font-weight: bold;
                padding: 14px 24px;
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                    stop:0 #1e90ff, stop:1 #00bfff);
                color: white;
                border-radius: 12px;
                border: 2px solid #007acc;
            }

            QPushButton#get_weather_button:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                    stop:0 #00bfff, stop:1 #1e90ff);
                border: 2px solid #ffffff;
            }

            QLabel#temprature_label {
                font-size: 80px;
                font-weight: bold;
                color: #ffd700;
                margin-top: 20px;
            }

            QLabel#emoji_label {
                font-size: 110px;
                font-family: 'Segoe UI Emoji';
                margin: 10px 0;
            }

            QLabel#description_label {
                font-size: 52px;
                color: #87ceeb;
                font-style: italic;
            }
        """)

        # Connect button click to fetch weather
        self.get_weather_button.clicked.connect(self.get_weather)

    # Fetch weather data from OpenWeather API
    def get_weather(self):
        api_key = "890c747b1435a7342f7a191ce392c967"  # Replace with your actual API key
        city = self.city_input.text()  # Get city name from input
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # If city found and data is valid, display the weather
            if data["cod"] == 200:
                self.display_weather(data)

        # Handle various HTTP errors with appropriate messages
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request: \n Please check your Input.")
                case 401:
                    self.display_error("Unauthorized: \n Invalid API Key.")
                case 403:
                    self.display_error("Forbidden: \n Access is Denied.")
                case 404:
                    self.display_error("Not Found: \n City Not Found.")
                case 500:
                    self.display_error("Internal Server Error: \n Please try again later.")
                case 502:
                    self.display_error("Bad Gateway: \n Invalid response from the server.")
                case 503:
                    self.display_error("Service is unavailable: \n Server is down.")
                case 504:
                    self.display_error("Gateway Timeout: \n No response from server.")
                case _:
                    self.display_error(f"HTTP error occurred: \n {http_error}")

        # Handle connection and request-related exceptions
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error: \n Check your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error: \n The request timed out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects: \n Check the URL")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error: \n {req_error}")

    # Display error messages on the GUI
    def display_error(self, message):
        self.temprature_label.setStyleSheet("font-size: 30px;")
        self.temprature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    # Display weather data (temperature, emoji, and description)
    def display_weather(self, data):
        self.temprature_label.setStyleSheet("font-size: 75px;")

        # Extract temperature and convert from Kelvin to Celsius and Fahrenheit
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5) - 459.67

        weather_id = data["weather"][0]["id"]  # Get weather condition code
        weateher_description = data["weather"][0]["description"]  # Get description

        # Display the temperature, emoji, and description
        self.temprature_label.setText(f"{temperature_c: .0f}℃")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(f"{weateher_description}")

    # Return appropriate emoji based on weather condition code
    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "🌩️⚡⛈️"      # Thunderstorm
        elif 300 <= weather_id <= 321:
            return "🌦️🌧️"       # Drizzle
        elif 500 <= weather_id <= 531:
            return "🌧️☔💧"      # Rain
        elif 600 <= weather_id <= 622:
            return "❄️☃️🌨️"     # Snow
        elif 701 <= weather_id <= 741:
            return "🌁🌫️"        # Mist/Fog
        elif weather_id == 762:
            return "🌋🔥"         # Volcanic ash
        elif weather_id == 771:
            return "💨🌬️"        # Squall/Wind
        elif weather_id == 781:
            return "🌪️🌪️"        # Tornado
        elif weather_id == 800:
            return "☀️🌞✨"        # Clear sky
        elif 801 <= weather_id <= 804:
            return "🌤️⛅🌥️"      # Cloudy
        else:
            return "❓🌈"          # Unknown condition

# Entry point for running the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weahter_app = WeatherApp()
    weahter_app.show()
    sys.exit(app.exec_())
