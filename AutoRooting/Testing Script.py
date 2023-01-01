class A1:
	def Method(self):
		print("A1 Method")

class A2:
	def Method(self):
		print("A2 Method")

class A3:
	def Method(self):
		print("A3 Method")

class B(A1, A2, A3):
	pass

ObjectB = B()
print(B.__bases__)