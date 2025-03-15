import re
from typing import List, Tuple, Union, Any
from cell import Cell
import pandas as pd
import matplotlib.pyplot as plt
import math_functions

Location = Tuple[int, int]


class TableCalculator:
    """
    class that represent one spreadsheet, holds cell objects.
    the class is responsible to all the table calculates.
    works mainly with pandas
    """
    COLUMNS = 26

    def __init__(self, title: str = "Baby Excel", data_frame: pd.DataFrame = pd.DataFrame()):
        self.__title = title
        self.rows: int = 40
        self.__EQUAL: str = '='
        self.__PROHIBIT_OPERATORS: List[str] = ['!', "@", "#", "$", "%", "^", "&", "<", ">", '}',
                                                '{', '|', "_", '\\', '`', '~', '?', ':', ';', "'", '"']
        # stack to save the cell states for back button
        self.cell_states_stack: List[Cell] = []
        if data_frame.empty:
            self.__data_frame: pd.DataFrame = self.initial_table()
        else:
            self.__data_frame = data_frame

    # functions regarding the table structure
    def initial_table(self) -> pd.DataFrame:
        """
        initializing an empty dataframe using pandas with empty Cell objects
        :return: dataframe of empty cells
        """
        matrix = []
        for i in range(self.rows):
            mid = []
            for j in range(self.COLUMNS):
                # add empty cells to the matrix
                mid.append(Cell((i, j)))
            matrix.append(mid)
        data_frame = pd.DataFrame(matrix)
        return data_frame

    def update_data_frame(self, matrix: List[List]) -> pd.DataFrame:
        """
        update the dataframe with a given matrix
        :param matrix: matrix of cells
        :return: dataframe of cells
        """
        try:
            self.__data_frame = pd.DataFrame(matrix)
            return self.__data_frame
        except Exception:
            raise Exception

    def add_row(self):
        """
        add row to the dataframe + matrix + update the num of rows
        we use it when the user push add new row
        """
        try:
            new_row = []
            matrix = self.table_as_matrix()
            if len(matrix) < 1000:
                for i in range(len(matrix[0])):
                    new_row.append(Cell((len(matrix), i)))
                matrix.append(new_row)
                self.update_data_frame(matrix)
                self.rows += 1
        except Exception:
            raise Exception

    def table_as_matrix(self) -> List[List]:
        """
        return the dataframe as matrix
        :return: matrix of cells"""
        return self.__data_frame.values.tolist()

    # getters and setters
    def get_data_frame_formula(self) -> pd.DataFrame:
        """
        I use it when I want to export the data to excel
        :return: dataframe of cells' formulas
        """
        matrix = []
        for i in range(len(self.table_as_matrix())):
            mid = []
            for j in range(len(self.table_as_matrix()[0])):
                mid.append(self.get_cell((i, j)).get_formula())
            matrix.append(mid)
        data_frame = pd.DataFrame(matrix)
        return data_frame

    def get_data_frame_seen_values(self) -> pd.DataFrame:
        """
        I use it to create the line chart
        :return: dataframe of cells' seen values
        """
        matrix = []
        for i in range(len(self.table_as_matrix())):
            mid = []
            for j in range(len(self.table_as_matrix()[0])):
                mid.append(self.get_cell((i, j)).get_seen_value())
            matrix.append(mid)
        data_frame = pd.DataFrame(matrix)
        return data_frame

    def get_title(self) -> str:
        """
        getter for table title
        :return: title of the table
        """
        return self.__title

    def get_cell(self, location: Location) -> Any:
        """
        getter for Cell object in given location
        :param location: location of the cell
        :return: cell object
        """
        return self.__data_frame.loc[location[0]][location[1]]

    def get_cell_seen_value(self, location: Location) -> Union[str, int, float]:
        """
        getter for seen value of a cell from table object using location
        :param location: location of the cell
        :return: seen value of the cell
        """
        return self.get_cell(location).get_seen_value()

    def get_formula(self, location: Location) -> str:
        """
        return the formula of a cell from table object using location
        :param location: location of the cell
        :return: formula of the cell
        """
        return self.get_cell(location).get_formula()

    def set_cell(self, cell: Cell, location: Location):
        """
        setter of cell object in a specific location
        :param cell: cell object,
        :param location: location of the cell
        """
        self.__data_frame.loc[location[0]][location[1]] = cell

    def set_rows(self, rows: int):
        """
        set the number of rows in the table
        :param rows: number of rows
        """
        self.rows = rows

    def set_cols(self, cols: int):
        """
        set the number of columns in the table
        :param cols: number of columns
        """
        self.COLUMNS = cols

    def set_title(self, new_title: str):
        """
        setter for table title
        :param new_title: title
        """
        self.__title = new_title

    # updates in table
    def update_cell_seen_value(self, location: Location, current_text: str):
        """
        update the cell with a new seen value
        :param location: location of the cell
        :param current_text: seen value
        """
        cell: Cell = self.get_cell(location)
        cell.set_seen_value(current_text)

    def update_cell_formula(self, location: Location, formula: str):
        """
        update the cell formula
        :param location: location of the cell
        :param formula: formula
        """
        cell: Cell = self.get_cell(location)
        cell.set_formula(formula)

    def update_table_with_color(self, cell_location: Location, color: str):
        """
        update cell's color
        :param cell_location: location of the cell
        :param color: color
        """
        cell: Cell = self.get_cell(cell_location)
        cell.set_color(color)

    # calculations
    def get_cell_dependencies(self, formula: str) -> List[str]:
        """
        get all the dependencies of a cell formula using regext

        for example: if the formula is 'A1 + B2' the function will return ['A1', 'B2']
        :param formula:
        :return: list of dependencies
        """
        # recognize the pattern of the cell location(letters and numbers)
        pattern = r'\b[a-z]\d{1,3}\b'
        dependencies: List[str] = re.findall(pattern, formula.lower())
        return dependencies

    def resolve_cell(self, formula: str) -> str:
        """
        when the user point to another cell he uses the table format 'A1'.
        this function replace the pointers with the cell value - so we can calculate them
        this function change recursively each pointer to the cell value

        for example: if the formula is 'A1 + B2' and A1 = 3 and B2 = 4 the function will return '3 + 4'
        :param formula: formula of the cell
        :return: formula without pointers
        """
        # pattern of cell location as I get from the user is 'A2' the regx helps me identify these patterns
        dependencies: List = self.get_cell_dependencies(formula)
        # a recursive call to convert all pointers to cell seen value
        if len(dependencies) == 0:
            return formula
        if len(dependencies) == 1 and len(formula) <= 4:
            location = self.convert_location_to_cord(dependencies[0])
            seen_value = self.get_cell(location).get_seen_value()
            cell_value = seen_value if seen_value != '' else 0
            formula = cell_value
            return formula
        for dep in dependencies:
            dep_location = self.convert_location_to_cord(dep)
            seen_value = self.get_cell(dep_location).get_seen_value()
            cell_value = seen_value if seen_value != '' else 0
            formula = formula.replace(dep, f'{cell_value}')
        return self.resolve_cell(formula)

    def calculate_cell(self, cell_location: Location, formula: str):
        """
        update a single cell with a given formula.
        check if the formula starts with '=' - it's a calculation.
        if it's not calculation -  update the cell with the formula.
        if it's calculation - check if the calculation stand with our pattern and if so, calculate using eval.
        Unless - update the cell with an error message.

        this function is the main function of the class it holds all the calculation of a cell.

        for example: if the formula is '=A1 + B2' and A1 = 3 and B2 = 4 the function will return '7'
        :param cell_location: location of the cell
        :param formula: formula
        """
        if not formula.startswith(self.__EQUAL):
            self.update_cell_seen_value(cell_location, formula)
            return
        try:
            lower_formula: str = formula.lower()
            # attention I call without_pointer function only if the formula starts with '='
            resolved_formula = self.resolve_cell(lower_formula)
            # check if the expression is empty or doesn't have numbers in it
            if self.non_numeric_formula(resolved_formula, lower_formula, cell_location):
                return
            # check if the expression has prohibited operators
            if resolved_formula != 0 and any(operator in lower_formula for operator in self.__PROHIBIT_OPERATORS):
                raise SyntaxError
            if resolved_formula != 0 and any(operator in resolved_formula for operator in self.__PROHIBIT_OPERATORS):
                self.update_cell_seen_value(cell_location, resolved_formula)
                return
            # calculate the expression
            if resolved_formula != 0 and resolved_formula.startswith('='):
                resolved_formula = resolved_formula[1:]
                result = eval(resolved_formula, {'average': math_functions.avg, 'sum': math_functions.custom_sum,
                                                 'min': min, 'max': max, 'sqrt': math_functions.sqrt,
                                                 'sin': math_functions.sinus, 'cos': math_functions.cosinus,
                                                 'tan': math_functions.tangens})
                self.update_cell_seen_value(cell_location, str(result))
                return
            self.update_cell_seen_value(cell_location, resolved_formula)

        # catch all the errors that can occur in the eval function
        except ZeroDivisionError:
            self.update_cell_seen_value(cell_location, 'ZeroDivision Error')
        except IndexError:
            self.update_cell_seen_value(cell_location, 'Index Error')
        except SyntaxError:
            self.update_cell_seen_value(cell_location, 'Prohibit Operator / Syntax Error')
        except NameError:
            self.update_cell_seen_value(cell_location, 'Name Error')
        except Exception:
            self.update_cell_seen_value(cell_location, 'Error')

    def non_numeric_formula(self, resolved_formula: str, lower_formula: str, cell_location: Location) -> bool:
        """
        check if the formula is not a calculation and update the cell with the formula
        string chain or letters chain are not allowed
        prohibited operators are not allowed
        :param resolved_formula:
        :param lower_formula:
        :param cell_location:
        :return: boolean if the cell seen value was updated
        """
        if resolved_formula != 0 and not any(char.isdigit() for char in resolved_formula):
            # to avoid letters / string chain
            if re.search(r'[+*/-][a-z]', resolved_formula) or re.search(r'[a-z][+*/-]', resolved_formula):
                raise SyntaxError
            # avoid forbidden operators
            elif any(operator in lower_formula for operator in self.__PROHIBIT_OPERATORS):
                raise SyntaxError
            else:
                self.update_cell_seen_value(cell_location, resolved_formula)
                return True
        return False

    def calculate_cells(self, cells_locations: List[Location]):
        """
        calculate all cells in a given list of locations
        :param cells_locations: list of locations
        """
        for location in cells_locations:
            self.calculate_cell(location, self.get_cell(location).get_formula())

    def get_current_level_deps(self, previous_level_deps: List[str]) -> List[Location]:
        """
        returns a list of coordinates of the current level cells based on all cells in all previous levels
        each dependency is determined by the union of all previous levels dependencies
        if a cell has a dependency which is not included in the previous levels,
        his formula can't be calculated, and therefore it's not included in the current level
        :param previous_level_deps: list of all previous levels dependencies
        :return: list of coordinates of the current level cells
        """
        try:
            current_level_deps: List = []
            for row in range(self.rows):
                for col in range(self.COLUMNS):
                    if (row, col) in previous_level_deps:
                        continue
                    # formula dependencies
                    deps = self.get_cell_dependencies(self.get_cell((row, col)).get_formula())
                    # convert the dependencies to coordinates
                    deps_locations = map(lambda dep: self.convert_location_to_cord(dep), deps)
                    is_cell_in_level: bool = True
                    for location in deps_locations:
                        if location not in previous_level_deps:
                            cell: Cell = self.get_cell((row, col))
                            cell.set_seen_value('Error')
                            is_cell_in_level = False
                            break
                    if is_cell_in_level:
                        current_level_deps.append((row, col))
            return current_level_deps
        except Exception:
            raise Exception

    def calculate_table(self, cell_location: Location, formula: str):
        """
        calculate all cells seen values in the order of the dependencies between the cells
        :param cell_location: location of the cell
        :param formula: formula
        """
        cell: Cell = self.get_cell(cell_location)
        cell.set_formula(formula)
        previous_level_deps: List[str] = []
        current_level_deps: List = self.get_current_level_deps(previous_level_deps)
        # each iteration of the loop is a dependency level
        while len(current_level_deps) != 0:
            # calculate all cells of the current level
            self.calculate_cells(current_level_deps)
            previous_level_deps = previous_level_deps + current_level_deps
            current_level_deps = self.get_current_level_deps(previous_level_deps)

    def convert_location_to_cord(self, location: str) -> Union[Location]:
        """
        the function get a string represent location such as 'A0' and return the string coordinate
        for example: 'A1' -> (0, 0)
        :param location: location
        :return: coordinate
        """
        letter: str = location[0].upper()
        coordinate: Location = (int(location[1:]) - 1, ord(letter) - 65)
        return coordinate

    # exports and features
    def to_json(self) -> Union[str, dict, Any]:
        """
        prepare to export the data to json file
        for each cell in the table, the function returns the formula, seen value and color
        example: {(0, 0): ['=4+3', 7, 'red']}
        :return: title and data of the table
        """
        table_data: dict = {}
        for i in range(len(self.table_as_matrix())):
            for j in range(len(self.table_as_matrix()[0])):
                cell: Cell = self.get_cell((i, j))
                table_data[str((i, j))] = [cell.get_formula(), cell.get_seen_value(), cell.get_color()]
        return self.__title, table_data

    def from_json(self, data: dict) -> pd.DataFrame:
        """
        get data from json and convert it to a dataframe
        :param data: dictionary represents the table
        :return: dataframe with cells
        """
        try:
            max_row: int = int(0)
            max_col: int = int(0)
            for coord_str in data[1].keys():
                # Parse the string representation of the tuple and extract x and y coordinates
                row, col = map(int, coord_str.strip("()").split(', '))
                # Update max_x and max_y if necessary
                max_row = max(max_row, row)
                max_col = max(max_col, col)
            matrix: List[List] = []
            for i in range(max_row + 1):
                mid: List = []
                for j in range(max_col + 1):
                    formula: str = data[1][str((i, j))][0]
                    seen_value: str = data[1][str((i, j))][1]
                    color: str = data[1][str((i, j))][2]
                    mid.append(Cell((i, j), formula, seen_value, color))
                matrix.append(mid)
            # set the matrix to data frame and update the table object with
            return self.update_data_frame(matrix)
        except Exception:
            raise Exception

    def clear_all(self) -> List[List]:
        """
        clear all the cells in the table
        :return: matrix of cells
        """
        self.__data_frame = self.initial_table()
        return self.table_as_matrix()

    def push_state(self, location: Location):
        """
        push the current state of the cell to the stack
        :param location: location of the cell
        """
        self.cell_states_stack.append(self.get_cell(location).copy_cell())

    def pop_last_state(self):
        """
        pop the last state of the cell from the stack
        """
        if len(self.cell_states_stack) == 0:
            return
        cell_state: Cell = self.cell_states_stack.pop()
        self.calculate_table(cell_state.get_location(), cell_state.get_formula())

    def create_line_chart(self):
        """
        create a bar chart of the seen values in the table
        """
        try:
            # create a data frame of all seen values to be presented in the chart
            df_seen_values: pd.DataFrame = self.get_data_frame_seen_values()
            df_seen_values.columns = df_seen_values.iloc[0]
            df_seen_values = df_seen_values.drop(0)
            # get rid of all strings in the table and convert them to numbers
            df_transpose = df_seen_values.apply(lambda x: pd.to_numeric(x, errors='coerce')).astype(float)
            # create the line chart
            df = df_transpose.plot(kind='line')
            # get rid of empty lines in the plot legend
            handles, labels = df.get_legend_handles_labels()
            non_empty_labels: List[str] = [label for label, column in zip(labels, df_transpose.columns)
                                           if df_transpose[column].any()]
            non_empty_handles: List[str] = [handle for handle, column in zip(handles, df_transpose.columns)
                                            if df_transpose[column].any()]
            df.legend(non_empty_handles, non_empty_labels, title='Line Names', loc='upper right')
            # show the chart
            plt.title(self.__title)
            plt.show()
        except Exception:
            raise Exception
