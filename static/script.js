document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const notification = document.getElementById('notification');
    const uploadUrl = form.getAttribute('data-upload-url');
    const piiResults = document.getElementById('pii-results');
    const documentViewer = document.getElementById('document-viewer');
    let uploadedText = '';

    // Define PII types
    const PII_TYPES = new Set([
        'PERSON', 'EMAIL', 'PHONE_NUMBER', 'SSN', 'CREDIT_CARD',
        'PASSPORT', 'BANK_ACCOUNT', 'ADDRESS', 'DOB', 'DRIVER_LICENSE'
    ]);

    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        const formData = new FormData(form);
        
        try {
            const response = await fetch(uploadUrl, {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            
            if (response.ok) {
                showNotification(data.message, 'success');
                displayResults(data.pii_result);
                
                // Read and display the uploaded file content
                const file = formData.get('file');
                const reader = new FileReader();
                reader.onload = function(e) {
                    uploadedText = e.target.result;
                    displayDocument(uploadedText, data.pii_result);
                };
                reader.readAsText(file);
            } else {
                showNotification(data.message, 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('An error occurred while processing the file.', 'error');
        }
    });

    function displayResults(results) {
        piiResults.innerHTML = '';
        
        // Create containers for PII and non-PII data
        const piiContainer = document.createElement('div');
        const nonPiiContainer = document.createElement('div');
        
        piiContainer.innerHTML = '<h3 class="results-subtitle">PII Data Found:</h3>';
        nonPiiContainer.innerHTML = '<h3 class="results-subtitle">Non-PII Data:</h3>';
        
        const piiList = document.createElement('ul');
        const nonPiiList = document.createElement('ul');
        
        if (results && results.length > 0) {
            results.forEach(result => {
                const li = document.createElement('li');
                li.innerHTML = `<strong>${result.entity}:</strong> ${result.text}`;
                
                // Categorize as PII or non-PII
                if (PII_TYPES.has(result.entity)) {
                    li.classList.add('pii-item');
                    piiList.appendChild(li);
                } else {
                    li.classList.add('non-pii-item');
                    nonPiiList.appendChild(li);
                }
            });
        }
        
        // Add lists to containers
        piiContainer.appendChild(piiList);
        nonPiiContainer.appendChild(nonPiiList);
        
        // Add containers to results
        piiResults.appendChild(piiContainer);
        piiResults.appendChild(nonPiiContainer);
        
        // Show message if no results
        if (!results || results.length === 0) {
            piiResults.innerHTML = '<li>No data detected</li>';
        }
    }

    function displayDocument(text, piiResults) {
        // Create a temporary div to handle HTML escaping
        const tempDiv = document.createElement('div');
        tempDiv.textContent = text;
        let displayText = tempDiv.innerHTML;
        
        // Sort results by start position in reverse order
        const sortedResults = [...piiResults].sort((a, b) => b.start - a.start);
        
        // Process each result
        sortedResults.forEach(result => {
            const before = displayText.substring(0, result.start);
            const content = displayText.substring(result.start, result.end);
            const after = displayText.substring(result.end);
            
            // Create the highlight span
            const isPII = PII_TYPES.has(result.entity);
            const className = `highlight ${isPII ? 'pii' : 'non-pii'}`;
            const highlightSpan = `<span class="${className}" data-type="${result.entity}">${content}</span>`;
            
            // Update the display text
            displayText = before + highlightSpan + after;
        });
        
        // Replace newlines with <br> tags and display the result
        documentViewer.innerHTML = displayText.replace(/\n/g, '<br>');
    }

    function showNotification(message, type = 'info') {
        notification.textContent = message;
        notification.className = `notification ${type}`;
        notification.classList.add('show');
        setTimeout(() => {
            notification.classList.remove('show');
        }, 4000);
    }
});
