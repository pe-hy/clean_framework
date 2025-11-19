import numpy as np
from vector_transformations import VectorTransformations
from state_rules import StateRules
import networkx as nx
import matplotlib.pyplot as plt
import random
import os
import json

num_values = 5
num_components = 5
max_path_length = 4
num_paths_per_node_train = 200
num_paths_per_node_test = 10
max_transformations = 20

rules = StateRules()

# Total number of possible vectors
total_vectors = num_values ** num_components
print(f"Total possible vectors: {total_vectors}")

# Dictionary to track rule violations
rule_violation_counts = {}
for _, description in rules.get_all_rules():
    rule_violation_counts[description] = 0

# Counter for valid vectors
invalid_vectors_count = 0

# Initialize the transformations
transformations = VectorTransformations(num_values)
all_transformations = transformations.get_all_transformations()[:max_transformations]

# Create a directed graph
G = nx.DiGraph()

# Function to generate all possible vectors
def generate_all_vectors(num_components, num_values):
    total = num_values ** num_components
    for i in range(total):
        vec = np.zeros(num_components, dtype=int)
        temp = i
        for j in range(num_components-1, -1, -1):
            vec[j] = temp % num_values
            temp //= num_values
        yield vec

# Check each possible vector
for vec in generate_all_vectors(num_components, num_values):
    valid, violations = rules.check_all_rules(vec)
    
    if not valid:
        invalid_vectors_count += 1
    else:
        G.add_node(tuple(vec))


# Print results
print(f"\nInalid vectors: {invalid_vectors_count} ({invalid_vectors_count/total_vectors:.2%})")


# Add edges for valid transformations
for node in G.nodes():
    vec = np.array(node)
    
    # Try each transformation
    for idx, (transform_func, description) in enumerate(all_transformations):
        # Apply the transformation
        transformed_vec = transform_func(vec)
        transformed_tuple = tuple(transformed_vec)
        
        # Check if the transformed vector is a valid node in the graph
        if transformed_tuple in G.nodes():
            # Add an edge with the transformation index as an attribute
            G.add_edge(node, transformed_tuple, transformation=idx)

# Count the number of nodes in the graph
num_nodes = G.number_of_nodes()
print(f"Number of nodes in the graph: {num_nodes}")

# Count the number of edges in the graph
num_edges = G.number_of_edges()
print(f"Number of edges in the graph: {num_edges}")

# Optional: Calculate average number of edges per node
avg_edges_per_node = num_edges / G.number_of_nodes() if G.number_of_nodes() > 0 else 0
print(f"Average number of edges per node: {avg_edges_per_node:.2f}")




train_paths = []
test_paths = []
for node in G.nodes():
    # Sample path length from 1 to max_path_length
    # We'll use this path length later when generating paths from this node
    # This allows us to create training examples with varying path lengths

    # Get all outgoing edges from this node
    outgoing_edges = G.out_edges(node, data=True)
    # Skip if no outgoing edges
    if not outgoing_edges:
        continue
    
    # Convert to list for easier sampling
    outgoing_edges_list = list(outgoing_edges)
    
    # Determine number of edges for test set (30%)
    num_test_edges = max(1, int(0.3 * len(outgoing_edges_list)))
    
    # Randomly select edges for test set
    test_indices = np.random.choice(
        len(outgoing_edges_list), 
        size=num_test_edges, 
        replace=False
    )
    
    # Add edges to appropriate sets
    train_data = []
    test_data = []
    for idx, edge in enumerate(outgoing_edges_list):
        source, target, attrs = edge
        if idx in test_indices:
            test_data.append((source, target, attrs['transformation']))
        else:
            train_data.append((source, target, attrs['transformation']))
    if len(train_data) == 0:
        continue
    num_path_per_edge_train = num_paths_per_node_train // len(train_data)
    num_path_per_edge_test = num_paths_per_node_test // len(test_data)

    # Generate paths for training data
    for source, target, transformation in train_data:
        # Start each path with the current edge
        for _ in range(num_path_per_edge_train):
            path = [(source, target, transformation)]
            current_node = target
            
            # Randomly determine path length for this sample (1 to max_path_length)
            path_length = np.random.randint(0, max_path_length)
            
            # Continue the path if needed (path_length > 1)
            for step in range(0, path_length):
                # Get outgoing edges from current node
                next_edges = list(G.out_edges(current_node, data=True))
                
                # Break if no more outgoing edges
                if not next_edges:
                    break
                
                # Randomly select the next edge
                next_edge = random.choice(next_edges)
                next_source, next_target, next_attrs = next_edge
                
                # Add to path
                path.append((next_source, next_target, next_attrs['transformation']))
                
                # Update current node
                current_node = next_target
            
            train_paths.append(path)
    
    # Generate paths for test data
    for source, target, transformation in test_data:
        # Similar process for test paths
        for _ in range(num_path_per_edge_test):
            path = [(source, target, transformation)]
            current_node = target
            
            path_length = np.random.randint(1, max_path_length)
            
            for step in range(0, path_length):
                next_edges = list(G.out_edges(current_node, data=True))
                if not next_edges:
                    break
                
                next_edge = random.choice(next_edges)
                next_source, next_target, next_attrs = next_edge
                
                path.append((next_source, next_target, next_attrs['transformation']))
                current_node = next_target
            
            test_paths.append(path)


node_to_id = {}
id_counter = 0

# Iterate through all nodes in the graph
for node in G.nodes():
    if node not in node_to_id:
        node_to_id[node] = id_counter
        id_counter += 1


train_examples = []
test_examples = []
for path in train_paths:
    start = node_to_id[path[0][0]]
    end = node_to_id[path[-1][1]]
    path_symbols = [f'E{start}']
    for edge in path:
        path_symbols.append(f'T{edge[2]}')
    
    input = ' . '.join(path_symbols)
    output = f'E{end}'

    train_examples.append({'input':input, 'output':output})

for path in test_paths:
    start = node_to_id[path[0][0]]
    end = node_to_id[path[-1][1]]
    path_symbols = [f'E{start}']
    for edge in path:
        path_symbols.append(f'T{edge[2]}')
    
    input = ' . '.join(path_symbols)
    output = f'E{end}'

    test_examples.append({'input':input, 'output':output})

# Create temp directory if it doesn't exist

temp_dir = "data"
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)
    print(f"Created directory: {temp_dir}")
else:
    print(f"Directory already exists: {temp_dir}")

# Save training and test examples to JSON files
# Define file paths
train_file_path = os.path.join(temp_dir, "train.json")
test_file_path = os.path.join(temp_dir, "test.json")

# Save training examples
with open(train_file_path, 'w') as f:
    json.dump(train_examples, f, indent=2)
print(f"Saved {len(train_examples)} training examples to {train_file_path}")

# Save test examples
with open(test_file_path, 'w') as f:
    json.dump(test_examples, f, indent=2)
print(f"Saved {len(test_examples)} test examples to {test_file_path}")



