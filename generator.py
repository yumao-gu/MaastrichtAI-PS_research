import random
from itertools import combinations
import multiprocessing

job_num = 8

def cmp_func(job1,job2):
    if job1.value < job2.value:
        return -1
    elif job1.value > job2.value:
        return 1
    else:
        return 0

def no_intersection(s1,s2):
    tmp = set(s1.indexes).intersection(set(s2.indexes))
    if not tmp:
        return 1
    else:
        return 0

def quick_show_solver(jobs_set,n):
    s = solver(jobs_set,n)
    s.solve()
    s.show()
    s_daul = daul_solver(jobs_set,n)
    s_daul.solve()
    s_daul.show()
    s_co = co_solver(jobs_set,n)
    s_co.solve()
    s_co.show()

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
        p_list = sorted([random.randint(1,10000) for i in range(self.job_num)],reverse = True)
        w_list = sorted([random.randint(1,10000) for i in range(self.job_num)])
        for i in range(self.job_num):
            self.jobs_set.append(job(p_list[i],w_list[i]))
        # for i in range(self.job_num):
        #     self.jobs_set.append(job(random.randint(1,1000),random.randint(1,1000)))
    def show(self):
        print("the jobs set includes:")
        for job in self.jobs_set:
            job.show()
    def sort(self):
        self.jobs_set = sorted(self.jobs_set,key = lambda t:t.value)

class solver:
    def __init__(self,jobs_set,m):
        self.jobs_set = jobs_set
        self.cmb_list = list(combinations(jobs_set,m))
        self.best_cmb = []
        self.best_score = float('inf')
        self.indexes = []
    def solve(self):
        for cmb in self.cmb_list:
            score = 0.0
            p = 0.0
            for job in cmb:
                p += job.p
                score += job.w * p
            #print("score : "+ str(score))
            if score < self.best_score:
                self.best_score = score
                self.best_cmb = cmb
        for job in self.best_cmb:
            self.indexes.append(self.jobs_set.index(job))
    def show(self):
        #print("best score : "+str(self.best_score))
        #print("best cmb : ")
        #for job in self.best_cmb:
        #    job.show()
        print(str(len(self.indexes))+" index solutions : ")
        print(self.indexes)

class daul_solver:
        def __init__(self,jobs_set,m):
            self.jobs_set = jobs_set
            self.cmb_list = list(combinations(jobs_set,m))
            self.best_cmb = []
            self.best_score = float('inf')
            self.indexes = []
        def solve(self):
            for cmb in self.cmb_list:
                score = 0.0
                w = 0.0
                for job in cmb:
                    w += job.w
                    score += w * job.p
                #print("score : "+ str(score))
                if score < self.best_score:
                    self.best_score = score
                    self.best_cmb = cmb
            for job in self.best_cmb:
                self.indexes.append(self.jobs_set.index(job))
        def show(self):
            #print("best score : "+str(self.best_score))
            #print("best cmb : ")
            #for job in self.best_cmb:
            #    job.show()
            print(str(len(self.indexes))+" dual index solutions : ")
            print(self.indexes)

class co_solver:
        def __init__(self,jobs_set,m):
            self.jobs_set = jobs_set
            self.cmb_list = list(combinations(jobs_set,m))
            self.best_cmb = []
            self.best_score = float('inf')
            self.indexes = []
        def solve(self):
            for cmb in self.cmb_list:
                score = 0.0
                p,w,wp = 0.0,0.0,0.0
                for job in cmb:
                    w += job.w
                    p += job.p
                    wp += job.w*job.p
                score = w*p# + wp
                #print("score : "+ str(score))
                if score < self.best_score:
                    self.best_score = score
                    self.best_cmb = cmb
            for job in self.best_cmb:
                self.indexes.append(self.jobs_set.index(job))
        def show(self):
            #print("best score : "+str(self.best_score))
            #print("best cmb : ")
            #for job in self.best_cmb:
            #    job.show()
            print(str(len(self.indexes))+" co index solutions : ")
            print(self.indexes)

def thread_func(n):
    x = jobs(n)
    x.random()
    x.sort()
    s1 = solver(x.jobs_set,1)
    s1.solve()
    s2 = solver(x.jobs_set,2)
    s2.solve()
    s3 = solver(x.jobs_set,3)
    s3.solve()
    if no_intersection(s3,s2) and no_intersection(s1,s2) and no_intersection(s1,s3):
        x.show()
        s1.show()
        s2.show()
        s3.show()
        return 1
    else:
        return 0

def test(n):
    x = jobs(n)
    x.jobs_set = [job(1438,9641),job(1457,9454),job(1573,8693),job(2087,6930),
job(4719,6870),job(4774,2932),job(5350,2594),job(7917,2031)]
    x.sort()
    x.show()
    for i in range(n):
        quick_show_solver(x.jobs_set,i+1)

def find():
    it = 0
    p = multiprocessing.Pool(processes = 4)
    while(it < 1000000):
        p.apply_async(thread_func,job_num)
        #thread_func()
        it += 1
    p.close()
    p.join()

test(job_num)
