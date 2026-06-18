from backend.services.score_generator import generate_score


def test_generate_score():

    midi_file = "data/midi/melody.mid"

    output = "data/scores/result.musicxml"

    result = generate_score(
        midi_file,
        output
    )

    print(result)


if __name__ == "__main__":
    test_generate_score()