import board
import busio
import adafruit_sht31d
import time
import sqlite3
from datetime import datetime


i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_sht31d.SHT31D(i2c)



humidity = []
temperature = []
sht30_data = {'temperature': temperature, 'humidity': humidity}

def probe_colletcting():
    probe_length = 60
    counter = 0
    while counter < probe_length:
        try:
            hum = sensor.relative_humidity
            temp = sensor.temperature
        except Exception as e:
            print(f"No data recive from senor or wrong data: {e}")
        humidity.append(hum)
        temperature.append(temp)
        print(temp)
        print(hum)      
        time.sleep(1)
        counter += 1

    return sht30_data
    
    
def average_of_chunks(data):
    avg = sum(data) / len(data)     
    return avg


def db_collecting():
    conn = sqlite3.connect("sht30_data.db")  # Corrected database name
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sht30_data (
			timestamp TEXT,
            humidity REAL,
            temperature REAL
        )
    ''')
    
    cursor.execute("INSERT INTO sht30_data (timestamp, humidity, temperature) VALUES (?, ?, ?)",
                   (timestamp, avarage_humidity, avarage_temperature))  
                   
    conn.commit()
    conn.close()
while True:
	sht30_data = probe_colletcting()
	avarage_humidity = average_of_chunks(sht30_data['humidity'])
	avarage_temperature = average_of_chunks(sht30_data['temperature'])
	timestamp = datetime.now().replace(second=0, microsecond=0)
	db_collecting()




