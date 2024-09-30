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

    // If init = 3, let the user select center points manually
    if (initInt === 3) {
        const kmeansImage = document.getElementById('kmeansImage');
        const centers = [];
        kmeansImage.addEventListener('click', function(event) {
            // Calculate the coordinates of the click relative to the image
            const rect = kmeansImage.getBoundingClientRect();
            const x = (event.clientX - rect.left) / kmeansImage.width;
            const y = (event.clientY - rect.top) / kmeansImage.height;

            // Log the coordinates for debugging
            console.log('User selected center point at', x, y);

            // Add the coordinates to the centers array
            centers.push([(1 - x), (1 - y));

            // Create a new div element
            const dot = document.createElement('div');
            // Add the dot class to the dot
            dot.classList.add('dot');

            // Position the dot
            dot.style.left = (x * kmeansImage.width + rect.left - 5) + 'px';
            dot.style.top = (y * kmeansImage.height + rect.top - 5) + 'px';

            // Add the dot to the DOM
            document.body.appendChild(dot);

            // If the user has selected k centers, send them to the server and run K-Means
            if (centers.length === kInt) {
                const formData = new FormData();
                formData.append('k', kInt);
                formData.append('init', initInt);
                formData.append('centers', JSON.stringify(centers));

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
        });
    } else {
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