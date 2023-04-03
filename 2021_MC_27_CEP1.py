from pyamaze import *
from random import *
row_size=8
column_size=8
a=maze(row_size,column_size)
a.CreateMaze(row_size,column_size, loopPercent=100)
agnt=agent(a,1,1,shape='arrow',footprints=True,color='red')

grid=a.maze_map

population_size=500
fitness_formula,inf=0,0
length,turn_weight,weight=2,3,3
solution=0
iterations=0


def random_population(x):
    
    
   
    y=[]
    j= [randint(1,row_size)  for _ in range (x)]
    j.insert(0,1) ; j.append(row_size)
    direc_bit= [randint(0,1) for _ in range (2)]
    empty_list_1=turns(j) ; y=[j]+[direc_bit]
    return y,empty_list_1

def turns(x):
    turns=0
    for j in range ((column_size)-1):        
        if x[j]!=x[j+1]:
            turns+=1
    return turns
    
def Solution_found(x):
    for i in range(population_size):
        if (x[i]==0):
            return 1
        else:
            return 0

def infeasible_steps(x):
    path=[]
    path.append((1,1))
    if row_size!=column_size:
        direction[0]=0
    select= direction[0] ^ direction[1]
    a=(1,1)
    k=1
    inf=0
    for g in range(len(population)-1):
        y=g+1
        Boundary=(population[g+1]+1) if population[g+1] >population[g] else (population[g+1]-1)
        while k!=Boundary:
            if direction[0]==0:
                x=(k,y+select)
            else:
                x=(y+select,k)
            if x not in ((1,1),(row_size,column_size)):
                path.append(x)
                if x[0]-a[0]!=0:
                    if x[0]-a[0]>0:
                        if grid[a]["S"]==0:
                            inf+=1
                    else:
                        if grid[a]['N']==0:
                            inf+=1
                elif x[1]-a[1]!=0:
                    if x[1]-a[1]>0:
                        if grid[a]["E"]==0:
                            inf+=1
                    else:
                        if grid[a]['W']==0:
                            inf+=1
            a=x
            if population[g+1]>population[g]:
                k+=1
            else:
                k-=1
        if population[g+1]>population[g]:
            k-=1
        else:
            k+=1     
    path.append((row_size,column_size))
    
    return inf,path,len(path)

def fitness_formula(total_turns,path_length,infesible_step):
    minimum_step=0
    fesible_turn=1-(total_turns-min(total_turns))/(max(total_turns)-min(total_turns))
    fesible_length=1-(path_length-min(path_length))/(max(path_length)-min(path_length))
    obstacle=1-(infesible_step-minimum_step)/(max(infesible_step)-minimum_step)
    most_fit=(100*weight*obstacle)*((length*fesible_length)+(turn_weight*fesible_turn))/(length+turn_weight)
    return most_fit

def mutation(b):
    for i in range (population_size):
        for j in range (i):
            b[i][randint(1,column_size-2)]=randint(1,9)
    return b 

def cross_over(b):
    breaking_point=randint(1,column_size-2)
    empty_list_2=len(b[0])
    # print(breaking_point)
    for i in range(0,len(b),2):
        b[i][breaking_point:empty_list_2],b[i+1][breaking_point:empty_list_2]=b[i+1][breaking_point:empty_list_2],b[i][breaking_point:empty_list_2]
    return b

while(iterations < 10000):
    print(f'Iterations: {iterations}')
    
    empty_list_1=[]
    empty_list_2=[]
    empty_list_3=[]
    empty_list_4=[]
    all_path=[]
    for _ in range(population_size):
            w,e=random_population(column_size-2)
          
            population,direction=w
            empty_list_4.append(w)
           
            x=infeasible_steps(w)
            
            empty_list_1.append(x[0]) ; empty_list_2.append(x[2]) ; empty_list_3.append(e) ; all_path.append(x[1])
            
            
    j=list(zip(empty_list_4,empty_list_1))
    d=sorted(j,key= lambda x: x[1])
    y=list(zip(all_path,empty_list_1))
    e=sorted(y,key= lambda x: x[1])
   
    sort_pop=[x[0] for x in d ]
   
    sort_inf=[x[1] for x in d ]
    sort_path=[x[0] for x in e ]
   

    sort_c=[dd for dd,ee in sort_pop]
    
    sort_f=[ee for dd,ee in sort_pop]
   
    s = Solution_found(sort_inf)
  
    sol_path = sort_path[0]
    if s==1:
        break

    g=cross_over(sort_c)
        

    ww=mutation(g)
    
    iterations += 1
   
if s==1:
    a.tracePath({agnt:sol_path})
    a.run()
else:
    print('Solution not found!')

print(infeasible_steps(x))