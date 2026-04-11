import numpy as np
EMPTY_STR = " "
def empty_matrix(height, width):
	return np.array(
		[
			[EMPTY_STR for j in range(width)]
			for i in range(height)
		]
	)
def find(word, row):
	for ccc, _ in enumerate(row):
		for offset, char in enumerate(word):
			if row[ccc+offset]!=char:
				break
		else:
			if ccc+len(word)==len(row) or row[ccc+len(word)]==EMPTY_STR:
				return ccc
	raise len(row)

class Puzzle:
	def __init__(self, grid, all_words, all_clues, max_w):
		self.grid = np.array(
			[[char for char in grid]] if isinstance(grid, str)
			else grid
		)
		self.db = np.array(
			[
				(word, desc, *self.grid.shape, False)
				for word, desc in zip(all_words, all_clues)
			],
			dtype = [
				("words", "U%d" % max_w),
				("clues", object),
				("addressy", "i4"),
				("addressx", "i4"),
				("transposed", bool),
			]
		)
		self.max_w = max_w
	def __str__(self):
		h, w = self.grid.shape
		return f"{h}x{w} Crossword Puzzle:\n{'\n'.join(
			[''.join(row) for row in self.grid]
		)}'\n'{self.db.__str__()}"
	def __eq__(self, other):
		return self.grid.shape==other.grid.shape and (self.grid==other.grid).all()
	def copy(self, transpose=False):
		return Puzzle(
			[
				[space for space in row]
				for row in (self.grid.transpose() if transpose else self.grid)
			],
			self.db["words"],
			self.db["clues"],
			self.max_w,
		)
	def expand_left(self, cols):
		self.grid = np.hstack((
			empty_matrix(len(self.grid), cols),
			self.grid
		))
	def expand_right(self, cols):
		self.grid = np.hstack((
			self.grid,
			empty_matrix(len(self.grid), cols)
		))
	def is_mece(self, easy_mode=False):
		self.db["addressy"], self.db["addressx"] = self.grid.shape
		for transposed in [False, True]:
			grid = self.grid.transpose() if transposed else self.grid
			_, width = grid.shape
			if width>self.max_w:
				return False
			for rrr, row in enumerate(grid):
				for word in "".join(row).split(EMPTY_STR):
					if len(word)<2:
						pass
					elif word in self.db["words"]:
						if not easy_mode:
							mask = self.db["words"]==word
							if transposed:
								self.db["addressy"][mask] = find(word, row)
								self.db["addressx"][mask] = rrr
							else:
								self.db["addressy"][mask] = rrr
								self.db["addressx"][mask] = find(word, row)
							self.db["transposed"][mask] = transposed
					else:
						return False
		height, width = self.grid.shape
		return easy_mode or (self.db["addressx"]!=height).all() and (self.db["addressy"]!=width).all()
	
class Clue:
	def __init__(self, number:int, text:str):
		self.number = number
		self.text = text
	
class PuzzlePropertyManager:
	def __init__(self, static_puzzle):
		_, width = static_puzzle.grid.shape
		def key(arg):
			rrr, ccc = arg
			return ccc + rrr*width
		self._address_list =  sorted(
			set(
				[
					(y, x) for y, x in zip(static_puzzle.db["addressy"], static_puzzle.db["addressx"])
				]
			), key = key,
		)
		self.filtered = {
			transposed: static_puzzle.db[static_puzzle.db["transposed"]==transposed]
			for transposed in (False, True)
		}
	def address2num(self, row_idx: int, col_idx: int) -> int | None:
			for num, (rrr, ccc) in enumerate(self._address_list):
				if row_idx==rrr and col_idx==ccc:
					return num+1
			return None
	def get_clues(self, transposed=False):
		return [
			Clue(self.address2num(rrr, ccc),  text)
			for rrr, ccc in self._address_list
			for text in self.filtered[transposed]["clues"][
				np.logical_and(
					self.filtered[transposed]["addressy"]==rrr,
					self.filtered[transposed]["addressx"]==ccc,
				)
			]
		]
	def __str__(self):
		return "\n".join(
			[f"{'Down' if transposed else 'Across'}: {self.get_clues(transposed)}" for transposed in (False, True)]
		)
