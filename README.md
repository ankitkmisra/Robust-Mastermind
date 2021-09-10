# A Robust Mastermind Player

In this project, we used the SAT solving techniques of the Z3 Theorem Prover to design and implement a robust player for the game Mastermind. By attempting to maximize the number of conditions met, this player can perform well even against unreliable adversaries that provide wrong feedback with some small probability. This work was completed as part of CS 228 - Logic for Computer Science.

`mastermind.py` contains the actual implementation of the player. `mastermind-reliable.py` and `mastermind-unreliable.py` are harnesses to test the player with a random game, against reliable and unreliable feedback respectively.
