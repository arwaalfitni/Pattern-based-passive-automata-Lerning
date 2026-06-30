# Pattern-based-passive-automata-Lerning

## 1. Project Overview

This project implements passive automata learning techniques for inferring finite-state models from traces. It supports several learning strategies, including pattern-based EDSM, DFASAT-based learning, classical EDSM, and variants that combine patterns with SAT solving. The workflow reads a reference automaton from the reference_automata folder, generates training and testing traces, learns a model, evaluates the result, and writes statistics and output files into the outputs directory.

The repository is designed for experiments on benchmark systems such as bluetooth, TCP, openSSL, coffeemachine, and several randomly generated systems. It is intended for researchers and students working on passive automata learning and model inference.

## 2. How to Run the Project

### Prerequisites

Make sure you have Python installed and that you are running the commands from the project root.

### Install uv

If [uv](https://docs.astral.sh/uv/getting-started/installation/) is not installed yet, install it with:

```bash
pip install uv
```

### Install dependencies

From the project root, install the project dependencies with:

```bash
uv sync
```

### Run the main script

The main entry point is:

```
uv run main.py  <seed> <Learning-algorithm> <system-name> <trial-number> <learning-walks-size> <number-of-traces> <coverage> 
```

A simple example is:

```bash
uv run main.py  5  BiasedEDSM1  Random1 2 3 NoCover

# Another example is:
uv run main.py  1185 DFASAT TextEditor 0 5 TransitionCover

```

The output statistics file is written to the outputs folder. For example, the previous command produces a file similar to:

```text
/outputs/Random1/NoCover/BiasedEDSM1/Random1_2_3_BiasedEDSM1_statistics.txt
```

## 3. Running Options

The command-line arguments are:

| Parameter name       | Allowed values | Explanation |
|----------------------|----------------|-------------|
| seed                 | Any integer value | Used for random functions |
| Learning algorithm   | `BiasedEDSM1`, `BiasedSAT1`, `DFASAT`, `classicalEDSM`, `BiasedSATPAT1`, `BiasedSiccoSAT`, `BiasedSiccoSATPAT` | Selects the learning strategy |
| system-name          | `bluetooth`, `TCP`, `openSSL`, `coffeemachine`, `Random1`, `Random2`, `Random3`, `Random4`, `Random5`, `Random6` | Target benchmark system |
| trial-number         | Any integer value | Distinguishes between different trials |
| learning_walks_size  | Any integer value | Number of traces used for training |
| coverage             | `NoCover`, `StateCover`, `TransitionCover` | Trace coverage strategy |

If you want to add another system, place its reference automaton in the `reference_automata` folder as a DOT file and mark the initial state using `isInitial=True`.

## 4. Implementation and Testing

The project is driven by `main.py`, which parses command-line arguments, loads a reference automaton from `reference_automata`, generates training and test traces, and builds an augmented prefix tree acceptor (APTA). Learning strategies are implemented in the `Learners` package, including classical EDSM, pattern-based EDSM, and SAT-based DFASAT, while evaluation logic in `evaluation.py` measures inference quality using precision, recall, accuracy, and balanced classification rate.

Testing is handled with Python `unittest` and organized under `tests/`. The suite covers core components such as graph operations, trace generation, pattern exploration, and learner compatibility checks, so the implementation can be validated by running the repository-wide test discovery command.

## 5. Running the Tests

To run the unit tests in this repository, use:

```bash
uv run -m unittest discover -v -s ./tests -p "*.py"
```

You can also use the provided make target:

```bash
make test
```

## 6. Makefile Commands

The repository includes a Makefile with the following useful commands:

- make help: shows the available targets.
- make venv: creates the virtual environment and installs dependencies using uv sync.
- make test: runs the unit tests.
- make clean: removes the virtual environment and temporary files.
- make run <args>: runs the main script with the supplied arguments.
- make run-help: shows help for the main script.
- make run-all: runs the main script for several predefined benchmark systems.

Example:

```bash
make run 8965 DFASAT Random1 0 0 TransitionCover
```

## 7. Acknowledgements

This work was carried out by:

- Student: Arwa A Alfitni <aaalfitni1@sheffield.ac.uk>
- Supervisor 1: k.bogdanov@sheffield.ac.uk
- Supervisor 2: n.walkinshaw@sheffield.ac.uk
