import random

# Function to generate random temperature and return description
def generate_temperature():
    temperature = random.randint(1, 100)
    if temperature <= 20:
        return "Cold"
    elif temperature <= 40:
        return "Comfortable"
    elif temperature <= 70:
        return "Hot"
    else:
        return "Unbearable Heat"

# Function to generate random light intensity and return description
def generate_light_intensity():
    light_intensity = random.randint(1, 100)
    if light_intensity <= 25:
        return "Dark"
    elif light_intensity <= 50:
        return "Dim"
    elif light_intensity <= 75:
        return "Normal"
    else:
        return "Bright"

# Function to generate random weather and return description
def generate_weather():
    weather_list = ['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Moderate Rain', 'Heavy Rain', 'Torrential Rain',
                    'Fog', 'Snow', 'Hail', 'Frost', 'Typhoon', 'Tornado', 'Sandstorm', 'Thunderstorm',
                    'Partly Cloudy', 'Partly Cloudy', 'Showers', 'Snow Showers', 'Hail', 'Heavy Snow', 'Blizzard',
                    'Freezing Fog', 'Freezing Rain', 'Sandstorm', 'Dust Storm', 'Sandstorm', 'Severe Weather']
    return random.choice(weather_list)


def generate_env():
    temperature_desc = generate_temperature()
    light_intensity_desc = generate_light_intensity()
    weather_desc = generate_weather()
    environment = [temperature_desc, light_intensity_desc, weather_desc]
    return environment

#
# # 打印结果
# print("环境参数：", environment)
