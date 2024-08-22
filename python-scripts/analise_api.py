import requests
import datetime
import statistics

# Constants
country_code = "BR"
year = 2024
latitude = -22.9068  # Rio de Janeiro
longitude = -43.1729

# 1. Get the list of public holidays in Brazil for 2024
def get_holidays(country_code, year):
    url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country_code}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# 2. Find the month with the most holidays
def month_with_most_holidays(holidays):
    holiday_counts = {}
    for holiday in holidays:
        month = holiday['date'].split('-')[1]
        if month in holiday_counts:
            holiday_counts[month] += 1
        else:
            holiday_counts[month] = 1
    return max(holiday_counts, key=holiday_counts.get)

# 3. Count how many holidays fall on weekdays
def count_weekday_holidays(holidays):
    weekday_holidays = 0
    for holiday in holidays:
        date_obj = datetime.datetime.strptime(holiday['date'], '%Y-%m-%d')
        if date_obj.weekday() < 5:  # Monday=0, Sunday=6
            weekday_holidays += 1
    return weekday_holidays

# 4. Fetch historical weather data for Rio de Janeiro
def get_weather_data(start_date, end_date, latitude, longitude):
    url = f"https://archive-api.open-meteo.com/v1/era5?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=America/Sao_Paulo"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# 5. Calculate average temperature and predominant weather per month
def calculate_monthly_weather(weather_data):
    monthly_temps = {}
    monthly_weather_codes = {}
    
    for i, date in enumerate(weather_data['daily']['time']):
        month = date.split('-')[1]
        temp_avg = (weather_data['daily']['temperature_2m_max'][i] + weather_data['daily']['temperature_2m_min'][i]) / 2
        weather_code = weather_data['daily']['weathercode'][i]
        
        if month not in monthly_temps:
            monthly_temps[month] = []
            monthly_weather_codes[month] = []
        
        monthly_temps[month].append(temp_avg)
        monthly_weather_codes[month].append(weather_code)
    
    avg_temps_per_month = {month: statistics.mean(temps) for month, temps in monthly_temps.items()}
    predominant_weather_per_month = {month: max(set(codes), key=codes.count) for month, codes in monthly_weather_codes.items()}
    
    return avg_temps_per_month, predominant_weather_per_month

# 6. Calculate weather and temperature for each holiday
def holiday_weather(holidays, weather_data):
    holiday_weather_info = {}
    
    for holiday in holidays:
        holiday_date = holiday['date']
        if holiday_date in weather_data['daily']['time']:
            idx = weather_data['daily']['time'].index(holiday_date)
            temp_avg = (weather_data['daily']['temperature_2m_max'][idx] + weather_data['daily']['temperature_2m_min'][idx]) / 2
            weather_code = weather_data['daily']['weathercode'][idx]
            holiday_weather_info[holiday_date] = {'temp_avg': temp_avg, 'weather_code': weather_code}
    
    return holiday_weather_info

# 7. Identify "non-enjoyable" holidays
def non_enjoyable_holidays(holiday_weather_info):
    non_enjoyable = []
    for date, info in holiday_weather_info.items():
        if info['temp_avg'] < 20 or info['weather_code'] not in [0, 1, 2, 3]:
            non_enjoyable.append(date)
    return non_enjoyable

# 8. Determine the most "enjoyable" holiday
def most_enjoyable_holiday(holiday_weather_info):
    best_holiday = None
    best_score = -float('inf')
    
    for date, info in holiday_weather_info.items():
        score = info['temp_avg']  # Temp is important for enjoyment
        if info['weather_code'] in [0, 1, 2, 3]:  # Favor sunny and partly cloudy days
            score += 10
        
        if score > best_score:
            best_score = score
            best_holiday = date
    
    return best_holiday

# Main script
try:
    holidays = get_holidays(country_code, year)
    
    # 1. Number of holidays in Brazil in 2024
    total_holidays = len(holidays)
    print(f"Total holidays in {year}: {total_holidays}")
    
    # 2. Month with the most holidays
    most_holiday_month = month_with_most_holidays(holidays)
    print(f"Month with the most holidays: {most_holiday_month}")
    
    # 3. Number of holidays that fall on weekdays
    weekday_holidays_count = count_weekday_holidays(holidays)
    print(f"Number of weekday holidays: {weekday_holidays_count}")
    
    # 4 & 5. Fetch weather data and calculate monthly averages and predominant weather
    weather_data = get_weather_data('2024-01-01', '2024-08-01', latitude, longitude)
    avg_temps_per_month, predominant_weather_per_month = calculate_monthly_weather(weather_data)
    print(f"Average temperatures per month: {avg_temps_per_month}")
    print(f"Predominant weather per month: {predominant_weather_per_month}")
    
    # 6. Weather on each holiday
    holiday_weather_info = holiday_weather(holidays, weather_data)
    print(f"Weather on holidays: {holiday_weather_info}")
    
    # 7. Identify non-enjoyable holidays
    non_enjoyable = non_enjoyable_holidays(holiday_weather_info)
    print(f"Non-enjoyable holidays: {non_enjoyable}")
    
    # 8. Most enjoyable holiday
    best_holiday = most_enjoyable_holiday(holiday_weather_info)
    print(f"Most enjoyable holiday: {best_holiday}")
    
except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
except Exception as err:
    print(f"Other error occurred: {err}")
