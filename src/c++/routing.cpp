#include <iostream>
#include <vector>
#include <algorithm>    // std::reverse
#include <stdexcept>
#include <fstream>
#include <math.h>       /* exp */
#include "cxxopts.hpp"


#define TRUE 1
#define FALSE 0

// Represent a terminal node (ie. 'N3')
struct Terminal{
    char dir;
    int val;
    Terminal(){};
    Terminal(char d,int v){
        dir = d;
        val = v;
    };     
    bool operator==(const Terminal& x) const
    {
        return (dir == x.dir && val == x.val);
    };
       
};

// RouteID contains the source and destination terminals (ie. 'N3<->S1')
struct RouteID{
    Terminal src;
    Terminal dest; 
    RouteID(){};
    RouteID(Terminal src_, Terminal dest_){
        src = src_;
        dest = dest_;
    };
    // Two routes are equal if either source or dest are equal (same net)
    bool operator==(const RouteID& x) const
    {
        return (src==x.src || src==x.dest || dest==x.src || dest==x.dest);
    };
    void print(){std::cout << "('" << src.dir << "'," << src.val << ") to ('" << dest.dir << "'," << dest.val << ")\n";}
};

// A node with x and y coordinate
struct Node{
    int x;
    int y;
    Node(){}
    Node(int x_,int y_){
        x = x_;
        y = y_;
    };
    bool operator==(const Node& n) const
    {
        return (x == n.x && y == n.y);
    };
    bool operator!=(const Node& n) const
    {
        return (x != n.x || y != n.y);
    };
    void print(){std::cout << "(" << x << "," << y << ")\n";}
    
};

// An edge comprising of two nodes, and a RouteID value to allow routes on same mesh to share an edge
struct Edge{
    Node a;
    Node b;
    RouteID id;
    Edge(){};
    Edge(Node a_, Node b_){
        a = a_;
        b = b_;
    };
    Edge(Node a_, Node b_, RouteID id_){
        a = a_;
        b = b_;
        id = id_;
    };
    // Edges are equal regardless of the order the nodes are represented
    bool operator==(const Edge& x) const
    {
        return ((a==x.a && b==x.b)||(b==x.a && a==x.b));
    };
    void print(){std::cout << "Edge: " << a.x << "," << a.y << "-" << b.x << "," << b.y << "\n";}
};

// A route has an ID and a vector of nodes
struct Route{
    RouteID id;
    std::vector<Node> nodes;
    Route(){};
    Route(RouteID id_, std::vector<Node> nodes_){
        id = id_;
        nodes = nodes_;
    };
    void print(){
        for (int i=0;i<nodes.size();i++){
            nodes[i].print();
        }
    };
};

// Class to represent the routing problem
class SB{    
    public:
        std::vector<Route> routes;
        int width;
        std::vector<RouteID> demands;

        SB(){};
        SB(int width_){
            width = width_;
        };
        SB(int width_, std::vector<RouteID> demands_){
            width = width_;
            demands = demands_;
        };

        void resetSB(){
            routes.clear();
        };
        int setDemands(std::vector<RouteID> demands_){
            demands = demands_;
        };
        void addRoute(Route newr){
            routes.push_back(newr);
        }

        // Checks if a potential move down an edge is valid
        bool checkTurn(Node src, Node dest, RouteID id){
            Edge testedge = Edge(src,dest);
            Edge curr_edge;

            if(src==dest){
                return FALSE;
            }
            // Check if dest off the grid
            if((dest.x>width-1)||(dest.x<0)){
                return FALSE;
            }
            if((dest.y>width-1)||(dest.y<0)){
                return FALSE;
            }

            // Check the two nodes only vary by maximum of one
            if((dest.y-src.y > 1)||(dest.y-src.y < -1)){
                return FALSE;
            }

            if((dest.x-src.x > 1)||(dest.x-src.x < -1)){
                return FALSE;
            }

            // Check only one coordinate of them varies
            if((dest.x-src.x != 0) && (dest.y-src.y != 0)){
                return FALSE;
            }            

            for (int i=0;i<routes.size();i++){              
                // Move valid if of the same net
                if (routes[i].id == id){
                    continue;
                }
                // Check if edge already appears in another route
                std::vector<Node> curr_route = routes[i].nodes;
                for (int j=0;j<curr_route.size()-1;j++){
                    curr_edge = Edge(curr_route[j],curr_route[j+1]);                                        
                    if (testedge==curr_edge){
                        return FALSE;
                    }   
                }
            }
            return TRUE;
        };

        // bool checkTurn(Edge testedge, RouteID id){
        //     Edge curr_edge;
        //     for (int i=0;i<routes.size();i++){
                
        //         if (routes[i].id == id){
        //             continue;
        //         }
        //         std::vector<Node> curr_route = routes[i].nodes;
        //         for (int j=0;j<curr_route.size()-1;j++){
        //             curr_edge = Edge(curr_route[i],curr_route[i+1]);
        //             if (testedge==curr_edge){
        //                 return FALSE;
        //             }   
        //         }
        //     }
        //     return TRUE;
        // }

        // Retrive node attached to a terminal
        Node getNodeFromTerminal(Terminal t){
            Node n;
            if (t.dir=='N'){
                n = Node(t.val,0);
            }
            else if (t.dir=='E'){
                n = Node(width-1,t.val);
            }
            else if (t.dir=='S'){
                n = Node(t.val,width-1);
            }
            else if (t.dir=='W'){
                n = Node(0,t.val);
            }
            else{
                throw std::runtime_error("Invalid direction"); 
            }
            return n;
        };

        void addDemands(std::vector<RouteID> demands_){
            // for (int i = 0; i < demands_.size(); i++)
            // {
            //     char dir = demands[i].
            // }
            
            demands = demands_;
        }

        // void parseDemands(std::string filepath){
        //     std::ifstream indata;
        //     indata.open(filepath.c_str());
        //     if(!indata) { // file couldn't be opened
        //         exit(1);
        //     }
        //     Terminal src,dest;
        //     char src_dir;
        //     int src_val;
        //     char dest_dir;
        //     int dest_val;
            
        //     while ( !indata.eof() ){
        //         indata >> src_dir;
        //         indata >> src_val;
        //         indata >> dest_dir;
        //         indata >> dest_val;

        //         if(src_val>width-1 || dest_val>width-1){
        //             throw std::runtime_error("Src/Dest exceeds SB width");
        //             exit(1);
        //         }
        //         src = Terminal(src_dir,src_val);
        //         std::cout << src_dir << std::endl;
        //         dest = Terminal(dest_dir,dest_val);
        //         demands.push_back(RouteID(src,dest));
        //     }            
        // };

        void exportData(std::string filename,std::string sb_id){
            std::ofstream routefile;
            routefile.open(filename,std::ios_base::app);
            std::string x_id = sb_id.substr(0,sb_id.find(','));
            std::string y_id = sb_id.substr(sb_id.find(',')+1,sb_id.size()-sb_id.find(','));
            
            for (int i = 0; i < routes.size(); i++)
            {
                routefile << x_id << "," << y_id << ",";
                Terminal src = routes[i].id.src;
                Terminal dest = routes[i].id.dest;
                routefile << src.dir << src.val << ',';
                routefile << dest.dir << dest.val << ',';
                for (int j = 0; j < routes[i].nodes.size(); j++)
                {
                    routefile << "'" << routes[i].nodes[j].x << ',' << routes[i].nodes[j].y << "'";
                    if(j!=routes[i].nodes.size()-1)
                        routefile << ',';
                }
                if(i!=routes.size()-1)
                    routefile << "\n";
            }
            routefile.close();
        };

        int getRouteSuccess(){
            return routes.size();
        };

        // Add up the total number of edges used by all routes
        int getTotalRouteLength(){
            int total = 0;
            for (int i = 0; i < routes.size(); i++)
            {
                total += routes[i].nodes.size()-1;
            }
            return total;
        }
};

// Calculates the sum of all the Manhatten distance between terminals,
// giving the total length of the optimal solution
int getTotalManhatten(SB &sb){
    int total_distance=0;
    int diffx, diffy;
    for (int i = 0; i < sb.demands.size(); i++)
    {   
        Node a = sb.getNodeFromTerminal(sb.demands[i].src);
        Node b = sb.getNodeFromTerminal(sb.demands[i].dest);
    
        if(a.x > b.x)
            diffx = a.x - b.x;
        else
            diffx = b.x - a.x;
        if (a.y > b.y)
            diffy = a.y - b.y;
        else
            diffy = b.y - a.y;
        total_distance += (diffx + diffy);
    }
    return total_distance;    
}

// From Hadlocks Algorthm: gets all possible moves which a 'Q-negative' - move away from destination
std::vector<Node> getQNegativeNeighbours(Node node, Node dest_node, int width, std::vector<Node> &visited, SB &sb, RouteID routeid){
    std::vector<Node> neighbours_temp, neighbours;

    if (dest_node.x > node.x){
        if (node.x-1 >= 0) {neighbours_temp.push_back(Node(node.x-1,node.y));}
    }
    else if (node.x > dest_node.x){
        if (node.x+1 <= width-1) {neighbours_temp.push_back(Node(node.x+1,node.y));}
    }
    else{
        if (node.x-1 >= 0) {neighbours_temp.push_back(Node(node.x-1,node.y));}
        if (node.x+1 <= width-1) {neighbours_temp.push_back(Node(node.x+1,node.y));}
    }

     
    if (dest_node.y > node.y){
        if (node.y-1 >= 0) {neighbours_temp.push_back(Node(node.x,node.y-1));}
    }
    else if (node.y > dest_node.y){
        if (node.y+1 <= width-1) {neighbours_temp.push_back(Node(node.x,node.y+1));}
    }
    else{
        if (node.y-1 >= 0) {neighbours_temp.push_back(Node(node.x,node.y-1));}
        if (node.y+1 <= width-1) {neighbours_temp.push_back(Node(node.x,node.y+1));}
    }
    bool valid;
    
    for (int i=0;i<neighbours_temp.size();i++){
        valid = TRUE;
        
        for (int j=0;j<visited.size();j++){
            if (neighbours_temp[i] == visited[j]){valid = FALSE;}
        }
        if (sb.checkTurn(node,neighbours_temp[i],routeid) == FALSE){
            valid = FALSE;
            
        }
        if (valid==TRUE){neighbours.push_back(neighbours_temp[i]);}
    }
    
    return neighbours;
};

// From Hadlocks Algorthm: gets all possible moves which a 'Q-positive' - move towards from destination
std::vector<Node> getQPositiveNeighbours(Node node, Node dest_node, int width, std::vector<Node> &visited, SB &sb, RouteID routeid){
    std::vector<Node> neighbours_temp, neighbours;

    if (dest_node.x > node.x){
        neighbours_temp.push_back(Node(node.x+1,node.y));
    }
    else if (node.x > dest_node.x){
        neighbours_temp.push_back(Node(node.x-1,node.y));
    }
    
     
    if (dest_node.y > node.y){
        neighbours_temp.push_back(Node(node.x,node.y+1));
    }
    else if (node.y > dest_node.y){
        neighbours_temp.push_back(Node(node.x,node.y-1));
    }
    
    bool valid;
    
    for (int i=0;i<neighbours_temp.size();i++){
        valid = TRUE;
        
        for (int j=0;j<visited.size();j++){
            if (neighbours_temp[i] == visited[j]){valid = FALSE;}
        }
        if (sb.checkTurn(node,neighbours_temp[i],routeid) == FALSE){
            valid = FALSE;
            
        }
        if (valid==TRUE){neighbours.push_back(neighbours_temp[i]);}
    }
    
    return neighbours;
};

// From Hadlocks Algorthm: Stack a node onto a given stack
int stack(std::vector<Node> &target_stack,Node input){
    target_stack.push_back(input);
}

// From Hadlocks Algorthm: Overload of stack function to accept a vector of nodes
int stack(std::vector<Node> &target_stack,std::vector<Node> input){
    for (int i=0;i<input.size();i++){
        target_stack.push_back(input[i]);
    }
}

// From Hadlocks Algorthm: Unstack a node from a given stack
Node unstack(std::vector<Node> &target_stack){
    Node output = target_stack.back();
    target_stack.pop_back();
    return output;
}

// From Hadlocks Algorthm: Ensure no previously visited nodes exist in a stack
int removeVisitedFromStack(Node node,std::vector<Node> &p_stack,std::vector<Node> &n_stack){
    for (int i = 0; i < p_stack.size(); i++)
    {
        if(node==p_stack[i]){p_stack.erase(p_stack.begin()+i);}
    }

    for (int i = 0; i < n_stack.size(); i++)
    {
        if(node==n_stack[i]){n_stack.erase(n_stack.begin()+i);}
    }
    
}

// Look back at a route vector and remove any deadends and impossible nodes added as
// artifacts of the algorithm
Route refineRoute(Route curr_route, SB &sb){
    std::vector<Node> new_route, old_route;
    old_route = curr_route.nodes;
    Node curr_node = old_route[old_route.size()-1];
    new_route.push_back(curr_node);
    for (int i=old_route.size()-2;i>-1;i--){
       if (sb.checkTurn(curr_node,old_route[i],curr_route.id)){
            curr_node = old_route[i];
            new_route.push_back(curr_node);
        }
    }
    std::reverse(new_route.begin(),new_route.end());
    Route result = Route(curr_route.id,new_route);
    return result;
}


// The Hadlocks Algorithm, inspired by " "
int Hadlocks(SB &sb){
    int width = sb.width;
    for (int i=0;i<sb.demands.size();i++){
        
        // std::cout << "Routing ";
        // sb.demands[i].print();

        RouteID demand_id = sb.demands[i]; 
        std::vector<Node> visited, p_stack, n_stack, route, q_pos;
        Node u_node = sb.getNodeFromTerminal(demand_id.src);
        Node dest = sb.getNodeFromTerminal(demand_id.dest);
        bool valid_route = TRUE;
        route.push_back(u_node);
        while(u_node != dest){
            visited.push_back(u_node);
            removeVisitedFromStack(u_node,p_stack,n_stack);
            stack(n_stack,getQNegativeNeighbours(u_node,dest,width,visited,sb,demand_id));
            q_pos = getQPositiveNeighbours(u_node,dest,width,visited,sb,demand_id);

            if (q_pos.size() == 0){
                if(p_stack.size() == 0){
                    if(n_stack.size() == 0){
                        // No move is possible, routing has failed
                        valid_route = FALSE;
                        break;
                    }
                    else{
                        p_stack = n_stack;
                    }
                }
                u_node = unstack(p_stack);
            }
            else{
                u_node = unstack(q_pos);
                stack(p_stack,q_pos);
            }

            route.push_back(u_node);
        }
        if (valid_route){
            Route route_struct = Route(demand_id,route); 
            route_struct = refineRoute(route_struct,sb);
            // route_struct.print();
            sb.addRoute(route_struct);
        }
        visited.clear();
        p_stack.clear();
        n_stack.clear();
        route.clear();
        q_pos.clear();
    }

        
}

// From Simulated Annealing: Swap randomly two elements in a list
int RandomSwap(std::vector<RouteID> &list){
    if (list.size() == 0){
        return 1;
    }
    int r1=0,r2=0;
    while(r1==r2){
        r1 = (std::rand() % list.size());
        r2 = (std::rand() % list.size());
    }
    RouteID temp = list[r1];
    list[r1] = list[r2];
    list[r2] = temp;

}

int SimAnnealing(SB &sb,int M_, float alpha_, float target_){
    std::vector<Route> sol;
    int E=0, E_new=0;
    int deltaE = 0;
    int R=0, R_new=0;
    int M=500;
    float alpha = alpha_;
    int k=0;
    float boltzmann = 0;
    float T = 100;

    Hadlocks(sb);
    R = sb.getRouteSuccess();
    E = sb.getTotalRouteLength();
    sol = sb.routes;

    while(k<M){
        std::cout << "Iteration " << k << " T= " << T << " success= "<< R << " E= " << E << "\n";
        if((R==sb.demands.size()) && (E<=(float)getTotalManhatten(sb)/target_))
            break;
       
        if(T<2){break;}
        sb.resetSB();
        RandomSwap(sb.demands);
        Hadlocks(sb);
        R_new = sb.getRouteSuccess();
        E_new = sb.getTotalRouteLength();

        if(R_new>R){
            sol = sb.routes;
            R = R_new;
            E = E_new;
            T = T*alpha;
        }

        else if(R_new==R){
            if(E_new<E){
                sol = sb.routes;
                R = R_new;
                E = E_new;
                T = T*alpha;
            }
            else{
                deltaE = E_new-E;
                boltzmann = exp(-deltaE/T);
                if(boltzmann>((float) rand()/RAND_MAX)){
                    sol = sb.routes;
                    R = R_new;
                    E = E_new;
                    T = T*alpha;
                }
            }
        }
        k++;
    }
    sb.resetSB();
    sb.routes = sol;
    if (sb.routes.size()==sb.demands.size()){
        return TRUE;
    }
    else{
        return FALSE;
    }
}

// int sbRoute(int width, std::string demands_filepath){
//     SB sb = SB(width);
//     sb.parseDemands(demands_filepath);
//     Hadlocks(sb);
//     sb.exportData();

// }

char capitalise(char a){
    if(a=='n')
        return 'N';
    if(a=='e')
        return 'E';
    if(a=='s')
        return 'S';
    if(a=='w')
        return 'W';
    return a;
}

// Take a vector of strings of demands, originating from the command line
// and form a vector of RouteIDs
std::vector<RouteID> parseDemands(std::vector<std::string> input_){    
    std::vector<RouteID> demands;
    for (int j = 0; j < input_.size(); j+=2)
    {
        char src_dir,dest_dir;
       // char src_val[4],dest_val[4];
        std::string src_val, dest_val;
        std::string src_string = input_[j];
        std::string dest_string = input_[j+1];


        src_dir = capitalise(src_string[0]);
        src_val = src_string.substr(1,src_string.size()-1);
        dest_dir = capitalise(dest_string[0]);
        dest_val = dest_string.substr(1,dest_string.size()-1);
              
        Terminal src = Terminal(src_dir,atoi(src_val.c_str()));
        Terminal dest = Terminal(dest_dir,atoi(dest_val.c_str()));
        
        demands.push_back(RouteID(src,dest));
    }
    return demands;  
}

// std::vector<RouteID> parseDemands(std::string input_){
//     std::stringstream ss(input_);
//     std::vector<std::string> v;
//     std::string value, subvalue;
//     while (ss >> value)
//     {   
//         getline(value,subvalue,',');
//         v.push_back(value);
//         std::cout << value << std::endl;

//     if (ss.peek() == ',' || ss.peek() == ' ')
//         ss.ignore();
//     }
//     char src_dir,dest_dir;
//     char src_val[4],dest_val[4];
//     std::vector<RouteID> demands;
//     for (int j = 0; j < v.size(); j+=2)
//     {
//         std::string src_string = v[j];
//         std::string dest_string = v[j+1];

//         src_dir = src_string[0];
//         int i=1;
//         while(src_string[i-1]!=src_string.at(src_string.size()-1)){
//             src_val[i-1] = src_string[i];
//             i++;
//         }
//         i=0;
//         dest_dir = dest_string[0];
//         i=1;
//         while(dest_string[i-1]!=dest_string.at(dest_string.size()-1)){
//             dest_val[i-1] = dest_string[i];

//             i++;
//         }
//         Terminal src = Terminal(src_dir,atoi(src_val));
//         Terminal dest = Terminal(dest_dir,atoi(dest_val));
//         demands.push_back(RouteID(src,dest));
//     }
//     return demands;  
// }

int main(int argc, char *argv[]){

  
    cxxopts::Options options("switchbox","Routes a switchbox using Simulated Annealing and the Hadlocks shortest path algorithm, saves routes in sb_routes.txt");
    options.add_options()
        ("n,iterations","Max number of iterations of algorithm",cxxopts::value<int>()->default_value("500"))
        ("w,width","Width of switchbox",cxxopts::value<int>()->default_value("8"))
        ("t,target","Target performance",cxxopts::value<float>()->default_value("0.95"))
        ("a,alpha","Alpha value",cxxopts::value<float>()->default_value("0.95"))
        ("d,demands","List of demands as string",cxxopts::value<std::vector<std::string>>())
        ("o,output","Output file path for routing results",cxxopts::value<std::string>()->default_value("sb_routes.txt"))
        ("i,id","Switchbox ID",cxxopts::value<std::string>()->default_value("0,0"))
        ("h,help","Print usage");
    options.parse_positional({"demands"});

    cxxopts::ParseResult results;
    try {
        results = options.parse(argc, argv);
    } catch (const cxxopts::OptionParseException &x) {
        std::cout << options.help() << std::endl;
        return EXIT_FAILURE;
    }
    
    if (results.count("help"))
    {
      std::cout << options.help() << std::endl;
      exit(0);
    }

     if (!results.count("width")) {
        std::cerr << "Must specify switchbox width with -w\n";
        return 1;
    }

      if (!results.count("demands")) {
        std::cerr << "No demands specified\n";
        return 1;
    }
     
     
    
    int N;
    float target;
    float alpha;
    int width;
    std::string sb_id;
    std::string output = "sb_out.txt";
    width = results["width"].as<int>();
    if(results.count("iterations")){N = results["iterations"].as<int>();}
    if(results.count("target")){target = results["target"].as<float>();}
    if(results.count("alpha")){alpha = results["alpha"].as<float>();}
    if(results.count("output")){output = results["output"].as<std::string>();}
    if(results.count("id")){sb_id = results["id"].as<std::string>();}
    // std::vector<std::string> demands = results["demands"].as<std::vector<std::string>>();
    std::vector<RouteID> demands = parseDemands(results["demands"].as<std::vector<std::string>>());
    
    SB sb = SB(width);
    sb.addDemands(demands);
    std::cout << "Now routing: \n";
    for (int i = 0; i < demands.size(); i++)
    {
        demands[i].print();
        // std::cout << demands[i];
    }
    
    SimAnnealing(sb,N,alpha,target);
    if(sb.getRouteSuccess() == sb.demands.size()){
        std::cout << "\nSuccess!\n";
    }
    else{
        std::cout << "\nRouting failed!\n";
    }
    std::cout << "Routed " << sb.getRouteSuccess() << "/" << sb.demands.size() << std::endl;
    std::cout << "Total route length= " << sb.getTotalRouteLength() << std::endl;
    sb.exportData(output,sb_id);
    return 0;
}