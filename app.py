from flask import Flask, render_template, request, jsonify, send_file, redirect, send_from_directory
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template 
import matplotlib 
from kmeans import KMeans
matplotlib.use('Agg') 

app = Flask(__name__)
counter = 0
num_iterations = 0

# Root URL 
@app.get('/') 
def home(): 
    return render_template('index.html')

@app.route('/generate_data', methods=['POST'])
def generate_data_route():
    # Generate random data
    KMeans.generate_data(200)
    return send_file('./static/data.png')

@app.route('/get_frame')
def get_frame():
    frameIndex = request.args.get('frameIndex')
    global num_iterations
    if int(frameIndex) >= num_iterations:
        return send_file('./static/temp.png')
    return send_from_directory(f'static/kmeans', f'frame{frameIndex}.png')

@app.route('/should_continue')
def should_continue():
    frameIndex = request.args.get('frameIndex')
    print(frameIndex)
    print(num_iterations)
    return {'continue': int(frameIndex) < num_iterations}

@app.route('/reset')
def reset_route():
    global counter
    counter = 0
    images = os.listdir('./static/kmeans')
    # Remove all images except the data image
    for image in images:
        if 'data' not in image and 'js' not in image and 'css' not in image:
            os.remove(f'./static/kmeans/{image}')
    return redirect('/')

@app.route('/run_kmeans', methods=['POST'])
def run_kmeans_route():
    # Get the number of clusters from the form data
    k = int(request.form.get('k'))
    # Get the type of initialization from the form data
    init = int(request.form.get('init'))
    print(k, init)
    # Read the data from the data.txt file
    data = np.loadtxt('./static/data.txt')
    # Run the Kmeans algorithm
    kmeans = KMeans(data, k)
    kmeans.lloyds(init)
    images = kmeans.snaps
    # Store all the images in static folder
    for i, image in enumerate(images):
        image.save(f'./static/kmeans/frame{i}.png')
    global counter
    global num_iterations
    counter = 0
    num_iterations = len(images)
    print(num_iterations)
    # Return the starting image
    return send_file('./static/temp.png')

# Main function
if __name__ == "__main__":
    app.run(port=3000, debug=True) 