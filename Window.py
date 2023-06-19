import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib import dates
import datetime


# class that sets up the visual part of the program
class Window:
    # if number of days is less than this the data shown is more exact
    exact_time_delta = 30

    # Default Error Message added before cause of error is displayed to user
    dem = 'Can not draw graph'

    def __init__(self, countries):
        # list of objects Country
        self.countries = countries
        # list of names of countries
        self.countries_names = get_names(countries)

        # check if any files were read
        if len(self.countries_names) < 1:
            raise FileNotFoundError('No csv files to read')

        # set up root, frames, labels and combo boxes
        # (visual parts) of the window

        # frames and root
        self.root = tk.Tk()
        frame_top = tk.Frame(self.root)
        frame_top.pack()
        frame_country_year = tk.Frame(self.root)
        frame_country_year.pack()
        frame_date = tk.Frame(self.root)
        frame_date.pack()
        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack()
        self.root.title('Temperature Graph Drawer')
        self.root.geometry('1200x800')

        """ various labels and combo boxes
            in particular: setting values returned from combo boxes to object attributes
                           and setting info label as object attribute
                           all of the above to be able to access them from methods of this class"""
        label_welcome = tk.Label(frame_top, text='Welcome to Temperature Graph Drawer', font=('Times', '20', 'bold'))
        label_welcome.pack()

        country_1_label = ttk.Label(frame_country_year, text='Country 1:')
        country_1_label.grid(row=0, column=0, pady=(20, 0))
        self.country_1 = tk.StringVar()
        country_1_combobox = ttk.Combobox(frame_country_year, textvariable=self.country_1, values=self.countries_names,
                                          state='readonly')
        country_1_combobox.set(self.countries_names[0])
        country_1_combobox.grid(row=0, column=1, padx=(0, 50), pady=(20, 0))

        year_1_label = ttk.Label(frame_country_year, text='Year 1:')
        year_1_label.grid(row=1, column=0)
        self.year_1 = tk.StringVar()
        country_1_object = self.get_country(self.country_1.get())
        country_1_min_year = country_1_object.get_min_year()
        country_1_max_year = country_1_object.get_max_year()

        year_1_combobox = ttk.Combobox(frame_country_year, textvariable=self.year_1,
                                       values=tuple(range(country_1_min_year, country_1_max_year + 1)),
                                       state='readonly')
        year_1_combobox.set(country_1_min_year)
        year_1_combobox.grid(row=1, column=1, padx=(0, 50))

        country_2_label = ttk.Label(frame_country_year, text='Country 2:')
        country_2_label.grid(row=0, column=3, pady=(20, 0))
        self.country_2 = tk.StringVar()
        country_2_combobox = ttk.Combobox(frame_country_year, textvariable=self.country_2, values=self.countries_names,
                                          state='readonly')
        country_2_combobox.set(self.countries_names[0])
        country_2_combobox.grid(row=0, column=4, pady=(20, 0))

        year_2_label = ttk.Label(frame_country_year, text='Year 2:')
        year_2_label.grid(row=1, column=3)
        self.year_2 = tk.StringVar()
        country_2_object = self.get_country(self.country_2.get())
        country_2_min_year = country_2_object.get_min_year()
        country_2_max_year = country_2_object.get_max_year()

        year_2_combobox = ttk.Combobox(frame_country_year, textvariable=self.year_2,
                                       values=tuple(range(country_2_min_year, country_2_max_year + 1)),
                                       state='readonly')
        year_2_combobox.set(country_2_min_year)
        year_2_combobox.grid(row=1, column=4)

        month_from_label = ttk.Label(frame_date, text='From month:')
        month_from_label.grid(row=6, column=0, pady=(50, 20))
        self.month_from = tk.StringVar()
        month_from_combobox = ttk.Combobox(frame_date, textvariable=self.month_from, values=tuple(range(1, 13)),
                                           state='readonly')
        month_from_combobox.set(1)
        month_from_combobox.grid(row=6, column=1, pady=(50, 20))

        day_from_label = ttk.Label(frame_date, text='From day:')
        day_from_label.grid(row=6, column=3, pady=(50, 20))
        self.day_from = tk.StringVar()
        day_from_combobox = ttk.Combobox(frame_date, textvariable=self.day_from, values=tuple(range(1, 32)),
                                         state='readonly')
        day_from_combobox.set(1)
        day_from_combobox.grid(row=6, column=4, pady=(50, 20))

        month_to_label = ttk.Label(frame_date, text='To month:')
        month_to_label.grid(row=7, column=0)
        self.month_to = tk.StringVar()
        month_to_combobox = ttk.Combobox(frame_date, textvariable=self.month_to, values=tuple(range(1, 13)),
                                         state='readonly')
        month_to_combobox.set(1)
        month_to_combobox.grid(row=7, column=1)

        day_to_label = ttk.Label(frame_date, text='To day:')
        day_to_label.grid(row=7, column=3)
        self.day_to = tk.StringVar()
        day_to_combobox = ttk.Combobox(frame_date, textvariable=self.day_to, values=tuple(range(1, 32)),
                                       state='readonly')
        day_to_combobox.set(1)
        day_to_combobox.grid(row=7, column=4)

        self.info_label = ttk.Label(frame_bottom, text='', font=('Times', '15', 'italic'))
        self.info_label.pack()

        # button that applies user defined settings and calls plot method
        draw_button = ttk.Button(frame_bottom, text='Draw', command=self.plot)
        draw_button.pack()

        # setting up showing plot and toolbar from matplotlib
        self.figure = Figure(figsize=(11, 5), dpi=100)
        self.chart = self.figure.add_subplot()

        self.canvas = FigureCanvasTkAgg(self.figure, master=frame_bottom)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect("key_press_event", key_press_handler)

        toolbar = NavigationToolbar2Tk(self.canvas, frame_bottom, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # method that plots graph according to user settings
    def plot(self):
        # clear chart and set defaults
        self.chart.cla()
        self.figure.autofmt_xdate()

        # prepare variables
        year_of_checking_1 = self.year_1.get()
        year_of_checking_2 = self.year_2.get()

        month_from = self.month_from.get().zfill(2)
        day_from = self.day_from.get().zfill(2)

        month_to = self.month_to.get().zfill(2)
        day_to = self.day_to.get().zfill(2)

        # reset info label
        self.info_label.config(text='', background='#F0F0F0')

        # check correctness of the dates
        try:
            datetime.datetime(year=int(year_of_checking_1), month=int(month_from), day=int(day_from))
            datetime.datetime(year=int(year_of_checking_2), month=int(month_from), day=int(day_from))
        except ValueError:
            self.info_label.config(text='{}: "Date from" you provided is incorrect'.format(self.dem), foreground='red')
            return
        try:
            datetime.datetime(year=int(year_of_checking_1), month=int(month_to), day=int(day_to))
            datetime.datetime(year=int(year_of_checking_2), month=int(month_to), day=int(day_to))
        except ValueError:
            self.info_label.config(text='{}": Date to" you provided is incorrect'.format(self.dem), foreground='red')
            return

        # get dates to plot charts
        date_from_1 = self.get_date_from(year_of_checking_1)
        date_to_1 = self.get_date_to(year_of_checking_1)
        date_from_2 = self.get_date_from(year_of_checking_2)
        date_to_2 = self.get_date_to(year_of_checking_2)

        # calculate time delta to check if "date to" is after "date from"
        time_delta = calculate_time_delta(date_from_1, date_to_1)
        if time_delta < 0:
            self.info_label.config(text='{}: "Date to" is after "Date from"'.format(self.dem), foreground='red')
            return

        # check if country and year are the same to provide user with information
        if self.country_1.get() == self.country_2.get() and self.year_1.get() == self.year_2.get():
            self.info_label.config(text='Country 1 and 2 and Year 1 and 2 are the same',
                                   foreground='yellow', background='black')

        # get dataframes for both countries
        data_1 = self.get_country(self.country_1.get()).get_data()
        data_2 = self.get_country(self.country_2.get()).get_data()

        # take part of the data frames
        part_of_data_frame_1 = data_1[date_from_1: date_to_1]
        part_of_data_frame_2 = data_2[date_from_2: date_to_2]

        # set chart formatting
        date_format = dates.DateFormatter('%d-%m (%H)')
        self.chart.set_xlabel('Date (in format: dd-mm (hh))')

        # resample if amount of data is too large
        if time_delta > self.exact_time_delta:
            part_of_data_frame_1 = resample_and_round(part_of_data_frame_1)
            part_of_data_frame_2 = resample_and_round(part_of_data_frame_2)
            date_format = dates.DateFormatter('%d-%m')
            self.chart.set_xlabel('Date (in format: dd-mm)')

        self.chart.xaxis.set_major_formatter(date_format)

        self.chart.set_ylabel('Temperature (in degree Celsius)')
        self.chart.set_title('Temperature Graph')

        # show data for one index
        self.chart.plot(part_of_data_frame_1.index, part_of_data_frame_1['temperature'],
                        label=self.country_1.get() + ' ' + self.year_1.get())
        self.chart.plot(part_of_data_frame_1.index, part_of_data_frame_2['temperature'],
                        label=self.country_2.get() + ' ' + self.year_2.get())
        self.chart.legend()

        self.canvas.draw()

    # get country object based on name
    def get_country(self, country_name):
        for country in self.countries:
            if country.get_name() == country_name:
                return country

    # construct date from based on class parameters and year (year_1 or year_2)
    def get_date_from(self, year_of_checking):
        month_from = self.month_from.get().zfill(2)
        day_from = self.day_from.get().zfill(2)
        return "{}-{}-{}".format(year_of_checking, month_from, day_from)

    # construct date to based on class parameters and year (year_1 or year_2)
    def get_date_to(self, year_of_checking):
        month_to = self.month_to.get().zfill(2)
        day_to = self.day_to.get().zfill(2)
        return "{}-{}-{}".format(year_of_checking, month_to, day_to)

    # get root
    def get_window(self):
        return self.root


# function name explains everything about it
def resample_and_round(dataframe):
    dataframe = dataframe.resample('D').mean()
    return dataframe.round(3)


# returns number of days between two dates
def calculate_time_delta(date_from, date_to):
    date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')
    date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d')

    delta = date_to - date_from

    return delta / datetime.timedelta(days=1)


# return list of names of countries loaded
def get_names(countries):
    names = list()
    for country in countries:
        names.append(country.get_name())
    return names
