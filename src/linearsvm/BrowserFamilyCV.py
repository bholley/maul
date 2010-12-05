from BrowserLinearCLI import runSVM

def runCV():


#    Clist = [0.1, 0.5, 1.0, 5.0, 10.0 ]
    Clist = [2.5, 3.0, 3.5]
# 3.0 looks best

    f = open('models/Family/CVoutputlinear.txt','a') 
    for C in Clist:
                print 'C = ',C
                accuracy = runSVM(float(C))
                s = str(C)+" " 
                s = s + str(accuracy)
                f.write(s+'\n')

    f.close()
    return

if __name__ == "__main__":
    runCV()


