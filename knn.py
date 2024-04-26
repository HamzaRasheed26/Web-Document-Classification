import networkx as nx
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import numpy as np

# Function to compute similarity/distance between two graphs based on MCS size
# Function to compute distance between two graphs based on MCS approximation
def compute_distance(graph1, graph2):
    isomorphic = nx.is_isomorphic(graph1, graph2)
    return not isomorphic  # Distance is 0 if graphs are isomorphic, 1 otherwise


# Function to convert graph to feature vector (here, using MCS size as feature)
def graph_to_feature(graph, graphs):
    return [compute_distance(graph, g) for g in graphs]

# Sample training and test sets of graphs
train_set = [nx.complete_graph(3), nx.complete_graph(4), nx.cycle_graph(5)]
test_set = [nx.complete_graph(3), nx.cycle_graph(3)]

# Convert graphs to feature vectors
X_train = [graph_to_feature(graph, train_set) for graph in train_set]
y_train = ['A', 'B', 'C']  # Labels for training set
X_test = [graph_to_feature(graph, train_set) for graph in test_set]

# Train KNN classifier
knn_classifier = KNeighborsClassifier(n_neighbors=3)  # K=3
knn_classifier.fit(X_train, y_train)

# Predict labels for test set
y_pred = knn_classifier.predict(X_test)

# Evaluate performance
accuracy = accuracy_score(['A', 'C'], y_pred)  # True labels for test set
print("Accuracy:", accuracy)
print("Classification Report:")
print(classification_report(['A', 'C'], y_pred))
print("Confusion Matrix:")
print(confusion_matrix(['A', 'C'], y_pred))
