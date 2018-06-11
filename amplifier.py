## Amplifier design
import random
import math
import numpy
import sys

maxiter=100000000
Vcc =10
beta=100
Vbe =0.7
Vth =0.025

des_gain=25
des_rin =10000
des_rout=100

R1=100000
R2=100000
R3=200
R4=1000
R=[R1, R2, R3, R4]

def find_parameters(Vcc, beta, Vbe, Vth, R):
    #small signal parameters
    Ic=(Vcc * R[1] / (R[0] + R[1]) - Vbe) / (R[1] * R[0] / (R[0] + R[1]) + R[3] * (beta+1)) * beta
    gm=Ic/Vth
    rt=beta/(beta+1)/gm

    Gain=(rt/(rt+R[3])*gm*R[2])
    R_out=R[2]
    R_in=R[0]*R[1]/(R[0]+R[1])

    return [Gain, R_in, R_out]

def perturb(R):
    a0 = R[0]*(random.random()+0.5)
    a1 = R[1]*(random.random()+0.5)
    a2 = R[2]*(random.random()+0.5)
    a3 = R[3]*(random.random()+0.5)

    return [a0, a1, a2, a3]

def distance_calculation(Gain, R_in, R_out, des_gain, des_rin, des_rout):
    gain_dis = (Gain-des_gain)**2
    r_in_dis = (R_in-des_rin)**2
    rout_dis = (R_out-des_rout)**2

    total_dis = gain_dis + r_in_dis + rout_dis
    total_dis = math.sqrt(total_dis)

    return total_dis

for i in range(maxiter):

    R_old = R

    if i==0:
        [Gain, R_in, R_out] = find_parameters(Vcc, beta, Vbe, Vth, R)
        distance = distance_calculation(Gain, R_in, R_out, des_gain, des_rin, des_rout)
        continue
    else:
        R = perturb(R)
        [Gain, R_in, R_out] = find_parameters(Vcc, beta, Vbe, Vth, R)
        distance_p = distance
        distance = distance_calculation(Gain, R_in, R_out, des_gain, des_rin, des_rout)
        if(distance < distance_p):
            R=R
        else:
            if(numpy.exp(-distance)*100>75):
                break
            distance=distance_p
            R=R_old
        sys.stdout.write("Similarity : %.2f %%  Iteration: %.2f %% \r" %(numpy.exp(-distance)*100, i/maxiter*100))
        sys.stdout.flush()

print("\n\nGain : %.2f\n" %Gain)
print("R_in : %.3f k\n" %(R_in/1000))
print("R_out: %.3f k\n" %(R_out/1000))
print(R)
