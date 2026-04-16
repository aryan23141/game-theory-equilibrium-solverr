import numpy as np
import itertools


from scipy.optimize import fsolve


def check(array,target,forstrat,util_matrix):
    #this function checks if nash equillibrium exist or note
    tf=0
    
    
    getindex=[]
    
    
    for i in range(len(array)):
        
        
        getindex.append(allpermut[array[i]])
        
        
    #print(getindex)
    for i in range(len(getindex)):
        #print(tuple(getindex[i]),util_matrix[tuple(getindex[i])][target],"hi",i)
        
        
        if util_matrix[tuple(getindex[i])][target]<=util_matrix[tuple(forstrat)][target]:
            
            tf+=1
    if tf==len(array):        
        return 1
    else:
        return 0




def psnegen(allpermut, util_matrix, player_count):
    psnelist = []

    for i in range(len(allpermut)):
        
        
        flag = 0

        for j in range(len(allpermut[i])):
            
            
            comparisonarray = []

            for l in range(len(allpermut)):
                
                
                matchflag = 0

                for k in range(len(allpermut[i])):
                    
                    if allpermut[l][k] == allpermut[i][k]:
                        
                        matchflag += 1
                        
                    elif j == k and l != i:
                        
                        
                        matchflag += 1

                if matchflag == player_count:
                    
                    
                    comparisonarray.append(l)

            flag += check(comparisonarray, j, allpermut[i], util_matrix)

        if flag == player_count:
            
            psnelist.append(allpermut[i])

    return psnelist
def weakly_dominated_strategies(allpermut,util_matrix,player_count,strategy):
    
    
    
    
    finalarray = [[] for _ in range(player_count)]

    for i in range(player_count):
        
        
        comparray = [[] for _ in range(strategy[i])]

        for j in range(strategy[i]):
            
            
            
            indexes = []
            for k in range(len(allpermut)):
                
                
                if allpermut[k][i] == j:
                    
                    
                    indexes.append(allpermut[k])

            for l in range(len(indexes)):
                
                
                comparray[j].append(util_matrix[tuple(indexes[l])][i])

        for m in range(len(comparray)):
            
            
            
            howmany = 0
            for n in range(len(comparray)):
                
                
                if m == n:
                    continue
                forall = 0
                
                
                for o in range(len(comparray[m])):
                    if comparray[m][o] >= comparray[n][o]:
                        
                        
                        forall += 1
                if forall == len(comparray[m]):
                    
                    
                    howmany += 1

            if howmany == len(comparray) - 1:
                
                
                finalarray[i].append(m)

    return finalarray




# expected payoff fucntion
def expected_payoff(player, all_profiles, mixed_strategies, util_matrix):
    
    
    expected_val = 0.0
    
    for pure_profile in all_profiles:
        
        prob = 1.0
        for i in range(len(mixed_strategies)):
            
            
            prob *= mixed_strategies[i][pure_profile[i]]
            
        expected_val += prob * util_matrix[tuple(pure_profile)][player]
    return expected_val


# ---------- MSNE (N-PLAYER) ----------
def msne_n_player(player_count,strategy,util_matrix,allpermut):
   
   
   
    init = []
    
    
    
    for s in strategy:
        
        init.extend([1.0 / s] * s)

    def equations(vars):
        
        
        mixed = []
        idx = 0
        for s in strategy:
            
            mixed.append(vars[idx:idx + s])
            
            idx += s

        eqs = []

        # sum to 1 constraints
        for i in range(player_count):
            
            
            eqs.append(sum(mixed[i]) - 1)

        # indifference conditions
        for i in range(player_count):
            
            base = None
            for s in range(strategy[i]):
                
                
                temp_mixed = [list(m) for m in mixed]

                for k in range(strategy[i]):
                    temp_mixed[i][k] = 0
                    
                temp_mixed[i][s] = 1
                

                val = expected_payoff(i, allpermut, temp_mixed, util_matrix)

                if base is None:
                    
                    base = val
                else:
                    
                    
                    eqs.append(val - base)

        return eqs

    try:
        
        
        sol = fsolve(equations, init)
    except:
        
        
        return None

    mixed = []
    idx = 0
    for s in strategy:
        
        
        probs = sol[idx:idx + s]

        # clean probabilities
        probs = [max(0, x) for x in probs]
        
        
        total = sum(probs)
        if total != 0:
            
            
            probs = [x / total for x in probs]

        mixed.append(probs)
        
        idx += s

    return mixed


# input
player_count = int(input())



strategy = list(map(int, input().strip().split()))[:player_count]

new = np.prod(strategy) * player_count


util_list = list(map(int, input().strip().split()))[:new]

#converted totuples
tup_list = []


for i in range(0, len(util_list), player_count):
    
    
    temp = []
    for j in range(player_count):
        temp.append(util_list[i + j])
    tup_list.append(tuple(temp))

#numpy reshaping
temp_str = "float"


temp_str2 = ",float" * (player_count - 1)


dt = np.dtype(temp_str + temp_str2)

data = np.array(tup_list, dtype=dt)


tup = tuple(strategy)



util_matrix = data.reshape(tup[::-1])


util_matrix = np.transpose(util_matrix)


# ---------- GENERATE ALL PERMUTATIONS ----------
somelists = []


for k in range(player_count):
    
    
    somelists.append([i for i in range(strategy[k])])

allpermut = list(itertools.product(*somelists))


allpermut = [list(x) for x in allpermut]


# run the code
psnelist = psnegen(allpermut, util_matrix, player_count)

finalarray = weakly_dominated_strategies(allpermut, util_matrix, player_count, strategy)


msne = msne_n_player(player_count, strategy, util_matrix, allpermut)


# outpuut
print(len(psnelist))



for profile in psnelist:
    
    
    print(*[x + 1 for x in profile])

for i in range(player_count):
    
    
    print(len(finalarray[i]), *[x + 1 for x in finalarray[i]])

print("MSNE:")

if msne is None:
    
    
    
    print("No MSNE found")
    
else:
    
    
    for i in range(len(msne)):
        
        print("player", i + 1, ":-", ["{:.3f}".format(x) for x in msne[i]])