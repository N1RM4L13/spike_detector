
# Spike Detector

This functionality can be applied in various real-time applications, such as network traffic monitoring, server load balancing, financial market analysis, and more. 




## Features

- Reading Offsets: The program reads message broadcast times from a specified file.
- Interval Calculation: It calculates the intervals between consecutive message times.
- Algorithm Selection: Users can choose between two algorithms for detecting spike periods:
    1. Viterbi Algorithm: Uses dynamic programming to
        find the most probable sequence of states.
    2. Bellman-Ford Algorithm: Uses a shortest-path
        approach to determine the state sequence.
- Parameterization: Users can specify the values for parameters s (scaling factor) and gamma (transition cost).
- Debug Mode: An optional debug mode can be enabled to print detailed diagnostic messages during computation.



## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Run the program

```bash
  python bursts.py [-s S] [-g GAMMA] [-d] (viterbi | trellis) OFFSETS_FILE
```



