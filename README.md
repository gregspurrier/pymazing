pymazing
========
Pymazing is a terminal maze generator written as an exercise in learning
Python. It is a work in progress.

Feedback on how to make the code more Pythonic is welcome and appreciated.

## Usage
````
./bin/pymazing [hexagon|square]
````

The command line argument determines the shape of the tiles that make
up the maze. If no argument is given, the default is `square`.

A random maze will be drawn, taking up as much of the terminal screen
as possible. Press any key to exit.

## Testing
Testing requires hypothesis.

````
pip3 install hypothesis
python3 -m unittest discover
````

## License
Pymazing is Copyright (C) 2019 Greg Spurrier. It is distributed under the terms
of the MIT License. See [LICENSE.txt](LICENSE.txt) for the details.
