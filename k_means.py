import tensorflow as tf
import numpy as np
import pandas as pd
import pymysql
import csv

n_features = 2
n_clusters = 3
n_samples_per_cluster = 100
seed = 700

#db connect
con=pymysql.connect(host='52.78.192.119',port=3306,user='root',password='Cap2bowoo!',db='abeekx',charset='utf8')
cursor=con.cursor()


def choose_random_centroids(samples, n_clusters):
    # Step 0: Initialisation: Select `n_clusters` number of random points
    n_samples = tf.shape(samples)[0]
    random_indices = tf.random_shuffle(tf.range(0, n_samples))
    begin = [0,]
    size = [n_clusters,]
    size[0] = n_clusters
    centroid_indices = tf.slice(random_indices, begin, size)
    initial_centroids = tf.gather(samples, centroid_indices)
    return initial_centroids

def assign_to_nearest(samples, centroids):
    # Finds the nearest centroid for each sample
    expanded_vectors = tf.expand_dims(samples, 0)
    expanded_centroids = tf.expand_dims(centroids, 1)
    distances = tf.reduce_sum( tf.square(tf.subtract(expanded_vectors, expanded_centroids)), 2)
    mins = tf.argmin(distances, 0)
    nearest_indices = mins
    return nearest_indices

def update_centroids(samples, nearest_indices, n_clusters):
    # Updates the centroid to be the mean of all samples associated with it.
    nearest_indices = tf.to_int32(nearest_indices)
    partitions = tf.dynamic_partition(samples, nearest_indices, n_clusters)
    new_centroids = tf.concat([tf.expand_dims(tf.reduce_mean(partition, 0), 0) for partition in partitions], 0)
    return new_centroids

cursor.execute("SELECT pm10,pm25 FROM sensors")
samples=[]
for row in cursor:
    samples.append(tf.constant([float(row[0]),float(row[1])],dtype=tf.float32))

# disconnect db
cursor.close()
con.close()

initial_centroids = choose_random_centroids(samples, n_clusters)
nearest_indices = assign_to_nearest(samples, initial_centroids)
updated_centroids = update_centroids(samples, nearest_indices, n_clusters)

model = tf.global_variables_initializer()
with tf.Session() as session:
    sample_values = session.run(samples)
    updated_centroid_value = session.run(updated_centroids)
    print(updated_centroid_value)


