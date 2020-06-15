import random
from itertools import combinations
import multiprocessing

job_num = 8
selection_num = 3

class job:
    def __init__(self,p,w):
        self.w = float(w)
        self.p = float(p)
        self.value = self.p / self.w
    def show(self):
        print("job w: "+str(self.w)+" p: "+str(self.p)+" value: "+str(self.value))

class jobs:
    def __init__(self,n):
        self.job_num = n
        self.jobs_set = []
    def random(self):
        # p_list = sorted([random.randint(1,10000) for i in range(self.job_num)],reverse = True)
        # w_list = sorted([random.randint(1,10000) for i in range(self.job_num)])
        # for i in range(self.job_num):
        #     self.jobs_set.append(job(p_list[i],w_list[i]))
        for i in range(self.job_num):
            self.jobs_set.append(job(random.randint(1,10000),random.randint(1,10000)))
    def show(self):
        print("the jobs set includes:")
        for job in self.jobs_set:
            job.show()
    def sort(self):
        self.jobs_set = sorted(self.jobs_set,key = lambda t:t.value)
    def gen(self):
        self.random()
        self.sort()

class local_min:
    def __init__(self,jobs_set,m):
        self.jobs_set = jobs_set
        self.cmb_list = list(combinations(jobs_set,m))
        self.score_set = {}
        self.local_set = {}
    def calculate(self):
        for cmb in self.cmb_list:
            score = 0.0
            p = 0.0
            index = []
            for job in cmb:
                p += job.p
                score += job.w * p
                index.append(str(self.jobs_set.index(job)))
            id = ''.join(index)
            self.score_set[id]=score
    def solve(self):
        self.calculate()
        for key,value in self.score_set.items():
            # print("key:{k}\tvalue:{v}".format(k=key,v=value))
            local = True
            for key1,value1 in self.score_set.items():
                # print("key1:{k}\tvalue1:{v}".format(k=key1,v=value1))
                if len(set(key)^set(key1)) == 2:
                    # print("only 1 diff in key")
                    if value > value1:
                        # print("local = False")
                        local = False
                        break
            if local:
                # print("find local")
                self.local_set[key]=value
    def show(self):
        # print(self.score_set)
        print(self.local_set)
        for key,value in self.local_set.items():
            local_projection={}
            for key1,value1 in self.score_set.items():
                if len(set(key)^set(key1)) == 2:
                    local_projection[key1]=value1
            print(local_projection)

def Search(n,k):
    x = jobs(n)
    x.gen()
    s = local_min(x.jobs_set,k)
    s.solve()
    if len(s.local_set)!=1:
        x.show()
        s.show()

for i in range(1000000):
    print("----------------------%d-----------------------"%(i))
    n = job_num
    k = selection_num
    x = jobs(n)
    x.gen()
    s = local_min(x.jobs_set,k)
    s.solve()
    if len(s.local_set)!=1:
        x.show()
        s.show()
        break
