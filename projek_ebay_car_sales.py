# -*- coding: utf-8 -*-
"""Projek ebay_car_sales.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1siRTCXkGiP_ppe7whSliRRO1mjbPIQsU
"""

# import library yang dibutuhkan
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from sklearn.preprocessing import OneHotEncoder, StandardScaler



# import library untuk ignore future warning
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Path data
path_data = "autos.csv"

# read data dari file
autos = pd.read_csv(path_data, encoding='latin-1')

# Menampilkan 5 data teratas
autos.head()

"""# Eksploration of Data & Preprocessing

Outline:
* Check data type and match with definition given by data source
* Check missing value and handle it
* Check Duplicated and handle it
* Check Inkonsistensi Data and handle it
* Check outlier and handle it

## Check Data Type
"""

# Cek tipe data dari data autos
autos.info()

"""1. Data berisi 20 kolom, dan ditemukan bahwa ada 13 kolom bertipe object, dan 7 kolom bertipe integer
2. Penamaan kolom menggunakan camelCase, hal tersebut tidak sesuai dengan aturan penamaan di Python
3. Ada beberapa kolom yang memiliki null value

kita akan mengubah nama kolom menjadi lebih mudah dibaca sehingga memudahkan dalam proses wrangling, nama kolom menggunkan format snake-case supaya lebih konsisten
"""

#cek nama kolom
autos.columns

# mengubah nama kolom yang menggunakan camelCase menjadi snake-case
change_name_column = {'dateCrawled': 'date_crawled',
                      'offerType': 'offer_type',
                      'vehicleType': 'vehicle_type',
                      'yearOfRegistration': 'registration_year',
                      'powerPS': 'power_ps',
                      'monthOfRegistration': 'registration_month',
                      'fuelType': 'fuel_type',
                      'notRepairedDamage': 'unrepaired_damage',
                      'dateCreated': 'ad_created',
                      'nrOfPictures': 'nr_of_picture',
                      'postalCode': 'postal_code',
                      'lastSeen': 'last_seen',
                      }

autos = autos.rename(columns = change_name_column)
autos.head(2)

"""## Ekploration of Data
#### Melihat statistik deskriptif semua kolom
"""

# melihat statistik deskiptif semua kolom
autos.describe(include='all')

"""1. kolom yang paling banyak memiliki NaN nilai:
- seller, offer_type, vehicle_type, brand

2. Kolom yang memiliki nilai kosong:
- nr_of_picture

3. kolom yang membutuhkan penyelidikan lebih lanjut:
- registration_year: memiliki nilai min dan max yang tidak realistis
- price : memiliki nilai min dan max harga yang tidak realistis

"""

# info dataset
autos.info()

"""kita drop dulu kolom nr_of_picture karena semua data bernilai 0 dan juga tidak dibutuhkan dalam proses analisis"""

# hapus kolom nr_of_picture
del autos['nr_of_picture']

"""mengubah tipe data dari date_crawled dari object menjadi datetime"""

# Convert kolom date_crawled
autos.date_crawled = pd.to_datetime(autos.date_crawled, yearfirst=True)

# Tampilkan data tanggal dan waktu setelah diconvert
autos.date_crawled

"""mengubah tipe data dari last_seen dari object menjadi datetime"""

# Convert kolom last_seen
autos.last_seen = pd.to_datetime(autos.last_seen, yearfirst=True)

# Tampilkan data tanggal dan waktu setelah diconvert
autos.last_seen

"""mengubah tipe data dari ad_created dari object menjadi datetime"""

# Convert kolom ad_created
autos.ad_created = pd.to_datetime(autos.ad_created, yearfirst=True)

# Tampilkan data tanggal dan waktu setelah diconvert
autos.ad_created

# cek kembali tipe data tiap kolom
autos.info()

"""## Cek Missing Value"""

# Mendapatkan jumlah missing value tiap kolom
# dan mengurutkan dari yang terbesar ke terkecil
missing = autos.isna().sum().sort_values(ascending = False)
# construct a dataframe consists of NaN count and NaN percentage from the dataset
missing_data = pd.DataFrame({'NaN_count': missing, 'NaN_percentage': missing / len(autos)}).sort_values(by = 'NaN_percentage', ascending = False)

# print the missing value information
missing_data

#data teratas kolom yang memiliki nan
autos[["unrepaired_damage",
       "vehicle_type",
       "fuel_type",
       "model",
       "gearbox"]].head(3)

# cek info data yang memiliki missing value
autos[["unrepaired_damage",
       "vehicle_type",
       "fuel_type",
       "model",
       "gearbox"]].info()

"""- kolom unrepaired_damage : kita ubah nilai "NaN" menjadi "other"
- kolom vehicle_type : kita ubah nilai "NaN" menjadi "other"
- kolom fuel_type : kita ubah nilai "NaN" menjadi "other"
- kolom model : kita ubah nilai "NaN" menjadi "other"
- kolom gearbox : kita ubah nilai "NaN" menjadi "not-exist"

## Handle missing value

handle missing value pada kolom unrepaired_damage
"""

# Mengganti nilai yang hilang dengan "other"
autos.unrepaired_damage.fillna('other', inplace=True)

# Menampilkan DataFrame setelah mengganti nilai yang hilang
autos.unrepaired_damage.unique()

"""handle missing value pada kolom vehicle_type


"""

# Mengganti nilai yang hilang dengan "other"
autos.vehicle_type.fillna('other', inplace=True)

# Menampilkan DataFrame setelah mengganti nilai yang hilang
autos.vehicle_type.unique()

"""handle missing value pada kolom fuel_type"""

# Mengganti nilai yang hilang dengan "other"
autos.fuel_type.fillna('other', inplace=True)

# Menampilkan DataFrame setelah mengganti nilai yang hilang
autos.fuel_type.unique()

"""handle missing value pada kolom model"""

# Mengganti nilai yang hilang dengan "other"
autos.model.fillna('other', inplace=True)

# Menampilkan DataFrame setelah mengganti nilai yang hilang
autos.model

"""handle missing value pada kolom gearbox

"""

# Mengganti nilai yang hilang dengan "not-exist"
autos.gearbox.fillna('not-exist', inplace=True)

# Menampilkan DataFrame setelah mengganti nilai yang hilang
autos.gearbox.unique()

"""Cek Kembali Jumlah Missing Value"""

# Mendapatkan jumlah missing value tiap kolom dan mengurutkan dari yang terbesar ke terkecil
missing = autos.isna().sum().sort_values(ascending = False)
# construct a dataframe consists of NaN count and NaN percentage from the dataset
missing_data = pd.DataFrame({'NaN_count': missing, 'NaN_percentage': missing / len(autos)}).sort_values(by = 'NaN_percentage', ascending = False)

# print the missing value information
missing_data

"""## Check Duplicated of Data"""

# cek jika terdapat data duplikat
autos[autos.duplicated()]

# menampilkan jumlah data yang duplikat
autos.duplicated().sum()

"""terdapat 4 data duplikat

## Handle Duplicated of Data
"""

# Menghapus baris duplikat dari DataFrame 'autos' dan mempertahankan baris pertama
autos = autos.drop_duplicates(keep='first')

# cek kembali data
autos.duplicated().sum()

"""## Check Inconsistence and Handle it"""

# cek kolom seller
autos.seller.unique()

"""Data kolom seller ditemukan konsisten, namun kita ingin mengubah nama dengan bahasa Jerman dengan nama yang mudah dipahami"""

# mengganti isi kolom seller menjadi mudah dipahami
autos.seller = autos.seller.replace({'privat':'private',
                                     'gewerblich':'commercial'})
autos.seller.unique()

# cek kolom offer type
autos.offer_type.unique()

"""Data kolom offer_type ditemukan konsisten, namun kita ingin mengubah nama dengan bahasa Jerman dengan nama yang mudah dipahami"""

# mengganti isi kolom offer_type menjadi mudah dipahami
autos.offer_type = autos.offer_type.replace({'Angebot':'Request',
                                             'Gesuch':'Offer'})
autos.offer_type.unique()

# cek kolom gearbox
autos.gearbox.unique()

"""Data kolom gearbox ditemukan konsisten, namun kita ingin mengubah nama dengan bahasa Jerman dengan nama yang mudah dipahami"""

# mengganti isi kolom gearbox menjadi mudah dipahami
autos.gearbox = autos.gearbox.replace({'manuell':'manual',
                                       'automatik':'automatic',
                                       'not-exist':'not-exist'})
autos.gearbox.unique()

# cek kolom fuel_type
autos.fuel_type.unique()

"""Data kolom fuel_type ditemukan konsisten, namun kita ingin mengubah nama dengan bahasa Jerman dengan nama yang mudah dipahami"""

# mengganti isi kolom gearbox menjadi mudah dipahami
autos.fuel_type = autos.fuel_type.replace({'benzin':'gasoline',
                                           'diesel':'automatic',
                                           'elektro':'electric'})
autos.fuel_type.unique()

# cek kolom unrepaired_damage
autos.unrepaired_damage.unique()

"""Data kolom unrepaired_damage ditemukan konsisten, namun kita ingin mengubah nama dengan bahasa Jerman dengan nama yang mudah dipahami"""

# mengganti isi kolom unrepaired_damage menjadi mudah dipahami
autos.unrepaired_damage = autos.unrepaired_damage.replace({'ja':'yes',
                                                           'nein':'no'})
autos.unrepaired_damage.unique()

"""ditemukan baris tahun yang tidak sesuai dengan tahun sekarang yaitu 2024 dan juga ditemukan tahun yang kurang dari tahun ditemukan mobil pertama kali yaitu tahun 1878 oleh Karl Benz"""

# cek kolom registration_year
autos.registration_year.unique()

# cek deskripsi dari komom registration_year
autos.registration_year.describe()

"""ditemukan data kolom tahun registrasi memiliki nilai yang tidak realistis.

tidak sesuai dengan tahun terakhir dataset dibuat, yaitu tahun 2016.
Dan juga ditemukan tahun yang kurang dari tahun ditemukan mobil pertama kali yaitu tahun 1878 oleh Karl Benz
"""

# drop baris yang memiliki tahun dibawaah 1878 dan tahun diatas 2016
autos = autos[(autos.registration_year >= 1878) & (autos.registration_year <= 2016)]

autos.registration_year

# cek kolom registration_month
autos.registration_month.unique()

"""kita akan mengubah data bulan menjadi 1 - 12, lalu ubah menjadi Jan-Dec"""

#mengubah nilai bulan
autos.registration_month.replace([0,12],[1,12],inplace=True)

#mengubah nilai bulan dari 1-12 menjadi Jan - Des
months = ["Jan", "Feb", "Mar" ,"Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

#mengubah nilai bulan dari 1-12 menjadi Jan - Des
autos.registration_month.replace([1,2,3,4,5,6,7,8,9,10,11, 12],months,inplace=True)

# cek kolom registration_month kembali
autos.registration_month.unique()

"""## Check Outlier

- Outlier biasanya terdapat pada kolom bertipe numeric.
- Pada kasus kali ini, kita akan mengidentifikasi outlier pada kolom price.
- Kita dapat menampilkan sebaran data price menggunakan boxplot
"""

# Buat figure & axes
fig, ax = plt.subplots(figsize=(10, 6))

# Buat boxplot untuk kolom "price"
sns.boxplot(data=autos,
            x="price",
            ax=ax)

# Tampilkan plot
plt.show()

"""kita cek dulu statistik deskripsinya"""

# cek statistik deskriptif
autos.price.describe()

""" cek kemunculan harga paling tinggi pada kolom price"""

# cek harga paling tinggi
autos.price.value_counts().sort_index(ascending=False).head()

"""hapus outlier harga yang memiliki nilai > 9999999 karena harga tersebut tidak menjadikan harga serius yang ditawarkan"""

# Menghapus baris yang memiliki nilai lebih dari 9999999 di kolom 'price'
autos = autos.loc[autos.price < 9999999]
# cek harga kembali
autos.price.value_counts().sort_index(ascending=False).head(2)

#cek harga yang memiliki nilai 0
autos.price.value_counts().sort_index(ascending=False).tail()

"""ternyata terdapat kemunculan harga 0 sebanyak 10014. kita cek dulu berapa presentasenya"""

# Hitung jumlah nilai 0 dalam kolom tertentu
jumlah_nilai_0 = (autos.price.values == 0).sum()

# Hitung jumlah total baris
jumlah_total_baris = autos.shape[0]

# Hitung persentase nilai 0
persentase_nilai_0 = (jumlah_nilai_0 / jumlah_total_baris) * 100

print(f"Persentase nilai 0 dalam kolom 'price': {persentase_nilai_0:.2f}%")

"""Ternyata nilai harga pada kolom price yang bernilai 0.0 berjumlah
2.81% dari total seluruh data. maka solusinya adalah dengan
menghapus semua data yang bernilai 0


"""

# Menghapus baris yang memiliki nilai 0.0 di kolom 'price'
autos = autos[autos.price != 0.0]

#cek kembali data kolom price
autos.price.value_counts().sort_index(ascending=False).tail()

# Buat figure & axes
fig, ax = plt.subplots(figsize=(10, 6))

# Buat boxplot untuk kolom "price"
sns.boxplot(data=autos,
            x="price",
            ax=ax)

# Tampilkan plot
plt.show()

"""outlier setidaknya berkurang, namun kita harus menyelidiki lebih lanjut untuk menangani outlier"""

# cek statistik deskriptif kembali
autos.price.describe()

# Cari Q1 & Q3
Q1 = autos.price.quantile(0.25)
Q3 = autos.price.quantile(0.75)

print(f"Q1 : {Q1:.2f}")
print(f"Q3 : {Q3:.2f}")

# Cari IQR & BATAS MAXIMUM
IQR = Q3 - Q1
max_bound = Q3 + 1.5*IQR

print(f"IQR : {IQR:.2f}")
print(f"Maximum Boundary : {max_bound:.2f}")

# Filter data tanpa outlier
autos = autos[autos["price"] < max_bound]

# Buat figure & axes
fig, ax = plt.subplots(figsize = (10, 6))

# Buat histogram plot price
sns.histplot(data = autos,
             x = "price",
             bins = 100,
             ax = ax)

plt.show()

# Validasi hasil filter
autos["price"].describe()

"""Terlihat Q3 dan nilai maximum masih berbeda jauh
Outlier telah belum sepenuhnya dihilangkan.
kita coba sekali lagi
"""

# Cari Q1 & Q3
Q1 = autos.price.quantile(0.25)
Q3 = autos.price.quantile(0.75)

print(f"Q1 : {Q1:.2f}")
print(f"Q3 : {Q3:.2f}")

# Cari IQR & BATAS MAXIMUM
IQR = Q3 - Q1
max_bound = Q3 + 1.5*IQR

print(f"IQR : {IQR:.2f}")
print(f"Maximum Boundary : {max_bound:.2f}")

# Filter data tanpa outlier
autos = autos[autos["price"] < max_bound]

# Validasi hasil filter
autos["price"].describe()

# Buat figure & axes
fig, ax = plt.subplots(figsize = (10, 6))

# Buat histogram plot price
sns.histplot(data = autos,
             x = "price",
             bins = 100,
             ax = ax)

plt.show()

"""ternyata distribusinya masih miring ke kanan kita coba melihat sebaran outlier dari 'price' berdasarkan 'vehicle_type'"""

# Membuat boxplot
plt.figure(figsize=(10, 6))  # Ukuran plot
sns.boxplot(x='vehicle_type', y='price', data=autos)
plt.title('Rentang Price base of Vehicle Type')
plt.xlabel('Vehicle Type')
plt.ylabel('Price')
plt.xticks(rotation=45)  # Memutar label sumbu x agar mudah dibaca
plt.grid(True)
plt.show()

"""ternyata terdapat outlier dari beberapa tipe mesin.
kita akan mengubah harga berdasarkan IQR, kita cari tahu dulu IQR dari masing-masing tipe
"""

# Menghitung IQR, Q1, dan Q3 dari price digroup berdasarkan vehicle_type
result = autos.groupby('vehicle_type')['price'].describe(percentiles=[.25, .75])

# Menghitung IQR
result['IQR'] = result['75%'] - result['25%']

# Menampilkan hasil
result['IQR']

# Menghapus outlier sesuai dengan data IQR
autos = autos[(autos.vehicle_type == 'andere') & (autos.price <= 3500) |
              (autos.vehicle_type == 'bus') & (autos.price <= 4790) |
              (autos.vehicle_type == 'cabrio') & (autos.price <= 5300) |
              (autos.vehicle_type == 'coupe') & (autos.price <= 5001) |
              (autos.vehicle_type == 'kleinwagen') & (autos.price <= 2710) |
              (autos.vehicle_type == 'kombi') & (autos.price <= 4920) |
              (autos.vehicle_type == 'limousine') & (autos.price <= 4699) |
              (autos.vehicle_type == 'other') & (autos.price <= 2099) |
              (autos.vehicle_type == 'suv') & (autos.price <= 6250)]

# Membuat boxplot
plt.figure(figsize=(10, 6))  # Ukuran plot
sns.boxplot(x='vehicle_type', y='price', data=autos)
plt.title('Rentang Price base of Vehicle Type')
plt.xlabel('Vehicle Type')
plt.ylabel('Price')
plt.xticks(rotation=45)  # Memutar label sumbu x agar mudah dibaca
plt.grid(True)
plt.show()

"""kita cek kembali data price"""

# Buat figure & axes
fig, ax = plt.subplots(figsize = (10, 6))

# Buat histogram plot price
sns.histplot(data = autos,
             x = "price",
             bins = 100,
             ax = ax)

plt.show()

autos.price.describe()

"""- Terlihat Q3 dan nilai maximum sudah tidak berbeda jauh
- Outlier telah dihilangkan

## Eksport Dataset
"""

#eksport dataset yang telah dicleaning
autos.to_csv('autos_cleaned.csv', index=False)