// Get the dropdown button and menu elements
const dropdownButton = document.getElementById('dropdownMenuButton1');
const dropdownMenu = document.getElementById('dropdownMenu');

// Function to toggle the dropdown menu visibility
function toggleDropdown() {
  dropdownMenu.classList.toggle('show');
}

// Event listener to show/hide the dropdown menu on button click
dropdownButton.addEventListener('click', toggleDropdown);

// Event listener to hide the dropdown menu when clicking outside of it
window.addEventListener('click', function(event) {
  if (!event.target.matches('.btn-secondary')) {
    dropdownMenu.classList.remove('show');
  }
});
