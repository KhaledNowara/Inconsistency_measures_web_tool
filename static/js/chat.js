const hamburgerMenu = document.querySelector('.hamburger-menu');
const menu = document.querySelector('.menu');
const content = document.querySelector('.content');

// Toggle the menu when the hamburger menu is clicked
hamburgerMenu.addEventListener('click', function() {
  hamburgerMenu.classList.toggle('open');
  menu.classList.toggle('open');
  
    document.documentElement.style.setProperty('--content-margin', '300px'); // Adjust the margin as needed


});

// Close the menu when clicking elsewhere on the website
document.addEventListener('click', function(event) {
  const targetElement = event.target;
  
  // Check if the clicked element is inside the menu or the hamburger menu icon
  if (!menu.contains(targetElement) && !hamburgerMenu.contains(targetElement)) {
    hamburgerMenu.classList.remove('open');
    menu.classList.remove('open');
    document.documentElement.style.setProperty('--content-margin', '20px'); // Reset the margin
  }
});
function resetTextBox() {
  document.getElementById('textbox').value = "";
}


function sendData() {
  const inputText = document.getElementById('textbox').value;
  const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
  const selectedOptions = Array.from(checkboxes).map(checkbox => checkbox.value);

  const data = {
    input_text: inputText,
    selected_options: selectedOptions
  };

  console.log(data)
  fetch('/process', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
    console.log(data.message);
    // Do something with the response data
  })
  .catch(error => {
    console.error('Error:', error);
  });

  document.getElementById('textbox').value = "";

}
