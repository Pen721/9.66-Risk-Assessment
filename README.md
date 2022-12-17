# 9.66-FInal-Project-
Caroline and I are studying how we computationally asses and act on risk!

# Set up 
make a conda environemnt with python 3.5 

# Run Game
To run the game, run this in the terminal
```
python3 game.py --name="penroline" --gender="F" --age="19" --balloons=10 --course=6
```

```
conda create --name YOUR_ENV_NAME_HERE python=3.5
conda activate YOUR_ENV_NAME_HERE
pip install pygame
python game.py
```

# Experiment 1 - Loss Aversion
```
python3 game.py --name="NAME" --gender="N" --age="20" --balloons=10 --course=6 --lossAversion=True
```

```
python3 game.py --name="NAME" --gender="N" --age="20" --balloons=10 --course=6 --lossAversion=False
```

# Experiment 2 - Same Distribution
```
python3 game.py --name="NAME" --gender="N" --age="20" --balloons=10 --course=6 --lossAversion=False --dist="GAUSSIAN 10 4 2" --obs="1,5,5,4,1,6,7,5,4,7"
```

# Experiment 3 - Hypothesis Space
```
python3 game.py --name="NAME" --gender="N" --age="20" --balloons=10 --course=6 --lossAversion=True --constrainedHypothesis=True
```