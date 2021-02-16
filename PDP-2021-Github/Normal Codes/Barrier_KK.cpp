#include <pthread.h>
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
#include <fstream>
#include <stack> 
#include <map>

using namespace std;

vector<int> A; 
vector<int> IA;
vector<int> JA;
vector<int> out_edges;
vector<int> no_out_edges;
vector<double> page_rank_prev, page_rank;
int nodes = 0, max_nodes = 400000;
double error = 1.000, thershold=0.0000000001,damping_factor=0.85;
int thdnum = 4;
double pg_no_out_edges = 0;
pthread_barrier_t b;
int start_node = 0;
vector<double> th_error, th_sum;
int iterations = 0;
int iteration_threshold = 10;

vector<vector<int>> in_edge;
vector<vector<int>> out_edge;
vector<int> in_edges;
vector<int> chain;
vector<int> Stack;
vector<int> visited;
vector<int> red;
vector<int> weight;
vector<int> rep_map;
// map<int, int> rep_map;
double prev_pg_no_out = 0;

void topoSort(int node) {

	visited[node] = 1;

	for(int i=0;i<out_edge[node].size();i++) {
		if(in_edges[out_edge[node][i]]==1&&out_edges[out_edge[node][i]]==1) {
			if(visited[out_edge[node][i]]==0) 
				topoSort(out_edge[node][i]);
		}
	}

	Stack.push_back(node);
}

void chainNodes() {
	for(int i=start_node;i<=nodes;i++) {
		if(in_edges[i]==1&&out_edges[i]==1) chain.push_back(i);
	}

	//Stack.resize(chain.size(),0);
	visited.resize(max_nodes,0);
	for(int i=0;i<chain.size();i++) {
		if(visited[chain[i]]==0)
			topoSort(chain[i]);
	}

	red.resize(max_nodes,-1);
	weight.resize(max_nodes,-1);

	for(int i=Stack.size()-1;i>=0;i--)
    { 
        int node = Stack[i];
        int c = in_edge[node][0];
        if(in_edges[c]==1&&out_edges[c]==1)  {
        	red[node] = red[c];
        	weight[node] = weight[c] + 1;
        }
        else {
        	red[node] = in_edge[node][0];
        	weight[node] = 1;
        }
        //Stack.pop(); 
    }
}


void print_vector(vector<double> vec) {
	for(int i=start_node;i<vec.size();i++) {
		cout<<vec[i]<<" ";
	}
	cout<<"\n";
}

void *thread_page_rank(void* thdnumber) {
	int *thdid = (int *)thdnumber;
	// while(error>thershold) {
	while(iterations < iteration_threshold) {
		th_error[*thdid] = 0;
		for(int i=*thdid+start_node;i<=nodes;i=i+thdnum) {
			if(red[i]==-1) {
				page_rank[i] = damping_factor/(nodes);
				//cout<<page_rank[i]<<" ";
				for(int j=IA[i-1];j<IA[i];j++) {
					//cout<<j<<" ";
					// if(red[JA[j]]!=-1 && rep_map[i] == i) {
					if(red[JA[j]]!=-1) {
						page_rank[JA[j]] = damping_factor/(nodes);
						// page_rank[JA[j]] = page_rank[JA[j]] + page_rank_prev[rep_map[red[JA[j]]]]/out_edges[red[JA[j]]] * pow((1-damping_factor),weight[JA[j]]);
						page_rank[JA[j]] = page_rank[JA[j]] + page_rank_prev[red[JA[j]]]/out_edges[red[JA[j]]] * pow((1-damping_factor),weight[JA[j]]);
						page_rank[JA[j]] = page_rank[JA[j]] + (1 - damping_factor - pow((1-damping_factor),weight[JA[j]]))/(nodes);
					}
					// page_rank[i] = page_rank[i] + page_rank_prev[rep_map[JA[j]]]/out_edges[JA[j]] * (1-damping_factor);
					page_rank[i] = page_rank[i] + page_rank_prev[JA[j]]/out_edges[JA[j]] * (1-damping_factor);
					//page_rank[i] = page_rank[i] + page_rank_prev[JA[j]]/out_edges[JA[j]];
				}
				th_error[*thdid] = max(th_error[*thdid],fabs(page_rank[i]-page_rank_prev[i]));
			}
			
		}
		pthread_barrier_wait(&b);

		if(*thdid==0) {
			iterations++;
			error = 0;
			for(int i=0;i<thdnum;i++)
				error = max(error,th_error[i]);

			page_rank_prev = page_rank;
		}
		pthread_barrier_wait(&b);

	}

};

void compute_page_rank() {
	int iterations = 0;

	pthread_t threads[thdnum];
	int thdid[thdnum];
	pthread_barrier_init(&b, 0, thdnum);
	th_error.resize(thdnum,0);

	for (int i = 0; i < thdnum; ++i) {
		thdid[i] = i;
		pthread_create(&threads[i], NULL, thread_page_rank, (void *)&thdid[i]);
	}

	for (int i = 0; i < thdnum; ++i) {
		pthread_join(threads[i], NULL);
	}
	pthread_barrier_destroy(&b);
}

bool comparePair(pair<double,double> i1, pair<double,double> i2) 
{ 
    return (i1.first > i2.first); 
} 


int main(int argc, char** argv)
{
	string filename = "", line, filename2 = "";
	if(argc == 7) {
		filename = argv[1];
		thdnum = atoi(argv[2]);
		start_node = atoi(argv[3]);
		max_nodes = atoi(argv[4]);
		iteration_threshold = atoi(argv[5]);
		filename2 = argv[6];
	}
	else {
		cout << "Check the arguments\n";
		return 0;
	}

	
	fstream file;
	file.open(filename.c_str());
	IA.resize(max_nodes,0);
	out_edges.resize(max_nodes,0);

	in_edge.resize(max_nodes,vector<int>());
	out_edge.resize(max_nodes,vector<int>());
	in_edges.resize(max_nodes,0);
	rep_map.resize(max_nodes+1,0);


	while(getline(file, line)){
	istringstream iss(line);
	        vector<int> tokens{istream_iterator<int>{iss}, istream_iterator<int>{}};
	        A.push_back(1);
	        JA.push_back(tokens[1]);
	        IA[tokens[0]]++;
	        out_edges[tokens[1]]++;
	        nodes = max(nodes,tokens[0]);
	        nodes = max(nodes,tokens[1]);

	        in_edge[tokens[0]].push_back(tokens[1]);
	        out_edge[tokens[1]].push_back(tokens[0]);
	        in_edges[tokens[0]]++;
	}
	file.close();

	file.open(filename2.c_str());
	while(getline(file, line)) {
		istringstream iss(line);
	    vector<int> tokens{istream_iterator<int>{iss}, istream_iterator<int>{}};
	    rep_map[tokens[0]] = tokens[1];
	}
	file.close();

	for(int i=1;i<IA.size();i++) {
		IA[i] = IA[i] + IA[i-1];
	}

	chainNodes(); 

	page_rank_prev.resize(nodes+1,1.0000/(nodes+1));
	page_rank.resize(nodes+1,0);

	struct timeval startwtime, endwtime;
    gettimeofday (&startwtime, NULL);

	compute_page_rank();

	gettimeofday (&endwtime, NULL);

	double time = (double)((endwtime.tv_usec - startwtime.tv_usec)/1.0e6
              + endwtime.tv_sec - startwtime.tv_sec);

	for(int i=Stack.size()-1;i>=0;i--) {
		// if(page_rank[Stack[i]]==0 && rep_map[Stack[i]] == Stack[i]) {
		if(page_rank[Stack[i]]==0) {
			int j = Stack[i];
			page_rank[j] = damping_factor/(nodes);
			// page_rank[j] = page_rank[j] + page_rank_prev[rep_map[red[j]]]/out_edges[red[j]] * pow((1-damping_factor),weight[j]);
			page_rank[j] = page_rank[j] + page_rank_prev[red[j]]/out_edges[red[j]] * pow((1-damping_factor),weight[j]);
			page_rank[j] = page_rank[j] + (1 - damping_factor - pow((1-damping_factor),weight[j]))/(nodes);
			// page_rank[j] = page_rank[j] + prev_pg_no_out * (1-damping_factor)* (pow((1-damping_factor),weight[j]) - 1)/(-damping_factor);
		}
	}

	// for(int i = start_node ; i <= nodes ; i++) {
	// 	if(rep_map[i] != i) {
	// 		page_rank[i] = page_rank[rep_map[i]];
	// 	}
	// }

	// double sum = 0;
	// for(int i=start_node;i<=nodes;i++) sum = sum + page_rank[i];

	std::ofstream outFile("Barrier_KK_out.txt");
	outFile << time << "\n";
	outFile << iterations << "\n";
	// outFile << sum << "\n";
	for(int i = start_node; i <= nodes; i++)
		outFile << page_rank[i] << "\n";
}
