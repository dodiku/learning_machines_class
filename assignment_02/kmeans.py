import numpy as np
# import matplotlib.pyplot as plt

## generate a random 2d points
class Kmeans:

    def __init__(self, number_of_points):
        self.number_of_points = number_of_points
        self.points = (np.random.randint(100, size=number_of_points),np.random.randint(100, size=number_of_points))

    def init_centers(self, number_of_clusters):
        self.centers = [ [], [] ]

        for i in range(number_of_clusters):
            self.centers[0].append(np.random.randint(100, size=self.number_of_points))
            self.centers[1].append(np.random.randint(100, size=self.number_of_points))

    def cluster(self, number_of_clusters):

        self.number_of_clusters = number_of_clusters

        self.init_centers(number_of_clusters)
        self.labels = self.points[0]

        return self.labels, self.centers


clusters = Kmeans(100)
labels, centers = clusters.cluster(3)

print ('🔆  ayyy')
