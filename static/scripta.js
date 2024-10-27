function showLoading() {
    const loadingPopup = document.getElementById('loading');
    loadingPopup.classList.add('active'); // Add active class to show loading
}

function hideLoading() {
    const loadingPopup = document.getElementById('loading');
    loadingPopup.classList.remove('active'); // Remove active class to hide loading
}

 // Call this to hide loading after 3 seconds

// Function to toggle the chat screen's visibility
function toggleChat() {
    const chatScreen = document.getElementById('chat-screen');
    
    if (chatScreen.classList.contains('hidden')) {
      chatScreen.classList.remove('hidden'); // Show chat screen
    } else {
      chatScreen.classList.add('hidden'); // Hide chat screen
    }
  }
  
  
    