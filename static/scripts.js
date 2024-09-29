function runKmeans() {
    // Get the input fields
    const kInput = document.getElementById('k');
    const initInput = document.getElementById('init');

    // Get the values of the input fields
    const k = kInput.value;
    const init = initInput.value;

    // Cast the values to integers
    const kInt = parseInt(k);
    const initInt = parseInt(init);

    // Log the values for debugging
    console.log('Running K-Means with k =', kInt, 'and init =', initInt);

    // Send a POST request to the '/run_kmeans' route with the form data
    const formData = new FormData();
    formData.append('k', kInt);
    formData.append('init', initInt);

    fetch('/run_kmeans', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        response.blob();
        location.reload();
    })
    .then(imageBlob => {
        // Convert the image blob to a URL and display the image
        const imageURL = URL.createObjectURL(imageBlob);
        const kmeansImage = document.getElementById('kmeansImage');
        kmeansImage.src = imageURL;
        kmeansImage.style.display = 'block';
    })
    .catch(error => console.error('Error:', error));
}

function generateData() {
    // Log a message for debugging
    console.log('Generating new data...');

    // Send a POST request to the '/generate_data' route
    fetch('/generate_data', {
        method: 'POST',
    })
    .then(response => response.blob())
    .then(imageBlob => {
        // Convert the image blob to a URL and display the image
        const imageURL = URL.createObjectURL(imageBlob);
        const kmeansImage = document.getElementById('kmeansImage');
        kmeansImage.src = imageURL;
        kmeansImage.style.display = 'block';
    })
    .catch(error => console.error('Error:', error));
}

let frameIndex = 0;
let intervalId = null;
let continueRunning = true;

function stepThroughKmeans() {
    fetch(`/should_continue?frameIndex=${frameIndex}`)
    .then(response => response.json())
    .then(data => {
        if (!data.continue) {
            clearInterval(intervalId);
            continueRunning = false;
        }
    })
    .catch(error => console.error('Error:', error));
    console.log(continueRunning);
    if (!continueRunning) {
        return;
    }
    fetch(`/get_frame?frameIndex=${frameIndex}`)
    .then(response => response.blob())
    .then(imageBlob => {
        const imageURL = URL.createObjectURL(imageBlob);
        const kmeansImage = document.getElementById('kmeansImage');
        kmeansImage.src = imageURL;
        kmeansImage.style.display = 'block';
        frameIndex++;
    })
    .catch(error => console.error('Error:', error));
}

function runToConvergence() {
    // Stop any ongoing autoplay
    if (intervalId) {
        clearInterval(intervalId);
    }
    frameIndex = 0;
    // Start autoplay
    intervalId = setInterval(stepThroughKmeans, 200);
}

function reset() {
    // Stop any ongoing autoplay
    if (intervalId) {
        clearInterval(intervalId);
    }
    // Reset the frame index
    frameIndex = 0;
    continueRunning = true;
    fetch('/reset')
    .then(() => {
        const kmeansImage = document.getElementById('kmeansImage');
        kmeansImage.src = '';
        kmeansImage.style.display = 'none';
        location.reload();
    })
    .catch(error => console.error('Error:', error));
}