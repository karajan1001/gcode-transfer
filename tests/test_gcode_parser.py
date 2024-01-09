import io
import pytest
import numpy as np

from gcode_transfer.gcode_parser import Point, ParseError
from gcode_transfer.gcode_parser import parse_line, parse_gcode


def test_point()->None:
    """test point class"""
    assert Point(1,2,3) == Point(1,2,3)
    assert Point(1,2,3) != Point(2,2,3)
    assert Point(1,2,3) != (1,2,3)


def test_parse_unrelated_line()->None:
    """test parse_line function"""
    header = Point(1,2,3)
    assert parse_line(";   retractBetweenLayers,1", header) == None
    assert header == header
    assert parse_line("M190 S110", header) == None
    assert header == header


def test_parse_error_line()->None:
    """error line parsing"""
    header = Point(0.0,0.0,0.0)
    with pytest.raises(ParseError):
        parse_line("G1 X116.413 378.500 E4.6347", header)

    with pytest.raises(ParseError):
        parse_line("G1 X116.413 M78.500 E4.6347", header)

    with pytest.raises(ValueError):
        parse_line("G1 X116.413 Y78.50.0 E4.6347", header)

def test_parse_line()->None:
    """test parse_line function"""
    header = Point(0.0,0.0,0.0)

    new, extrude = parse_line("G1 Z0.25", header)
    assert new == Point(0.0, 0.0, 0.25)
    assert extrude == False

    new, extrude = parse_line("G1 X116.413 Y78.500 E4.6347", new) 
    assert new == Point(116.413, 78.500, 0.25)
    assert extrude == True


def test_parse_gcode()->None:
    """test parse_line function"""
    gcode_file = """
    G1 Z0.25
    G1 X116.413 Y78.500 
    G1 X113.413 E4.6347
    G1 Y77.500 E4.6347
    """
    lines = parse_gcode(io.StringIO(gcode_file))
    assert np.array_equal(lines[0][0],  np.asarray([116.413, 78.5, 0.25]))
    assert np.array_equal(lines[0][1],  np.asarray([113.413, 78.5, 0.25]))
    assert np.array_equal(lines[1][0],  np.asarray([113.413, 78.5, 0.25]))
    assert np.array_equal(lines[1][1],  np.asarray([113.413, 77.5, 0.25]))