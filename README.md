# 9.66-FInal-Project-
Using Bayesian models to approxiamte risk in BART tasks

# Set up 
Python 3.5 with Pygame

```
pip install pygame
```

# Experiment 1 - Loss Aversion
```
python3 game.py --name="NAME" --gender="N" --age="0" --balloons=10 --course=0 --exp=1 --lossAversion=True
```

```
python3 game.py --name="NAME" --gender="N" --age="0" --balloons=10 --course=0 --exp=1 --lossAversion=False
```

# Experiment 2 - Standardize Distribution for Risk Measurement
```
python3 game.py --name="NAME" --gender="N" --age="0" --balloons=10 --course=0 --exp=2 --lossAversion=True --dist="GAUSSIAN 10 4 2" --obs="1,5,5,4,1,6,7,5,4,7"
```

# Experiment 3 - Hypothesis Space
```
python3 game.py --name="NAME" --gender="N" --age="0" --balloons=10 --course=0 --exp=2 --lossAversion=True --seenGraphs=True

```
python3 game.py --name="NAME" --gender="N" --age="0" --balloons=10 --course=0 --exp=2 --lossAversion=True --seenGraphs=False
```
