from pulp import *
import json

class lp_class:
    def __init__(self,data):
        self.message = {}
        self.message["code"] = 0
        self.message["message"] = "None"
        self.data = data
        
    # Check Matrix/Vector Lengths
    def check(self):
        # Check objective
        if "c" not in self.data:
            self.message["message"] = "Missing 'c' vector"
            return False
        if "r" not in self.data:
            self.data["r"] = 0    
        for n in self.data["c"]:
            if not isinstance(n, (int, long, float, complex)):
                self.message["message"] = "Non-numeric value found in 'c' vector"
                return False
        if not isinstance(self.data["r"], (int, long, float, complex)):
            self.message["message"] = "Non-numeric 'r' value found"
            return False

        # Check inequalities
        if "b" not in self.data:
            self.message["message"] = "Missing 'b' vector"
            return False
        if "A" not in self.data:
            self.message["message"] = "Missing 'A' matrix"
            return False           
        if( len(self.data["A"]) != len(self.data["b"]) ):
            self.message["message"] = "Lengths of 'A' and 'b' do not match"
            return False
        for n in self.data["b"]:
            if not isinstance(n, (int, long, float, complex)):
                self.message["message"] = "Non-numeric value found in 'b' vector"
                return False        
        for ls in self.data["A"]:
            if( len(ls) != len(self.data["c"]) ):
                self.message["message"] = "Number of variables in 'A' and 'c' do not match"
                return False
            for n in ls:
                if not isinstance(n, (int, long, float, complex)):
                    self.message["message"] = "Non-numeric value found in 'A' matrix"
                    return False  

        # Check equalities
        if "d" not in self.data:
            self.message["message"] = "Missing 'd' vector"
            return False
        if "E" not in self.data:
            self.message["message"] = "Missing 'E' matrix"
            return False           
        if( len(self.data["E"]) != len(self.data["d"]) ):
            self.message["message"] = "Lengths of 'E' and 'd' do not match"
            return False
        for n in self.data["d"]:
            if not isinstance(n, (int, long, float, complex)):
                self.message["message"] = "Non-numeric value found in 'd' vector"
                return False        
        for ls in self.data["E"]:
            if( len(ls) != len(self.data["c"]) ):
                self.message["message"] = "Number of variables in 'E' and 'c' do not match"
                return False
            for n in ls:
                if not isinstance(n, (int, long, float, complex)):
                    self.message["message"] = "Non-numeric value found in 'E' matrix"
                    return False

        # Check bounds and types
        if "bounds" not in self.data:
            self.data["bounds"] = []
        for ls in self.data["bounds"]:
            #if len(ls) < 2:
            #    return False
            if (ls[0] != "Default") and (not isinstance(ls[0], (int)) or ls[0] >= len(self.data["c"])):
                self.message["message"] = "Value in 'bounds' is not a valid index"
                return False
            for n in ls[1:]:
                if not isinstance(n, (int, long, float, complex)) and n != "None":
                    self.message["message"] = "Non-numeric value found in 'bounds'"
                    return False
            if len(ls) >= 3 and ls[1] != "None" and ls[2] != "None":
                if ls[1] > ls[2]:
                    self.message["message"] = "Lower bound is greater than upper bound"
                    return False
            
        if "integer" not in self.data:
            self.data["integer"] = []
        for n in self.data["integer"]:
            if not isinstance(n, (int)) or n >= len(self.data["c"]):
                self.message["message"] = "Value in 'int' is not a valid index"
                return False             
        if "binary" not in self.data:
            self.data["binary"] = []               
        for n in self.data["binary"]:
            if not isinstance(n, (int)) or n >= len(self.data["c"]):
                self.message["message"] = "Value in 'binary' is not a valid index"
                return False               

        return True
    # Solve LP and return solution
    def solve(self):
        prob = LpProblem("LP", LpMinimize)
        numV = len(self.data["c"])
        indices = range(numV)
        # Variable List
        # Use None for +/- Infinity, i.e. z <= 0 -> LpVariable("z", None, 0)
        upper = None
        lower = None
        for i in self.data["bounds"]:
            if i[0] == "Default":
                if len(i) == 2:
                    if i[1] != "None":
                        lower = i[1]        
                elif len(i) == 3:
                    if i[1] != "None":
                        lower = i[1]
                    if i[2] != "None":
                        upper = i[2]
        # In printed LP problem, integers default to -inf <= x <= inf (free) while
        # continuous variables default to x > 0. Therefore, inf and 0 may not appear in
        # Bounds statement. In PuLP, -inf <= x <= inf is default for int and continous.
        varList = LpVariable.dicts("x",range(numV),lowBound=lower,upBound=upper)
        # Set as integer
        for i in self.data["integer"]:
            if int(i) in indices:
                varList[int(i)].cat = LpInteger

        # Set bounds
        for i in self.data["bounds"]:
            if i[0] == "Default":
                continue
            if len(i) == 2:
                if i[1] != "None":
                    varList[int(i[0])].lowBound = i[1]
            elif len(i) == 3:
                if i[1] != "None":
                    varList[int(i[0])].lowBound = i[1]
                if i[2] != "None":
                    varList[int(i[0])].upBound = i[2]
            elif len(i) == 4:
                if i[1] != "None":
                    varList[int(i[0])].lowBound = i[1]
                if i[2] != "None":
                    varList[int(i[0])].upBound = i[2]
                if i[3] != "Int":
                    varList[int(i[0])].car = LpInteger
                    
        # Set as binary
        for i in self.data["binary"]:
            if int(i) in indices:
                varList[int(i)].cat = LpInteger
                # Error in docs (lowBound, not lowbound)
                varList[int(i)].lowBound = 0
                varList[int(i)].upBound = 1
        
        
        # Objective and Variables
        # (the name at the end is facultative)
        prob += lpSum([varList[i]*self.data["c"][i] for i in indices]) - self.data["r"], "Obj_min"

        # Inequalities
        for i in range(0,len(self.data["A"])):
            name = "Inequality_"+str(i)
            prob += lpSum([varList[j]*self.data["A"][i][j] for j in indices]) <= self.data["b"][i], name

        # Equalities
        for i in range(0,len(self.data["E"])):
            name = "Equality_"+str(i)
            prob += lpSum([varList[j]*self.data["E"][i][j] for j in indices]) == self.data["d"][i], name
                    
        # Solve
        prob.solve()
        
        prob.writeLP('lpp')
        
        # Print the status of the solved LP
        self.message["message"] = str(LpStatus[prob.status])
        self.message["code"] = prob.status
        if prob.status > 0:
            valueList = [0]*len( prob.variables() )
            variableNames = [0]*len( prob.variables() )
            # Print the value of the variables at the optimum
            for v in prob.variables():
                    #r += str(v.name)+ "="+ str(v.varValue)
                    # Variables are in alphabetical order. Therefore...
                    index = int(v.name.split('_')[1]) # Get index from name
                    valueList[index] = v.varValue
            # Check for integers
            for i in self.data["integer"]:
                if int(i) in indices:
                    valueList[int(i)] = int(valueList[int(i)])
            for i in self.data["binary"]:
                if int(i) in indices:
                    valueList[int(i)] = int(valueList[int(i)])               
            
            self.message["x"] = valueList

            # Print the value of the objective
            self.message["objective"] = value(prob.objective)
