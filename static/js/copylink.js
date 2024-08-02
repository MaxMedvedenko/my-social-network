function copyPostLink(buttonElement) {
    // Get the relative URL from the data attribute
    const relativeUrl = buttonElement.getAttribute('data-relative-url');
    
    // Construct the full URL
    const baseUrl = window.location.origin;
    const fullUrl = `${baseUrl}${relativeUrl}`;
    
    // Create a temporary input element to hold the URL
    const tempInput = document.createElement('input');
    tempInput.value = fullUrl;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);
    
    // Optionally, provide feedback to the user
    alert('Post link copied to clipboard!');
}
