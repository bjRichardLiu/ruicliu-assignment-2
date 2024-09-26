from flask import Flask, render_template, request, jsonify, send_file
from backend import run_kmeans


app = Flask(__name__)

# Root URL 
@app.get('/') 
def home(): 
    return render_template('index.html')

@app.route('/run_kmeans')
def run_kmeans_route():
    # Get the number of clusters from the query parameters
    k = int(request.args.get('k'))
    # Get the type of initialization from the query parameters
    init = request.args.get('init')
    # Run the Kmeans algorithm
    run_kmeans(k, init)
    
    # Send the plot back to the front-end
    return send_file('./kmeans.png', mimetype='image/png')

# Main function
if __name__ == "__main__":
    app.run(debug=True) 