import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


# The frequency() function shows to us the amount of frequncy in terms of brands and color in ads
def frequency():
    my_db = mysql.connector.connect(host='127.0.0.1', user='root', password='javad76mi', database='CarInfo')
    ads_number = len(pd.read_sql("SELECT ID FROM CarFeatures;", my_db))
    brand_df = pd.read_sql("SELECT brand, COUNT(brand) FROM CarFeatures GROUP BY brand;", my_db)
    brand_frequency_df = pd.DataFrame(columns=['Brand', 'frequency'])
    sum_other = 0
    for i in range(len(brand_df)):
        frequency = float(brand_df.at[i, 'COUNT(brand)']) * 100 / ads_number
        if frequency < 1:
            sum_other += frequency
        else:
            new_row = pd.Series([brand_df.at[i, 'brand'], frequency], index=brand_frequency_df.columns)
            brand_frequency_df = brand_frequency_df.append(new_row, ignore_index=True)
    new_row = pd.Series(['other', sum_other], index=brand_frequency_df.columns)
    brand_frequency_df = brand_frequency_df.append(new_row, ignore_index=True)
    brand_frequency_df = brand_frequency_df.set_index('Brand')
    plot = brand_frequency_df.plot.pie(y='frequency')
    color_df = pd.read_sql("SELECT color, COUNT(color) FROM CarFeatures GROUP BY color;", my_db)
    color_frequency_df = pd.DataFrame(columns=['Color', 'frequency'])
    sum_other = 0
    for i in range(len(color_df)):
        frequency = float(color_df.at[i, 'COUNT(color)']) * 100 / ads_number
        if frequency < 1:
            sum_other += frequency
        else:
            new_row = pd.Series([color_df.at[i, 'color'], frequency], index=color_frequency_df.columns)
            color_frequency_df = color_frequency_df.append(new_row, ignore_index=True)
    new_row = pd.Series(['other', sum_other], index=color_frequency_df.columns)
    color_frequency_df = color_frequency_df.append(new_row, ignore_index=True)
    translate_dict = {'آبی': 'blue', 'خاکستری': 'gray', 'سفید': 'white', 'سفید صدفی': 'pearl white', 'قرمز': 'red',
                      'مشکی': 'black', 'نقرهu200cای': 'silver', 'نوکu200cمدادی': 'graphite grey', 'other': 'other'}
    for i in range(len(color_frequency_df)):
        color_frequency_df = color_frequency_df.replace(color_frequency_df.at[i, 'Color'],
                                                        translate_dict[color_frequency_df.at[i, 'Color']])
    color_frequency_df = color_frequency_df.set_index('Color')
    print(color_frequency_df)
    plot = color_frequency_df.plot.pie(y='frequency')
    plt.show()


frequency()
