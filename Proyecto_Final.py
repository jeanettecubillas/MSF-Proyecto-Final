"""
Proyecto Final: Sistema Renal- Síndrome Nefrótico

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Jeanette Cubillas Arteaga
Número de control: 20212948
Correo institucional: l20212948@tectijuana.edu.mx

Nombre del alumno: Kenya Fernanda Rodriguez Castro
Número de control: 20213058
Correo institucional: kenya.rodriguez201@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

# Librerías para cálculo numérico y generación de gráficas
import numpy as np 
import math as m 
import matplotlib.pyplot as plt 
import control as ctrl

x0,t0,tF,dt,w,h = 0,0,10,1E-3,10,5
N = round((tF-t0)/dt)+1 #Numero total de iteraciones
t = np.linspace(t0,tF,N) #Arreglo del tiempo de 0:dt:10 segundos

def sys_renal(Cs,Rs,Ls,Ra,Rm,Cv):
    alpha3 = Cs*Cv*Ls*Rm
    alpha2 = Cs*Cv*Ra*Rm+Cs*Cv*Rm*Rs+Cs*Ls
    alpha1 = Cs*Ra+Cs*Rm+Cv*Rm+Cs*Rs
    alpha0 = 1
    num = [Cs*Rs,1]
    den = [alpha3, alpha2, alpha1, alpha0]
    return ctrl.tf(num, den)

# Individuo sano (control)
Cs,Rs,Ls,Ra,Rm,Cv= 1E-6, 60, 10E-3, 480, 10, 47E-6
sysN = sys_renal(Cs,Rs,Ls,Ra,Rm,Cv)
print('Individuo sano [control]:')
print(sysN)

# Individuo enfermo (síndrome nefrótico)
Cs,Rs,Ls,Ra,Rm,Cv= 10E-6, 180, 10E-3, 480, 10, 47E-6
sysE = sys_renal(Cs,Rs,Ls,Ra,Rm,Cv)
print('Individuo enfermo (caso):')
print(sysE)

# Controlador
Cr=1E-9
Re=2.4767E5
Rr=4.0074E7
Ce=5.5894E-9
numPID = [Rr*Re*Cr*Ce,Re*Ce+Rr*Cr,1]
denPID = [Re*Cr,0]
PID = ctrl.tf(numPID,denPID)
#Sistema de control: Tratamiento
X=ctrl.series(PID,sysE)
sysPID = ctrl.feedback(X,1,sign = -1)
print(sysPID)

# Colores
Morado = [70/255, 53/255, 177/255]
Verde = [62/255, 123/255, 39/255]
Rosa = [255/255, 116/255, 139/255]
Azul = [7/255, 71/255, 153/255]

u= 2*np.sin(m.pi*2*t)
u1= np.sin(m.pi*2*t)

ts,Vs = ctrl.forced_response(sysN,t,u,x0)
plt.plot(t,Vs, '-', color = Morado, label = '$V_S(t): Control$')
ts,Vs = ctrl.forced_response(sysE,t,u1,x0)
plt.plot(t,Vs, '-', color = Rosa, label = '$V_S(t): Caso$')
ts,Vs = ctrl.forced_response(sysPID,t,u,x0)
plt.plot(t,Vs, ':', color = Verde, linewidth=3,label = '$V_S(t): Tratamiento$')

plt.grid(True)
plt.xlim(0, 10)
plt.ylim(-2, 2.1)
plt.xticks(np.arange(0, 11, 1.0))
plt.yticks(np.arange(-2, 2.1, 0.5))
plt.xlabel('$t$ $[s]$')
plt.ylabel('$V_s(t)$ $[V]$')
plt.title('Sistema Renal - Sano VS. Síndrome Nefrótico')
plt.legend(bbox_to_anchor=(0.5,-0.23),loc='center',ncol=4)
plt.show()
fig = plt.figure()
fig.set_size_inches(w,h)
fig.tight_layout()
fig.savefig('python.png', dpi = 600,bbox_inches='tight')
fig.savefig('python.pdf', dpi = 600,bbox_inches='tight')

