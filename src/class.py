
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
