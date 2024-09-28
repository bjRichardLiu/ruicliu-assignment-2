from flask import Flask, render_template, request, jsonify, send_file
from backend import run_kmeans, generate_data
import os
import json


app = Flask(__name__)
counter = 0
num_iterations = 0

# Root URL 
@app.get('/') 
def home(): 
    return render_template('index.html')

@app.route('/generate_data')
def generate_data_route():
    # Generate random data
    generate_data(200)
    return send_file('./static/data.png')

@app.route('/step_through_kmeans')
def step_through_kmeans_route():
    # returns the next img to show
    global counter
    global num_iterations
    counter += 1
    if counter > num_iterations:
        counter = num_iterations
    return send_file(f'./static/kmeans_step_{counter}.png')

@app.route('/run_to_converg')
def run_to_converg_route():
    images = os.listdir('./static')
    images = [image for image in images if 'kmeans_step' in image]
    images.sort()
    image_urls = [f'/static/{image}' for image in images]
    return jsonify(image_urls)

@app.route('/reset')
def reset_route():
    global counter
    counter = 0
    images = os.listdir('./static')
    # Remove all images except the data image
    for image in images:
        if 'data' not in image:
            os.remove(f'./static/{image}')
    return 'Counter reset'

@app.route('/run_kmeans')
def run_kmeans_route():
    # Get the number of clusters from the query parameters
    k = int(request.args.get('k'))
    # Get the type of initialization from the query parameters
    init = request.args.get('init')
    # Run the Kmeans algorithm
    iter = run_kmeans(k, init)
    counter = 0
    num_iterations = iter
    images = os.listdir('./static')
    for image in images:
        if 'data' not in image:
            os.remove(f'./static/{image}')
    
    # Return the number of iterations
    return iter

# Main function
if __name__ == "__main__":
    app.run(port=3000, debug=True) 