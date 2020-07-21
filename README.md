# About
This is the original code of my master thesis in 2019. It finds some Coxeter quotients of (very small) knots, in particular, knots with reasonable diagrams of bridge index at most 3, or 4 if you are very patient.

# Using Natively
If you have python and numpy installed you can just run

    python interactive.py

to enter interactive mode, which lets you enter a knot and tells you whether it found any Coxeter quotients.

# Using with Docker
In case you don't have python or you don't want to pollute it with numpy, you can also run interactive mode in a Docker container. To do this, first build a numpy image as follows.

    docker build -t coxeter_numpy .

Note the dot at the end. This produces a new Docker image which we can now use to execute interactive mode. Make sure to navigate into a clone and execute the following.

## On Linux/Mac

    docker run -it -v $(pwd):/src coxeter_numpy python interactive.py

## On Windows

    docker run -it -v %cd%:/src coxeter_numpy python interactive.py