def solution(dimensions, your_position, trainer_position, distance):
    

    #function red(x)
    #takes one [1]x[2] arrays as input representing a fraction
    #returns one [1]x[2] array equalling the reduction of the fraction
    #customized for this problem
    def red(x):
          a = x[0]
          b = x[1]
          if a == 1 or b == 1:
              return([a,b]) # if the numerator or denominator = 1, return the fraction
          if a == 0 and b == 0:
              return([a,b]) # if input fraction is 0 over 0, return 0 over 0
          if b == 0:
              return([int(1*(a/abs(a))),0]) #if denominator is 0, depending on numerator, return 1 or -1 over 0
          
          if a == 0:
               return([0,int(1*(b/abs(b)))]) # if numerator is 0, depending on denominator, return 0 over 1 or -1
          
          if a < 0:
              signa = -1
          else:
              signa = 1
              
          if b < 0:
              signb = -1
          else: 
              signb = 1
           
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
          return([int(signa*abs(a)),int(signb*abs(b))]) # return reduced fraction with same signs and input
         
       
       
    
    #function to determine if the ray hits yourself
    #aim is initial direction of shot represented as vector
    #function assumes aim is reduced, using red() function above
    def selfhit(aim, dimensions, your_position, trainer_position):
       
       #position will track position of ray starting at your position 
       position = your_position
       
       t = aim[0]
       n = aim[1]
       
       #mov will be current vector of ray direction
       mov = [t,n]
       
       
       
      #loop will follow movement of ray and will continue until it hits you or trainer
      #input ensures that it will hit the trainer
       while True: 
           
           #update position
           position = [position[0] + mov[0], position[1] + mov[1]]
           
           #loop to correct position when it is out of bounds
           while position[0] < 0 or position[1] < 0 or position[0] > dimensions[0] or position[1] > dimensions[1]:
             
             #ray hit the left wall
             if position[0] < 0:
               p = position[0] * -1
               position[0]= p
               p = mov[0] * -1
               mov[0] = p
             
             #ray hit the bottom wall
             if position[1] < 0:
               p = position[1] * -1 
               position[1] = p
               p = mov[1] * -1
               mov[1] = p
               
             #ray hit the right wall  
             if position[0] > dimensions[0]:
               position[0]= dimensions[0] - (position[0]-dimensions[0])
               p = mov[0] * -1
               mov[0] = p
             
             #ray hit the top wall  
             if position[1] > dimensions[1]:
               position[1]= dimensions[1] - (position[1]-dimensions[1]) 
               p = mov[1] * -1
               mov[1] = p
           
           #if ray hits a corner, it will reflect to yourself: return True
           #shouldnt be applicable with current algorithm
           if position[0] == 0 and position[1] == 0:
               return True
           if position[0] == 0 and position[1] == dimensions[1]:
               return True 
           if position[0] == dimensions[0] and position[1] == 0:
               return True 
           if position[0] == dimensions[0] and position[1] == dimensions[1]:
                return True
           
           #if ray hits you, return True
           if position == your_position:
                return True
           #if ray its trainder, return False  
           if position == trainer_position:
                return False
    
     
    #fuction findmirror takes a point (target) and dimensions
    #returns a set of all mirror points to the target
    def findmirror(target, dimensions):
        
        
        mirrors = set()

        # going up
        mirrors.add((target[0], target[1] - 2*(target[1] - dimensions[1])))
        
        # going down
        mirrors.add((target[0], target[1] - 2*(target[1])))
        
        # going left
        mirrors.add((target[0] - 2*(target[0]), target[1]))
        
        # going right
        mirrors.add((target[0] - 2*(target[0] - dimensions[0]), target[1]))
        
        return mirrors


    #check to see if ray can reach trainer from you
    if distance**2 < (trainer_position[0] - your_position[0]) ** 2 + (trainer_position[1] - your_position[1])**2:
        return(0)
    

    #check to see if you and trainer are on the same spot
    #should not be applicable
    if your_position == trainer_position:
        return 0


    
    trackingtgt = set() #tracks directions to shoot trainer and trainer mirrors, within distance (solution)
    
    
    tgtreflections = set() #tracks all trainer mirror positions created to prevent duplicate mirror checks
    tgtreflections.add((trainer_position[0], trainer_position[1])) 
    
    
    
    
    
    #current, and initial, mirror sets to process
    tgt = findmirror(trainer_position, dimensions)
    
    
    #add to our total list
    tgtreflections |= tgt

    
    
    #loop for irratively finding all mirrors of you and trainer are found w/n the distance. 
    #stop when no more mirrors are found w/n distance
    check = True
    while check:
        check = False
        
        #going through trainer mirrors
        #if mirror is found w/n distance from your position add reduced AIM to tracking and check to True
        for t in tgt:
            bingo = red([t[0] - your_position[0], t[1] - your_position[1]])
            if distance**2 >= (t[0] - your_position[0])**2 + (t[1] - your_position[1])**2:
                trackingtgt.add((bingo[0], bingo[1]))
                check = True
    
                
        
        #find mirrors to our current trainer mirrors        
        tmp = set()    
        for t in tgt:
            tmp |= findmirror(t, dimensions)
        #remove mirrors we have seen and update total list
        tmp -= tgtreflections
        tgt = tmp
        tgtreflections |= tgt
        
        
    
     
        
    
    #check to make sure are trainer aiming directions will not hit you before hitting trainer
    hitself = set() 
    for t in trackingtgt:
       tmp = [t[0], t[1]]
       if selfhit(tmp, dimensions, your_position, trainer_position):
           hitself.add(t)
    
    
    #remove shots that will hit you
    trackingtgt -= hitself
    
    
    #add the direct shot to trainer
    tmp = red([trainer_position[0] - your_position[0], trainer_position[1] - your_position[1]])
    trackingtgt.add((tmp[0], tmp[1]))
    
    #print(trackingtgt) #this will show all directions to aim to hit trainer
    
    
    return(len(trackingtgt))




#print(solution([1250,1250], [150,150], [185,100], 1000))


#print(solution([300,275], [150,150], [185,100], 500))

print(solution([10,100], [6,60], [3,50], 80))
