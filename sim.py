import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense
from operator import attrgetter


class Inhabitant:
    def __init__(self):
        self.model = self.create_brain()
        self.position = np.array(
            [random.uniform(0, world_size), random.uniform(0, world_size)]
        )

    def create_brain(self):
        model = Sequential()
        model.add(Dense(8, input_dim=2, activation="relu"))
        model.add(Dense(2, activation="tanh"))
        return model

    def move(self):
        move_vector = self.model.predict(self.position.reshape(1, -1))[0] * max_movement
        self.position += move_vector
        self.position = np.clip(self.position, 0, world_size)


class EvolutionSimulation:
    def __init__(
        self,
        world_size,
        max_movement,
        num_inhabitants,
        num_generations,
        num_offspring,
        top_performers,
    ):
        self.world_size = world_size
        self.max_movement = max_movement
        self.num_inhabitants = num_inhabitants
        self.num_generations = num_generations
        self.num_offspring = num_offspring
        self.top_performers = top_performers
        self.population = [Inhabitant() for _ in range(num_inhabitants)]

    def fitness(self, inhabitant):
        return -inhabitant.position[
            0
        ]  # Negative x-coordinate represents staying closer to the left side

    def select_parents(self):
        sorted_population = sorted(self.population, key=self.fitness, reverse=True)
        return sorted_population[: self.top_performers]

    def breed(self, parent1, parent2):
        child = Inhabitant()
        child.model.set_weights(
            [
                (w1 + w2) / 2
                for w1, w2 in zip(
                    parent1.model.get_weights(), parent2.model.get_weights()
                )
            ]
        )
        return child

    def run_simulation(self):
        for generation in range(self.num_generations):
            for inhabitant in self.population:
                inhabitant.move()

            parents = self.select_parents()
            offspring = [
                self.breed(*random.sample(parents, 2))
                for _ in range(self.num_offspring)
            ]

            random.shuffle(offspring)
            self.population = parents + offspring[: self.num_inhabitants - len(parents)]

            print(
                f"Generation {generation + 1} complete. Average x-coordinate: {-np.mean([self.fitness(inhabitant) for inhabitant in self.population]):.2f}"
            )


if __name__ == "__main__":
    world_size = 100
    max_movement = 5
    num_inhabitants = 100
    num_generations = 200
    num_offspring = 150
    top_performers = 50

    simulation = EvolutionSimulation(
        world_size,
        max_movement,
        num_inhabitants,
        num_generations,
        num_offspring,
        top_performers,
    )
    simulation.run_simulation()
