from ortools.sat.python import cp_model

class NRC:

    def __init__(self, blocks, code="NONE", course_code="NONE"):
        self.blocks = blocks
        self.code = code
        self.course = course_code

    def add_block(self, new_block):
        if not isinstance(new_block, Block):
            print(f"This new block isn't a valid block object, class found was {type(new_block)}")
            return
        self.blocks.append(new_block)


class Block:

    def __init__(self, time_day, classification):
        self.time_day = time_day
        self.type = classification


class Calendar:

    def __init__(self, nrcs, score=0):
        self.nrcs = nrcs
        self.score = score


asd = Block("M5", "cat")

test_nrc = NRC([])
test_nrc.add_block(asd)
print(test_nrc.blocks)

class AllSolutionsPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables_dict):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables_dict = variables_dict
        self.__solution_count = 0

    def OnSolutionCallback(self):
        self.__solution_count += 1
        print(f"\nSolución {self.__solution_count}:")
        for name, var in self.__variables_dict.items():
            if self.Value(var) == 1:
                print(name, "= 1")

    def SolutionCount(self):
        return self.__solution_count