import random
import csv
from faker import Faker # type: ignore
from datetime import datetime
import pandas as pd

fake = Faker()

for i in range(3,5):
    data = []
    rows = random.randint(10000,15000)

    for _ in range(rows):
        invoice_id = fake.random_int(min=1,max=1000)
        start_date = datetime.strptime(f'202{i}-01-01', '%Y-%m-%d')
        end_date = datetime.strptime(f'202{i}-12-31', '%Y-%m-%d')
        purchase_date = fake.date_between(start_date = start_date, end_date = end_date)
        time = fake.time(pattern = '%H:%M')
        
        while not (time >= '09:00' and time < '21:00'):
            time = fake.time(pattern = '%H:%M')
        
        gender = random.choice(['Male','Female'])
        invoice_amount = round(random.uniform(10, 1000), 2)
        payment_method = random.choice(['Credit Card','Cash','Paypal'])
        city = random.choice(['Mexico City','Torremolinos','Fuengirola','Malaga','Marbella','Benalmedena'])
        data.append([invoice_id, purchase_date, time, gender, city, payment_method, invoice_amount])

    filename = f'data_202{i}.csv'
    with open(filename, 'w', newline= '') as file:
        writer = csv.writer(file)
        writer.writerow(['invoice_id', 'purchase_date', 'time', 'gender', 'city', 'payment_method', 'invoice_amount'])
        writer.writerows(data)

    print(f"Archivo CSV '{filename}' creado exitosamente.")