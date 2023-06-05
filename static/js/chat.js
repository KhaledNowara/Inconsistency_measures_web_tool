const menu = document.querySelector(".menu");
const content = document.querySelector(".mainView");
const measure = document.getElementById("measure");
const results = document.getElementById("results");
const createWitness = document.getElementById("createWitness")
const deduction = document.getElementById("deduction");
const cut1 = document.getElementById("cut1");
const cut2 =  document.getElementById("cut2")
const sidebar = document.getElementById("sidebar")
const ctx = document.getElementById("myChart");
const ctx2 = document.getElementById("myChart2");
const witness_list = ['Resolution', 'Membership', 'Mpc', 'Complementary'];
const listContainer = document.getElementById('checkboxList');
const menuItems = document.querySelectorAll('.menu .icon');
var result_chart = null;
var timing_chart = null

witness_list.forEach((item) => {
  // Create checkbox element
  checkbox = document.createElement('input');
  checkbox.type = 'checkbox';
  checkbox.name = "witnesses";
  checkbox.value = item ;
  if (item === "Resolution"){
    const numbox = document.createElement('input');
    numbox.type = 'number'
    numbox.className = 'num-input'
    numbox.id = "res_depth"
    numbox.min = "0"
    numbox.max = "9999999999"
    numbox.step = "1"
    numbox.value = "100"
    const container = document.createElement('div');
    container.className = "res_input";
    container.appendChild(checkbox);
    container.appendChild(numbox);
    checkbox = container   
  }
  // Create label element
  const label = document.createElement('label');
  label.textContent = item;
  label.className = "checkbox-label"
  // label.setAttribute('for', checkbox.id);
  
  // Create list item element
  const listItem = document.createElement('li');
  
  // Append checkbox and label to the list item
  listItem.appendChild(label);
  listItem.appendChild(checkbox);
 
  
  // Append list item to the list container
  listContainer.appendChild(listItem);
});

menuItems.forEach((menuItem) => {
  const label = menuItem.querySelector('.label').textContent;
  menuItem.addEventListener('click', () => {
    // Perform the desired action based on the label
    switch (label) {
      case 'Measure':
        // Action for Home label
        viewCompute()
        break;
      case 'Create E-Witness':

      measure.style.display  = "none";
      results.style.display = "none";
      createWitness.style.display = "flex";

      viewDeduction()
        break;
      // Add cases for other labels
      default:
        // Default action
        console.log('Clicked on unknown label');
        break;
    }
    // Add your code here to handle the click event for each label
  });
});

function viewDeduction (){

  deduction.style.display = "flex"
  cut1.style.display = "none"
  cut2.style.display = "none"


  
  const container = document.getElementById('dropdownContainer');
  container.innerHTML = ""

  // Create select element
  const selectElement = document.createElement('select');
  selectElement.id = ('deduction_dropdown')

  // Iterate over the list and create option elements
  witness_list.forEach((item) => {
    const option = document.createElement('option');
    option.value = item;
    option.text = item;
    selectElement.appendChild(option);
  });

  // Append the select element to the container
  container.appendChild(selectElement);
}

function viewCut1 (){

  deduction.style.display = "none"
  cut1.style.display = "flex"
  cut2.style.display = "none"

  const container = document.getElementById('dropdownContainer1');
  const container2 = document.getElementById('dropdownContainer2');

  container.innerHTML = ""
  container2.innerHTML = ""

  // Create select element
  const selectElement = document.createElement('select');
  selectElement.id = ('cut1_dropdown1')
  const selectElement2 = document.createElement('select');
  selectElement2.id = ('cut1_dropdown2')

  // Iterate over the list and create option elements
  witness_list.forEach((item) => {
    const option = document.createElement('option');
    option.value = item;
    option.text = item;
    const option2 = document.createElement('option');
    option2.value = item;
    option2.text = item;
    selectElement.appendChild(option);
    selectElement2.appendChild(option2);

  });

  // Append the select element to the container
  container.appendChild(selectElement);
  container2.appendChild(selectElement2);
  

}

function viewCut2 (){

  deduction.style.display = "none"
  cut1.style.display = "none"
  cut2.style.display = "flex"




  const container = document.getElementById('c2dropdownContainer1');
  const container2 = document.getElementById('c2dropdownContainer2');

  container.innerHTML = ""
  container2.innerHTML = ""

  // Create select element
  const selectElement = document.createElement('select');
  selectElement.id = ('cut2_dropdown1')
  const selectElement2 = document.createElement('select');
  selectElement2.id = ('cut2_dropdown2')

  // Iterate over the list and create option elements
  witness_list.forEach((item) => {
    const option = document.createElement('option');
    option.value = item;
    option.text = item;
    const option2 = document.createElement('option');
    option2.value = item;
    option2.text = item;
    selectElement.appendChild(option);
    selectElement2.appendChild(option2);

  });

  // Append the select element to the container
  container.appendChild(selectElement);
  container2.appendChild(selectElement2);
  

}




function createDeductionWitness() {
  const dropdown = document.getElementById('deduction_dropdown');
  const selectedOption = dropdown.options[dropdown.selectedIndex];
  const witness = selectedOption.value;
  const name = document.getElementById("deduction_name").value;
  const data = {
    witness: witness,
    name: name,

  };
  witness_list.push(name)
  checkbox = document.createElement('input');
  checkbox.type = 'checkbox';
  checkbox.name = "witnesses";
  checkbox.value = name ;
  const label = document.createElement('label');
  label.textContent = name;
  label.className = "checkbox-label"
  // label.setAttribute('for', checkbox.id);
  
  // Create list item element
  const listItem = document.createElement('li');
  
  // Append checkbox and label to the list item
  listItem.appendChild(label);
  listItem.appendChild(checkbox);
 
  
  // Append list item to the list container
  listContainer.appendChild(listItem);

  console.log(data);
  fetch("/createD", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {

    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function createCut1Witness() {
  const dropdown1 = document.getElementById('cut1_dropdown1');
  const selectedOption1 = dropdown1.options[dropdown1.selectedIndex];
  const dropdown2 = document.getElementById('cut1_dropdown2');
  const selectedOption2 = dropdown2.options[dropdown2.selectedIndex];
  const witness1 = selectedOption1.value;
  const witness2 = selectedOption2.value;
  const languageSubset = document.getElementById("cut1_language").value;

  const name = document.getElementById("cut1_name").value;
  const data = {
    witness1: witness1,
    witness2: witness2,
    languageSubset:languageSubset,
    name: name

  };


  console.log(data);
  fetch("/createC1", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      witness_list.push(name)
      checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.name = "witnesses";
      checkbox.value = name ;
      const label = document.createElement('label');
      label.textContent = name;
      label.className = "checkbox-label"
      // label.setAttribute('for', checkbox.id);
      
      // Create list item element
      const listItem = document.createElement('li');
      
      // Append checkbox and label to the list item
      listItem.appendChild(label);
      listItem.appendChild(checkbox);
     
      
      // Append list item to the list container
      listContainer.appendChild(listItem);

    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
function createCut2Witness() {
  const dropdown1 = document.getElementById('cut2_dropdown1');
  console.log(dropdown1)
  const selectedOption1 = dropdown1.options[dropdown1.selectedIndex];
  const dropdown2 = document.getElementById('cut2_dropdown2');
  const selectedOption2 = dropdown2.options[dropdown2.selectedIndex];
  const witness1 = selectedOption1.value;
  const witness2 = selectedOption2.value;
  const languageSubset = document.getElementById("cut2_language").value;

  const name = document.getElementById("cut2_name").value;
  const data = {
    witness1: witness1,
    witness2: witness2,
    languageSubset:languageSubset,
    name: name

  };


  console.log(data);
  fetch("/createC2", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      witness_list.push(name)
      checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.name = "witnesses";
      checkbox.value = name ;
      const label = document.createElement('label');
      label.textContent = name;
      label.className = "checkbox-label"
      // label.setAttribute('for', checkbox.id);
      
      // Create list item element
      const listItem = document.createElement('li');
      
      // Append checkbox and label to the list item
      listItem.appendChild(label);
      listItem.appendChild(checkbox);
     
      
      // Append list item to the list container
      listContainer.appendChild(listItem);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
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
      let resultsForThesis = ""
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
        resultsForThesis = resultsForThesis + label

        resultsForThesis = resultsForThesis + yAxis     
        timesSet.push(dataset);
      }
      console.log ("xAxis:",measures)
      console.log("yAxis:",resultsForThesis)
      // console.log ("yAxis:", resultsForThesis)
//       resultsForThesis.forEach((witness) => {
//         console.log(witness)
//         // witness[1].forEach((res) => {
//         //   console.log(res)
//         // })
//     }
// );
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
      deduction.style.display = "none";
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
  createWitness.style.display = "none";

  result_chart.destroy()
  timing_chart.destroy()
}
function resetCompute(){
  document.getElementById("textbox").value = "";
  document.getElementById("res_depth").value = "100";
  const measure_boxes = document.querySelectorAll(
    'input[name="measures"]:checked'
  );
  const witness_boxes = document.querySelectorAll(
    'input[name="witnesses"]:checked'
  );
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
