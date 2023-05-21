# Convert SVG to Turtle draw

## Description

This script allows you to convert Scalable Vector Graphics (SVG) files into Turtle draw commands. Turtle graphics is a popular way to introduce programming concepts to beginners, and it provides a simple way to draw shapes and patterns on a screen using a virtual "turtle".

The script reads an SVG file and extracts the path data from it. It then converts the path data into a series of Turtle draw commands that can be executed by a Turtle graphics library. This enables you to take advantage of the rich graphics capabilities offered by SVG files and replicate them using the Turtle graphics library.

## Features

- Converts SVG files to Turtle draw commands.
- Supports basic SVG path commands like `M` (Move to), `L` (Line to), `C` (Cubic Bézier Curve), and `Z` (Close path).
- Translates SVG coordinates and scales them to fit within the Turtle graphics coordinate system.
- Maintains the color and stroke properties of the SVG shapes in the Turtle drawings.
- Outputs the Turtle draw commands in a format compatible with popular Turtle graphics libraries.

## Setup

```
1. Clone the repository:
> git clone https://github.com/Tuanpluss02/turtle-svg.git

2. Change into the project directory:
> cd turtle-svg

3. Create a virtual environment:
> py -m venv venv

4. Activate the virtual environment:
> source venv/bin/activate (Linux)
> venv\Scripts\activate (Windows)

5. Install dependencies:
> pip install -r requirements.txt
```

# Usage
1. To vectorize an image as an SVG file
Use this website: https://vectorizer.ai. **Do use this one, the code is meant to run with the SVG spec associated with this tool specifically**.
2. To convert an SVG file to Turtle draw commands
```
> py draw.py -s <svg_file> 
```

# Example
```
> py draw.py -s input\h1.svg
> py draw.py -s input\ava.svg
```

# Output
![image](https://github.com/Tuanpluss02/turtle-svg/assets/82562559/a199cf3d-bfae-4fc6-a0de-a86f7a3c011e)

## License

This script is licensed under the [MIT License](https://opensource.org/license/mit/).