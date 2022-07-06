#include <iostream>
#include <vector>
#include <algorithm>    // std::reverse
#include <stdexcept>
#include <fstream>


#define TRUE 1
#define FALSE 0

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

struct RouteID{
    Terminal src;
    Terminal dest; 
    RouteID(){};
    RouteID(Terminal src_, Terminal dest_){
        src = src_;
        dest = dest_;
    };

    bool operator==(const RouteID& x) const
    {
        return ((src==x.src && dest==x.dest)||(src==x.dest && dest==x.src));
    };
    void print(){std::cout << src.dir << src.val << " to " << dest.dir << dest.val << "\n";}
};

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
    bool operator==(const Edge& x) const
    {
        return ((a==x.a && b==x.b)||(b==x.a && a==x.b));
    };
    void print(){std::cout << "Edge: " << a.x << "," << a.y << "-" << b.x << "," << b.y << "\n";}
};

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

class SB{
    // private:
               
        
        
    public:
        std::vector<Route> routes;

        int width;
        std::vector<RouteID> demands;
        std::vector<Edge> used_edges;
        SB(){};
        SB(int width_){
            width = width_;
        };
        SB(int width_, std::vector<RouteID> demands_){
            width = width_;
            demands = demands_;
        };
        int setDemands(std::vector<RouteID> demands_){
            demands = demands_;
        };
        void addRoute(Route newr){
            routes.push_back(newr);
        }
        int addEdge(Edge newedge){
            for(int i=0;i<used_edges.size();i++){
                if (newedge==used_edges[i]){
                    return 1;
                }
            }
            used_edges.push_back(newedge);
        };
        bool checkTurn(Node src, Node dest, RouteID id){
            Edge testedge = Edge(src,dest);
            Edge curr_edge;
            for (int i=0;i<routes.size();i++){
               
                
                if (routes[i].id == id){
                    continue;
                }
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
            return n;
        };

        void parseDemands(){
            std::ifstream indata;
            indata.open("demands.txt");
            if(!indata) { // file couldn't be opened
                exit(1);
            }
            Terminal src,dest;
            char src_dir;
            int src_val;
            char dest_dir;
            int dest_val;
            
            while ( !indata.eof() ){
                indata >> src_dir;
                indata >> src_val;
                indata >> dest_dir;
                indata >> dest_val;
                src = Terminal(src_dir,src_val);
                dest = Terminal(dest_dir,dest_val);
                demands.push_back(RouteID(src,dest));
            }            
        };
};


std::vector<Node> getQNegativeNeighbours(Node node, Node dest_node, int width, std::vector<Node> &visited, SB &sb, RouteID routeid){
    std::vector<Node> neighbours_temp, neighbours;
    // node.print();
    // dest_node.print();
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
            if (neighbours_temp[i] == visited[i]){valid = FALSE;}
        }
        if (sb.checkTurn(node,neighbours_temp[i],routeid) == FALSE){
            valid = FALSE;
            
        }
        if (valid==TRUE){neighbours.push_back(neighbours_temp[i]);}
    }
    
    return neighbours;
};

std::vector<Node> getQPositiveNeighbours(Node node, Node dest_node, int width, std::vector<Node> &visited, SB &sb, RouteID routeid){
    std::vector<Node> neighbours_temp, neighbours;
    // node.print();
    // dest_node.print();
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
            if (neighbours_temp[i] == visited[i]){valid = FALSE;}
        }
        if (sb.checkTurn(node,neighbours_temp[i],routeid) == FALSE){
            valid = FALSE;
            
        }
        if (valid==TRUE){neighbours.push_back(neighbours_temp[i]);}
    }
    
    return neighbours;
};

int stack(std::vector<Node> &target_stack,Node input){
    target_stack.push_back(input);
}

int stack(std::vector<Node> &target_stack,std::vector<Node> input){
    for (int i=0;i<input.size();i++){
        target_stack.push_back(input[i]);
    }
}

Node unstack(std::vector<Node> &target_stack){
    Node output = target_stack.back();
    target_stack.pop_back();
    return output;
}

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



int Hadlocks(SB &sb){
    int width = sb.width;
    for (int i=0;i<sb.demands.size();i++){
        
        std::cout << "Routing ";
        sb.demands[i].print();

        RouteID demand_id = sb.demands[i]; 
        std::vector<Node> visited, p_stack, n_stack, route, q_pos;
        Node u_node = sb.getNodeFromTerminal(demand_id.src);
        Node dest = sb.getNodeFromTerminal(demand_id.dest);
    
        route.push_back(u_node);
        while(u_node != dest){
            visited.push_back(u_node);
            removeVisitedFromStack(u_node,p_stack,n_stack);
            stack(n_stack,getQNegativeNeighbours(u_node,dest,width,visited,sb,demand_id));
            q_pos = getQPositiveNeighbours(u_node,dest,width,visited,sb,demand_id);

            if (q_pos.size() == 0){
                if(p_stack.size() == 0){
                    if(n_stack.size() == 0){
                        std::cout << "Error routing ";
                        demand_id.print();
                        return -1;
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
        Route route_struct = Route(demand_id,route); 
        route_struct = refineRoute(route_struct,sb);
        // route_struct.print();
        sb.addRoute(route_struct);
    }
    
    
    
}

int main(){

    SB sb = SB(16);
    // Terminal t = Terminal('E',14);
    // Terminal s = Terminal('S',14);
    // Terminal j = Terminal('S',15);
    // Terminal k = Terminal('S',8);
    // Node n = sb.getNodeFromTerminal(s);
    
    // RouteID id = RouteID(t,s);
    // RouteID id2 = RouteID(j,k);
    // std::vector<RouteID> demands;
    // demands.push_back(id);
    // demands.push_back(id2);
    // sb.setDemands(demands);
    sb.parseDemands();
    Hadlocks(sb);
    std::cout << sb.routes.size() << " routes routed!\n";
    
    // // if (id==id2){
    // //     std::cout << "TRUE";
    // // }
    // // else{
    // //     std::cout << "FALSE";
    // // }

    // SB sb = SB(8);  
    // std::vector<Node> visited;
    // std::vector<Node> results_neg, results_pos;
    // results_neg = getQNegativeNeighbours(Node(0,0),Node(10,10),12,visited,sb);
    // results_pos = getQPositiveNeighbours(Node(0,0),Node(10,10),12,visited,sb);
   
    // std::cout << results_pos.size();
    // Node output = unstack(results_pos);
    // output.print();
    // std::cout << (results_pos.size());
    
    
}