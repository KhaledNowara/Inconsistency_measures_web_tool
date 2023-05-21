const hamburgerMenu = document.querySelector(".hamburger-menu");
const menu = document.querySelector(".menu");
const content = document.querySelector(".mainView");
const measure = document.getElementById("measure");
const results = document.getElementById("results");
const ctx = document.getElementById("myChart");
const ctx2 = document.getElementById("myChart2");
var result_chart = null;
var timing_chart = null

// Toggle the menu when the hamburger menu is clicked
hamburgerMenu.addEventListener("click", function () {
  hamburgerMenu.classList.toggle("open");
  menu.classList.toggle("open");

  document.documentElement.style.setProperty("--content-margin", "300px"); // Adjust the margin as needed
});

// Close the menu when clicking elsewhere on the website
document.addEventListener("click", function (event) {
  const targetElement = event.target;
  // Check if the clicked element is inside the menu or the hamburger menu icon
  if (!menu.contains(targetElement) && !hamburgerMenu.contains(targetElement)) {
    // measure.style.display= "none";
    // results.style.display= "flex";
    hamburgerMenu.classList.remove("open");
    menu.classList.remove("open");
    document.documentElement.style.setProperty("--content-margin", "50px"); // Reset the margin
  }
});
function resetTextBox() {
  document.getElementById("textbox").value = "";
}

function sendData() {
  const inputText = document.getElementById("textbox").value;
  const measure_boxes = document.querySelectorAll(
    'input[name="measures"]:checked'
  );
  const witness_boxes = document.querySelectorAll(
    'input[name="witnesses"]:checked'
  );
  const res_depth = document.getElementById("res_depth").value;
  const measures = Array.from(measure_boxes).map((checkbox) => checkbox.value);
  const witnesses = Array.from(witness_boxes).map((checkbox) => checkbox.value);

  const data = {
    kb: inputText,
    measures: measures,
    witnesses: witnesses,
    res_depth: res_depth,
  };

  console.log(data);
  fetch("/process", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data.message);

      let timesSet = [];
      let resultsSet = [];
      // Iterate over the dataList
      for (let i = 0; i < data.message[0].length; i++) {
        let label = data.message[0][i][0]; // Extract the label
        let yAxis = data.message[0][i].slice(1);
        let dataset = {
          label: label,
          data: yAxis,
          borderWidth: 1,
        };

        resultsSet.push(dataset);
      }
      for (let i = 0; i < data.message[1].length; i++) {
        let label = data.message[1][i][0]; // Extract the label
        let yAxis = data.message[1][i].slice(1);
        let dataset = {
          label: label,
          data: yAxis,
          borderWidth: 1,
        };

        timesSet.push(dataset);
      }

      result_chart = createChart(ctx, measures, resultsSet, "Results");
      timing_chart = createChart(ctx2, measures, timesSet, "Elapsed timed");
      var tableBody = document.querySelector("#myTable tbody");
      var measures_row = document.createElement("tr");
      var results_row = document.createElement("tr");
      var timing_row = document.createElement("tr");

      // var cellm = document.createElement('th');
      // cellm.textContent = "Measure"
      // var cellr = document.createElement('th');
      // cellr.textContent = "Inconsistency Results"
      // var cellt = document.createElement('th');
      // cellt.textContent = "Time Elapsed in ms "
      // measures_row.append(cellm)
      // results_row.append(cellr)
      // timing_row.append(cellt)

      // for (var i = 0; i < measures.length; i++){
      //   var cellm = document.createElement('th');
      //   cellm.textContent = measures[i]
      //   var cellr = document.createElement('td');
      //   cellr.textContent = m_results[i].toFixed(2)
      //   var cellt = document.createElement('td');
      //   cellt.textContent = time[i].toFixed(4)
      //   measures_row.append(cellm)
      //   results_row.append(cellr)
      //   timing_row.append(cellt)
      // }
      tableBody.appendChild(measures_row);
      tableBody.appendChild(results_row);
      tableBody.appendChild(timing_row);

      measure.style.display = "none";
      results.style.display = "flex";

      // Do something with the response data
    })
    .catch((error) => {
      console.error("Error:", error);
    });
    


 
}

function createChart(chart, xAxis, yAxis, label) {
  return new Chart(chart, {
    type: "bar",
    data: {
      labels: xAxis,
      datasets: yAxis,
    },
    options: {
      plugins: {
        legend: {
          labels: {
            color: "#86c232", // Specify the desired font color
            font: {
              family: "Arial",
              size: 30,
            },
          },
        },
      },
      scales: {
        x: {
          ticks: {
            color: "#62893f", // Specify the desired font color
            font: {
              family: "Arial",
              size: 30,
            },
          },
        },
        y: {
          ticks: {
            color: "#62893f", // Specify the desired font color
            font: {
              family: "Arial",
              size: 30,
            },
          },
        },
      },
    },
  });
}

function viewCompute(){
  measure.style.display = "flex";
  results.style.display = "none";
  result_chart.destroy()
  timing_chart.destroy()
}
function resetCompute(){
  document.getElementById("textbox").value = "";
  document.getElementById("res_depth").value = "100";
  measure_boxes.forEach((checkbox) => {
    checkbox.checked = false;
  });
  witness_boxes.forEach((checkbox) => {
    checkbox.checked = false;
  });
  viewCompute()
}





// new Chart(ctx, {
//   type: 'bar',
//   data: {
//     labels: ['Red', 'Blue', 'Yellow', 'Green'],
//     datasets: [{
//       label: '# of Votes',
//       data: [12, 19, 3, 5],
//        backgroundColor: '#62893f', // Customize the colors here, // Optional: Set border colors
//       hoverBackgroundColor: '#86c232', // Optional: Set hover colors

//       borderWidth: 1
//     }]

//   },
//   options: {
//     plugins: {
//       legend: {
//         labels: {
//           color: '#86c232', // Specify the desired font color
//           font: {
//             family: 'Arial',
//             size: 30
//           }
//         }
//       }
//     },
//     scales: {
//       x: {
//         ticks: {
//           color: '#62893f', // Specify the desired font color
//           font: {
//             family: 'Arial',
//             size: 30
//           }
//         }
//       },
//       y: {
//         ticks: {
//           color: '#62893f', // Specify the desired font color
//           font: {
//             family: 'Arial',
//             size: 30
//           }
//         }
//       }
//     }
//   }
// });
// new Chart(ctx2, {
//   type: 'bar',
//   data: {
//     labels: ['Red', 'Blue', 'Yellow', 'Green'],
//     datasets: [{
//       label: '# of Votes',
//       data: [12, 19, 3, 5],
//       backgroundColor: '#86c232', // Customize the colors here
//       borderColor: '#86c232', // Optional: Set border colors
//       hoverBackgroundColor: '#86c232', // Optional: Set hover colors
//       hoverBorderColor: '#86c232', // Optional: Set hover border colors
//       borderWidth: 2
//     }]
//   },
//   options: {

//     scales: {
//       y: {
//         beginAtZero: true
//       }
//     }
//   }
// });
