// let triggers = document.querySelectorAll('.dd-trigger');
//
// triggers.forEach(element => {
//     element.addEventListener('click', () => {
//         const firstElement = element.nextElementSibling;
//         if (firstElement && firstElement.classList.contains('dropdown')) {
//             // Toggle the display style
//             if (firstElement.style.display === 'flex') {
//                 firstElement.style.display = 'none'; // Hide dropdown
//             } else {
//                 firstElement.style.display = 'flex'; // Show dropdown
//             }
//         }
//     });
// });
//
//
// // Get all the elements with the class "target-element"
// var targetElements = document.querySelectorAll('.dd-trigger');
//
// // Loop through each target element
// targetElements.forEach(function(element) {
//   // Add an onclick event listener to each target element
//   element.addEventListener('click', function() {
//     // Get the corresponding tooltip element
//     var tooltip = this.nextElementSibling;
//
//     // Check the current display property value
//     var currentDisplay = window.getComputedStyle(tooltip).display;
//     // var currentOpacity = window.getComputedStyle(tooltip).opacity;
//
//     // Toggle the display property of the tooltip element
//     tooltip.style.display = currentDisplay === 'flex' ? 'none' : 'flex';
//     // tooltip.style.opacity = currentOpacity === '1' ? '0' : '1';
//   });
// });
