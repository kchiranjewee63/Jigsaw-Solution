#Algorithm
#To measure how good the arrangement is a cost is defined. Lower the cost better the arrangement.
#The algorithm tries all possible arrangement and choose the one with the lowest cost.
#To speed up the algorithm following things are done:
#1. While searching for arrangement the total_cost build up is continous compared with minimun cost of arrangement found till that 
#  time if the cost build up is found to be larger than then minimum cost then all the following permutation is discarded.(Backtracking)
#2. The computed cost between two images is stored in a array, so that recomputation is not necessary(memoization). 


#Libary used
#PIL->For reading and saving image.
#numpy->For vectorization implementation of calculation of cost.



from PIL import Image
import numpy as np
import os
import sys
file_name=sys.argv[1]
N=int(sys.argv[2])




#Store all mini_images as a numpy array in a list 
images=[]
for i in range(N*N):
    images.append(np.array(Image.open(os.path.join(file_name,str(i)+'.png'))))







def give_cost(first_image_no,second_image_no,direction):
    #Gives the cost when a mini_image is placed to the side of another
    #Cost for a color is calculated as sum of absolute difference of a color values of two mini_images at the edge of common border
    #Total cost is sum of costs of all colors(red,green,blue)
    
    #Lower the cost better the fit so we will choose the combination with lowest cost
     
    
    #'R'->Right side
    #'D'->Down side

    first_image=images[first_image_no]
    second_image=images[second_image_no]
    if direction=='R':
        red_cost   = np.sum(np.abs(first_image[:,-1,0].astype('int')-second_image[:,0,0].astype('int')))
        green_cost = np.sum(np.abs(first_image[:,-1,1].astype('int')-second_image[:,0,1].astype('int')))
        blue_cost  = np.sum(np.abs(first_image[:,-1,2].astype('int')-second_image[:,0,2].astype('int')))
        return np.sum([red_cost,green_cost,blue_cost])
    elif direction=='D':
        red_cost   = np.sum(np.abs(first_image[-1,:,0].astype('int')-second_image[0,:,0].astype('int')))
        green_cost = np.sum(np.abs(first_image[-1,:,1].astype('int')-second_image[0,:,1].astype('int')))
        blue_cost  = np.sum(np.abs(first_image[-1,:,2].astype('int')-second_image[0,:,2].astype('int')))
        return np.sum([red_cost,green_cost,blue_cost])





#Array for storing already computed cost between two mini_images
#Array has size N*N and each entry has two items
#First item gives cost if image is in Right direction
#Second item gives cost if image in in Down direction
store_costs=[[[-1,-1] for i in range(N*N)] for i in range(N*N)]





#Swap two items of a list
def swap(my_list,i,j):
    temp=my_list[i]
    my_list[i]=my_list[j]
    my_list[j]=temp







def Update_cost(my_list,l,Ops):

    #Update the cost when new mini_image is added or removed form the group of mini_images
    #There are three cases
    #1.mini_image is in the first row where cost is caclulated by only considering previous mini_image in first row [ ]->[ ] 
    #  and that cost is added to or subtracted from the total_cost 
    #2.mini_image is in the first column where cost is calculated by only considering the mini_image just above it  [ ]
    #                                                                                                                ↓ 
    #                                                                                                               [ ]
    #and that cost is added to or subtracted from total_cost
    #3.mini_image is in any other position where cost is calculated by considering mini_image just above it and mini_image previous to 
    # it in the row and that cost is added to or subtracted from total_cost  


    if l>0:
        if l>=N:
            ai=my_list[(l//N-1)*N+l%N] #ai->Above mini_image
        pi=my_list[l-1]                #pi->Previous mini_image
        ci=my_list[l]                  #ci->Current mini_image
        if l<N:
            cost=store_costs[pi][ci][0]
            if cost==-1:
                cost=give_cost(pi,ci,'R')
                store_costs[pi][ci][0]=cost
        elif l%N==0:
            cost=store_costs[ai][ci][1]
            if cost==-1:
                cost=give_cost(ai,ci,'D')
                store_costs[ai][ci][1]=cost
        else:
            cost1=store_costs[pi][ci][0]
            if cost1==-1:
                cost1=give_cost(pi,ci,'R')
                store_costs[pi][ci][0]=cost1
            cost2=store_costs[ai][ci][1]
            if cost2==-1:
                cost2=give_cost(ai,ci,'D')
                store_costs[ai][ci][1]=cost2
            cost=cost1+cost2
                
        #Update the total_cost
        if Ops=='+':
            give_arrangement.cost+=cost
        elif Ops=='-':
            give_arrangement.cost-=cost





def give_arrangement(my_list,l=0):
    #Add cost of adding l-1 mini_image to the arrangement
    Update_cost(my_list,l-1,'+')
    
    #If cost build up is already larger the minimum cost of arrangement found till now skip other possible permutation 
    #form here(Backtracking) as it not gonna give minimum cost solution
    if give_arrangement.min_cost is not None and give_arrangement.cost>give_arrangement.min_cost[0]:
        return
    
    if len(my_list)==l:
        #Arrangement with lower cost then the minimum till now is found
        give_arrangement.min_cost=(give_arrangement.cost,list(my_list))
    
    for i in range(l,len(my_list)):
        #Taking i as first element
        swap(my_list,l,i)
        #Permute over list from l+1 
        give_arrangement(my_list,l+1)
        #Remove cost of lth image in list
        Update_cost(my_list,l,'-')
        #Backtrack 
        swap(my_list,l,i)
give_arrangement.min_cost=None
give_arrangement.cost=0



give_arrangement(np.arange(N*N))

#Code for printing output
for i in range(N*N):
    if i!=0 and i%N==0:
        print('\n',end='')
    print(give_arrangement.min_cost[1][i],end=' ')
	



#----------------------Code for saving image-----------------------------------
	

#Function to save image
def save_image(images,N,name):
    final_image=None
    for i in range(N):
        images_in_row=images[i*N]
        for j in range(1,N):
            images_in_row=np.concatenate((images_in_row,images[i*N+j]),axis=1)
        if final_image is None:
            final_image=images_in_row
        else:
            final_image=np.concatenate((final_image,images_in_row),axis=0)
    final_image=Image.fromarray(final_image,'RGB')
    final_image.save(name)

    

#Display original image. Uncomment below line to save image
save_image(images,N,'scrambled.png')


#Display arranged image. Uncomment below line to save image
save_image([images[i] for i in give_arrangement.min_cost[1]],N,'arranged.png')