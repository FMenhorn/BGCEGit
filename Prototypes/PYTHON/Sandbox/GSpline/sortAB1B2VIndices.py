import numpy as np

def sortAB1B2VIndices(oldA,oldB1,oldB2,oldC):

    def mimic_matlab_row_intersect(M1, M2):
        M1_dict = {tuple(M1[i,:]):i for i in range(M1.shape[0])}
        M2_dict = {tuple(M2[i,:]):i for i in range(M2.shape[0])}

        keys = M1_dict.viewkeys() & M2_dict.viewkeys()
        print keys
        MM = []
        for key in keys:
            MM.append(list(key))

        MM = np.array(MM)

        i = np.lexsort((MM[:,1],MM[:,0]))

        MM=MM[i]

        M1_ids = []
        M2_ids = []
        for key in MM:
            M1_ids.append(M1_dict[tuple(key)])
            M2_ids.append(M2_dict[tuple(key)])

        return MM, M1_ids, M2_ids


    mod_index = lambda i, modul: (i-1)%modul + 1
    shifted_indices = lambda ind, modul: mod_index(np.array(range(modul)) + ind,modul)
    newB1 = np.zeros(oldB1.shape)
    newB2 = np.zeros(oldB2.shape)
    newA = np.zeros(oldA.shape)
    newC = np.zeros(oldC.shape)

    for i in range(oldB2.shape[0])
        m = getNumOfEdgesMeetingMatlab(oldB2,i)
        indicesLocB1 = np.zeros[1,m]
        indicesLocB2 = np.zeros[1,m]
        indicesLocA = np.zeros[1,m]
        indicesLocC = np.zeros[1,m]

        BB1 = np.reshape(oldB1[i,0:m,2:4],[m,2])
        BB2 = np.reshape(oldB2[i,0:m,2:4],[m,2])
        idontcare,B1Indices,B2Indices = mimic_matlab_row_intersect(BB1,BB2) #todo hopefully this is right...

        nextIndex = 1
        for local_quad_index in range(m):
            current_quad = B2Indices[nextIndex]
            neighbour = B1Indices[nextIndex]
            neighbourQuad = oldB1[i,neighbour,1]
            neighbourAIndex = np.where(oldA[i,0:m,1] == neighbourQuad)[0][0]
            neighbourB2Index = np.where(oldB2[i,0:m,1] == neighbourQuad)[0][0]
            neighbourCIndex = np.where(oldC[i,0:m,1] == neighbourQuad)[0][0]
            nextIndex = np.where(B2Indices == neighbourB2Index)[0][0]
            indicesLocA[mod_index(local_quad_index+1,m)] = neighbourAIndex
            indicesLocB1[mod_index(local_quad_index+1,m)] = neighbour
            indicesLocC[mod_index(local_quad_index+1,m)] = neighbourCIndex
            indicesLocB2[local_quad_index] = current_quad

        newA[i,0:m,:] = oldA[i,indicesLocA,:]
        newB1[i,0:m,:] = oldB1[i,indicesLocB1,:]
        newB2[i,0:m,:] = oldB2[i,indicesLocB2,:]
        newC[i,0:m,:] = oldC[i,indicesLocC,:]

    return newA,newB1,newB2,newC