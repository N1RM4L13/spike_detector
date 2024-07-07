import sys
import argparse
import math
from collections import deque

def exponential_distribution(x, lam):
    return lam * math.exp(-lam * x)

def parse_offsets_file(filename):
    with open(filename, 'r') as f:
        times = [float(line.strip()) for line in f]
    return times

def calculate_intervals(times):
    return [times[i + 1] - times[i] for i in range(len(times) - 1)]

def viterbi_algorithm(intervals, s=2, gamma=1, debug=False):
    n = len(intervals)
    k = math.ceil(math.log(n, s))
    C = [[float('inf')] * (k + 1) for _ in range(n + 1)]
    P = [[0] * (n + 1) for _ in range(k + 1)]
    
    C[0][0] = 0

    for t in range(1, n + 1):
        for j in range(k + 1):
            min_cost = float('inf')
            for l in range(k + 1):
                cost = -math.log(exponential_distribution(intervals[t - 1], s**j)) + C[t - 1][l] + (gamma * (j - l) if j > l else 0)
                if cost < min_cost:
                    min_cost = cost
                    P[j][t] = l
            C[t][j] = min_cost
        if debug:
            print([round(C[t][j], 2) for j in range(k + 1)])

    S = [0] * (n + 1)
    S[n] = C[n].index(min(C[n]))
    for t in range(n, 0, -1):
        S[t - 1] = P[S[t]][t]
    
    return S

def bellman_ford_algorithm(intervals, s=2, gamma=1, debug=False):
    n = len(intervals)
    k = math.ceil(math.log(n, s))
    C = [[float('inf')] * (k + 1) for _ in range(n + 1)]
    P = [[0] * (n + 1) for _ in range(k + 1)]
    
    C[0][0] = 0

    for t in range(1, n + 1):
        for j in range(k + 1):
            min_cost = float('inf')
            for l in range(k + 1):
                cost = -math.log(exponential_distribution(intervals[t - 1], s**j)) + C[t - 1][l] + (gamma * (j - l) if j > l else 0)
                if cost < min_cost:
                    min_cost = cost
                    P[j][t] = l
            C[t][j] = min_cost
            if debug:
                print(f"({t}, {j}) {round(C[t][j], 2)} -> {round(min_cost, 2)} from ({t-1}, {P[j][t]}) {round(C[t-1][P[j][t]], 2)} + {round(cost, 2)}")
    
    S = [0] * (n + 1)
    S[n] = C[n].index(min(C[n]))
    for t in range(n, 0, -1):
        S[t - 1] = P[S[t]][t]
    
    return S

def main():
    parser = argparse.ArgumentParser(description='Identify the activity periods of a system using Viterbi or Bellman-Ford algorithm.')
    parser.add_argument('-s', type=float, default=2, help='Value of the s parameter of the algorithm.')
    parser.add_argument('-g', '--gamma', type=float, default=1, help='Value of the gamma parameter of the algorithm.')
    parser.add_argument('-d', '--debug', action='store_true', help='Print diagnostic messages.')
    parser.add_argument('algorithm', choices=['viterbi', 'trellis'], help='Algorithm to use: viterbi or trellis.')
    parser.add_argument('offsets_file', help='File containing the broadcast times of the messages.')

    args = parser.parse_args()

    times = parse_offsets_file(args.offsets_file)
    intervals = calculate_intervals(times)

    if args.algorithm == 'viterbi':
        states = viterbi_algorithm(intervals, s=args.s, gamma=args.gamma, debug=args.debug)
    else:
        states = bellman_ford_algorithm(intervals, s=args.s, gamma=args.gamma, debug=args.debug)

    start_time = 0
    for i in range(1, len(states)):
        if states[i] != states[i - 1]:
            print(f"{states[i - 1]} [{start_time} {times[i - 1]})")
            start_time = times[i - 1]
    print(f"{states[-1]} [{start_time} {times[-1]})")

if __name__ == '__main__':
    main()
