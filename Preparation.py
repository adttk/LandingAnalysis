import pandas as pd


class Preparation:

    raw_data = None
    clean_attributes = None
    data_after_sorting = None
    data_touchdown = None
    data_time_timestamp_difference = None
    data_tier1 = None
    data_with_runway = None

    def set_raw_data(self, df):

        self.raw_data = df

    def drop_columns(self):

        self.clean_attributes = self.raw_data.drop(
            columns=['icao24', 'ground_speed', 'radar', 'squawk', 'departure', 'destination', 'number', 'airline_iata', 'on_ground', 'vertical_speed'])

    def get_touchdown(self):

        self.data_after_sorting = self.clean_attributes.sort_values(
            ['registration', 'flight_id'], ascending=True)
        self.data_after_sorting.reset_index(drop=True, inplace=True)
        df_touchdown = pd.DataFrame(columns=self.clean_attributes.columns)

        i = 0
        while (True):

            if (self.data_after_sorting['altitude'][i] > 0 and self.data_after_sorting['altitude'][i+1] == 0):

                df_touchdown.loc[i] = self.data_after_sorting.loc[i]
                df_touchdown.loc[i+1] = self.data_after_sorting.loc[i+1]

            i += 1

            if (i == len(self.data_after_sorting)):
                break

        df_touchdown.reset_index(drop=True, inplace=True)
        self.data_touchdown = df_touchdown

    def get_tier1(self):

        # Add new Attribute timestamp_difference
        self.data_timestamp_difference = pd.DataFrame(self.data_touchdown)
        self.data_timestamp_difference['timestamp_difference'] = ''

        # Calculate difference of timestamp
        i = 0
        while (True):

            if (i >= len(self.data_timestamp_difference)):
                break

            self.data_timestamp_difference['timestamp_difference'][i +
                                                                   1] = self.data_timestamp_difference['time'][i+1]-self.data_timestamp_difference['time'][i]

            i += 2

        # filter and save data tier 1 to new csv file
        self.data_tier1 = pd.DataFrame(self.data_timestamp_difference)
        self.data_tier1 = self.data_tier1[self.data_tier1['timestamp_difference'] != '']
        self.data_tier1 = self.data_tier1[self.data_tier1['timestamp_difference'] < 10]

    def add_runway(self):
        self.data_with_runway = pd.DataFrame(self.data_tier1)
        self.data_with_runway.reset_index(drop=True, inplace=True)
        self.data_with_runway['Runway'] = ''

        i = 0
        while (True):

            if (i >= len(self.data_with_runway)):
                break

            if (self.data_with_runway['heading'][i] >= 90 and self.data_with_runway['heading'][i] <= 225):
                self.data_with_runway['Runway'][i] = 18

            if ((self.data_with_runway['heading'][i] >= 0 and self.data_with_runway['heading'][i] <= 90) or (self.data_with_runway['heading'][i] >= 225 and self.data_with_runway['heading'][i] <= 360)):
                self.data_with_runway['Runway'][i] = 36

            i += 1

    def check_data(self, df):
        count = ''

        # check duplicate value
        cek_duplicated = df.duplicated()
        for i in cek_duplicated.index:
            if (cek_duplicated.loc[i] == True):
                count += str(i)+'\n'

        # distinc value observation
        aircraft = df.value_counts(['aircraft_code'], dropna=False)
        airline = df.value_counts(['airline_icao'], dropna=False)

        # find the missing value and save on new csv file
        missing_value = df.isna().sum()

        a = ('ATTRIBUTES VALUE : ' +
             '\n' + str(aircraft) + '\n'
             '\n' + str(airline) + '\n'
             '\n'+'\n'+'MISSING VALUE : ' +
             '\n' + str(missing_value) +
             '\n'+'\n'+'COUNT OF DUPLICATED DATA : ' +
             '\n' + str(count) + '\n')
        return a
