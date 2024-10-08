'''
Backend for a web application, that allows users to visualize Kmeans clustering on a 2D dataset.
'''

# Importing required libraries
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template 
import os
import matplotlib 
matplotlib.use('Agg') 


# enum for different strategies to determine cluster centers
class Strategy:
    RANDOM = 0
    FARTHEST_FIRST = 1
    KMEANS_PLUS_PLUS = 2
    MANUAL_INPUT = 3

# Function to generate random data
def generate_data(n=200):
    '''
    Generates n random data points.
    
    Parameters:
    n (int): Number of data points to generate.
    
    Returns:
    Store the np.array to data.txt file
    '''
    data = np.random.rand(n, 2)
    np.savetxt('./static/data.txt', data)
    # Plot the unclustered data using matplotlib
    plt.scatter(data[:, 0], data[:, 1])
    plt.title('KMeans Clustered Data')
    # Save the plot as a PNG file in the static folder
    plt.savefig('./static/data.png')
    return data

# Function to perform Kmeans clustering
def kmeans(data, centers, k=2, max_iter=100):
    '''
    Performs Kmeans clustering on the given data.
    
    Parameters:
    data (np.array): n x 2 array of data points.
    k (int): Number of clusters.
    max_iter (int): Maximum number of iterations.
    
    Returns:
    np.array: n x 1 array of cluster labels.
    '''
    
    # Perform Kmeans clustering
    for a in range(max_iter):
        # Assign each data point to the nearest cluster
        labels = np.argmin(np.linalg.norm(data[:, None] - centers, axis=2), axis=1)
        
        # Update cluster centers
        new_centers = np.array([data[labels == i].mean(axis=0) for i in range(k)])
        
        # Plot the data and cluster centers using matplotlib
        plt.scatter(data[:, 0], data[:, 1], c=labels)
        plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='x')
        plt.title('Kmeans Clustering')
        plt.xlabel('X')
        plt.ylabel('Y')
        # Save the plot as a PNG file in the static folder, with a unique name
        name = "kmeans_step_" + str(a) + ".png"
        plt.savefig(os.path.join('static', name))
        # plt.savefig('static/kmeans.png')
        
        # Check for convergence
        if np.all(centers == new_centers):
            break
        centers = new_centers
    return a

# Function to determine random cluster centers
def random_centers(data, k=2):
    '''
    Determines random cluster centers.
    
    Parameters:
    data (np.array): n x 2 array of data points.
    k (int): Number of clusters.
    
    Returns:
    np.array: k x 2 array of cluster centers.
    '''
    return data[np.random.choice(data.shape[0], k, replace=False)]

# Function for Farthest First strategy to determine cluster centers
def farthest_first(data, k=2):
    '''
    Determines cluster centers using the Farthest First strategy.
    
    Parameters:
    data (np.array): n x 2 array of data points.
    k (int): Number of clusters.
    
    Returns:
    np.array: k x 2 array of cluster centers.
    '''
    centers = np.zeros((k, 2))
    centers[0] = data[np.random.randint(data.shape[0])]
    for i in range(1, k):
        dist = np.linalg.norm(data[:, None] - centers[:i], axis=2).min(axis=1)
        centers[i] = data[np.argmax(dist)]
    return centers

# Function to determine cluster centers using Kmeans++
def kmeans_plus_plus(data, k=2):
    '''
    Determines cluster centers using the Kmeans++ strategy.
    
    Parameters:
    data (np.array): n x 2 array of data points.
    k (int): Number of clusters.
    
    Returns:
    np.array: k x 2 array of cluster centers.
    '''
    centers = np.zeros((k, 2))
    centers[0] = data[np.random.randint(data.shape[0])]
    for i in range(1, k):
        dist = np.linalg.norm(data[:, None] - centers[:i], axis=2).min(axis=1)
        prob = dist**2 / (dist**2).sum()
        centers[i] = data[np.random.choice(data.shape[0], p=prob)]
    return centers

# Allow manual input from the user via point and click
def manual_input(data, k=2):
    '''
    Allows manual input of data points by the user.
    
    Parameters:
    data (np.array): n x 2 array of data points.
    k (int): Number of clusters.
    
    Returns:
    np.array: n x 2 array of data points.
    '''
    # plt.figure()
    plt.scatter(data[:, 0], data[:, 1])
    plt.title('Click on the cluster centers')
    plt.xlabel('X')
    plt.ylabel('Y')
    centers = np.array(plt.ginput(k))
    plt.close()
    return centers

# Function to run the Kmeans clustering algorithm
def run_kmeans(k=2, strategy=0):
    '''
    Runs the Kmeans clustering algorithm on the data points.
    '''
    # Get data
    if not os.path.exists('./static/data.txt'):
        generate_data()
    data = np.loadtxt('./static/data.txt')
    
    # Delete all previous images
    images = os.listdir('./static')
    for image in images:
        if 'data' not in image:
            os.remove(f'./static/{image}')
    
    switcher = {
        Strategy.RANDOM: random_centers,
        Strategy.FARTHEST_FIRST: farthest_first,
        Strategy.KMEANS_PLUS_PLUS: kmeans_plus_plus,
        Strategy.MANUAL_INPUT: manual_input
    }

    # Determine cluster centers based on the selected strategy
    centers = switcher.get(strategy)(data, k)
    
    # Perform Kmeans clustering
    iter = kmeans(data, centers, k)
    return iter

def main():
    generate_data()
    # Run the Kmeans clustering algorithm
    run_kmeans(4, 0)

if __name__ == '__main__':
    main()