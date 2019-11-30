"""
    Lab 6 and 7 - Pierre Lelièvre and Robinson Mathieu 
    
    We didn't really understand what were the boundaries of lab6, so we basically did the 2 labs in one. 
    
"""


"""
Initialisation part
"""

#number of words per frame/page
nb_words=4
#there are 8 pages/frames
nb_frames=8
#the logical memory and the physical memory are composed of words, and this number is the number of words time the number of words per page/frame
logical_mem = [0]*(nb_words*nb_frames)
physical_mem = [0]*(nb_words*nb_frames)
#we initialize a paging table that is made of nb_frames couples [i1,i2] where i1 represents the index of the page, and i2 the index of the frame
paging_table = [[False,False]]*nb_frames
#available_frames represents, for each frame, if it is used or not (basically, in our case where there is only one process that will try to allocate memory, if this memory can be allocated onto this frame, or if this frame is already occupied by another process
available_frames =[True]*nb_frames
#used_pages represents the pages that are completly of partially used (in logical memory)
used_pages = [False]*nb_frames
#we initialize the physical memory with some frames that are taken (by OS, by other proccesses, etc...)
taken = [0,2,3,6]
for elem in taken:
    available_frames[elem] = False
#note : we consider that the whole logical memory is available at start


"""
Allocation function
"""

#n is the number of words you want to allocate
#allocate returns : 
    #on success, the array [spot, n] with spot being the address in the logical memory of the allocated memory and n being the number of words
    #on error, -1
def allocate(n):
    new_pages_needed = []
    
    #finds a spot that is large enough and available
    for i in range(len(logical_mem)):
        available = True
        for j in range(n):
            if logical_mem[i+j] == 1:
                available = False
                break
        if available == True:
            spot = i
            break
    #at this point, we have a spot where we can store n words contiguously
    
    #allocation word-by-word
    for i in range(spot, spot+n):
        #checks if the upcoming word needs a new page to be allocated, and in this case, will modify the mapping table accordingly
        if used_pages[i//nb_words]==False:
            for j in range(len(available_frames)):
                new_frame=False
                if available_frames[j] == True:
                    available_frames[j] = False
                    used_pages[i//nb_words]=True
                    new_frame = j
                    print("The frame that is being given is ", j, ", as we need a new page for the spot ", i)
                    break
            #now we update the mapping table
            if new_frame != False:                
                for k in range(len(paging_table)):
                    if paging_table[k] == [False,False]:
                        paging_table[k] = [i//nb_words, new_frame]
                        new_pages_needed.append(k)
                        break
        #if we could find a physical equivalent frame for this word, we say it is allocated in the logical memory and in the physical memory
        for h in range(len(paging_table)):
            could_allocate=False
            if (i//nb_words == paging_table[h][0]):
                could_allocate = True
                logical_mem[i] = 1
                physical_mem[ paging_table[i//nb_words][1]*nb_words + (i%nb_words)] = 1
                break
        
        #unallocate all words (on physical and logical) that were given if at least one word cant be allocated (solves the problem where an element was too large to be on 1 page, and where the first page could be allocated, while the second part of it couldn't (for space reasons)
        #also rolls back the changes on the mapping table 
        if could_allocate==False:
            print("The word ", i, " couldn't be allocated")
            
            for l in range(spot, i):
                logical_mem[l] = 0
                physical_mem[ paging_table[l//nb_words][1]*nb_words + (l%nb_words)] = 0                
                used_pages[ paging_table[l//nb_words][0]]=False
            for m in range(len(new_pages_needed)):
                paging_table[new_pages_needed[m]] = [False,False]
            print("The changes have been rollbacked.")
            break        
            
    if could_allocate==False:
        return(-1)
        
    #printing some interesting infos about the allocation
    else :
        print("New pages needed :",new_pages_needed)
        print("mapping table :", paging_table)
        print("physical :",physical_mem) 
        print ("logical :",logical_mem)
        return([spot,n])   
    


"""
Freeing function
"""
#elem is the element that allocate gives
#free returns:
    #1 on success
    #-1 on error
def free(elem):
    spot = elem[0]
    size = elem[1]
    
    for i in range(spot, spot+size):
        print("tcha")
    #update mapping_table
    #update logical_memory
    #update physical_memory
        
    


tab = allocate (5)
free(tab)
print(tab)
