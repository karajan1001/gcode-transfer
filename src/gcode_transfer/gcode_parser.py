# file to parse gcode
import numpy as np
from typing import Optional, TYPE_CHECKING, Any, Union, Tuple, List

if TYPE_CHECKING:
    from io import TextIOWrapper
    from numpy.typing import NDArray


class ParseError(Exception):
    """Line parse error"""
    def __init__(self, line: str):
        """store error line"""
        self.line = line

    def __str__(self) -> str:
        return f"cannot parse line '{self.line}'."


class Point:
    """A point object hold the """
    def __init__(self,x: float, y: float, z: float):
        """Initialize a point"""
        self._point: "NDArray" = np.asarray([x, y, z])

    @property
    def x(self) -> float:
        """property x"""
        return self._point[0]

    @property
    def y(self) -> float:
        """property y"""
        return self._point[1]

    @property
    def z(self) -> float:
        """property z"""
        return self._point[2]
  
    @x.setter
    def x(self, x: float):
        """property x"""
        self._point[0] = x

    @y.setter
    def y(self, y: float):
        """property y"""
        self._point[1] = y

    @z.setter
    def z(self, z: float):
        """property z"""
        self._point[2] = z

    @property
    def value(self) -> "NDArray":
        return self._point

    
    def __eq__(self, other: Any) -> bool:
        """check if two point is the same"""
        if isinstance(other, Point):
            if np.array_equal(self._point, other._point):
                return True
        return False


def parse_line(line: str, header: "Point") -> Optional[Tuple["Point", bool]]:
    """Parse a line of command, return the new header position, and if extruded"""
    line = line.strip()
    
    if line.startswith(";"):
        return None
    
    if line.startswith("G1 "):
        _, *vec = line.split(" ")
        x,y,z = None, None, None
        extrude = False
        for data in vec:
            if data[0] == "X":
                x = float(data[1:])
            elif data[0] == "Y":
                y = float(data[1:])
            elif data[0] == "Z":
                z = float(data[1:])
            elif data[0] == "F":
                continue
            elif data[0] == "E":
                if float(data[1:]) > 0:
                    extrude = True
                    break
            else:
                raise ParseError(line)
        return Point(x or header.x, y or header.y, z or header.z), extrude
        
    return None
        

def parse_gcode(file: "TextIOWrapper") -> List[Tuple["NDArray", "NDArray"]]:
    """Parse a gcode stream data return list of lines

    Args:
        file (str): gcode stream data
    """

    current = Point(0.0,0.0,0.0)
    nodes = []
    extrude = False

    for line in file.readlines():
        try:
            g1_command = parse_line(line, current)
        except ValueError as err:
            raise ParseError(line) from err
        if g1_command:
            new, extrude = g1_command
            if extrude:
                nodes.append((current._point, new._point))
            current = new
    return nodes