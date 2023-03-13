from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))



import time

# Some global color constants that might be useful
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GRAY = (50, 50, 50)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.1

#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

# Class constructor
	def __init__( self):
		super().__init__()
		self.pause = False

# Some helper methods that make calls to the GUI, allowing us to send updates
# to be displayed.

	def showTangent(self, line, color):
		self.view.addLines(line,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		self.view.clearLines(line)

	def blinkTangent(self,line,color):
		self.showTangent(line,color)
		self.eraseTangent(line)

	def showHull(self, polygon, color):
		self.view.addLines(polygon,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseHull(self,polygon):
		self.view.clearLines(polygon)

	def showText(self,text):
		self.view.displayStatusText(text)

	def get_slope(self, x1, x2, y1, y2):
		return float(y1-y2) / float(x1-x2)			# O(4)

	def is_upper_tangent_single_set(self, set, point1, point2):
		current_slope = self.get_slope(point1.x(), point2.x(), point1.y(), point2.y())								# O(1)
		for i in set:																								# O(n)
			if float(f'{i.y():.11f}') > float(f'{(current_slope * (i.x() - point1.x()) + point1.y()):.11f}'):		# O(1)
				return False																						# ___________
		return True																									# Total: O(n) 

	def is_lower_tangent_single_set(self, set, point1, point2):
		current_slope = self.get_slope(point1.x(), point2.x(), point1.y(), point2.y())								# O(1)
		for i in set:																								# O(n)
			if float(f'{i.y():.11f}') < float(f'{(current_slope * (i.x() - point1.x()) + point1.y()):.11f}'):		# O(1)
				return False																						# ___________
		return True																									# Total: O(n) 

	def find_lower_tangent(self, p, q, leftHull, rightHull):
		line = [p, q]
		left_hull_polygon = [QLineF(leftHull[i], leftHull[(i+1) % len(leftHull)]) for i in range(len(leftHull))]
		right_hull_polygon = [QLineF(rightHull[i], rightHull[(i+1) % len(rightHull)]) for i in range(len(rightHull))]
		self.showHull(left_hull_polygon, GREEN)
		self.showHull(right_hull_polygon, BLUE)
		done = False
		while not done:
			done = True
			if len(leftHull) == 1:
				left_upper_tangent = True
			else:
				left_upper_tangent = self.is_lower_tangent_single_set(leftHull, p, q)
			if len(rightHull) == 1:
				right_upper_tangent = True
			else:
				right_upper_tangent = self.is_lower_tangent_single_set(rightHull, p, q)
			upper_tang = []
			while left_upper_tangent == False:
				r = leftHull[(leftHull.index(p) + 1) % len(leftHull)]
				temp = [r, q]
				self.eraseTangent(upper_tang)
				upper_tang = [QLineF(temp[0], temp[1])]
				self.showTangent(upper_tang, GRAY)
				p = r
				done = False
				left_upper_tangent = self.is_lower_tangent_single_set(leftHull, p, q)
			while right_upper_tangent == False:
				r = rightHull[(rightHull.index(q) - 1) % len(rightHull)]
				temp = [p, r]
				self.eraseTangent(upper_tang)
				upper_tang = [QLineF(temp[0], temp[1])]
				self.showTangent(upper_tang, GRAY)
				q = r
				done = False
				right_upper_tangent = self.is_lower_tangent_single_set(rightHull, p, q)
		self.eraseTangent(upper_tang)
		self.eraseHull(left_hull_polygon)
		self.eraseHull(right_hull_polygon)
		return [p, q]


	def find_upper_tangent(self, p, q, leftHull, rightHull):
		line = [p, q]
		left_hull_polygon = [QLineF(leftHull[i], leftHull[(i+1) % len(leftHull)]) for i in range(len(leftHull))]
		right_hull_polygon = [QLineF(rightHull[i], rightHull[(i+1) % len(rightHull)]) for i in range(len(rightHull))]
		self.showHull(left_hull_polygon, GREEN)
		self.showHull(right_hull_polygon, BLUE)															
		done = False
		while done == False:																			# O(1)
			done = True
			if len(leftHull) == 1:																		# O(1)
				left_upper_tangent = True
			else:
				left_upper_tangent = self.is_upper_tangent_single_set(leftHull, p, q)					# O(n)
			if len(rightHull) == 1:																		# O(1)
				right_upper_tangent = True
			else:
				right_upper_tangent = self.is_upper_tangent_single_set(rightHull, p, q)					# O(n)
			upper_tang = []

		
			while left_upper_tangent == False:															# O(n)
				r = leftHull[(leftHull.index(p) - 1) % len(leftHull)]	
				temp = [r, q]																			# O(1)
				self.eraseTangent(upper_tang)
				upper_tang = [QLineF(temp[0], temp[1])]
				self.showTangent(upper_tang, GRAY)
				p = r																					# O(1)
				done = False
				left_upper_tangent = self.is_upper_tangent_single_set(leftHull, p, q)					# O(n)
			while right_upper_tangent == False:
				r = rightHull[(rightHull.index(q) + 1) % len(rightHull)]								# O(1)
				temp = [p, r]
				self.eraseTangent(upper_tang)
				upper_tang = [QLineF(temp[0], temp[1])]
				self.showTangent(upper_tang, GRAY)
				q = r																					# O(1)
				done = False
				right_upper_tangent = self.is_upper_tangent_single_set(rightHull, p, q)					# O(n)
		self.eraseTangent(upper_tang)
		self.eraseHull(left_hull_polygon)
		self.eraseHull(right_hull_polygon)																# _________
		return [p, q]																					# Total: O( n^2 )

	def combine_hulls(self, leftHull, rightHull):

		if len(leftHull) == 1 and len(rightHull) == 1:												# O(1)
			return [leftHull[0], rightHull[0]]
		p, q = 0, 0
		for i in range(len(leftHull)):																# O(n)
			if leftHull[i].x() > leftHull[p].x():													# O(1)
				p = i
		for i in range(len(rightHull)):																# O(n)
			if rightHull[i].x() < rightHull[q].x():													# O(1)
				q = i
		upper_tangent = self.find_upper_tangent(leftHull[p], rightHull[q], leftHull, rightHull)		# O(n)
		lower_tangent = self.find_lower_tangent(leftHull[p], rightHull[q], leftHull, rightHull)		# O(n)
		combined_hull = []
		current_point = leftHull.index(lower_tangent[0])											# O(1)
		while current_point != leftHull.index(upper_tangent[0]):									# O(n)
			combined_hull.append(leftHull[current_point])											# O(1)
			current_point = ((current_point + 1) % len(leftHull))									# O(1)
		combined_hull.append(upper_tangent[0])														# O(1)
		current_point = rightHull.index(upper_tangent[1])											# O(1)
		while current_point != rightHull.index(lower_tangent[1]):									# O(n)
			combined_hull.append(rightHull[current_point])											# O(1)
			current_point = ((current_point + 1) % len(rightHull))									# O(1)
		combined_hull.append(lower_tangent[1])														# O(1)
		return combined_hull																		#__________
																									# Total: O( n )



	def divide_conquer(self, hull):
		if len(hull) < 2:													# O(1)
			return hull
		leftHull, rightHull = self.divide_hull(hull)						# O(n)
		left_hull = self.divide_conquer(leftHull)							# O( log(n) )
		right_hull = self.divide_conquer(rightHull)							# O( log(n) )
		if left_hull == None:												# O(1)
			return right_hull								
		elif right_hull == None:											# O(1)
			return left_hull
		combined_hull = self.combine_hulls(left_hull, right_hull)           # O(n)
		return combined_hull												#________________
																			# Total: O( nlog(n) )



	def divide_hull(self, hull):
		if len(hull) <= 1:													# O(1)
			return hull														
		else:
			return hull[:int(len(hull)/2)], hull[int(len(hull)/2):]			# O(n)
																			# Total: O(n)


	def compute_hull( self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		t1 = time.time()
		points.sort(key=lambda p: p.x())
		t2 = time.time()

		t3 = time.time()
		divided_conquered_list = self.divide_conquer(points)
		polygon_list_of_points = [QLineF(divided_conquered_list[i], divided_conquered_list[(i+1) % len(divided_conquered_list)]) for i in range(len(divided_conquered_list))]
		t4 = time.time()

		self.showHull(polygon_list_of_points,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))





			# print("\n\n\n\n")
			# print("CURRENT SLOPE: ")
			# print(current_slope)
			# print()
			# print("CURRRENT POINTS [P, Q]:")
			# print(point1)
			# print(point2)
			# print()
			# print()
			# print()
			# print("LEFT SIDE TEST:")
			# print(current_slope * (i.x() - point1.x()) + point1.y())
			# print("Y VALUE: ")
			# print(i.y())
			# print("X-VALUE")
			# print(i.x())
