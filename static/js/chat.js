const hamburgerMenu = document.querySelector('.hamburger-menu');
const menu = document.querySelector('.menu');
const content = document.querySelector('.content');

// Toggle the menu when the hamburger menu is clicked
hamburgerMenu.addEventListener('click', function() {
  hamburgerMenu.classList.toggle('open');
  menu.classList.toggle('open');
  
    document.documentElement.style.setProperty('--content-margin', '300px'); // Adjust the margin as needed
    console.log("I am trying")

});

// Close the menu when clicking elsewhere on the website
document.addEventListener('click', function(event) {
  const targetElement = event.target;
  
  // Check if the clicked element is inside the menu or the hamburger menu icon
  if (!menu.contains(targetElement) && !hamburgerMenu.contains(targetElement)) {
    hamburgerMenu.classList.remove('open');
    menu.classList.remove('open');
    document.documentElement.style.setProperty('--content-margin', '0px'); // Reset the margin
  }
});
