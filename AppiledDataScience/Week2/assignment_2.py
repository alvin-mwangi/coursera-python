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
    weather_df_subset = (weather_df[(weather_df['Date'] >= '2005-01-01') & (weather_df['Date'] < '2015-01-01') &
                                    (weather_df['Date'].str[-5:] != '02-29')  # skip leap day
                                    ]
    )

    #     for i in weather_df_subset['Date'].sort_values().unique():
    #         if("-02-" in i):
    #             print(i)
    pd.options.mode.chained_assignment = None  # default='warn'
    weather_df_subset['MonthDay'] = weather_df_subset['Date'].str[-5:]

    t_max_data = weather_df_subset[weather_df_subset['Element'] == 'TMAX'][['MonthDay', 'Data_Value']]
    t_max_grouped = t_max_data.groupby(['MonthDay'])['Data_Value'].max()

    t_min_data = weather_df_subset[weather_df_subset['Element'] == 'TMIN'][['MonthDay', 'Data_Value']]
    t_min_grouped = t_min_data.groupby(['MonthDay'])['Data_Value'].min()

    t_max_grouped.sort_index(inplace=True)
    t_min_grouped.sort_index(inplace=True)

    print(t_max_grouped.shape)
    print(t_max_grouped.head())

    print(t_min_grouped.shape)
    print(t_min_grouped.head())

    plt.figure()
    #     plt.plot(t_max_dates, t_max_testdata, 'r-o', t_min_dates, t_min_testdata, 'c-.', markersize=1)
    plt.plot(t_max_grouped.values, '-', color='red')
    plt.plot(t_min_grouped.values, '-', color='blue')

    #     # fill the area between the linear data and exponential data
    plt.gca().fill_between(range(1, 366),
                           t_max_grouped.values, t_min_grouped.values,
                           #                            facecolor='cyan',
                           alpha=0.35)


get_weather_data(400, 'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')
