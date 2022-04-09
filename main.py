import requests
from datetime import datetime
import smtplib
import time

# CONSTANTS
MY_EMAIL = "patryktester5@yahoo.com"
MY_PASSWORD = "jgxjyyvchnanomwv"
HOST = "smtp.mail.yahoo.com"
MESSAGE = "Subject:LOOK UP!\n\nThe ISS is above you in the sky!"
MY_LAT = 52.399171  # Your latitude
MY_LONG = -1.520776  # Your longitude


def is_the_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_it_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    curr_hour = time_now.hour

    if curr_hour >= sunset or curr_hour <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_the_iss_overhead() and is_it_dark():
        with smtplib.SMTP(host=HOST) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=MY_EMAIL,
                                msg=MESSAGE)

# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
