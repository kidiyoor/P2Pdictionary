# P2Pdictionary
There are N identical processes in a peer-to-peer system, which are arranged in a circular topology. The system supports a set of operations which are   defined by a language, like  
a. GET key  
b. POST key value  
c. PUT key value  
d. DELETE key  It is possible to operate these instructions from any process. 

For example we can do this,  
Process 1:  ADD key1 value1  
Process 2:  GET key1   
Process 3:  DELETE key1  
Process 1:  Get key1  
Process 2:  Get key1  

The system should behave in a consistent way; meaning answer to any such command should give same result across all processes.  Implement the above system, assuming the processes are perfect and do not fail.
