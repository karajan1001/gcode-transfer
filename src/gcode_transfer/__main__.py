"""Command-line interface."""
import click
import matplotlib.pyplot as plt

from .gcode_parser import parse_gcode
from .model_convert import model_transfer


@click.command()
@click.version_option()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--draw", is_flag=True, default=False)
@click.argument("output", type=click.Path(exists=False))
@click.option(
    "--distance", help="Distance used in sampling point in lines", default=0.5
)
@click.option(
    "--alpha", help="Alpha value used in the alpha shape", default=0.5
)
def main(filename: str, output: str, draw: bool, distance, alpha) -> None:
    """Gcode Transfer."""
    with open(filename, encoding="utf-8") as f_r:
        lines = parse_gcode(f_r)
    if draw:
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection="3d")
        for line in lines:
            ax.plot(
                [line[0][0], line[1][0]],
                [line[0][1], line[1][1]],
                [line[0][2], line[1][2]],
                color="g",
            )

        plt.show()

    vertices, triangles = model_transfer(lines, distance, alpha)
    with open(output, "w", encoding="utf-8") as f_w:
        f_w.write("vertices:\n")
        for data in vertices:
            f_w.write(str(data))
            f_w.write("\n")
        f_w.write("triangles:\n")
        for data in triangles:
            f_w.write(str(data))
            f_w.write("\n")


if __name__ == "__main__":
    main()
