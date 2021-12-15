import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl


# The frequency() function shows to us the amount of frequncy in terms of brands and color in ads
def frequency():
    # Connecting to database and reading cars brand data
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

    # Show frequency brands with pyplot in pie chart
    brand_slices = brand_frequency_df['frequency'].tolist()
    brand_labels = brand_frequency_df.index.tolist()
    brand_fig = plt.figure(figsize=[10, 10])
    brand_ax = brand_fig.add_subplot(111)
    brand_ax.set_title('Cars Brand Frequency')
    brand_ax.pie(brand_slices, labels=brand_labels, labeldistance=1.05)

    # Reading cars color data to dataframe
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
    translation_dict = {'آبی': 'blue', 'خاکستری': 'gray', 'سفید': 'white', 'سفید صدفی': 'pearl white', 'قرمز': 'red',
                        'مشکی': 'black', 'نقرهu200cای': 'silver', 'نوکu200cمدادی': 'graphite grey', 'other': 'other'}
    for i in range(len(color_frequency_df)):
        color_frequency_df = color_frequency_df.replace(color_frequency_df.at[i, 'Color'],
                                                        translation_dict[color_frequency_df.at[i, 'Color']])
    color_frequency_df = color_frequency_df.set_index('Color')

    # Display color frequency in pie chart
    color_slices = color_frequency_df['frequency'].tolist()
    colors = ['blue', 'gray', 'white', '#FAF8FA', 'red', 'black', '#D3D3D3', '#A9A9A9', 'green']
    color_labels = color_frequency_df.index.tolist()
    color_dict = {}
    for [l, c] in zip(color_labels, colors):
        color_dict[l] = c
    color_fig = plt.figure(figsize=[10, 10])
    color_ax = color_fig.add_subplot(111)
    pie_wedge_collection = color_ax.pie(color_slices, labels=color_labels, labeldistance=1.05)
    for pie_wedge in pie_wedge_collection[0]:
        pie_wedge.set_edgecolor('#99004C')
        pie_wedge.set_facecolor(color_dict[pie_wedge.get_label()])
    color_ax.set_title('Cars Color Frequency')
    plt.show()


frequency()
