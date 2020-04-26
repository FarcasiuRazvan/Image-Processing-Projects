'''
Created on Dec 17, 2019

@author: WOLF
'''
'''
LAB 3
'''
import math

if __name__ == '__main__':
    pass

pixelsY=[]
pixelsU=[]
pixelsV=[]
Q=[[6,   4,   4,   6,   10,  16,  20,  24],
   [5,   5,   6,   8,   10,  23,  24,  22],
   [6,   5,   6,   10,  16,  23,  28,  22],
   [6,   7,   9,   12,  20,  35,  32,  25],
   [7,   9,   15,  22,  27,  44,  41,  31],
   [10,  14,  22,  26,  32,  42,  45,  37],
   [20,  26,  31,  35,  41,  48,  48,  40],
   [29,  37,  38,  39,  45,  40,  41,  40]]

filetype=""
filedescription=""
width=0
height=0
    
def DCcoefficient(val):
    if val>=-1 and val<=1:
        return 1
    elif (val>=-3 and val<=-2) or (val>=2 and val<=3) :
        return 2
    elif (val>=-7 and val<=-4) or (val>=4 and val<=7) :
        return 3
    elif (val>=-15 and val<=-8) or (val>=8 and val<=15) :
        return 4
    elif (val>=-31 and val<=-16) or (val>=16 and val<=31) :
        return 5
    elif (val>=-63 and val<=-32) or (val>=32 and val<=63) :
        return 6
    elif (val>=-127 and val<=-64) or (val>=64 and val<=127) :
        return 7
    elif (val>=-255 and val<=-128) or (val>=128 and val<=255) :
        return 8
    elif (val>=-511 and val<=-256) or (val>=256 and val<=511) :
        return 9
    elif (val>=-1023 and val<=-512) or (val>=512 and val<=1023) :
        return 10
    else:
        print("PROBLEM")
        return -1
     

def convertFileFromRGBtoYUV():
    global width,height,pixelsY,pixelsU,pixelsV,filetype,filedescription
    print("Start the program !")
    fp = open('nt-P3.ppm', 'r')
    filetype=fp.readline()
    filedescription=fp.readline()
    dimensions=fp.readline().strip().split(" ")
    doicincicinci=fp.readline()
    width=int(dimensions[0])
    height=int(dimensions[1])
    print("read from file and convert from RGB to YUV")
    
    for line in range(0,height):
        pixelsY.append([])
        pixelsU.append([])
        pixelsV.append([])
        for column in range(0,width):
            red= int(fp.readline())
            green= int(fp.readline())
            blue= int(fp.readline())
            
            YUV=RGBtoYUV(red, green, blue)
            
            pixelsY[line].append( YUV[0] )
            pixelsU[line].append( YUV[1] )
            pixelsV[line].append( YUV[2] )
    fp.close()

sampledY=[]
forSampleU=[]
forSampleV=[]

def to_8by8_for_sampling():
    global width,height,pixelsY,pixelsU,pixelsV,forSampleU,forSampleV, sampledY
    y=0
    for i in range(0,height-7,8):
        for s in range(0,width-7,8):
            forSampleU.append([])
            forSampleV.append([])
            sampledY.append([])
            j=i
                
            while j<i+7:
                m=s
                forSampleU[y].append([])
                forSampleU[y].append([])
                forSampleV[y].append([])
                forSampleV[y].append([])
                sampledY[y].append([])
                sampledY[y].append([])
                while m<s+7:
                    
                    sampledY[y][j-i].append(pixelsY[j][m])
                    sampledY[y][j-i].append(pixelsY[j][m+1])
                    
                    sampledY[y][j-i+1].append(pixelsY[j+1][m])
                    sampledY[y][j-i+1].append(pixelsY[j+1][m+1])
                    
                    forSampleU[y][j-i].append(pixelsU[j][m])
                    forSampleU[y][j-i].append(pixelsU[j][m+1])
                    
                    forSampleU[y][j-i+1].append(pixelsU[j+1][m])
                    forSampleU[y][j-i+1].append(pixelsU[j+1][m+1])
                    
                    forSampleV[y][j-i].append(pixelsV[j][m])
                    forSampleV[y][j-i].append(pixelsV[j][m+1])
                    
                    forSampleV[y][j-i+1].append(pixelsV[j+1][m])
                    forSampleV[y][j-i+1].append(pixelsV[j+1][m+1])
                    
                    m+=2
                j+=2
            y+=1

sampledU=[]
sampledV=[]

def subsampling():
    global width,height,pixelsY,pixelsU,pixelsV,forSampleU,forSampleV, sampledY, sampledU, sampledV
    print("Subsampling...")
    to_8by8_for_sampling()
    for i in range(0,len(forSampleU)):
        sampledU.append([[],[],[],[]])
        sampledV.append([[],[],[],[]])
        for j in range(0,8,2):
            for x in range(0,8,2):
                averageU=(forSampleU[i][j][x]+forSampleU[i][j][x+1]+forSampleU[i][j+1][x]+forSampleU[i][j+1][x+1])/4
                averageV=(forSampleV[i][j][x]+forSampleV[i][j][x+1]+forSampleV[i][j+1][x]+forSampleV[i][j+1][x+1])/4
                sampledU[i][j//2].append(averageU)
                sampledV[i][j//2].append(averageV)
    
    
upsampledY=sampledY
upsampledU=[]
upsampledV=[]
def to_8by8_for_upsampling():
    global upsampledU,upsampledV,sampledU,sampledV
    for i in range(0,len(sampledU)):
        upsampledU.append([[],[],[],[],[],[],[],[]])
        upsampledV.append([[],[],[],[],[],[],[],[]])
        for j in range(0,8,2):
            for x in range(0,8,2):
                upsampledU[i][j].append(sampledU[i][j//2][x//2])
                upsampledU[i][j].append(sampledU[i][j//2][x//2])
                upsampledU[i][j+1].append(sampledU[i][j//2][x//2])
                upsampledU[i][j+1].append(sampledU[i][j//2][x//2])
                
                
                upsampledV[i][j].append(sampledV[i][j//2][x//2])
                upsampledV[i][j].append(sampledV[i][j//2][x//2])
                upsampledV[i][j+1].append(sampledV[i][j//2][x//2])
                upsampledV[i][j+1].append(sampledV[i][j//2][x//2])
   
def upsampling():
    global width,height,pixelsY,pixelsU,pixelsV,sampledU,sampledV
    print("upsampling")
    to_8by8_for_upsampling()
    y=0
    for i in range(0,height-7,8):
        for s in range(0,width-7,8):
            j=i
            
            while j<i+7:
                m=s
                while m<s+7:
                    pixelsU[j][m]=upsampledU[y][j-i][m-s]
                    pixelsV[j][m]=upsampledV[y][j-i][m-s]
                    pixelsY[j][m]=upsampledY[y][j-i][m-s]
                    m+=1
                j+=1
            y+=1
            
def convertFromYUVtoRGBinFile():
    global width,height,pixelsY,pixelsU,pixelsV,filetype,filedescription
    fp = open('lab3.ppm', 'w')
    fp.write(filetype)
    fp.write(filedescription)
    fp.write(str(width)+" "+str(height)+"\n")
    fp.write("255"+"\n")
    print("convert from YUV to RGB and write it to file")
    
    for line in range(0,height):
        for column in range(0,width):
            
            RGB=YUVtoRGB(pixelsY[line][column], pixelsU[line][column], pixelsV[line][column])
            red=RGB[0]
            green=RGB[1]
            blue=RGB[2]
            
            fp.write(str(int(red))+"\n")
            fp.write(str(int(green))+"\n")
            fp.write(str(int(blue))+"\n")
    
    fp.close()
    print("Finish !")

def RGBtoYUV(red,green,blue):
    y=0.299*red+0.587*green+0.114*blue  
    u=128-0.1687*red-0.3312*green+0.5*blue 
    v=128+0.5*red-0.4186*green-0.0813*blue 
    return (y,u,v)

def YUVtoRGB(y,u,v):
    green= 135.4635+y - 0.334*u - 0.7142*v 
    red= y - 179.4784 - 0.0196*u + 1.4019*v
    blue= y + 1.7724*u-226.8672
    
    if red>255 : 
        red=255
    if green>255 : 
        green=255
    if blue>255 : 
        blue=255
    if red<0 : 
        red=0
    if green<0 : 
        green=0
    if blue<0 : 
        blue=0
    return (red,green,blue)

def printRGBtoYUV(red,green,blue):
    print( "y: ",0.299*red+0.587*green+0.114*blue  )
    print( "u: ",128-0.1687*red-0.3312*green+0.5*blue )
    print( "v: ",128+0.5*red-0.4186*green-0.0813*blue )

def printYUVtoRGB(y,u,v):
    blue= y + 1.7724*u-226.8672
    green= 135.4635+y - 0.334*u - 0.7142*v
    red= y - 179.4784 - 0.0196*u + 1.4019*v
    print("red: ",red)
    print("green: ",green)
    print("blue: ",blue)

dctU=[]
dctV=[]
dctY=[]
def apply_FDCT_formula():
    global dctU,dctV,dctY,upsampledU,upsampledV,upsampledY
    print("Apply FDCT formula...")
    for i in range(0,len(upsampledU)):
        dctU.append([[],[],[],[],[],[],[],[]])
        dctV.append([[],[],[],[],[],[],[],[]])
        dctY.append([[],[],[],[],[],[],[],[]])
        for u in range(0,8):
            for v in range(0,8):
                U=0
                V=0
                Y=0
                if u==0:
                    alfaU=1/math.sqrt(2)
                else:
                    alfaU=1
                if v==0:
                    alfaV=1/math.sqrt(2)
                else:
                    alfaV=1
                    
                
                for x in range(0,8):
                    for y in range(0,8):
                        U+=(upsampledU[i][x][y]-128)*math.cos(((2*x+1)*u*math.pi)/16)*math.cos(((2*y+1)*v*math.pi)/16)
                        V+=(upsampledV[i][x][y]-128)*math.cos(((2*x+1)*u*math.pi)/16)*math.cos(((2*y+1)*v*math.pi)/16)
                        Y+=(upsampledY[i][x][y]-128)*math.cos(((2*x+1)*u*math.pi)/16)*math.cos(((2*y+1)*v*math.pi)/16)
                
                U=U*(1/4)*alfaU*alfaV
                V=V*(1/4)*alfaU*alfaV
                Y=Y*(1/4)*alfaU*alfaV
                
                dctU[i][u].append(U)
                dctV[i][u].append(V)
                dctY[i][u].append(Y)

quantU=[]
quantV=[]
quantY=[]
def quantization(): 
    global dctU,dctV,dctY,quantU,quantV,quantY,upsampledU,upsampledV,upsampledY,Q
    print("Quantization phase...")
    for i in range(0,len(dctU)):
        quantU.append([[],[],[],[],[],[],[],[]])
        quantV.append([[],[],[],[],[],[],[],[]])
        quantY.append([[],[],[],[],[],[],[],[]])
        for u in range(0,8):
            for v in range(0,8):
                U=dctU[i][u][v]/Q[u][v]
                V=dctV[i][u][v]/Q[u][v]
                Y=dctY[i][u][v]/Q[u][v]
                if U<0:
                    U=math.ceil(U)
                else:
                    U=math.floor(U)
                if V<0:
                    V=math.ceil(V)
                else:
                    V=math.floor(V)
                if Y<0:
                    Y=math.ceil(Y)
                else:
                    Y=math.floor(Y)
                quantU[i][u].append(U)
                quantV[i][u].append(V)
                quantY[i][u].append(Y)

ZigZagU=[]
ZigZagV=[]
ZigZagY=[]
def zigzag():
    global quantU,quantY,quantV,ZigZagU,ZigZagV,ZigZagY
    print("ZigZag")
    for block in range(0,len(quantU)):
        ZigZagU.append([])
        ZigZagV.append([])
        ZigZagY.append([])
        #deasupra diagonalei principale
        aux=0
        while aux<8:
            if aux%2==0:
                #parcurgere in sus
                for i in range(0,aux+1):
                    ZigZagU[block].append(quantU[block][aux-i][i])
                    ZigZagV[block].append(quantV[block][aux-i][i])
                    ZigZagY[block].append(quantY[block][aux-i][i])
            else:
                #parcurgere in jos
                for i in range(aux,-1,-1):
                    ZigZagU[block].append(quantU[block][aux-i][i])
                    ZigZagV[block].append(quantV[block][aux-i][i])
                    ZigZagY[block].append(quantY[block][aux-i][i])
            aux+=1
        #sub diagonala principala
        aux=1
        while aux<8:
            if aux%2==0:
                #parcurgere in jos
                for i in range(aux,8):
                    ZigZagU[block].append(quantU[block][i][7+aux-i])
                    ZigZagV[block].append(quantV[block][i][7+aux-i])
                    ZigZagY[block].append(quantY[block][i][7+aux-i])
            else:
                #parcurgere in sus
                for i in range(7,aux-1,-1):
                    ZigZagU[block].append(quantU[block][i][7+aux-i])
                    ZigZagV[block].append(quantV[block][i][7+aux-i])
                    ZigZagY[block].append(quantY[block][i][7+aux-i])
            aux+=1

dc_acU=[]
dc_acV=[]
dc_acY=[]
def DC_AC():
    global ZigZagU,ZigZagV,ZigZagY,dc_acU,dc_acV,dc_acY
    print("DC_AC")
    for i in range(0,len(ZigZagU)):
        dc_acU.append([])
        dc_acV.append([])
        dc_acY.append([])
        u=0
        v=0
        y=0
        for j in range(0,len(ZigZagU[0])):
            if j==0:
                dc_acU[i].append((DCcoefficient(ZigZagU[i][j]),ZigZagU[i][j]))
                dc_acV[i].append((DCcoefficient(ZigZagV[i][j]),ZigZagV[i][j]))
                dc_acY[i].append((DCcoefficient(ZigZagY[i][j]),ZigZagY[i][j]))
            else:
                if ZigZagU[i][j]!=0:
                    dc_acU[i].append((u,DCcoefficient(ZigZagU[i][j]),ZigZagU[i][j]))
                    u=0
                else:
                    u+=1
                if ZigZagV[i][j]!=0:
                    dc_acV[i].append((v,DCcoefficient(ZigZagV[i][j]),ZigZagV[i][j]))
                    v=0
                else:
                    v+=1
                if ZigZagY[i][j]!=0:
                    dc_acY[i].append((y,DCcoefficient(ZigZagY[i][j]),ZigZagY[i][j]))
                    y=0
                else:
                    y+=1
        if u!=0:
            dc_acU[i].append((0,0))
        if v!=0:
            dc_acV[i].append((0,0))
        if y!=0:
            dc_acY[i].append((0,0))

encodedVect=[]
def encodeDC_AC():
    global dc_acU,dc_acV,dc_acY,encodedVect
    print("Encode")
    for i in range(0,len(dc_acU)):
        for j in dc_acY[i]:
            encodedVect.append(j)
        for j in dc_acU[i]:
            encodedVect.append(j)
        for j in dc_acV[i]:
            encodedVect.append(j)

dc_ac_backY=[]
dc_ac_backU=[]
dc_ac_backV=[]
def decodeDC_AC():
    global dc_ac_backU,dc_ac_backV,dc_ac_backY,encodedVect
    print("Decode")
    i=0
    doneY=False
    doneU=True
    doneV=True
    while i<len(encodedVect):
        if doneY==False and doneU==True and doneV==True:
            doneY=True
            doneU=False
            dc_ac_backY.append([])
            dc_ac_backY[len(dc_ac_backY)-1].append(encodedVect[i])
            i+=1
            while len(encodedVect[i])>2 and i<len(encodedVect):
                dc_ac_backY[len(dc_ac_backY)-1].append(encodedVect[i])
                i+=1
            if i<len(encodedVect) and encodedVect[i]==(0,0):
                dc_ac_backY[len(dc_ac_backY)-1].append(encodedVect[i])
                i+=1
                
        if doneY==True and doneU==False and doneV==True:
            doneU=True
            doneV=False
            dc_ac_backU.append([])
            dc_ac_backU[len(dc_ac_backU)-1].append(encodedVect[i])
            i+=1
            while len(encodedVect[i])>2 and i<len(encodedVect):
                dc_ac_backU[len(dc_ac_backU)-1].append(encodedVect[i])
                i+=1
            if i<len(encodedVect) and encodedVect[i]==(0,0):
                dc_ac_backU[len(dc_ac_backU)-1].append(encodedVect[i])
                i+=1
                
        if doneY==True and doneU==True and doneV==False:
            doneV=True
            doneY=False
            dc_ac_backV.append([])
            dc_ac_backV[len(dc_ac_backV)-1].append(encodedVect[i])
            i+=1
            while len(encodedVect[i])>2 and i<len(encodedVect):
                dc_ac_backV[len(dc_ac_backV)-1].append(encodedVect[i])
                i+=1
            if encodedVect[i]==(0,0):
                dc_ac_backV[len(dc_ac_backV)-1].append(encodedVect[i])
                i+=1
                
toQuantU=[]     
toQuantV=[]     
toQuantY=[]
def DC_ACback():
    global toQuantU,toQuantV,toQuantY,dc_ac_backU,dc_ac_backV,dc_ac_backY
    print("DC_AC back")
    for i in range(0,len(dc_ac_backU)):
        toQuantU.append([])   
        toQuantV.append([])    
        toQuantY.append([])
        
        toQuantU[i].append(dc_ac_backU[i][0][1])
        for j in range(1,len(dc_ac_backU[i])):
            if dc_ac_backU[i][j]!=(0,0):
                for x in range(0,dc_ac_backU[i][j][0]):
                    toQuantU[i].append(0)
                toQuantU[i].append(dc_ac_backU[i][j][2])
            else:
                for x in range(len(dc_ac_backU[i]),65):
                    toQuantU[i].append(0)
                break
                    
        toQuantV[i].append(dc_ac_backV[i][0][1])
        for j in range(1,len(dc_ac_backV[i])):
            if dc_ac_backV[i][j] !=(0,0):
                for x in range(0,dc_ac_backV[i][j][0]):
                    toQuantV[i].append(0)
                toQuantV[i].append(dc_ac_backV[i][j][2])
            else:
                for x in range(len(dc_ac_backV[i]),65):
                    toQuantV[i].append(0)
                break
        
        toQuantY[i].append(dc_ac_backY[i][0][1])
        for j in range(1,len(dc_ac_backY[i])):
            if dc_ac_backY[i][j]!=(0,0):
                for x in range(0,dc_ac_backY[i][j][0]):
                    toQuantY[i].append(0)
                toQuantY[i].append(dc_ac_backY[i][j][2])
            else:
                for x in range(len(dc_ac_backY[i]),65):
                    toQuantY[i].append(0)
                break

qU=[]
qV=[]
qY=[]
def zigzagBack():
    global qU,qV,qY,toQuantU,toQuantV,toQuantY
    print("ZigZagBack")
    for block in range(0,len(quantU)):
        qU.append([[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]])
        qV.append([[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]])
        qY.append([[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]])
        #deasupra diagonalei principale
        aux=0
        cont=0
        while aux<8:
            if aux%2==0:
                #parcurgere in sus
                for i in range(0,aux+1):
                    qU[block][aux-i][i]=toQuantU[block][cont]
                    qV[block][aux-i][i]=toQuantV[block][cont]
                    qY[block][aux-i][i]=toQuantY[block][cont]
                    cont+=1
            else:
                #parcurgere in jos
                for i in range(aux,-1,-1):
                    qU[block][aux-i][i]=toQuantU[block][cont]
                    qV[block][aux-i][i]=toQuantV[block][cont]
                    qY[block][aux-i][i]=toQuantY[block][cont]
                    cont+=1
            aux+=1
        #sub diagonala principala
        aux=1
        while aux<8:
            if aux%2==0:
                #parcurgere in jos
                for i in range(aux,8):
                    qU[block][i][7+aux-i]=toQuantU[block][cont]
                    qY[block][i][7+aux-i]=toQuantV[block][cont]
                    qV[block][i][7+aux-i]=toQuantY[block][cont]
                    cont+=1
            else:
                #parcurgere in sus
                for i in range(7,aux-1,-1):
                    qU[block][i][7+aux-i]=toQuantU[block][cont]
                    qV[block][i][7+aux-i]=toQuantV[block][cont]
                    qY[block][i][7+aux-i]=toQuantY[block][cont]
                    cont+=1
            aux+=1
                
dequantU=[]
dequantV=[]
dequantY=[]
def dequantization():
    global quantU,quantV,quantY,dequantU,dequantV,dequantY,Q,qU,qV,qY
    print("Dequantization phase...")
    for i in range(0,len(quantU)):
        dequantU.append([[],[],[],[],[],[],[],[]])
        dequantV.append([[],[],[],[],[],[],[],[]])
        dequantY.append([[],[],[],[],[],[],[],[]])
        for u in range(0,8):
            for v in range(0,8):
                dequantU[i][u].append(qU[i][u][v]*Q[u][v])
                dequantV[i][u].append(qV[i][u][v]*Q[u][v])
                dequantY[i][u].append(qY[i][u][v]*Q[u][v])

idctU=[]
idctV=[]
idctY=[]
def apply_IDCT_formula():
    global idctU,idctV,idctY,dequantU,dequantV,dequantY
    print("Apply IDCT formula...")
    for i in range(0,len(dequantU)):
        idctU.append([[],[],[],[],[],[],[],[]])
        idctV.append([[],[],[],[],[],[],[],[]])
        idctY.append([[],[],[],[],[],[],[],[]])
        for x in range(0,8):
            for y in range(0,8):
                U=0
                V=0
                Y=0
                
                for u in range(0,8):
                    for v in range(0,8):
                        if u==0:
                            alfaU=1/math.sqrt(2)
                        else:
                            alfaU=1
                        if v==0:
                            alfaV=1/math.sqrt(2)
                        else:
                            alfaV=1
                        U+=alfaU*alfaV*dequantU[i][u][v]*math.cos(((2*x+1)*u*math.pi)/16)*math.cos(((2*y+1)*v*math.pi)/16)
                        V+=alfaU*alfaV*dequantV[i][u][v]*math.cos(((2*x+1)*u*math.pi)/16)*math.cos(((2*y+1)*v*math.pi)/16)
                        Y+=alfaU*alfaV*dequantY[i][u][v]*math.cos(((2*x+1)*u*math.pi)/16)*math.cos(((2*y+1)*v*math.pi)/16)
                
                U=U*(1/4)+128
                V=V*(1/4)+128
                Y=Y*(1/4)+128
                
                idctU[i][x].append(U)
                idctV[i][x].append(V)
                idctY[i][x].append(Y)
    
def upsampling2():
    global width,height,pixelsY,pixelsU,pixelsV,idctU,idctV,idctY,dequantU,dequantV,dequantY
    print("upsampling2")
    y=0
    for i in range(0,height-7,8):
        for s in range(0,width-7,8):
            j=i
            
            while j<i+7:
                m=s
                while m<s+7:
                    pixelsU[j][m]=idctU[y][j-i][m-s]
                    pixelsV[j][m]=idctV[y][j-i][m-s]
                    pixelsY[j][m]=idctY[y][j-i][m-s]
                    m+=1
                j+=1
            y+=1

convertFileFromRGBtoYUV()
subsampling()
# upsampling()
# convertFromYUVtoRGBinFile()
to_8by8_for_upsampling()
apply_FDCT_formula()
quantization()

zigzag()
DC_AC()
encodeDC_AC()
decodeDC_AC()
DC_ACback()
#print(len(toQuantU),toQuantU[0])
#print(len(quantU),quantU[0])
zigzagBack()

dequantization()
apply_IDCT_formula()
  
upsampling2()
convertFromYUVtoRGBinFile()