# from fastapi import FastAPI, Form

# app = FastAPI()

# @app.get('/')
# def read_root():
#     return {'Ping': 'Pong'}

# @app.get('/pipelines/parse')
# def parse_pipeline(pipeline: str = Form(...)):
#     return {'status': 'parsed'}

# from fastapi import FastAPI, Form, HTTPException
# from pydantic import BaseModel
# from typing import List, Dict

# app = FastAPI()

# # Define the structure for a pipeline request
# class Node(BaseModel):
#     id: str
#     type: str

# class Edge(BaseModel):
#     source: str
#     target: str

# class Pipeline(BaseModel):
#     nodes: List[Node]
#     edges: List[Edge]

# # Helper function to check for a Directed Acyclic Graph (DAG)
# def is_dag(nodes, edges):
#     graph = {node['id']: [] for node in nodes}
#     for edge in edges:
#         graph[edge['source']].append(edge['target'])

#     visited = set()
#     rec_stack = set()

#     def dfs(node):
#         if node in rec_stack:
#             return False
#         if node in visited:
#             return True
        
#         visited.add(node)
#         rec_stack.add(node)

#         for neighbor in graph.get(node, []):
#             if not dfs(neighbor):
#                 return False
        
#         rec_stack.remove(node)
#         return True

#     for node in graph:
#         if not dfs(node):
#             return False
#     return True

# @app.post('/pipelines/parse')
# def parse_pipeline(pipeline: Pipeline):
#     nodes = pipeline.nodes
#     edges = pipeline.edges
    
#     # Count the number of nodes and edges
#     num_nodes = len(nodes)
#     num_edges = len(edges)
    
#     # Check if the pipeline forms a DAG
#     dag_result = is_dag(nodes, edges)
    
#     return {
#         "num_nodes": num_nodes,
#         "num_edges": num_edges,
#         "is_dag": dag_result
#     }

# # Basic root endpoint to test if the server is working
# @app.get('/')
# def read_root():
#     return {'Ping': 'Pong'}


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace '*' with the specific frontend URL if needed (e.g., "http://localhost:3000")
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Define the structure for a pipeline request
class Node(BaseModel):
    id: str
    type: str

class Edge(BaseModel):
    source: str
    target: str

class Pipeline(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

# Helper function to check for a Directed Acyclic Graph (DAG)
def is_dag(nodes, edges):
    graph = {node['id']: [] for node in nodes}
    for edge in edges:
        graph[edge['source']].append(edge['target'])

    visited = set()
    rec_stack = set()

    # Depth-First Search to detect cycles
    def dfs(node):
        if node in rec_stack:
            return False  # Cycle detected
        if node in visited:
            return True  # Already processed
        
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph.get(node, []):
            if not dfs(neighbor):
                return False
        
        rec_stack.remove(node)
        return True

    for node in graph:
        if not dfs(node):
            return False  # If any node is part of a cycle, it's not a DAG
    return True

@app.post('/pipelines/parse')
def parse_pipeline(pipeline: Pipeline):
    print(f"Received pipeline: {pipeline}")
    nodes = pipeline.nodes
    edges = pipeline.edges
    
    if not nodes or not edges:
        raise HTTPException(status_code=400, detail="Nodes or edges cannot be empty")

    # Count the number of nodes and edges
    num_nodes = len(nodes)
    num_edges = len(edges)
    
    # Check if the pipeline forms a DAG
    dag_result = is_dag(nodes, edges)
    
    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "is_dag": dag_result
    }

# Basic root endpoint to test if the server is working
@app.get('/')
def read_root():
    return {'Ping': 'Pong'}
