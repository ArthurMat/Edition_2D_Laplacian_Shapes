import triangle as tr
from forme import Forme
import numpy as np
import matplotlib.pyplot as plt
from triPoint import triPoint,crossProd
from tkinter import Tk, Canvas,Button,Frame
import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


class Surface:
    def __init__(self,forme:Forme) -> None:
        """
        Une Surface est composée :
        -d'un maillage généré par la bibliothèque triangle (https://rufat.be/triangle/)
        -d'une liste de point fixes (fixPoint)
        -d'un dictionnaire de voisin l et r d'un segment (i,j)
        """
        self.forme=forme
        seg=[]
        cmp=len(forme.getPoint())
        for i in range(0,cmp):
            seg.append([i%(cmp),(i+1)%(cmp)])
        points=dict(vertices=np.array(forme.getPoint()),segments=np.array(seg))
        self.nombrePointOrigine=cmp
        self.maillage=tr.triangulate(points,"pa1")
        self.FixPoint=[]
        self.adjSeg={}
        self.adjSegContour={}
        self.constructVoisin()

    def getPointWithIndex(self,index:int):
        """
        Renvoie les coordonnées du points index
        """
        return self.maillage['vertices'][index]

    def find_closest_point(self, x:float, y:float) -> int:
        """
        Renvoie l'index du point le plus proche de (x,y)
        """
        dist_min = float("inf")
        i_min = -1
        p_ref = np.array([x, y])
        for i, p in enumerate(self.maillage['vertices']):
            dist = np.linalg.norm(p-p_ref)
            if dist_min>dist:
                i_min = i
                dist_min = dist
        return i_min
    def find_closest_FixPoint(self, x:float, y:float) -> int:
        """
        Renvoie l'index du point fixe le plus proche de (x,y)
        """
        dist_min = float("inf")
        i_min = -1
        p_ref = np.array([x, y])
        for i, p in enumerate(self.maillage['vertices']):
            if i in self.FixPoint:
                dist = np.linalg.norm(p-p_ref)
                if dist_min>dist:
                    i_min = i
                    dist_min = dist
        return i_min

    def addFixPoint(self, x:float, y:float) -> None:
        """
        Fix the closest point to (x,y)
        """
        i = self.find_closest_point(x, y)
        plt.clf()
        plt.xlim(self.forme.minaxisX,self.forme.maxaxisX)
        plt.ylim(self.forme.minaxisY,self.forme.maxaxisY)
        self.drawMaillage()
        if i not in self.FixPoint:
            self.FixPoint.append(i)
        else:
            self.FixPoint.remove(i)
        self.drawPointfix()

    def moveFixPoint(self, x:float, y:float,inv) -> None:
        """
        Move the closest fix point to (x,y)
        """
        i = self.find_closest_FixPoint(x, y)
        plt.clf()
        plt.xlim(self.forme.minaxisX,self.forme.maxaxisX)
        plt.ylim(self.forme.minaxisY,self.forme.maxaxisY)
        w = 1000

        Coordx, Coordy = self.calculNewCoordinate(w, i, (x,y))


        for c in range(0,len(Coordx)):
            x = Coordx[c]
            y = Coordy[c]
            self.maillage['vertices'][int(c)]=np.array([x,y])


        self.drawMaillage()
        self.drawPointfix()


    def interactionFixPoint(self, x:float, y:float,canvas,inv) -> None:
        """
        Permet de bouger un point fixe graphiquement
        """
        canvas._tkcanvas.after(10)#10s entre chaque capture de position de la souris
        x,y=inv.transform((x,y))#on se place dans les coordonnées du graphes
        self.moveFixPoint(x,self.forme.maxaxisY-y,inv)#On appelle la fonction movepoint (attention l'axe des y est inversé)
        plt.gcf().canvas.draw()#On met a jour l'affichage

    def drawMaillage(self):
        """
        Affiche graphiquement le maillage
        """

        for p1,p2,p3 in self.maillage['triangles']:
            coordp1,coordp2,coordp3=self.getPointWithIndex(p1),self.getPointWithIndex(p2),self.getPointWithIndex(p3)
            plt.plot([coordp1[0],coordp2[0],coordp3[0],coordp1[0]],[coordp1[1],coordp2[1],coordp3[1],coordp1[1]],c='blue')
        plt.draw()

    def drawPointfix(self):
        """
        Affiche graphiquement les points fixes
        """
        xCoord=[]
        yCoord=[]
        for i in self.FixPoint:
            coordx,coordy=self.getPointWithIndex(i)
            xCoord.append(coordx)
            yCoord.append(coordy)
        plt.scatter(xCoord,yCoord,c='red')#On affiche les points en rouge
        plt.draw()


    def draw(self) -> None:
        """
        Dessine la Forme
        """
        fig, _ = plt.subplots()
        plt.xlim(self.forme.minaxisX,self.forme.maxaxisX)
        plt.ylim(self.forme.minaxisY,self.forme.maxaxisY)
        self.drawMaillage()
        fig.canvas.mpl_connect('button_press_event', lambda event: self.addFixPoint(event.xdata, event.ydata))
        plt.show()



    def drawStep2(self,root):
        """
        Phase d'affichage permettant de modifier les points fixes
        """
        fig,ax = plt.subplots()
        plt.xlim(self.forme.minaxisX,self.forme.maxaxisX)
        plt.ylim(self.forme.minaxisY,self.forme.maxaxisY)
        self.drawMaillage()
        self.drawPointfix()
        plt.gcf().canvas.draw()
        canvas = FigureCanvasTkAgg(fig, master=root)
        inv = ax.transData.inverted()#Fonction de changement de repère (fenetre->graphe)
        canvas.get_tk_widget().pack(padx=20,side=tk.TOP, fill=tk.BOTH, expand=False)
        button = Button(root, text = 'Close the window', command = root.quit)#Boutton pour quitter proprement
        button.pack(pady = 10)
        canvas._tkcanvas.bind("<B1-Motion>",lambda event: self.interactionFixPoint(event.x, event.y,canvas,inv))#Captute des positions de la souris lorsque le clic est enfoncé


    def constructVoisin(self):
        """
        Constuit un dictionnaire de clé (vi,vj) contentant les points [vl,vr]
        """
        #Traitement des segments partagés
        dicVoisinSegment={}
        for t1 in self.maillage['triangles']:
            for t2 in self.maillage['triangles']:
                compare=np.in1d(t1,t2)
                if sum(compare)==2:
                    [vi,vj]=np.array(t1)[compare]
                    if (vi,vj) in dicVoisinSegment:
                        vi,vj=vj,vi
                    compare2=np.in1d(t2,t1)
                    [vl,vr]=np.concatenate((t1,t2))[~np.concatenate((compare,compare2))]
                    pi,pj,pl,pr=self.getPointWithIndex(vi),self.getPointWithIndex(vj),self.getPointWithIndex(vl),self.getPointWithIndex(vr)
                    ordre=triPoint(pi,pj,pl,pr)
                    dicVoisinSegment[(vi,vj)]=np.array([vl,vr])[ordre]
        self.adjSeg=dicVoisinSegment
        dicVoisinSegmentContour={}
        #Traitement du contour
        inContour=self.maillage['vertex_markers']
        print('contour : ', inContour)
        for t1 in self.maillage['triangles']:
            [p1,p2,p3]=t1
            compare=np.array([inContour[p1],inContour[p2],inContour[p3]])
            compare=np.array([bool(b) for b in compare])
            print('boucle')
            for i in range(len(compare)):
                print('compare : ', compare[i])
            if sum(compare)==3:
                cp1,cp2,cp3=self.getPointWithIndex(p1),self.getPointWithIndex(p2),self.getPointWithIndex(p3)
                ordre=triPoint(cp1,cp2,cp3,cp1)
                dicVoisinSegmentContour[(p1,p2)]=np.array([p3,"NoPoint"])[ordre]
                ordre=triPoint(cp2,cp3,cp1,cp2)
                dicVoisinSegmentContour[(p2,p3)]=np.array([p1,"NoPoint"])[ordre]
                ordre=triPoint(cp3,cp1,cp2,cp3)
                dicVoisinSegmentContour[(p3,p1)]=np.array([p2,"NoPoint"])[ordre]
            elif sum(compare)==2:
                v=np.array(t1)[~compare][0]
                i,j=np.array(t1)[compare]
                p,pi,pj=self.getPointWithIndex(v),self.getPointWithIndex(i),self.getPointWithIndex(j)
                ordre=triPoint(pi,pj,p,pi)
                dicVoisinSegmentContour[(i,j)]=np.array([v,"NoPoint"])
        self.adjSegContour=dicVoisinSegmentContour

    def Gij(self,i:int,j:int):
        """
        Calcule la matrice G pour les points vi,vj
        """
        vix,viy=self.getPointWithIndex(i)
        vjx,vjy=self.getPointWithIndex(j)
        if (i,j) in self.adjSegContour:
            l,r=self.adjSegContour[(i,j)]
            if l=="NoPoint":
                vrx,vry=self.getPointWithIndex(int(r))
                Gij=np.array([[vix,viy,vjx,vjy,0,0,vrx,vry],[viy,-vix,vjy,-vjx,0,0,vry,-vrx]])
            else:
                vlx,vly=self.getPointWithIndex(int(l))
                Gij=np.array([[vix,viy,vjx,vjy,vlx,vly,0,0],[viy,-vix,vjy,-vjx,vly,-vlx,0,0]])
        else:
            l,r=self.adjSeg[(i,j)]
            vlx,vly=self.getPointWithIndex(l)
            vrx,vry=self.getPointWithIndex(r)
            Gij=np.array([[vix,viy,vjx,vjy,vlx,vly,vrx,vry],[viy,-vix,vjy,-vjx,vly,-vlx,vry,-vrx]])
        return Gij.T

    def calculA1b1(self,w, C, coord):
        """calcul les matrices A1 et b1"""
        fait = []
        A1=[]
        b = []
        #Pour chaque segment:
        for seg in self.adjSeg:
            #si le segment n'est pas déja fait
            if(seg not in fait and (seg[1],seg[0]) not in fait):
                #on va rajouter 2 lignes dans A1
                l1 = [ 0 for i in range(len(self.maillage['vertices'])*2)]
                l2 = [ 0 for i in range(len(self.maillage['vertices'])*2)]

                #Ces deux lignes sont associe au segment ek
                point1 = self.getPointWithIndex(seg[0])
                point2 = self.getPointWithIndex(seg[1])
                ek = (point2[0] - point1[0], point2[1]-point1[1])

                #le segment va maintenant etre traite
                fait.append(seg)
                #on calcul Gk et H
                Gk = self.Gij(seg[0],seg[1])
                l,r=self.adjSeg[seg]
                H = self.calculH(Gk, ek)

                #on ajoute le bloc associe a vi
                l1[seg[0]*2] = H[0][0]
                l1[seg[0]*2+1] = H[0][1]
                l2[seg[0]*2] = H[1][0]
                l2[seg[0]*2+1] = H[1][1]

                #celui associe a vj
                l1[seg[1]*2] = H[0][2]
                l1[seg[1]*2+1] = H[0][3]
                l2[seg[1]*2] = H[1][2]
                l2[seg[1]*2+1] = H[1][3]

                #celui associe a vl
                l1[l*2] = H[0][4]
                l1[l*2+1] = H[0][5]
                l2[l*2] = H[1][4]
                l2[l*2+1] = H[1][5]

                #celui associe a vr
                l1[r*2] = H[0][6]
                l1[r*2+1] = H[0][7]
                l2[r*2] = H[1][6]
                l2[r*2+1] = H[1][7]

                #on ajoute les deux ligne dans la matrice
                A1.append(l1)
                A1.append(l2)

                #on ajoute deux nouveaux 0 dans b
                b.append(0)
                b.append(0)

        #on ajoute maintenant les points du contour
        for i,nextPoint in self.adjSegContour:
            l1 = [ 0 for i in range(len(self.maillage['vertices'])*2)]
            l2 = [ 0 for i in range(len(self.maillage['vertices'])*2)]
            Gk = self.Gij(i,nextPoint)
            point1 = self.getPointWithIndex(i)
            point2 = self.getPointWithIndex(nextPoint)
            ek = (point2[0] - point1[0], point2[1]-point1[1])
            H = self.calculH(Gk, ek)
            l,r=self.adjSegContour[(i,nextPoint)]

            #on ajoute le bloc associe a vi
            l1[i*2] = H[0][0]
            l1[i*2+1] = H[0][1]
            l2[i*2] = H[1][0]
            l2[i*2+1] = H[1][1]

            #celui associe a vj
            l1[nextPoint*2] = H[0][2]
            l1[nextPoint*2+1] = H[0][3]
            l2[nextPoint*2] = H[1][2]
            l2[nextPoint*2+1] = H[1][3]

            if l=="NoPoint":
                #celui associe a vr
                r = int(r)
                l1[r*2] = H[0][6]
                l1[r*2+1] = H[0][7]
                l2[r*2] = H[1][6]
                l2[r*2+1] = H[1][7]
            else:
                l = int(l)
                #celui associe a vl
                l1[l*2] = H[0][4]
                l1[l*2+1] = H[0][5]
                l2[l*2] = H[1][4]
                l2[l*2+1] = H[1][5]

            A1.append(l1)
            A1.append(l2)
            #on ajoute deux nouveaux 0 dans b
            b.append(0)
            b.append(0)

        #on ajoute maintenant la partie point fixe de la matrice
        for p in self.FixPoint:
            l1 = [ 0 for i in range(len(self.maillage['vertices'])*2)]
            l2 = [ 0 for i in range(len(self.maillage['vertices'])*2)]
            l1[2*p] = w
            l2[2*p+1]= w

            #on ajoute les deux ligne dans la matrice
            A1.append(l1)
            A1.append(l2)

            #on ajoute 2 lignes dans b
            if(p!=C):
                b.append(w * self.getPointWithIndex(p)[0])
                b.append(w * self.getPointWithIndex(p)[1])
            else:
                b.append(w*coord[0])
                b.append(w*coord[1])

        return np.array(A1),np.transpose(np.array(b))


    def calculNewCoordinate(self, w, C, coord):
        """calcul la nouvelle position de chaque point"""

        #on construit A1 et b1
        A1,b1 = self.calculA1b1(w, C, coord)
        #on construit la matrice de l'equation
        A = np.matmul(np.transpose(A1),A1)
        b = np.matmul(np.transpose(A1),b1)

        #on resoud l'equation
        vprime =  np.linalg.solve(A, b)

        #on fixe le scale
        A2,b2_x,b2_y = self.CalculA2B2(vprime,w,C,coord)
        A = np.matmul(np.transpose(A2),A2)
        b_x = np.matmul(np.transpose(A2),b2_x)
        b_y = np.matmul(np.transpose(A2),b2_y)

        vx = np.linalg.solve(A, b_x)
        vy = np.linalg.solve(A, b_y)

        return(vx,vy)


    def calculH(self,G,ek):
        """On calcul H pour un segment ek associé a une matrice G"""
        M = np.array([[-1,0,1,0,0,0,0,0],
                      [0,-1,0,1,0,0,0,0]])

        mat2 = np.array([[ek[0], ek[1]],[ek[1], -ek[0]]])

        mat3 = np.matmul(np.transpose(G),G)
        mat3 = np.linalg.inv(mat3)
        mat3 = np.matmul(mat3,np.transpose(G))

        M = M - np.matmul(mat2,mat3)


        return M

    def CalculA2B2(self,vprime, w, C, coord):

        fait = []
        A2=[]
        b2_x = []
        b2_y = []
        #Pour chaque segment:
        for seg in self.adjSeg:
            #si le segment n'est pas déja fait
            if(seg not in fait or (seg[1],seg[0]) not in fait):
                #on va rajouter 2 lignes dans A1
                l1 = [ 0 for i in range(len(self.maillage['vertices']))]

                #Ces deux lignes sont associe au segment ek
                point1 = self.getPointWithIndex(seg[0])
                point2 = self.getPointWithIndex(seg[1])
                ek = (point2[0] - point1[0], point2[1]-point1[1])

                #le segment va maintenant etre traite
                fait.append(seg)

                #on calcul Gk
                Gk = self.Gij(seg[0],seg[1])

                #on calcul l et r
                l,r=self.adjSeg[seg]

                #on prend v'i, 'vj, v'l, v'r grace a v'
                i = seg[0]
                j = seg[1]

                vi = (vprime[2*i], vprime[2*i+1])
                vj = (vprime[2*j], vprime[2*j+1])
                vl = (vprime[2*l],vprime[2*l+1])
                vr = (vprime[2*r],vprime[2*r+1])

                #on a [v'i,
                #      v'j,
                #      v'l,
                #      v'r]
                coordinates = [vi[0],vi[1],vj[0],vj[1],
                         vl[0],vl[1],vr[0],vr[1]]
                coordinates = np.transpose(np.array(coordinates))

                #on calcul Gkt * Gk
                mat3 = np.matmul(np.transpose(Gk),Gk)
                #on calcul (Gkt*Gk)-1
                mat3 = np.linalg.inv(mat3)
                #on calcul mat3 [ck, sk]
                mat3 = np.matmul(mat3,np.transpose(Gk))
                mat3 = np.transpose(np.matmul(mat3,coordinates))
                ck = mat3[0]
                sk = mat3[1]

                #on calcul Tk
                a = 1/(ck**2 + sk**2)
                Tk = [[a*ck, a * sk],
                     [-a*sk, a*ck]]

                #Calcul de A2
                #on veut calculer vi''-vj'' - T'i ek
                l1[i] = -1 #vi''
                l1[j] = 1 #-vj''

                #on ajoute la ligne dans A2
                A2.append(l1)

                #calcul de b
                #ek [ekx,
                #    eky]
                ek = np.transpose(np.array(ek))
                #b = Tkek
                ek = np.transpose(np.matmul(Tk,ek))
                #on ajoute dans b2_x et b2_y
                b2_x.append(ek[0])
                b2_y.append(ek[1])


        #on ajoute maintenant les points du contour
        for i,nextPoint in self.adjSegContour:
            #on ajoute une nouvelle ligne dans A et b
            l1 = [ 0 for i in range(len(self.maillage['vertices']))]
            #on calcul Gk
            Gk = self.Gij(i,nextPoint)
            #on calcul ek
            point1 = self.getPointWithIndex(i)
            point2 = self.getPointWithIndex(nextPoint)
            ek = (point2[0] - point1[0], point2[1]-point1[1])

            #on calcul l et r
            l,r=self.adjSegContour[(i,nextPoint)]

            #on calcul v'i
            vi = (vprime[i*2],vprime[i*2+1])
            #v'j
            vj = (vprime[nextPoint*2],vprime[nextPoint*2+1])
            #v'l et v'r
            if l=="NoPoint":
                r = int(r)
                vl = (0,0)
                vr = (vprime[r*2],vprime[r*2+1])
            else:
                l = int(l)
                vr = (0,0)
                vl = (vprime[l*2],vprime[l*2+1])

            #on a [v'i,
            #      v'j,
            #      v'l,
            #      v'r]
            coordinates = [vi[0],vi[1],vj[0],vj[1],
                     vl[0],vl[1],vr[0],vr[1]]
            coordinates = np.transpose(np.array(coordinates))

            #on calcul Gkt * Gk
            mat3 = np.matmul(np.transpose(Gk),Gk)
            #on calcul (Gkt * Gk)-1
            mat3 = np.linalg.inv(mat3)
            mat3 = np.matmul(mat3,np.transpose(Gk))

            #on calcul ck, sk
            mat3 = np.transpose(np.matmul(mat3,coordinates))
            ck = mat3[0]
            sk = mat3[1]
            #on calcul Tk
            a = 1/(ck**2 + sk**2)
            Tk = [[a*ck, a * sk],
                 [-a*sk, a*ck]]

            #v''i - v''j
            l1[i] = -1
            l1[nextPoint] = 1

            A2.append(l1)

            #calcul de b2
            ek = np.transpose(np.array(ek))
            ek = np.transpose(np.matmul(Tk,ek))

            b2_x.append(ek[0])
            b2_y.append(ek[1])

        #on ajoute maintenant la partie point fixe de la matrice
        for p in self.FixPoint:
            l1 = [ 0 for i in range(len(self.maillage['vertices']))]
            l1[p] = w

            #on ajoute les deux ligne dans la matrice
            A2.append(l1)

            #on ajoute 2 lignes dans b
            if(p!=C):
                b2_x.append(w * self.getPointWithIndex(p)[0])
                b2_y.append(w * self.getPointWithIndex(p)[1])
            else:
                b2_x.append(w*coord[0])
                b2_y.append(w*coord[1])
        return np.array(A2), np.array(b2_x), np.array(b2_y)
