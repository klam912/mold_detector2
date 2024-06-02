document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('image-upload');
    const resultDiv = document.getElementById('result');
    const moldyInfoDiv = document.getElementById('moldy-info');
    const nonMoldyInfoDiv = document.getElementById('non-moldy-info');

    if (fileInput.files.length === 0) {
        resultDiv.innerText = 'Please select an image file to upload.';
        return;
    }

    resultDiv.innerText = 'Uploading and classifying...';

    const formData = new FormData();
    formData.append('image', fileInput.files[0]);

    try {
        const response = await fetch('http://127.0.0.1:5000/upload/', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }

        const result = await response.json();
        resultDiv.innerText = `${result.classification}`;

        // Show additional information based on the result
        if (result.classification.toLowerCase() === 'moldy') {
            moldyInfoDiv.style.display = 'block';
            nonMoldyInfoDiv.style.display = 'none';
        } else {
            nonMoldyInfoDiv.style.display = 'block';
            moldyInfoDiv.style.display = 'none';
        }
    } catch (error) {
        resultDiv.innerText = `Error: ${error.message}`;
    }
});