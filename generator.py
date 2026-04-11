from model import Puzzle, EMPTY_STR
def put(word, puzzle, rrr, ccc):
	if ccc<0:
		puzzle.expand_left(-ccc)
		ccc = 0
	_, width = puzzle.grid.shape
	if ccc+len(word)>width:
		puzzle.expand_right(ccc+len(word)-width)
	counter = 0
	for idx, char in enumerate(word):
		if puzzle.grid[rrr, ccc+idx]==EMPTY_STR:
			puzzle.grid[rrr, ccc+idx] = char
		elif puzzle.grid[rrr, ccc+idx]==char:
			counter += 1
		else:
			return False
	return counter!=len(word)
class Propagater:
	def __init__(self, print_interval):
		self.print_interval = print_interval
	def __call__(self, puzzle, words_to_add_desc, known_puzzles=[]):
		if len(words_to_add_desc):
			word = words_to_add_desc[0]
			for offset, joint in enumerate(word):
				for transpose in [False, True]:
					for rrr, row in enumerate(puzzle.grid.transpose() if transpose else puzzle.grid):
						for ccc, space in enumerate(row):
							if joint==space:
								kid = puzzle.copy(transpose)
								if put(word, kid, rrr, ccc-offset) and kid.is_mece(easy_mode=True) and (kid not in known_puzzles):
									known_puzzles.append(kid)
									if self.print_interval and len(known_puzzles)%self.print_interval==0:
										print("# Known Puzzles: %d" % len(known_puzzles))
									yield from self.__call__(kid, words_to_add_desc[1:], known_puzzles)
		elif puzzle.is_mece():
			yield puzzle
def generate(words_in_desending_order_of_length, clues_corresponding_to_words, max_w, print_interval):
	yield from Propagater(print_interval)(
		puzzle = Puzzle(
			grid = words_in_desending_order_of_length[0],
			all_words = words_in_desending_order_of_length,
			all_clues = clues_corresponding_to_words,
			max_w = max_w,
		),
		words_to_add_desc = words_in_desending_order_of_length[1:],
	)