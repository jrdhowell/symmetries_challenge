
def solution(m):
  
  # create an array with all possible 
  # numbers between 1 and the target  
  
  tmp=[]
  for x in range(m):
    tmp.append(x+1)
  
  
  # create a matrix to keep track of 
  # pairs we have seen and keep our count
  
  global tab
  tab = [[0 for i in range(m+1)] for j in range(m+1)]
 
  
 
  # function that takes an array of numbers, index count
  # and target sum 
  # function will return number of unique combinations 
  # in the array of numbers that add to the target
  
  def subsetSumCount(tmp, n, m):
      
    # If the sum is zero it means
    # we got our expected sum
    # and return 1 to add to the count
    if (m == 0):
        return 1
    
        
    # If we exhaust the list, return 0 
    if (n <= 0):
        return 0
         
    # If the value is not 0 it means we
    # have calculated this sum so 
    # we can return the same count
    # it will save from some repeated steps
    if (tab[n - 1][m] != 0):
        return tab[n - 1][m]
         
    # if the value of tmp[n-1] is
    # greater than the sum.
    # we call for the next value
    if (tmp[n - 1] > m):
        tab[n - 1][m] += subsetSumCount(tmp, n - 1, m)
        return tab[n - 1][m]
    else:
         
        # Here we do two calls because we
        # don't know which value will
        # fulfill our criteria
        tab[n - 1][m] += subsetSumCount(tmp, n - 1, m)
        tab[n-1][m] += subsetSumCount(tmp, n - 1, m - tmp[n - 1])
        return tab[n - 1][m]
    
  
  # we use m-1 to avoid the target number in our list  
    
  return subsetSumCount(tmp, m-1, m)



m = 6
print(solution(m))

