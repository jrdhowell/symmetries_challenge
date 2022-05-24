def solution(M):
  Q = []
  R = []
  N = []
  
  
  endstate = []
  stepstate = []
  
  #find endstates and stepstates
  #endstate and stepstate will keep row numbers 
 
  for y in range(len(M)):
    check = True
    for p in range(len(M[y])):
      if M[y][p] != 0:
        if y != p:
          check = False
    if check:
      endstate.append(y)
    else:
      stepstate.append(y)
  
    
               
  #FUNCTIONS
  
  
  
  #function lcmfun(a)
  #find the lowest common multiple
  #aid in finding common denominators 
  #input an [x]x[2] array representing fractions
  #returns the lowest common multiple among all demoninators in array
  
  def lcmfun(a):
    # choose the greater number
    greater  = 1
    for p in range(len(a)):
      for r in range(len(a)):
        x = a[p][1]
        y = a[r][1]             
      if x > y and x > greater:
        greater = x
      elif y > greater:
        greater = y

      while(True):
        if((greater % x == 0) and (greater % y == 0)):
          lcm = greater
          break
        greater += 1

    return lcm


  #function mul(a,b)
  #takes two [1]x[2] arrays as input representing fractions
  #returns one [1]x[2] array equaling the product of the fractions, not reduced
  def mul(a, b):
    return([a[0]*b[0], a[1]*b[1]])
  
  #function div(a,b)
  #takes two [1]x[2] arrays as input representing fractions
  #returns one [1]x[2] array equaling the division of the fractions, not reduced
  def div(a, b):
    if a[0]*b[0] < 0:
      c = -1
    else:
      c = 1
    return([c*a[0]*b[1], abs(a[1]*b[0])])
  
  
  #function add(a,b)
  #takes two [1]x[2] arrays as input representing fractions
  #returns one [1]x[2] array equaling the additiona of the fractions, not reduced
  def add(a, b):
    return([a[0]* b[1] + b[0] *a[1], b[1]*a[1]])
  
    
  #function sub(a,b)
  #takes two [1]x[2] arrays as input representing fractions
  #returns one [1]x[2] array equaling the difference of the fractions, not reduced
  def sub(a, b):
    return([a[0]* b[1] - b[0] *a[1], b[1]*a[1]])
  
  
  #function red(x)
  #takes one [1]x[2] arrays as input representing a fraction
  #returns one [1]x[2] array equalling the reduction of the fraction, not reduced
  def red(x):
    a = x[0]
    b = x[1]
    def gcd(a, b):
        while b != 0:
            t = b
            b = a%b
            a = t
        return a
    if b==0:
      return([0,1])
    if a == 0:
      return([0,1])
    greatest=gcd(a,b)
    a/=greatest
    b/=greatest
    return([a,b])
  
    
  
  #function getMatrixMinor(m,i,j)
  #takes array of arrays of unknown size, and target row and columns
  #returns an array of arrays minus the target row and column
  def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]
  
  
  #function getMatrixDeterminant(m)
  #takes array of arrays of unknown size
  #return determinant of such matrix as [1]x[2] array representing fraction
  def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return sub(mul(m[0][0], m[1][1]), mul(m[0][1],m[1][0]))

    determinant = [0,1]
    for c in range(len(m)):
        if ((-1)**c) == 1:
          determinant = red(add(determinant, mul(m[0][c], getMatrixDeternminant(getMatrixMinor(m,0,c)))))
        else:
          determinant = red(sub(determinant, mul(m[0][c], getMatrixDeternminant(getMatrixMinor(m,0,c)))))
    return determinant


  #function getMatrixInverse(m)
  #takes array of arrays of unknown size
  #return inverse of such matrix as array of array
  #function presumes an inverse exists
  def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[red(div(m[1][1], determinant)), red(div(sub([0, 1], m[0][1]), determinant))],
                [red(div(sub([0, 1], m[1][0]), determinant)), red(div(m[0][0], determinant))]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            tmp = red(mul([(-1)**(r+c), 1], getMatrixDeternminant(minor  )))
            cofactorRow.append(tmp)
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = red(div(cofactors[r][c], determinant))
    return cofactors  
  
  def transposeMatrix(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0])) ] 
    
  
  
  
  #check for special case where the initial state is an end state
  #if so, build and return the results manually
  if 0 in endstate:
    tmp = []
    tmp.append(1)
    for x in endstate:
      if x != 0:
        tmp.append(0)
    tmp.append(1)
    return(tmp)
  
  
  
  #Making matrix (array of arrays) N
  #matrix N converts original matrix result counts into probably counts reprepesented as fractions in [1]x[2] arrays
  for x in range(len(M)):
    tmp = []
    for y in range(len(M[x])):
      if x in stepstate:
        tmp.append(red([M[x][y], sum(M[x])]))
      else:
        if x == y:
          tmp.append([1,1,])
        else:
          tmp.append([0, 1])
    N.append(tmp)


 
  #create matrix Q 
  #Q is a matrix of only the step states (rows and columns) from matrix N 
  for x in stepstate:
    tmp = []
    for y in stepstate:
      tmp.append(N[x][y])
    Q.append(tmp)
  
    
  #create matrix  R
  #R is a matrix of only the end states (rows and columns) from matrix N   
  for x in stepstate:
    tmp = []
    for y in endstate:
      tmp.append(N[x][y])
    R.append(tmp)
  
    
  #create IQ matrix which is the identity matrix minus Q
  IQ=[]
  for x in range(len(Q)):
    tmp = []
    for y in range(len(Q[x])):
      if x == y:
        tmp.append(sub([1,1], Q[x][y])) 
      else:
        tmp.append([-Q[x][y][0], Q[x][y][1]])
    IQ.append(tmp)
  
  #get the inverse of IQ
  IQ = getMatrixInverse(IQ)

  
  #create A matrix
  #A matrix is the results of pmuliplying the IQ and R matrix
  A = []
  for i in range(len(IQ)):
  #iterate through columns of IQ
    tmp2 = []
    for j in range(len(R[0])):
       # iterate through rows of IQ
      tmp = [0,1]
      for k in range(len(R)):
          tmp = red(add(tmp, mul(IQ[i][k], R[k][j]))) 
      tmp2.append(tmp)
    A.append(tmp2)
  
  
  #the first row of matrix A gives the results
  tmp = A[0]
  
  
  #processing the results
  #finding the lowest common denominator for our results and adjust fractions accordingly
  #add only the intended results into the array ans
  
  lcm2 = lcmfun(tmp)
  ans = []
  for y in range(len(tmp)):
    if tmp[y][1] != 0:
      ans.append(tmp[y][0] * lcm2 / tmp[y][1])
  ans.append(lcm2)
  
  
  return(ans)

#M = [[0, 1, 0, 0, 0, 1, 0, 0], [4, 0, 3, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
M = [[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
#M = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]




print(solution(M))