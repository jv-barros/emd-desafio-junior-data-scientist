import streamlit as st
import basedosdados as bd
import requests
import datetime
import statistics

# Function to get data from your analysis scripts
def get_data():
    # Place your Python scripts logic here or import functions
    from analise_python import (
        get_total_chamados_by_date,
        get_most_frequent_tipo_by_date,
        get_top_3_bairros_by_date,
        get_top_subprefeitura_by_date,
        get_chamados_without_bairro_or_subprefeitura,
        get_total_chamados_by_subtype_and_date_range,
        get_chamados_during_events,
        get_total_chamados_for_each_event,
        get_daily_average_calls_for_each_event,
        get_daily_average_calls_during_events_and_total
    )
    
    from analise_api import (
        get_holidays,
        month_with_most_holidays,
        count_weekday_holidays,
        get_weather_data,
        calculate_monthly_weather,
        holiday_weather,
        non_enjoyable_holidays,
        most_enjoyable_holiday
    )
    
    # Fetch data
    date = '2023-04-01'
    holidays = get_holidays('BR', 2024)
    weather_data = get_weather_data('2024-01-01', '2024-08-01', -22.9068, -43.1729)
    
    # Example data fetching and processing
    total_chamados = get_total_chamados_by_date(date)
    frequent_tipo = get_most_frequent_tipo_by_date(date)
    top_bairros = get_top_3_bairros_by_date(date)
    top_subprefeitura = get_top_subprefeitura_by_date(date)
    chamados_without_info = get_chamados_without_bairro_or_subprefeitura(date)
    total_chamados_subtype = get_total_chamados_by_subtype_and_date_range('Perturbação do sossego', '2022-01-01', '2023-12-31')
    chamados_during_events = get_chamados_during_events('Perturbação do sossego', ['Reveillon', 'Carnaval', 'Rock in Rio'])
    total_chamados_for_each_event = get_total_chamados_for_each_event('Perturbação do sossego', ['Reveillon', 'Carnaval', 'Rock in Rio'])
    daily_avg_calls_for_each_event = get_daily_average_calls_for_each_event('Perturbação do sossego', ['Reveillon', 'Carnaval', 'Rock in Rio'])
    daily_avg_calls_during_events_and_total = get_daily_average_calls_during_events_and_total('Perturbação do sossego', ['Reveillon', 'Carnaval', 'Rock in Rio'], '2022-01-01', '2023-12-31')
    
    most_holiday_month = month_with_most_holidays(holidays)
    weekday_holidays_count = count_weekday_holidays(holidays)
    avg_temps_per_month, predominant_weather_per_month = calculate_monthly_weather(weather_data)
    holiday_weather_info = holiday_weather(holidays, weather_data)
    non_enjoyable = non_enjoyable_holidays(holiday_weather_info)
    best_holiday = most_enjoyable_holiday(holiday_weather_info)
    
    return {
        'total_chamados': total_chamados,
        'frequent_tipo': frequent_tipo,
        'top_bairros': top_bairros,
        'top_subprefeitura': top_subprefeitura,
        'chamados_without_info': chamados_without_info,
        'total_chamados_subtype': total_chamados_subtype,
        'chamados_during_events': chamados_during_events,
        'total_chamados_for_each_event': total_chamados_for_each_event,
        'daily_avg_calls_for_each_event': daily_avg_calls_for_each_event,
        'daily_avg_calls_during_events_and_total': daily_avg_calls_during_events_and_total,
        'most_holiday_month': most_holiday_month,
        'weekday_holidays_count': weekday_holidays_count,
        'avg_temps_per_month': avg_temps_per_month,
        'predominant_weather_per_month': predominant_weather_per_month,
        'holiday_weather_info': holiday_weather_info,
        'non_enjoyable': non_enjoyable,
        'best_holiday': best_holiday
    }

# Streamlit App Layout
def main():
    st.title("Data Analysis Dashboard")

    data = get_data()
    
    st.header("Calls Analysis")
    st.subheader("Total Calls by Date")
    st.write(data['total_chamados'])

    st.subheader("Most Frequent Call Type")
    st.write(data['frequent_tipo'])
    
    st.subheader("Top 3 Neighborhoods by Calls")
    st.write(data['top_bairros'])
    
    st.subheader("Top Subprefecture by Calls")
    st.write(data['top_subprefeitura'])
    
    st.subheader("Calls Without Neighborhood or Subprefecture")
    st.write(data['chamados_without_info'])
    
    st.subheader("Total Calls by Subtype and Date Range")
    st.write(data['total_chamados_subtype'])
    
    st.subheader("Calls During Specific Events")
    st.write(data['chamados_during_events'])
    
    st.subheader("Total Calls for Each Event")
    st.write(data['total_chamados_for_each_event'])
    
    st.subheader("Daily Average Calls for Each Event")
    st.write(data['daily_avg_calls_for_each_event'])
    
    st.subheader("Daily Average Calls During Events and Total Period")
    st.write(data['daily_avg_calls_during_events_and_total'])
    
    st.header("Holidays Analysis")
    st.subheader("Month with Most Holidays")
    st.write(data['most_holiday_month'])
    
    st.subheader("Number of Weekday Holidays")
    st.write(data['weekday_holidays_count'])
    
    st.subheader("Average Temperatures per Month")
    st.write(data['avg_temps_per_month'])
    
    st.subheader("Predominant Weather per Month")
    st.write(data['predominant_weather_per_month'])
    
    st.subheader("Weather on Holidays")
    st.write(data['holiday_weather_info'])
    
    st.subheader("Non-Enjoyable Holidays")
    st.write(data['non_enjoyable'])
    
    st.subheader("Most Enjoyable Holiday")
    st.write(data['best_holiday'])

if __name__ == "__main__":
    main()
