#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <omp.h>

#include <bitset>
#include <cstdlib>
#include <iostream>
#include <atomic>
#include <mutex>
#include <vector>
#include <sstream>
#include <fstream>
#include <string>
#include <algorithm>
#include <iterator>
#include <cmath> 
#include <sys/time.h>
#include <bits/stdc++.h>

using namespace std;


int main(int argc, char** argv)
{
	string filename = "", line;
	int max_nodes;

	if(argc == 3) {
		filename = argv[1];
		max_nodes = atoi(argv[2]);
	}
	else {
		cout << "Check the arguments\n";
		return 0;
	}

	vector<vector<int>> edges;
	fstream file;
	file.open(filename.c_str());
	

	edges.resize(max_nodes,vector<int>());


	while(getline(file, line)){
	istringstream iss(line);
	        vector<int> tokens{istream_iterator<int>{iss}, istream_iterator<int>{}};
	        edges[tokens[0]].push_back(tokens[1]);
	}
	file.close();

	ofstream outfile(filename.substr(0,filename.size()-4)+"_Sort.txt");

	for(int i=0;i<edges.size();i++) {
		for(int j=0;j<edges[i].size();j++) {
			outfile<<i<<" "<<edges[i][j]<<"\n";
		}
	}

	outfile.close();
}