from generator import generate
import random, csv

def __read_and_sort(fileobj):
    def key(pair):
        word, _ = pair
        return len(word)
    vocabs = sorted(csv.reader(fileobj), key=key, reverse=True)
    words, descs = zip(*vocabs)
    if len(words)==len(set(words)):
        return words, descs
    else:
        raise Exception("File seems to have duplicated words!!!")

def pick_puzzles(fileobj, grid_size_leq, stop_picking_at, random_seed, print_interval):
	random.seed(random_seed)
	puzzles = []
	sorted_words, sorted_descs = __read_and_sort(fileobj)
	for idx, puzzle in enumerate(
		generate(
			words_in_desending_order_of_length = sorted_words,
			clues_corresponding_to_words = sorted_descs,
			max_w = grid_size_leq,
            print_interval = print_interval,
		)
	):
		if idx<stop_picking_at:
			puzzles.append(puzzle)
		else:
			random.shuffle(puzzles)
			return puzzles
	raise Exception(f"Required: {stop_picking_at} variants > Generated: {len(puzzles)} puzzles")