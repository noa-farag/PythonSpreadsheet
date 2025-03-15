from spreadsheet_gui import SpreadSheetGUI
from table_calculator import TableCalculator
from file import File
import argparse

description: str = ("""
Below are instructions on how to use the program:
    1. The table opens with 26 columns and 40 rows. You can add up tp 1,000 rows using 'Add Row' button.
    2. You can navigate between cells using the arrow keys.
    3. You can add strings, numbers, and formulas to the cells.
    4. If you want to enter a formula in a cell start with '=' (e.g. =4+3) and press enter to see the result.
    5. You can also enter a formula with a cell reference (e.g. =A1+3) and press enter to see the result.
    6. To use the min/max/average/sin/cos/tan functions, you need to enter '=', the function name and the 
        cell reference separated by ',' (e.g. =min(A1,A2,A3,A4), =average(B2, B4)).
    7. you can combine functions with other functions and numbers (e.g. =min(A1,A2,A3,A4,max(3,4), =max(1,B2,min(3,4))).
    8. If you want to save the table, go to File -> Save and choose the file path. 
        You can save in Excel or export to JSON.
    9. If you want to load data, go to File -> Load and choose the file path. 
        You can load only from JSON with the exporting template.
    10. If you want to clear the data, use the button 'Clear'.
    11. to add a new row, use the button 'Add Row'.
    12. to change the color of a cell, use the button 'Change Color'.
    13. Use the 'Back' button to cancel the last formula, you can use it multiple times to cancel previous formulas.
    14. Feel free to change the spreadsheet name using the 'Change Name' button (relevant mainly for saving the file).
    15. Use the 'Line Chart' button to create a line chart from the data. Pay attention it works only with numbers 
        only at the top right corner of the table.
    ENJOY! :)
    NF
""")


def main():
    """
    main function that runs the program
    """

    try:
        table = TableCalculator()
        file = File()
        spreadsheet = SpreadSheetGUI(table, file)
        spreadsheet.run()
    except Exception as e:
        print(f"{'Sorry, we had an'}, {e}, {'error - please try again.'}")


if __name__ == '__main__':
    """
    set -- help to the program and
    run the main function
    """
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    args = parser.parse_args()

    main()
