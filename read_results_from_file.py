import csv


def read_results_from_file(file_name):
    results = []

    with open(file_name, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            results.append([int(score) for score in row])

    return results


def calculate_total_scores(results):
    total_scores = [0] * len(results[0])

    for result in results:
        for i, score in enumerate(result):
            total_scores[i] += score

    return total_scores


def main():
    file_name = "results.txt"
    results = read_results_from_file(file_name)
    total_scores = calculate_total_scores(results)

    for i, score in enumerate(total_scores):
        print(f"Player {i + 1}'s total score: {score}")

    max_score = max(total_scores)
    winners = [i for i, score in enumerate(total_scores) if score == max_score]

    if len(winners) == 1:
        print(
            f"\nThe winner is Player {winners[0] + 1} with a total score of {max_score}"
        )
    else:
        tied_players = ", ".join([f"Player {i + 1}" for i in winners])
        print(
            f"\nThere is a tie between {tied_players} with a total score of {max_score}"
        )


if __name__ == "__main__":
    main()
