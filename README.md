# Coding Challenge: Counting Symmetries (Burnside's lemma)

Create a function solution(w, h, s) that takes three integers as arguments and returns a string as descibed below:

Given a matrix of size w x h, and each entry in the matrix have s number of possible items (or integers), count 
how many unique configurations of the matrix there can be considering that any symmetries in the matrix 
are equivelant. 

Two matrices are considered symmetrical if rows or columns (or both) can be swapped to make the matrix equal.

For example, the following matrices are equivalent because the rows or columns can be swapped:

[ 0 1 ]<br/> 
[ 2 0 ]<br/>

[ 0 2 ]<br/>
[ 1 0 ]<br/>

But the following matrices are not equivalent:

[ 0 1 ]<br/>
[ 2 0 ]<br/>

[ 1 2 ]<br/>
[ 0 0 ]<br/>


A matrix of size 2 x 2, where each entry can be s where 0 <= s < 2, there are 7 unique matrix configurations:

[0 0] <space><space>  [1 0] <space><space>  [1 1] <space><space>  [1 1] <space><space>  [1 1] <space><space>  [1 0] <space><space>  [1 0]<br/>
[0 0] <space><space>  [0 0] <space><space>  [0 0] <space><space>  [1 0] <space><space>  [1 1] <space><space>  [0 1] <space><space>  [1 0] 



So the function solution(2, 2, 2) will return "7".

## Code and Resources Used
**Python:** Python 3.8.10 <br/>
**Packages:** none <br/>
**Resources:** code inspired by  (https://math.stackexchange.com/users/371679/awokeknowing), Number of equivalence classes of $w \times h$ matrices under switching rows and columns, URL (version: 2018-08-24): https://math.stackexchange.com/q/2185854)
