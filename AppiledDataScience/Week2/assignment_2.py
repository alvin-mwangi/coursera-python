def fix_labels():
    x = plt.gca().xaxis

    # rotate the tick labels for the x axis
    for item in x.get_ticklabels():
        item.set_rotation(45)

    # adjust the subplot so the text doesn't run off the image
    plt.subplots_adjust(bottom=0.25)


def get_tmax_tmin_data(input_subset):
    max_data = input_subset[input_subset['Element'] == 'TMAX'][['MonthDay', 'Data_Value']]
    max_grouped = max_data.groupby(['MonthDay'])['Data_Value'].max()

    min_data = input_subset[input_subset['Element'] == 'TMIN'][['MonthDay', 'Data_Value']]
    min_grouped = min_data.groupby(['MonthDay'])['Data_Value'].min()

    max_grouped.sort_index(inplace=True)
    min_grouped.sort_index(inplace=True)

    return max_grouped, min_grouped


def get_weather_data(binsize, hashid):
    file_path = f'data/C2A2_data/BinnedCsvs_d{binsize}/{hashid}.csv'

    weather_df = pd.read_csv(file_path)
    weather_df['Data_Value'] = weather_df[
                                   'Data_Value'] * 0.1  # convert to whole degrees Celcius (from 10ths of degrees)
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

    t_max_grouped, t_min_grouped = get_tmax_tmin_data(weather_df_subset)

    weather_df_2015 = (weather_df[(weather_df['Date'] >= '2015-01-01') & (weather_df['Date'] < '2016-01-01') &
                                  (weather_df['Date'].str[-5:] != '02-29')  # skip leap day
                                  ]
    )

    weather_df_2015['MonthDay'] = weather_df_2015['Date'].str[-5:]

    t_max_grouped_2015, t_min_grouped_2015 = get_tmax_tmin_data(weather_df_2015)

    t_max_2015_merged = (t_max_grouped.to_frame(name='t_max_10_years')
                         .join(t_max_grouped_2015.to_frame(name='t_max_2015'))
                         )
    t_max_2015_merged['rn'] = np.arange(len(t_max_2015_merged))

    t_min_2015_merged = (t_min_grouped.to_frame(name='t_min_10_years')
                         .join(t_min_grouped_2015.to_frame(name='t_min_2015'))
                         )
    t_min_2015_merged['rn'] = np.arange(len(t_min_2015_merged))

    t_mins_defeated_in_2015 = (t_min_2015_merged[t_min_2015_merged['t_min_2015'] <
                                                 t_min_2015_merged['t_min_10_years']
                                                 ]
    )

    t_maxs_defeated_in_2015 = (t_max_2015_merged[t_max_2015_merged['t_max_2015'] >
                                                 t_max_2015_merged['t_max_10_years']
                                                 ]
    )

    plt.figure()

    plt.scatter(t_maxs_defeated_in_2015['rn'],
                t_maxs_defeated_in_2015['t_max_2015'],
                color='#ef5675',
                marker='^',
                s=48,
                label='Record-Breaking 2015 High'
                )
    plt.scatter(t_mins_defeated_in_2015['rn'],
                t_mins_defeated_in_2015['t_min_2015'],
                color='#7a5195',
                marker='v',
                s=48,
                label='Record-Breaking 2015 Low'
                )

    plt.plot(t_max_grouped.values, '-', color='#ffa600', alpha=0.5, label='Record High')
    plt.plot(t_min_grouped.values, '-', color='#003f5c', alpha=0.5, label='Record Low')

    # fill the area between the linear data and exponential data
    plt.gca().fill_between(range(1, 366),
                           t_max_grouped.values, t_min_grouped.values,
                           facecolor='#bc5090',
                           alpha=0.15
                           )

    plt.xticks(np.arange(1, 366, 31), calendar.month_abbr[1:13], rotation=45)
    plt.legend(fontsize='x-small', loc='lower right', ncol=2, fancybox=True, bbox_to_anchor=(1, 0.05))
    plt.title('Record Temperatures Observed in Ann Arbor, MI\n(From 2005-2014)')
    plt.ylabel('Temp. (°C)')

    # adjust the subplot so the text doesn't run off the image
    plt.subplots_adjust(bottom=0.25)


get_weather_data(400, 'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')
