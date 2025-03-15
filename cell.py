from typing import Tuple, Union


Location = Tuple[int, int]


class Cell:
    """
    class that represents one cell.
    it holds all the data about the cell.
    call is an object with location, formula, seen value and color (set as default)
    """

    WHITE: str = '#ffffff'

    def __init__(self, location: Location, formula: str = '', seen_value: str = '', color: str = WHITE) -> None:
        self.__formula: str = formula
        self.__seen_value: str = seen_value
        self.__color: str = color
        self.__location: Location = location

    def copy_cell(self) -> 'Cell':
        """return a copy of the cell object"""
        return Cell(self.__location, self.__formula, self.__seen_value, self.__color)

    def get_location(self) -> Location:
        """getter function for cell location"""
        return self.__location

    def get_formula(self) -> str:
        """getter function for cell formula"""
        return self.__formula

    def get_color(self) -> str:
        """getter function for cell color"""
        return self.__color

    def get_seen_value(self) -> Union[str, int, float]:
        """getter function for cell seen value"""
        return self.__seen_value

    def set_seen_value(self, new_seen_value: str):
        """set a new value as the cell seen value"""
        self.__seen_value = new_seen_value

    def set_formula(self, new_formula: str):
        """set a new formula as the cell formula"""
        self.__formula = new_formula

    def set_color(self, new_color: str):
        """set a new color as the cell color"""
        self.__color = new_color
