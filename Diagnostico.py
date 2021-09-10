import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

class CartaGenerica(object):
    def __init__(self,archivo):
        #----------------------Constructor de la clase 4N----------------------
        self.data = pd.read_csv(archivo, header=0, delim_whitespace=True, decimal=".")
        self.df=pd.DataFrame(self.data)
        self.r=0
        self.ultimo=len(self.df)-1
        self.posicion=self.data.iloc[:,0]                       #pos
        self.carga=self.data.iloc[:,1]                          #car
        
  
    def normalizacion(self,pos,car):
        #----------------------normaizacion de la carta usando formula---------
        dmin=np.min(pos)
        dmax=np.max(pos)
        smin=np.min(car)
        smax=np.max(car)
        dnlist=[]
        lnlist=[]
        for i in range(len(self.df)):
            dn=(pos[i]-dmin)/(dmax-dmin)
            ln=(car[i]-smin)/(smax-smin)
            dnlist.append(dn)
            lnlist.append(ln)
        return lnlist,dnlist
        
    def angulo(self,lnlist,dnlist): 
        #----------------------calculo angulo----------------------------------
        global l1;
        l1=len(self.df)-1
        An=[]
        for i in range(0, len(self.df)-1):
            Ang =np.arctan2(lnlist[i+1] - lnlist[i], dnlist[i+1]-dnlist[i])* 180 / np.pi
            An.append(Ang)   
        Ang1 =np.arctan2(lnlist[0] - lnlist[l1], dnlist[0]-dnlist[l1])* 180 / np.pi
        An.append(Ang1)
        return An
        
               
    def codigocomprimido(self,codcadena,pos,car):
        #------------------------calcula el codigo de cadena comprimido--------
        vx=[] #vertices en x
        vy=[] #vertices en y
        kk=[]
        l=len(codcadena)
        k=0
        self.cdccomprimido=[]
        for k in range(0, l-1):
            if (codcadena[k]==codcadena[k+1]):
                k=k+1
            else:
                #self.graficarvertices(f,c,N,k,x1,y1)#  grafico dos
                self.cdccomprimido.append(codcadena[k])
                vx.append(pos[k])
                vy.append(car[k])
                kk.append(k)
        self.numver=(len(vx)) #numer es la longitud de la lista me indica cuantos puntos hay sobre la grafica.
        u=codcadena[-1] #ultimo elemento de la lista
        self.cdccomprimido.append(u)#agrafo el ultimo elemento
        self.cadena=(codcadena)
        self.dt=list(zip(vx,vy))
        return vx,vy,self.numver,self.cdccomprimido
        
    def filtro(self,pos,car):
        #--------------------------filtro--------------------------------------
        x=pos
        y=car
        dnfilt=[]
        lnfilt=[]
        for i in range(0,len(self.df)-2): #0->>171  #0-->>lend-3
            dnf=(x[i]+x[i+1]+x[i+2])/3
            lnf=(y[i]+y[i+1]+y[i+2])/3
            dnfilt.append(dnf)
            lnfilt.append(lnf)
        l1=len(self.df)-1
        l2=len(self.df)-2 
        dnf_pen=(x[l2]+x[l1]+x[0])/3  
        dnf_ult=(x[l1]+x[0]+x[1])/3 
        dnfilt.extend([dnf_pen,dnf_ult])
        lnf_pen=(y[l2]+y[l1]+y[0])/3  
        lnf_ult=(y[l1]+y[0]+y[1])/3
        lnfilt.extend([lnf_pen,lnf_ult])        
        lnlist,dnlist = self.normalizacion(dnfilt,lnfilt)
        An = self.angulo(lnlist,dnlist)
        codcadena = self.codigo(An,dnfilt,lnfilt)
        vx,vy,self.numver,self.cdccomprimido=self.codigocomprimido(codcadena,dnfilt,lnfilt)
        return dnfilt,lnfilt,vx,vy,self.numver

        
    def Ejecutar(self,tipo):
        # =================== Ejecucion =======================================
        #posicion=self.data.iloc[:,0]                       #pos
        #carga=self.data.iloc[:,1]                          #car
        lnlist,dnlist = self.normalizacion(self.posicion,self.carga) #normalizacion(self,pos,car)
        An = self.angulo(lnlist,dnlist)                    #angulo(self,lnlist,dnlist)
        codcadena = self.codigo(An,self.posicion,self.carga)         #codigo(self,An,pos,car)
        vx,vy,self.numver,self.cdccomprimido=self.codigocomprimido(codcadena,self.posicion,self.carga) #def codigocomprimido(self,codcadena,pos,car)
        dnfilt,lnfilt,vx,vy,self.numver=self.filtro(self.posicion,self.carga) #filtro(self,pos,car)
        sx,sy=self.Autofiltrar(dnfilt,lnfilt)                       #Autofiltrar(self,f1,f2)
        return self.graficoOriginal(1,1,1,self.posicion,self.carga,self.sx,self.sy,tipo)
        
    
    def Autofiltrar(self,f1,f2):
        # ------------------- Auto Filtra la carta,usando recursividad---------
        for i in range(0,(800)): #0-->4
            self.r=self.r+1 #5
            if (self.cdccomprimido==[1, 0, 3, 2, 1] or self.cdccomprimido==[0, 3, 2, 1, 0]) and self.numver==4 or self.numver==4:
               self.numrecur=self.r
               return (0,0)
            else:
                dnfilt,lnfilt,vx,vy,self.numver=self.filtro(f1,f2)
                self.sx=(vx)
                self.sy=(vy)
                self.du=(dnfilt)
                self.lu=(lnfilt)
                self.cdc=(self.cdccomprimido)
                #print("esto es sx",self.sx)
                #print("codigo comprimido finalll",self.cdccomprimido)
                #self.grafico_proceso_filtrado(20,3,self.r,dnfilt,lnfilt,vx,vy) #grafico_proceso_filtrado(numero de cartasxcolumna,numero de columnas,numero de recursividad,dnfilt,lnfilt,vx,vy)
                dnfilt,lnfilt = self.Autofiltrar(dnfilt,lnfilt) 
   
    
    def graficoOriginal(self,a,b,j,xx,yy,lx,ly,tipo):
        #----------------Graficas de las cartas--------------------------------
        fig2 = plt.figure(tipo)
        fig2.subplots_adjust(hspace=0.5, wspace=0.5)
        zx = fig2.add_subplot(a, b, j)
        zx.plot(xx, yy,"b--")
        zx.fill(xx, yy, "w", edgecolor="black", linewidth=1)
        zx.set_xlabel(r"$Carrera(pulgadas)$", fontsize = 12, color = (1,0,0))
        zx.set_ylabel(r"$Peso(LBS)$", fontsize = 12, color = (1,0,0))
        zx.set_title(tipo)
        zx.grid(color='gray', linestyle='dashed', linewidth=1, alpha=0.4)
        zx.axhline(0, color='black', linewidth=0.5)
        puntos =zx.plot(lx,ly, 'ko')        
        #impresion del punto inicial del funcionamiento de la bomba
        puntoi =zx.plot(xx[0], yy[0], 'rd')
        nota = plt.annotate(r'$ inicio(Bomba)$',
        xy=(xx[0], yy[0]), xycoords='data',
        xytext=(20, 0.4), fontsize=9,
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
        #impresion del punto final del funcionamiento de la bomba
        puntof =zx.plot(xx[self.ultimo], yy[self.ultimo], 'm^')
        nota = plt.annotate(r'$fin(Bomba)$',
        xy=(xx[self.ultimo], yy[self.ultimo]), xycoords='data',
        xytext=(-10, -0.1), fontsize=9,
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))       
        #fig3 = plt.figure(" ")
        fig2.subplots_adjust(hspace=0.5, wspace=0.5)
        cz = fig2.add_subplot(1, 1, 1)
        cz.plot(self.du, self.lu,"r--")
        cz.fill(self.du, self.lu, "w", edgecolor="black", linewidth=1)

class Carta4N(CartaGenerica):
    
    def __init__(self,archivo):
        CartaGenerica.__init__(self,archivo)                       #car
  
        
    def codigo(self,An,pos,car):
        #-------------------------calcula el codigo de cadena------------------
        codcadena=[]
        for i in range(0,len(An)): 
            if (-200<An[i]<-45): 
                codcadena.append(3)
              
            elif (-45<An[i]<45):
                codcadena.append(0)
         
            elif (45<= An[i] <=135):
                codcadena.append(1)            
            elif (An[i]>135):
                codcadena.append(2)
        return codcadena

   
    def Autofiltrar(self,f1,f2):
        # ------------------- Auto Filtra la carta,usando recursividad---------
        for i in range(0,(800)): #0-->4
            self.r=self.r+1 #5
            #print("numero de recursividad",self.r)
            #antes estaba self.numver se evaluava por el numero de puntos en la carta
            #ahora evaluo por el codigo de cadena comprimido cdccomprimido
            if (self.cdccomprimido==[1, 0, 3, 2, 1] or self.cdccomprimido==[0, 3, 2, 1, 0]) and self.numver==4 or self.numver==4:
               self.numrecur=self.r
               return (0,0)
            else:
                dnfilt,lnfilt,vx,vy,self.numver=self.filtro(f1,f2)
                self.sx=(vx)
                self.sy=(vy)
                self.du=(dnfilt)
                self.lu=(lnfilt)
                self.cdc=(self.cdccomprimido)
                #print("esto es sx",self.sx)
                #print("codigo comprimido finalll",self.cdccomprimido)
                #self.grafico_proceso_filtrado(20,3,self.r,dnfilt,lnfilt,vx,vy) #grafico_proceso_filtrado(numero de cartasxcolumna,numero de columnas,numero de recursividad,dnfilt,lnfilt,vx,vy)
                dnfilt,lnfilt = self.Autofiltrar(dnfilt,lnfilt) 
   
    def vertices_4N(self):
        return self.dt
    

class Carta8N(CartaGenerica):
    
    def __init__(self,archivo):
        CartaGenerica.__init__(self,archivo)  
        

   
    def codigo(self,An,pos,car):
        codcadena=[]
        #-------------------------calcula el codigo de cadena------------------
        for i in range(0,len(An)): #<--aqui itera toda la columan
                if (0<=An[i]<45): #<--aqui mira si es true
                    codcadena.append(0)
                
                elif (45<= An[i] <90):
                    codcadena.append(1)
                    
                elif (90<=An[i]<135): 
                    codcadena.append(2)
                    
                elif (An[i]>135): 
                    codcadena.append(3)
                
                elif (An[i] <-135):
                    codcadena.append(4)
                    
                elif (-135 <= An[i] <-90): 
                    codcadena.append(5)
                
                elif (-90<=An[i]< -45): 
                    codcadena.append(6)
                    
                elif (-45 <=An[i] < 0): 
                    codcadena.append(7)
        return codcadena
                  

    def Autofiltrar(self,f1,f2):
        for i in range(0,(800)): #0-->4
            self.r=self.r+1 #5
            #print("numero de recursividad",self.r)
            #antes estaba self.numver se evaluava por el numero de puntos en la carta
            #ahora evaluo por el codigo de cadena comprimido cdccomprimido
            if (self.cdccomprimido==[0,7,6,5,4,3,2,1,0] and self.numver==8) or self.numver==8:
               self.numrecur=self.r
               return (0,0)
            else:
                dnfilt,lnfilt,vx,vy,self.numver=self.filtro(f1,f2)
                self.sx=(vx)
                self.sy=(vy)
                self.du=(dnfilt)
                self.lu=(lnfilt)
                self.cdc=(self.cdccomprimido)
                #print("esto es sx",self.sx)
                #print("codigo comprimido finalll",self.cdccomprimido)
                #self.grafico_proceso_filtrado(20,3,self.r,dnfilt,lnfilt,vx,vy) #grafico_proceso_filtrado(numero de cartasxcolumna,numero de columnas,numero de recursividad,dnfilt,lnfilt,vx,vy)
                dnfilt,lnfilt = self.Autofiltrar(dnfilt,lnfilt) 

    def vertices_8N(self):
        return self.dt
    
   
    

class Carta16N(CartaGenerica):
    
    def __init__(self,archivo):
        
        CartaGenerica.__init__(self,archivo)                           #car
  
           
    def codigo(self,An,pos,car):
        codcadena=[]
        #-------------------------calcula el codigo de cadena------------------
        for i in range(0,len(An)): #<--aqui itera toda la columan
                if (0<=An[i]<22.5): #<--aqui mira si es true
                    codcadena.append(0)
                
                elif (22.5<= An[i] <45):
                    codcadena.append(1)
                    
                elif (45<=An[i]<67.5): 
                    codcadena.append(2)
                    
                elif (67.5<=An[i]<90): 
                    codcadena.append(3)
                
                elif (90<=An[i]<112.5):
                    codcadena.append(4)
                    
                elif (112.5<=An[i]<135): 
                    codcadena.append(5)
                
                elif (135<=An[i]<157.5): 
                    codcadena.append(6)
                    
                elif (157.5<=An[i]<180): 
                    codcadena.append(7)                                 
                    
                elif (-180<=An[i]<-157.5): #<--aqui mira si es true
                    codcadena.append(8)
                
                elif (-157.5<= An[i] <-135):
                    codcadena.append(9)
                    
                elif (-135<=An[i]<-112.5): 
                    codcadena.append(10)
                    
                elif (-112.5<=An[i]<-90): 
                    codcadena.append(11)
                
                elif (-90<=An[i]<-67.5):
                    codcadena.append(12)
                    
                elif (-67.5<=An[i]<-45): 
                    codcadena.append(13)
                
                elif (-45<=An[i]<-22.5): 
                    codcadena.append(14)
                    
                elif (-22.5<=An[i]<0): 
                    codcadena.append(15)
        return codcadena
                  

    def Autofiltrar(self,f1,f2):
        for i in range(0,(800)): #0-->4
            self.r=self.r+1 #5
            #print("numero de recursividad",self.r)
            #antes estaba self.numver se evaluava por el numero de puntos en la carta
            #ahora evaluo por el codigo de cadena comprimido cdccomprimido
            if (self.cdccomprimido==[0,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0] and self.numver==16) or self.numver==16:
               self.numrecur=self.r
               return (0,0)
            else:
                dnfilt,lnfilt,vx,vy,self.numver=self.filtro(f1,f2)
                self.sx=(vx)
                self.sy=(vy)
                self.du=(dnfilt)
                self.lu=(lnfilt)
                self.cdc=(self.cdccomprimido)
                #print("esto es sx",self.sx)
                #print("codigo comprimido finalll",self.cdccomprimido)
                dnfilt,lnfilt = self.Autofiltrar(dnfilt,lnfilt) 
                
    def vertices_16N(self):
        return self.dt


        
def informe(carta):
    A=Carta4N(carta)
    A.Ejecutar('Carta Dinagrafica 4N')
    value_4n=A.vertices_4N()
    B=Carta8N(carta)
    B.Ejecutar('Carta Dinagrafica 8N')
    value_8n=B.vertices_8N()
    C=Carta16N(carta)
    C.Ejecutar('Carta Dinagrafica 16N')
    value_16n=C.vertices_16N()
    vertices={'4N':pd.Series(value_4n),'8N':pd.Series(value_8n),'16N':pd.Series(value_16n)}
    df=pd.DataFrame(vertices)
    df.to_csv('PuntosCriticos.csv')
    print(df)

informe("fondotorunos.txt")

