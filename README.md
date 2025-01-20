# BART Task Bayesian Model
This project implements a modified version of the Balloon Analogue Risk Task (BART) to study how people make decisions under uncertainty and whether human intuition reflects Bayesian inference. The study explores risk assessment through a game-based interface where participants must learn underlying probability distributions to maximize their score.

## Project Overview
The BART task presents participants with balloons that can be pumped up to earn points, but may pop at any time. This implementation adds Bayesian modeling to analyze risk-taking behavior and includes three key experiments:

1. Loss Aversion - Testing how displaying or hiding potential losses affects risk behavior
2. Standardized Risk Assessment - Comparing human performance against Bayesian models
3. Hypothesis Space - Examining how prior knowledge of probability distributions impacts decision-making

## Project Writeup
[9_66_Final_Project.pdf](https://github.com/user-attachments/files/18482738/9_66_Final_Project.pdf)

## Setup

### Requirements
- Python 3.5+
- PyGame

### Installation
```bash
pip install pygame
```

## Running Experiments

### Experiment 1: Loss Aversion
Test with visible losses:
```bash
python3 game.py --name="NAME" --gender="N" --age="0" --balloons=10 --course=0 --exp=1 --lossAversion=True
```

Test without visible losses:
```bash
python3 game.py --name="NAME" --gender="N" --age="0" --balloons=10 --course=0 --exp=1 --lossAversion=False
```

### Experiment 2: Standardized Distribution
```bash
python3 game.py --name="NAME" --gender="N" --age="0" --balloons=10 --course=0 --exp=2 --lossAversion=True --dist="GAUSSIAN 10 4 2" --obs="1,5,5,4,1,6,7,5,4,7"
```

### Experiment 3: Hypothesis Space
With prior distribution knowledge:
```bash
python3 game.py --name="NAME" --gender="N" --age="0" --balloons=10 --course=0 --exp=2 --lossAversion=True --seenGraphs=True
```

Without prior distribution knowledge:
```bash
python3 game.py --name="NAME" --gender="N" --age="0" --balloons=10 --course=0 --exp=2 --lossAversion=True --seenGraphs=False
```

## Results

Our experiments found that:
- Loss aversion had an insignificant effect on participants' scores
- A Bayesian model with horizon=2 and decay rate=0 best matched human gameplay
- Prior knowledge of probability distributions had minimal impact on performance

For detailed findings, please see the [full project writeup](9_66_Final_Project.pdf).

## Project Paper

The complete research paper detailing methodology, experiments, and findings is available in [9_66_Final_Project.pdf](9_66_Final_Project.pdf).

## Authors
- Penny Brant (pennyb@mit.edu)
- Caroline Cunningham (ccunning@mit.edu)

MIT Course 9.66 (Computational Cognitive Science) Final Project
