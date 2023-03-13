#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import random

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1

class GeneSequencing:

	def __init__( self ):
		pass

# This is the method called by the GUI.  _seq1_ and _seq2_ are two sequences to be aligned, _banded_ is a boolean that tells
# you whether you should compute a banded alignment or full alignment, and _align_length_ tells you
# how many base pairs to use in computing the alignment

	def find_path_and_strings(self, alignment_matrix, seq1, seq2):
		current_row = len(alignment_matrix) - 1
		current_column = len(alignment_matrix[0]) - 1
		while current_column > 1 or current_row > 1:
			current_value = alignment_matrix[current_row][current_column]
			if current_value - INDEL == alignment_matrix[current_row][current_column - 1]:
				# INSERT FROM THE LEFT
				print("INSERT FROM LEFT")
				current_row -= 1
			elif current_value - INDEL == alignment_matrix[current_row - 1][current_column]:
				# INSERT FROM THE TOP
				print("INSERT FROM TOP")
				current_column -= 1
			else:
				if current_value - MATCH == alignment_matrix[current_row - 1][current_column - 1]:
					# MATCH DIAGONALLY
					print("MATCH DIAGONALLY")
					current_column -= 1
					current_row -= 1
				else:
					# SUBSTITUTION DIAGONALLY
					print("SUBSTITUTION DIAGONALLY")
					current_row -= 1
					current_column -= 1
		

	def unbanded_alignment(self, seq1, seq2, align_length):
		self.MaxCharactersToAlign = align_length
		seq1 = seq1[:align_length]
		seq2 = seq2[:align_length]
		self.alignment_matrix = []
		sequence_matrix = []
		for i in range(len(seq2) + 2):
			added_matrix = []
			for j in range(len(seq1) + 2):
				added_matrix.append(0)
			self.alignment_matrix.append(added_matrix)
			sequence_matrix.append(added_matrix)

		for row in range(len(seq1) + 2):
			if row > 1:
				self.alignment_matrix[0][row] = seq1[row - 2]
				self.alignment_matrix[1][row] = self.alignment_matrix[1][row - 1] + INDEL
		for column in range(len(seq2) + 2):
			if column > 1:
				self.alignment_matrix[column][0] = seq2[column - 2]
				self.alignment_matrix[column][1] = self.alignment_matrix[column - 1][1] + INDEL
			
		for row in range(2, len(seq2) + 2):
			for column in range(2, len(seq1) + 2):
					
				left = self.alignment_matrix[row - 1][column] + INDEL
				top = self.alignment_matrix[row][column - 1] + INDEL
				diagonal = self.alignment_matrix[row - 1][column - 1]
				if self.alignment_matrix[0][column] == self.alignment_matrix[row][0]:
					diagonal += MATCH
				else:
					diagonal += SUB
				if left <= diagonal and left <= top:
					self.alignment_matrix[row][column] = left
				elif top <= diagonal and top <= left:
					self.alignment_matrix[row][column] = top
				else:
					self.alignment_matrix[row][column] = diagonal

		print("FINAL MATRIX")
		for i in self.alignment_matrix:
			print(i)

		self.find_path_and_strings(self.alignment_matrix, seq1, seq2)
		
		return self.alignment_matrix, self.alignment_matrix[-1][-1]



	def banded_alignment( self, seq1, seq2, align_length):
		self.MaxCharactersToAlign = align_length
		seq1 = seq1[:align_length]
		seq2 = seq2[:align_length]
		self.alignment_matrix = []
		sequence_matrix = []
		max_indel = []
		for i in range(len(seq2) + 2):
			added_matrix = []
			added_2 = []
			for j in range(len(seq1) + 2):
				added_matrix.append(0)
				added_2.append(0)
			self.alignment_matrix.append(added_matrix)
			sequence_matrix.append(added_matrix)
			max_indel.append(added_2)

		for row in range(len(seq1) + 2):
			if row > 1:
				self.alignment_matrix[0][row] = seq1[row - 2]
				max_indel[1][row] = max_indel[1][row - 1] + 1
				if max_indel[1][row] <= MAXINDELS:
					self.alignment_matrix[1][row] = self.alignment_matrix[1][row - 1] + INDEL
				else:
					self.alignment_matrix[1][row] = float('inf')

		for column in range(len(seq2) + 2):
			if column > 1:
				self.alignment_matrix[column][0] = seq2[column - 2]
				max_indel[column][1] = max_indel[column - 1][1] + 1
				print(max_indel[column][1])
				print(MAXINDELS)
				if max_indel[column][1] <= MAXINDELS:
					self.alignment_matrix[column][1] = self.alignment_matrix[column - 1][1] + INDEL
				else:
					self.alignment_matrix[column][1] = float('inf')


		for row in range(2, len(seq2) + 2):
			for column in range(2, len(seq1) + 2):
				print(row, column)
				left = self.alignment_matrix[row - 1][column] + INDEL
				top = self.alignment_matrix[row][column - 1] + INDEL
				diagonal = self.alignment_matrix[row - 1][column - 1]
				if self.alignment_matrix[0][column] == self.alignment_matrix[row][0]:
					diagonal += MATCH
				else:
					diagonal += SUB

				if left <= diagonal and left <= top:
					max_indel[row][column] = max_indel[row - 1][column] + 1
					if max_indel[row][column] <= MAXINDELS:
						self.alignment_matrix[row][column] = left
					else:
						self.alignment_matrix[row][column] = float('inf')
				elif top <= diagonal and top <= left:
					max_indel[row][column] = max_indel[row][column - 1] + 1
					if max_indel[row][column] <= MAXINDELS:
						self.alignment_matrix[row][column] = top
					else:
						self.alignment_matrix[row][column] = float('inf')
				else:
					self.alignment_matrix[row][column] = diagonal

		print("FINAL MATRIX")
		for i in self.alignment_matrix:
			print(i)
		return self.alignment_matrix, self.alignment_matrix[-1][-1]

	def align( self, seq1, seq2, banded, align_length):

		self.banded = banded
		self.MaxCharactersToAlign = align_length
		if banded == True:
			am, s = self.banded_alignment(seq1, seq2, self.MaxCharactersToAlign)
		else:
			am, s = self.unbanded_alignment(seq1, seq2, self.MaxCharactersToAlign)
	
		score = s
		alignment1 = 'abc-easy  DEBUG:({} chars,align_len={}{})'.format(
			len(seq1), align_length, ',BANDED' if banded else '')
		alignment2 = 'as-123--  DEBUG:({} chars,align_len={}{})'.format(
			len(seq2), align_length, ',BANDED' if banded else '')
		

###################################################################################################

		return {'align_cost':score, 'seqi_first100':alignment1, 'seqj_first100':alignment2}
