# Modified based on in class code

import numpy as np
from PIL import Image as im
import matplotlib.pyplot as plt
import sklearn.datasets as datasets
import matplotlib 
matplotlib.use('Agg') 

class KMeans():

    def __init__(self, data, k):
        self.data = data
        self.k = k
        self.assignment = [-1 for _ in range(len(data))]
        self.snaps = []
    
    def snap(self, centers):
        TEMPFILE = "./static/temp.png"

        fig, ax = plt.subplots()
        ax.scatter(self.data[:, 0], self.data[:, 1], c=self.assignment)
        ax.scatter(centers[:,0], centers[:, 1], c='r')
        fig.savefig(TEMPFILE)
        plt.close(fig)
        self.snaps.append(im.fromarray(np.asarray(im.open(TEMPFILE))))

    def isunassigned(self, i):
        return self.assignment[i] == -1
    
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
        plt.close()
        return data
    
    # Function to determine random cluster centers
    def random_centers(self):
        '''
        Determines random cluster centers.
        
        Parameters:
        data (np.array): n x 2 array of data points.
        k (int): Number of clusters.
        
        Returns:
        np.array: k x 2 array of cluster centers.
        '''
        return self.data[np.random.choice(len(self.data) - 1, size=self.k, replace=False)]

    # Function for Farthest First strategy to determine cluster centers
    def farthest_first(self):
        '''
        Determines cluster centers using the Farthest First strategy.
        
        Parameters:
        data (np.array): n x 2 array of data points.
        k (int): Number of clusters.
        
        Returns:
        np.array: k x 2 array of cluster centers.
        '''
        centers = np.zeros((self.k, 2))
        centers[0] = self.data[np.random.randint(self.data.shape[0])]
        for i in range(1, self.k):
            dist = np.linalg.norm(self.data[:, None] - centers[:i], axis=2).min(axis=1)
            centers[i] = self.data[np.argmax(dist)]
        return centers

    # Function to determine cluster centers using Kmeans++
    def kmeans_plus_plus(self):
        '''
        Determines cluster centers using the Kmeans++ strategy.
        
        Parameters:
        data (np.array): n x 2 array of data points.
        k (int): Number of clusters.
        
        Returns:
        np.array: k x 2 array of cluster centers.
        '''
        centers = np.zeros((self.k, 2))
        centers[0] = self.data[np.random.randint(self.data.shape[0])]
        for i in range(1, self.k):
            dist = np.linalg.norm(self.data[:, None] - centers[:i], axis=2).min(axis=1)
            prob = dist**2 / (dist**2).sum()
            centers[i] = self.data[np.random.choice(self.data.shape[0], p=prob)]
        return centers

    # Allow manual input from the user via point and click
    def manual_input(self):
        '''
        Allows manual input of data points by the user.
        
        Parameters:
        data (np.array): n x 2 array of data points.
        k (int): Number of clusters.
        
        Returns:
        np.array: n x 2 array of data points.
        '''
        # plt.figure()
        plt.scatter(self.data[:, 0], self.data[:, 1])
        plt.title('Click on the cluster centers')
        plt.xlabel('X')
        plt.ylabel('Y')
        centers = np.array(plt.ginput(self.k))
        plt.close()
        return centers

    def initialize(self, strategy=0):
        if strategy == 3:
            return self.manual_input()
        elif strategy == 1:
            return self.farthest_first()
        elif strategy == 2:
            return self.kmeans_plus_plus()
        else:
            return self.random_centers()

    def make_clusters(self, centers):
        for i in range(len(self.assignment)):
            for j in range(self.k):
                if self.isunassigned(i):
                    self.assignment[i] = j
                    dist = self.dist(centers[j], self.data[i])
                else:
                    new_dist = self.dist(centers[j], self.data[i])
                    if new_dist < dist:
                        self.assignment[i] = j
                        dist = new_dist
                    
        
    def compute_centers(self):
        centers = []
        for i in range(self.k):
            cluster = []
            for j in range(len(self.assignment)):
                if self.assignment[j] == i:
                    cluster.append(self.data[j])
            centers.append(np.mean(np.array(cluster), axis=0))

        return np.array(centers)
    
    def unassign(self):
        self.assignment = [-1 for _ in range(len(self.data))]

    def are_diff(self, centers, new_centers):
        for i in range(self.k):
            if self.dist(centers[i], new_centers[i]) != 0:
                return True
        return False

    def dist(self, x, y):
        # Euclidean distance
        return sum((x - y)**2) ** (1/2)

    def lloyds(self, strategy):
        centers = self.initialize(strategy)
        self.make_clusters(centers)
        new_centers = self.compute_centers()
        self.snap(new_centers)
        while self.are_diff(centers, new_centers):
            self.unassign()
            centers = new_centers
            self.make_clusters(centers)
            new_centers = self.compute_centers()
            self.snap(new_centers)
        return

'''
X = np.random.rand(200, 2)
kmeans = KMeans(X, 4)
kmeans.lloyds(2)
images = kmeans.snaps

images[0].save(
    './static/kmeans.gif',
    optimize=False,
    save_all=True,
    append_images=images[1:],
    loop=0,
    duration=500
)
'''