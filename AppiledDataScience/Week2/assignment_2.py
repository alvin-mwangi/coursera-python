def fix_labels():
    x = plt.gca().xaxis

    # rotate the tick labels for the x axis
    for item in x.get_ticklabels():
        item.set_rotation(45)

    # adjust the subplot so the text doesn't run off the image
    plt.subplots_adjust(bottom=0.25)


def get_weather_data(binsize, hashid):
    file_path = f'data/C2A2_data/BinnedCsvs_d{binsize}/{hashid}.csv'

    weather_df = pd.read_csv(file_path)
    # print(weather_df)
    weather_df_subset = weather_df[(weather_df['Date'] >= '2005-01-01') & (weather_df['Date'] < '2015-01-01')]

    t_max_data = weather_df_subset[weather_df_subset['Element'] == 'TMAX'][['Date', 'Data_Value']]
    t_max_grouped = t_max_data.groupby(['Date'])['Data_Value'].max()
    #     print(t_max_grouped)

    t_min_data = weather_df_subset[weather_df_subset['Element'] == 'TMIN'][['Date', 'Data_Value']]
    t_min_grouped = t_min_data.groupby(['Date'])['Data_Value'].min()
    #     print(t_min_grouped)

    #     t_max_data.sort_values(by='Date', inplace=True)
    #     print(t_max_data.head(10))
    samplesize = 75
    t_max_dates = t_max_grouped.index.values
    t_max_dates = list(map(pd.to_datetime, t_max_dates))  # [:samplesize]
    t_max_testdata = t_max_grouped.tolist()
    #     print(t_max_testdata[:5])
    #     t_max_testdata = t_max_testdata[:samplesize]

    t_min_dates = t_min_grouped.index.values
    t_min_dates = list(map(pd.to_datetime, t_min_dates))  # [:samplesize]
    t_min_testdata = t_min_grouped.tolist()
    #     print(t_max_testdata[:5])
    #     t_min_testdata = t_min_testdata[:samplesize]
    print(len(t_min_testdata))

    #     print(t_max_dates)
    #     print(t_max_testdata)
    plt.figure()
    #     plt.plot(t_max_dates, t_max_testdata, 'r-o', t_min_dates, t_min_testdata, 'c-.', markersize=1)
    plt.plot(t_max_dates, t_max_testdata, '-', color='red')
    plt.plot(t_min_dates, t_min_testdata, '-', color='blue')

    #     # fill the area between the linear data and exponential data
    plt.gca().fill_between(t_max_dates,
                           t_max_testdata, t_min_testdata,
                           facecolor='cyan',
                           alpha=0.35)

    fix_labels()


get_weather_data(400, 'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')
