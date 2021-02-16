import os
import sys
import shlex
import subprocess as sp
from subprocess import Popen

# programs = ["Sequential.cpp", "Barriers.cpp", "Lock_variant_1b.cpp", "Lock_variant_2b.cpp", "No_Sync_b.cpp"]
#programs = ["Sequential.cpp", "Barriers.cpp", "Lock_variant_fine_grained.cpp", "No_Sync.cpp", "Barrier_helper.cpp", "Barrier_KK.cpp", "No_Sync_KK.cpp", "Barrier_helper_KK.cpp", "Barriers_sleep.cpp", "Barrier_helper_sleep.cpp", "Barrier_helper_td_fail.cpp"]
#programs = ["Sequential.cpp", "Barriers.cpp", "No_Sync.cpp", "Barrier_helper.cpp", "Barrier_KK.cpp", "No_Sync_KK.cpp"]
#programs = ["Barrier_identical.cpp"]
#programs = ["No_Sync_identical.cpp"]
#programs = ["No_Sync.cpp", "Barrier_helper.cpp"]
# Add more input files here along with start nodes and max nodes
#input_files = ["web-Stanford.txt", "web-Notre.txt", "web-BerkStan.txt","web-Google.txt","10.txt", "20.txt", "30.txt", "40.txt", "50.txt", "60.txt", "70.txt", "RMAT_21.txt","RMAT_22.txt","RMAT_23.txt"]
#start_nodes = [1,1,1,0,0,0,0,0,0,0,0,0,0,0]
#max_nodes = [9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000]
#input_files = ["web-Stanford.txt", "web-Notre.txt", "web-BerkStan.txt","web-Google.txt","10.txt", "20.txt", "30.txt", "40.txt", "50.txt", "60.txt", "70.txt", "RMAT_21.txt","RMAT_22.txt"]
#start_nodes = [1,1,1,0,0,0,0,0,0,0,0,0,0]
#max_nodes = [9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000]
#input_files = ["road-italy-osm.txt","great-britain_osm.txt","asia_osm.txt","germany_osm.txt"]
#start_nodes = [0,0,0,0]
#max_nodes = [9000000,9000000,90000000,9000000]
#start_nodes = [0,0,0]
#max_nodes = [9000000,9000000,9000000]
#input_files = ["soc-LiveJournal1.txt", "soc-Epinions1.txt", "Slashdot0811.txt", "Slashdot0902.txt"]
#start_nodes = [0,0,0,0]
#max_nodes = [9000000,9000000,9000000,9000000,9000000]

#programs = ["Sequential.cpp","Barriers.cpp","Barrier_identical.cpp","No_Sync.cpp","No_Sync_identical.cpp","Barrier_helper.cpp"]
programs = ["Barrier_identical.cpp","No_Sync_identical.cpp"]
threads = [7, 14, 21, 28, 32, 56] 
input_files = ["web-Stanford.txt", "web-Notre.txt", "web-BerkStan.txt","web-Google.txt","soc-LiveJournal1.txt", "soc-Epinions1.txt", "Slashdot0811.txt", "Slashdot0902.txt","road-italy-osm.txt","great-britain_osm.txt","asia_osm.txt","germany_osm.txt","10.txt", "20.txt", "30.txt", "40.txt", "50.txt", "60.txt", "70.txt", "RMAT_21.txt","RMAT_22.txt"]
start_nodes = [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
max_nodes = [9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000,9000000]

for program in programs :
	cmd1 = "g++ -std=c++11 -pthread " + program
	print cmd1
	cmd1 = Popen(cmd1.split(), stdin=sp.PIPE, stdout=sp.PIPE)
	cmd1.wait()

	for i in range (len(input_files)) :
		if program == "Sequential.cpp" :
			for count in range(0, 1) :
				cmd2 = "./a.out " + input_files[i] + " " + str(start_nodes[i]) + " " + str(max_nodes[i]) + " 50"
				print cmd2
				cmd2 = Popen(cmd2.split(), stdin=sp.PIPE, stdout=sp.PIPE)
				cmd2.wait()

				cmd3 = "mv " + program[:-4] + "_out.txt " + program[:-4] + "_" + input_files[i][:-4] + "_pg_" + str(count) + ".txt"
				cmd3 = Popen(cmd3.split(), stdin=sp.PIPE, stdout=sp.PIPE)
				cmd3.wait()
		elif program in ["Barrier_KK.cpp", "Barrier_helper_KK.cpp", "No_Sync_KK.cpp", "Barrier_identical.cpp", "No_Sync_identical.cpp"] :
			#cmd2 = "python3 identical.py " + input_files[i]
			#print cmd2
			#cmd2 = Popen(cmd2.split(), stdin=sp.PIPE, stdout=sp.PIPE)
			#cmd2.wait()

			for thd_num in threads :
				for count in range(0, 3) :
					cmd3 = "./a.out " + input_files[i] + " " + str(thd_num) + " " + str(start_nodes[i]) + " " + str(max_nodes[i]) + " 50 " + input_files[i][:-4] + "_rep_map.txt"
					print cmd3
					cmd3 = Popen(cmd3.split(), stdin=sp.PIPE, stdout=sp.PIPE)
					cmd3.wait()

					cmd4 = "mv " + program[:-4] + "_out.txt " + program[:-4] + "_" + input_files[i][:-4] + "_thd_" + str(thd_num) + "_" + str(count) + ".txt"
					cmd4 = Popen(cmd4.split(), stdin=sp.PIPE, stdout=sp.PIPE)
					cmd4.wait()
		else :
			for thd_num in threads :
				for count in range(0, 3) :
					cmd2 = "./a.out " + input_files[i] + " " + str(thd_num) + " " + str(start_nodes[i]) + " " + str(max_nodes[i]) + " 50"
					print cmd2
					cmd2 = Popen(cmd2.split(), stdin=sp.PIPE, stdout=sp.PIPE)
					cmd2.wait()

					cmd3 = "mv " + program[:-4] + "_out.txt " + program[:-4] + "_" + input_files[i][:-4] + "_thd_" + str(thd_num) + "_" + str(count) + ".txt"
					cmd3 = Popen(cmd3.split(), stdin=sp.PIPE, stdout=sp.PIPE)
					cmd3.wait()

