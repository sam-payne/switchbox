#include <iostream>
#include <vector>

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
};

class SB{
    private:
        int width;
        std::vector<RouteID> demands;
        
    public:
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
        int addEdge(Edge newedge){
            for(int i=0;i<used_edges.size();i++){
                if (newedge==used_edges[i]){
                    return 1;
                }
            }
            used_edges.push_back(newedge);
        };
        bool checkTurn(Node src, Node dest){
            Edge testedge = Edge(src,dest);
            for (int i=0;i<used_edges.size();i++){
                if (testedge==used_edges[i]){
                    return FALSE;
                }
            }
            return TRUE;
        }
};


std::vector<Node> getQNegativeNeighbours(Node node, Node dest_node, int width, std::vector<Node> &visited, SB &sb){
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
        if (sb.checkTurn(node,neighbours_temp[i]) == FALSE){
            valid = FALSE;
            
        }
        if (valid==TRUE){neighbours.push_back(neighbours_temp[i]);}
    }
    
    return neighbours;
};

std::vector<Node> getQPositiveNeighbours(Node node, Node dest_node, int width, std::vector<Node> &visited, SB &sb){
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
        if (sb.checkTurn(node,neighbours_temp[i]) == FALSE){
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

int main(){

    Terminal t = Terminal('N',10);
    Terminal s = Terminal('S',9);
    Terminal j = Terminal('W',7);
    RouteID id = RouteID(t,s);
    RouteID id2 = RouteID(s,t);
    // if (id==id2){
    //     std::cout << "TRUE";
    // }
    // else{
    //     std::cout << "FALSE";
    // }

    SB sb = SB(8);  
    std::vector<Node> visited;
    std::vector<Node> results_neg, results_pos;
    results_neg = getQNegativeNeighbours(Node(0,0),Node(10,10),12,visited,sb);
    results_pos = getQPositiveNeighbours(Node(0,0),Node(10,10),12,visited,sb);
    for (int i=0;i<results_neg.size();i++){
        results_neg[i].print();
    }
    for (int i=0;i<results_pos.size();i++){
        results_pos[i].print();
    }
    stack(results_neg,Node(0,0));
    for (int i=0;i<results_neg.size();i++){
        results_neg[i].print();
    }
    Node output = unstack(results_pos);
    output.print();
    for (int i=0;i<results_pos.size();i++){
        results_pos[i].print();
    }
    
    
}