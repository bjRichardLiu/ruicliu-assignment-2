from flask import Flask, render_template, request, jsonify, send_file, redirect
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

@app.route('/step_through_kmeans')
def step_through_kmeans_route():
    # Step through the kmeans.gif
    global counter
    global num_iterations
    counter += 1
    if counter > num_iterations:
        counter = 0
    # TODO
    return render_template('index.html', image_url='kmeans.gif')

@app.route('/run_to_converg')
def run_to_converg_route():
    # Returns the kmeans.gif
    return render_template('index.html', image_url='kmeans.gif')

@app.route('/reset')
def reset_route():
    global counter
    counter = 0
    images = os.listdir('./static')
    # Remove all images except the data image
    for image in images:
        if 'data' not in image and 'js' not in image and 'css' not in image:
            os.remove(f'./static/{image}')
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
    images[0].save(
        './static/kmeans.gif',
        optimize=False,
        save_all=True,
        append_images=images[1:],
        loop=0,
        duration=500
    )
    global counter
    global num_iterations
    counter = 0
    num_iterations = len(images)
    # Return the starting image
    return send_file('./static/temp.png')

# Main function
if __name__ == "__main__":
    app.run(port=3000, debug=True) 