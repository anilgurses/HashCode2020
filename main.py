## Hash Code 2020
## Collected 8,581,603 points


class Library():
    def __init__(self, bookcnt, sgnup, perday, bookarr):
        self.bookcnt = bookcnt
        self.bookarr = bookarr
        self.perday = perday
        self.sgnup = sgnup
        self.score = 0
        self.uniques = []

          

class Collector():
    def __init__(self, days, lbrcnt, bkcnt,scores):
        self.days = days
        self.lbrcnt = lbrcnt
        self.bkcnt = bkcnt
        self.libs = []
        self.scores = scores
        self.libscores = []
    
    def getBookScore(self, boid):
        return self.scores[boid]

    def calcScores(self):
        for lib in self.libs:
            score = 0
            for book in lib.bookarr:
                scr = self.getBookScore(book)
                score += scr
            lib.score = score
            self.libscores.append(score)

    def calcUniqScore(self,ids):
        score = 0
        for i in ids:
            score += self.getBookScore(i)
        return score
    
    def appendlib(self,library):
        self.libs.append(library)
    
    
    def getlib(self,libid):
        return self.libs[libid]
    

def calcFactor(col,isuniq=True,isSign=False):
    libFacts = []

    for a in col.libs:
        score = 0
        
        if isuniq and not isSign:
            for b in col.libs:
                if b == a:
                    continue
                uniq = list(set(a.bookarr) - set(b.bookarr))
                uniqscore = col.calcUniqScore(uniq)
                score += uniqscore
            
            rate = (col.days * a.perday) / a.bookcnt
            fact = (uniqscore * rate) / a.sgnup
            fact = 10e6 - fact
            libFacts.append(fact)
        elif not isuniq and isSign:
            libFacts.append(a.perday)
        else:
            libFacts.append(a.score)
    
    return libFacts



def process(inname,outname):
    f = open(inname, "r")
    lines = f.readlines()
    col = lines[0].split(" ")
    scores = [int(i) for i in lines[1].split(" ")]
    colc = Collector(int(col[2]), int(col[1]), int(col[0]), scores)

    for libid in range(2, 3+int(colc.lbrcnt), 2):
        info1 = [int(i) for i in lines[libid].split(" ")]
        info2 = [int(i) for i in lines[libid+1].split(" ")]
        lib = Library(info1[0], info1[1], info1[2], info2)
        colc.appendlib(lib)

    colc.calcScores()

    facts = calcFactor(colc,True,False)
    factcp = facts.copy()

    sublibs = {"libid": [], "sendlen": [], "books": []}

    for _ in range(len(facts)):

        mfact = max(factcp)
        factind = facts.index(mfact)
        cpind = factcp.index(mfact)
        del factcp[cpind]

        lib = colc.libs[factind]
        if factind in sublibs["libid"]:
            continue

        books = colc.libs[factind].bookarr
        bookscores = {"id": [], "score": []}
        bkorder = []

        for book in books:
            bookscores["id"].append(book)
            bookscores["score"].append(colc.getBookScore(book))

        bkscrcp = bookscores.copy()

        for _ in range(len(books)):
            score = max(bookscores["score"])
            scrind = bkscrcp["score"].index(score)
            bkid = bkscrcp["id"][scrind]

            bkorder.append(bkid)
            
            del bookscores["score"][scrind]
            del bookscores["id"][scrind]

        
        sublibs["books"].append(bkorder)
        sublibs["sendlen"].append(len(bkorder))
        
        sublibs["libid"].append(factind)

    wr = open(outname, "w+")

    wr.write("{} \n".format(len(sublibs["libid"])))

    for i in range(len(sublibs["libid"])):
        wr.write("{} {} \n".format(sublibs["libid"][i], sublibs["sendlen"][i]))
        book = [str(i) for i in sublibs["books"][i]]
        books = " ".join(book)
        wr.write(books+"\n")

    wr.close()
    f.close()


if __name__ == '__main__':
    
    cases = ["a_example", "b_read_on",
             "c_incunabula", "d_tough_choices", "e_so_many_books", "f_libraries_of_the_world"]
    
    for case in cases:
        out = case + "_out.txt"
        incase = case + ".txt"
        process(incase,out)
        
    
    
        




