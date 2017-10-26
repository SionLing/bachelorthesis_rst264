import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np
import time
import pandas as pd
import math
import sim2net.packet_loss.gilbert_elliott as sim
from global_variables import *

# header which is used in case of nom_dist
norm_dist_header = ['id', 'frame_id', 'arrival_time', 'deadline', 'lost']

# header which is used in case of gilbert_elliott
gilber_elliott_header = ['packed_id','frame','id','lost']

default_csv_dir = project_path + "output/"

def simulate_packet_loss_norm_dist(buffer, seed, filename, fps=30, mean=0.125, std=0.025, max_delay=0.15,csv_dir = default_csv_dir):


    np.random.seed(seed)

    # Ein Frame (identifiziert durch nummer i) besteht aus x_i Paketen der Länge l_i

    #  Die Anzhal der Pakete pro frame ist iid
    #  Annahme für diesen Fall: Die Anzhal der Pakete pro Frame ist Gleichverteilt

    #  Die Längen l_i seien konstant 512 Byte

    # numPackets_rv enthält für jedes Frame die Anzhal der Pakete
    # In meinem Anwendungsfall lassen sich hier reale Zhalen ermitteln:
    # Es ist die Anzhal der RTP-Pakete die für eine Accessunit benötigt wird (bei gegebener Max. Länge)
    numPackets_rv = list(map(lambda x: len(x),buffer))
    frame_id = np.array(range(len(buffer)))

    # proc_time gibt für jedes Frame an um wie viel Zeit es nach beginn versendet werden soll
    proc_time = frame_id / fps

    # jedes Paket wird gemäß einer Normalverteilung verzögert
    # Bsp: Mittelwert 125ms (0.125) und Standardabweichung 0.025
    # Wir gehen von einem maximal erlaubten Delay von 150ms aus

    numOfPackets = np.sum(numPackets_rv)
    packet_id = np.array(range(numOfPackets))

    myclip_a, myclip_b = (0, 5)

    a, b = (myclip_a - mean) / std, (myclip_b - mean) / std

    # in delay_rvs ist für jedes Paket gemäß einer Normalverteilung dessen Delay angegeben
    delay_rvs = stats.truncnorm.rvs(a, b, loc=mean, scale=std, size=numOfPackets)

    # wann kommen die Pakete nun beim Empfaenger an?
    # Um das rauszubekommen muessen wir erstmal wissen, wann die Pakete vom Encoder
    # an den Sender uebergeben werden

    # proc_packet gibt die Zeit an zu der ein Paket versendet werden soll
    # sie richtet sich nach der Zeit für das jeweilige Frame
    proc_packet = np.repeat(proc_time, numPackets_rv)

    # das Delay bzw. die simulierte Ankunftszeit eines einzelnen Pakets ergibt sich aus
    # Zeit an der es losgeschickt wird + zufälliges Delay
    proc_delayed = proc_packet + delay_rvs

    # Die Deadlines für ein jeweiliges Paket ergeben sich aus:
    # Zeit and der Paket versendet wird + max. Verzögerung des Paketes
    deadlines = proc_packet + max_delay


    arrival_deadline_array = list(zip(proc_delayed,deadlines))
    drop_list = list(map(lambda x: x[0] > x[1],arrival_deadline_array))

    # Speichern der Simulation in einer csv Datei
    csv_file = open(csv_dir + filename + '.csv', 'w')
    csv_file.write("seed: " + str(seed) + "\n")
    csv_file.write("fps: " + str(fps) + "\n")
    csv_file.write("mean: " + str(mean) + "\n")
    csv_file.write("std: " + str(std) + "\n")
    csv_file.write("max_delay: " + str(max_delay) + "\n")
    csv_file.write(str(norm_dist_header) + '\n')
    csv_file.write("total packets: " + str(len(drop_list)) + "\n")
    csv_file.write("lost packets: " + str(len(list(filter(lambda x: x,drop_list)))) + "\n")
    csv_file.close()

    packet_times = []
    id = 0
    frame_id = 0
    for num_packets in numPackets_rv:
        for j in range(num_packets):
            arrival_time = proc_delayed[id]
            deadline = deadlines[id]
            lost = arrival_time > deadline

            df = pd.DataFrame([id, frame_id, arrival_time, deadline, lost]).T
            df.to_csv(csv_dir + filename + '.csv',mode='a',header=False)
            packet_times.append(df)

            id += 1
        frame_id += 1

    return drop_list

def simulate_packet_loss_guilbert_eliot(buffer,filename, p=0.00001333, r=0.00601795, h=0.55494900, k=0.99999900,csv_dir = default_csv_dir):
    g_e_model = sim.GilbertElliott((p,r,h,k))
    num_packets = sum(list(map(lambda x: len(x),buffer)))
    numPackets_rv = list(map(lambda x: len(x), buffer))

    lost_array = []
    for i in range(num_packets):
        temp = g_e_model.packet_loss()
        lost_array.append(temp)

    f = open(csv_dir + filename + '.csv', 'w')
    f.write("gilber_elliott\n")
    f.write("p: " + str(p) + "\n")
    f.write("r: " + str(r) + "\n")
    f.write("h: " + str(h) + "\n")
    f.write("k: " + str(k) + "\n")
    f.write(str(gilber_elliott_header) + "\n")
    f.write("total packets: " + str(num_packets) + "\n")
    f.write("lost packets: " + str(sum(list(map(lambda x: 1 if x else 0,lost_array)))) + "\n")
    f.close()

    packet_id = 0
    frame_id = 0
    for num_pack in numPackets_rv:
        for i in range(num_pack):
            df = pd.DataFrame([packet_id, frame_id, lost_array[packet_id]]).T
            df.to_csv(csv_dir + filename + '.csv', mode='a', header=False)
            packet_id += 1
        frame_id += 1

def read_loss_array_from_csv(filepath):
    header = []
    skiprows = 0
    if("elliot" in filepath):
        header = gilber_elliott_header
        skiprows = 3
    elif("nrom_dist"):
        header = norm_dist_header
        skiprows = 8

    csv_file = pd.read_csv(filepath, skiprows=skiprows,names=header)

    return csv_file['lost'].values








































