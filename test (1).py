from Pyro4 import expose
import random

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers


    def solve(self):

        n = self.read_input()
        step = n / len(self.workers)

        # map
        mapped = []
        for i in xrange(0, len(self.workers)):
            mapped.append(self.workers[i].gogo(i * step, i * step + step))



        # reduce
        reduced = self.myreduce(mapped)


        # output
        self.write_output(reduced)



    @staticmethod
    @expose
    def myreduce(mapped):
        output = []
        for x in mapped:
            output.append(x.value)
        return output

    @staticmethod
    @expose
    def gogo(x_s, x_e):
        res = []
        for i in range(x_s, x_e):
            if Solver.solovay_strassen(i):
                res.append(i)
        return res

    def read_input(self):
        f = open(self.input_file_name, 'r')
        line = f.readline()
        f.close()
        return int(line)

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()


    @staticmethod
    @expose
    def solovay_strassen(n):
        if (n == 2) or (n == 3):
            return True
        elif (n % 2 == 0) or (n == 0) or (n == 1):
            return False

        for _ in range(8):  # confidence t=8
            a = random.randrange(2, n - 1)
            at = a
            nt = n
            while at != 0 and nt != 0:
                if at > nt:
                    at %= nt
                else:
                    nt %= at

            gcd = at + nt
            if(gcd > 1):
                return False
            
            def legendre(a, p):
		        if (a == 0) or (a == 1):
			        return a

		        if a % 2 == 0:
		        	r = legendre(a / 2, p)
		        	if p * p - 1 & 8 != 0:
		        		r *= -1

		        else:
		        	r = legendre(p % a, a)
		        	if (a - 1) * (p - 1) & 4 != 0:
		        		r *= -1

		        return r

            pown=(n-1)/2
            powres=pow(a, pown, n)
            res=legendre(a, n)
            if(powres != powres):
            	return False
        return True