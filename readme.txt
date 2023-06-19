Temperature Graph Drawer information

1. What the program does
    It allows user to compare temperature data for a given year and country.
    User is asked to provide data they wish to visualise in a CSV file and
    is able, based on that data, to draw line charts comparing two chosen
    time periods.

2. Libraries used
     - Pandas - library used to read CSV files and convert them into a data
       frames that are later used for chart plotting.
     - Matplotlib - library used for plotting the charts based on data frames
     - Tkinter - library used to allow user input so that user can select data
       they want to visualise

3. How to run
    To run the project user is required to have installed python
    and it's libraries:
         - Pandas
         - Matplotlib
         - Tkinter
    User should provide data they want to visualise in csv format to data
    folder located in the same directory as main.py file. The csv file name
    should be full name of a country or its abbreviation. The csv file should
    contain two columns: 'utc_timestamp' with date in any reasonable
    (not obscure, relatively popular), python readable format and 'temperature'
    with float data.

4. Examples
    Program can, among others, to compare temperatures between years in
    the same country to derive insights about coldness of the winter or
    hotness of the summer year by year.
    It is also possible to compare temperatures in the same year between
    different countries which may lead to understanding the differences
    between climates.

5. Key features
    Plotting charts based on provided data.
    Customizing charts to user's liking.

6. Challenges faced
    Combining libraries together was a difficulty especially tkinter and
    matplotlib. Designing interface with tkinter.

7. Lessons learned
    Combining multiple libraries together to achieve goal in which use of one of
    them would not be sufficient. Indexing and slicing dataframe based on date.