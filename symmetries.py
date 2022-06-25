def solution(w, h, s):
  
   #function to multiply fractions contained in list
   # a = [n,d]    b = [n,d]
   # returns a * b as [n,d]
   def mulfrac(a, b):
     return([a[0]*b[0], a[1]*b[1]])
   
   #function to add fractions
   # a = [n,d]   b = [n,d]
   # returns a + b as [n,d]
   def addfrac(a, b):
     return([a[0]* b[1] + b[0] *a[1], b[1]*a[1]])

   #function to make deepcopy of a list
   def deepcopy(L):
      if isinstance(L, list):
        ret = []
        for i in L:
            ret.append(deepcopy(i))
      else:
          ret = L
      
      return ret



   def expand(frac, terml):
       for term in terml:
           term[0] = mulfrac(frac, term[0])
       return terml

   

   def multiplyTerm(sub, terml):
    
       terml = deepcopy(terml)
       for term in terml:
           alreadyIncluded = False
           for a in term[1]:    # term[1] is a list like [[1,1],[2,3]]  where the
               if a[0] == sub:  # first item is subscript and second the exponent
                   alreadyIncluded = True
                   a[1] += 1
                   break
           if not alreadyIncluded:
               term[1].append([sub, 1])

       return terml

   #function to combine cycles lists
   #and adding coefficent fractions with similar calculated cycles
   def add(termla, termlb):
       terml = termla + termlb
       # add coefficents of any repeated cycles 
       if len(terml) <= 1:
           return terml
       for i in range(len(terml) - 1):
           for j in range(i + 1, len(terml)):
               if set([(a[0], a[1]) for a in terml[i][1]]) == set([(b[0], b[1]) for b in terml[j][1]]):
                   terml[i][0] = addfrac(terml[i][0], terml[j][0])
                   terml[j][0] = [0, 1]
       
       #return coefficents and cycles where coefficient is not zero
       return [term for term in terml if term[0] != [0, 1]]

   #function to find lowest common multiple
   def lcm(a, b):
       def gcd(a, b):
           while b != 0:
               t = b
               b = a%b
               a = t
           return a
       
       return abs(a * b) / gcd(a, b) if a and b else 0
   
   #create global set to hold all unique cycles 
   global pet_cycnn_cache
   pet_cycnn_cache = {}
   
   
   #function to find all cycles and contributing coefficient in a list of size n
   def pet_cycleind_symm(n):
       global pet_cycnn_cache
       # if n = 0, break recursive loop, return coefficient of 1 and empty list
       if n == 0:
           return [ [[1,1], []] ]
       
        
       #if cycles for length n have been calculated, return previously found cycles set
       if n in pet_cycnn_cache:
           return pet_cycnn_cache[n]
       
        
       
       #find cycles, using recursive method 
       terml = []
       for l in range(1, n + 1):
           terml = add(terml, multiplyTerm(l,  pet_cycleind_symm(n - l)) )

       #add cycles and coefficient to solution set
       pet_cycnn_cache[n] = expand([1, n], terml)
       return pet_cycnn_cache[n]

   #function to combine two cycle indices
   #done term by term 
   def pet_cycles_prodA(cyca, cycb):
       alist = []
       
       for ca in cyca:
           lena = ca[0]
           insta = ca[1]

           for cb in cycb:
               lenb = cb[0]
               instb = cb[1]

               vlcm = lcm(lena, lenb)
               alist.append([vlcm, (insta * instb * lena * lenb) / vlcm])

       #combine terms (this actually ends up being faster than if you don't)
       if len(alist) <= 1:
           return alist
       for i in range(len(alist) - 1):
           for j in range(i + 1, len(alist)):
               if alist[i][0] == alist[j][0] and alist[i][1] != -1:
                   alist[i][1] += alist[j][1]
                   alist[j][1] = -1
       return [a for a in alist if a[1] != -1]

   #function to find all cycles in rows and columns
   #and each term's contribution to the complet set of cycle groups
   def pet_cycleind_symmmatrix(n, m):
       indA = pet_cycleind_symm(n)
       indB = pet_cycleind_symm(m)
       
       terml = []
       for flatA in indA:
           for flatB in indB:
               newterml = [
                   [mulfrac(flatA[0], flatB[0]), pet_cycles_prodA(flatA[1], flatB[1])]
               ]
               terml.extend(newterml)
  
       return terml


   def substitute(term, v):
       total = 1
       for a in term[1]:
    #need to cast the v and a[1] to int or 
    #they will be silently converted to double in python 3 
    #causing answers to be wrong with larger inputs
         total *= int(v)**int(a[1])
    
       return (mulfrac(term[0], [total,1]))

   
   terml = pet_cycleind_symmmatrix(w, h)
   total = [0,1]
   for term in terml:
       total = addfrac(substitute(term, s), total)

   return str(total[0] / total[1])


print(solution(2, 3, 3))