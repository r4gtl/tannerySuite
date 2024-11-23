
// Dichiarare una variabile globale per memorizzare il riferimento al grafico
var myChart;
var fromDate = '';
var toDate = '';
var produzioneUrl = document.getElementById('url-container').getAttribute('data-produzione-url');
var energiaUrl = document.getElementById('url-container').getAttribute('data-energia-url');
var gasUrl = document.getElementById('url-container').getAttribute('data-gas-url');


function updateChartWithData(data, fromDate, toDate) {
  // Elabora i dati e aggiorna il grafico utilizzando Chart.js
  var labels = [];
  var quantities = [];

  for (var i = 0; i < data.length; i++) {
    labels.push(data[i].industries_served);
    quantities.push(data[i].total_quantity);
  }

  // Se il grafico è già stato creato, aggiorna i dati
  if (myChart) {
      myChart.data.labels = labels;
      myChart.data.datasets[0].data = quantities;
      myChart.update(); // Aggiorna il grafico con i nuovi dati
  } else {
      // Altrimenti, crea un nuovo grafico
      var ctx = document.getElementById('produzione').getContext('2d');
      myChart = new Chart(ctx, {
          type: 'bar',
          data: {
              labels: labels,
              datasets: [{
                  label: 'Total Quantity',
                  data: quantities,
                  backgroundColor: getRandomColor(),
                  borderColor: 'rgba(75, 192, 192, 1)',
                  borderWidth: 1
              }]
          },
          options: {
              scales: {
                  y: {
                      beginAtZero: true
                  }
              },
              plugins: {
                  legend: {
                      display: false  // Imposta il display della legenda su false per rimuoverla
                  }
              }
          }
      });
  }
}


function updateChartWithDataEnergia(data, fromDate, toDate) {
  
  var labels = [];
  var quantities = [];

  for (var i = 0; i < data.length; i++) {
    
    labels.push(data[i].mese);
    
    quantities.push(data[i].rapporto);
    
  }

  var ctx = document.getElementById('energia').getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Rapporto mensile in MJ tra Mq produzione e Kwh',
        data: quantities,
        backgroundColor: 'rgba(75, 192, 192, 0.2)', // Specifica un colore predefinito
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
      
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      },
      plugins: {
        legend: {
          display: false  // Imposta il display della legenda su false per rimuoverla
        }
      }
    }
  });
  
};  



function updateChartWithDataGas(data, fromDate, toDate) {
 
  
  var labels = [];
  var quantities = [];

  for (var i = 0; i < data.length; i++) {
    
    labels.push(data[i].mese);
    
    quantities.push(data[i].rapporto);
    
  }

  var ctx = document.getElementById('gas').getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Rapporto mensile in MJ tra Mq produzione e MC',
        data: quantities,
        backgroundColor: 'rgba(75, 192, 192, 0.2)', // Specifica un colore predefinito
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      },
      plugins: {
        legend: {
          display: false  // Imposta il display della legenda su false per rimuoverla
        }
      }
    }
  });
};


    function updateChart(url) {
      console.log("url produzione: " + url)
      fetch(url)
          .then(response => response.json())
          .then(data => {
              const labels = data.map(entry => entry.industries_served);
              const quantities = data.map(entry => entry.total_quantity);
  
              const ctx = document.getElementById('produzione').getContext('2d');
              const myChart = new Chart(ctx, {
                  type: 'bar',
                  data: {
                      labels: labels,
                      datasets: [{
                          label: 'Total Quantity',
                          data: quantities,
                          backgroundColor: 'rgba(75, 192, 192, 0.2)',
                          borderColor: 'rgba(75, 192, 192, 1)',
                          borderWidth: 1
                      }]
                  },
                  options: {
                      scales: {
                          y: {
                              beginAtZero: true
                          }
                      }
                  }
              });
          })
          .catch(error => console.log(error));
  }





  function setModalDates(submitButtonText = "Aggiorna dati") {
    
    // Imposta le date nel form del modal
    document.getElementById('from_date').value = fromDate;
    document.getElementById('to_date').value = toDate;
      
    // Cambia il testo del pulsante di invio nel modal
  document.querySelector('#myModal button[type="submit"]').innerText = submitButtonText;

    // Apri il modal
    var myModal = new bootstrap.Modal(document.getElementById('myModal'));
    myModal.show();
}


document.getElementById('date_form').addEventListener('submit', function (e) {
  e.preventDefault(); // Impedisce l'invio del form

  if (validateForm()) {
    // Ottieni le date selezionate
    var fromDate = document.getElementById('from_date').value;
    var toDate = document.getElementById('to_date').value;

    $('#myModal').modal('hide');

    //var intervalButton = document.getElementById('interval_button');
    //intervalButton.innerHTML = '<i class="bi bi-calendar3"></i> Dalla data ' + fromDate + ' alla data ' + toDate;
    document.getElementById('interval_button').innerHTML = '<i class="bi bi-calendar3"></i> Dalla data ' + new Date(fromDate).toLocaleDateString('it-IT') + '<br>alla data ' + new Date(toDate).toLocaleDateString('it-IT');


    // Esegui una richiesta AJAX per ottenere i dati aggiornati
    //var url = "{% url 'core:produzione' %}?from_date=" + fromDate + "&to_date=" + toDate;
    var url = produzioneUrl + "?from_date=" + fromDate + "&to_date=" + toDate;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Aggiorna il grafico con i nuovi dati
            updateChartWithData(data, fromDate, toDate);
            renderDataInTemplate(data, from_date, to_date);
        })
        .catch(error => console.error('Errore durante il recupero dei dati:', error));
        //Energia
        //var url = "{% url 'core:energia' %}?from_date=" + fromDate + "&to_date=" + toDate;
        var url = energiaUrl + "?from_date=" + fromDate + "&to_date=" + toDate;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                // Aggiorna il grafico con i nuovi dati
                updateChartWithDataEnergia(data, fromDate, toDate);
                renderDataInTemplateEnergia(data, from_date, to_date);
            })
            .catch(error => console.error('Errore durante il recupero dei dati:', error));
        //Gas
        //var url = "{% url 'core:gas' %}?from_date=" + fromDate + "&to_date=" + toDate;
        var url = gasUrl + "?from_date=" + fromDate + "&to_date=" + toDate;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                // Aggiorna il grafico con i nuovi dati
                updateChartWithDataGas(data, fromDate, toDate);
                renderDataInTemplateGas(data, from_date, to_date);
            })
            .catch(error => console.error('Errore durante il recupero dei dati:', error));
}
});


function renderDataInTemplateGas(data, from_date, to_date) {
// Seleziona l'elemento della tabella nel tuo template
 var tableBody = document.getElementById('data-table-body-gas');
 
 // Svuota il contenuto precedente della tabella
 tableBody.innerHTML = '';
 
 // Itera sui dati e crea righe della tabella per ogni record
 data.forEach(function(record) {
   var row = document.createElement('tr');
   
   // Crea le colonne della tabella per ogni campo del record
   var mesecolumn = document.createElement('td');
   var meseDate = new Date(record.mese);
   var meseText = meseDate.toLocaleString('default', { month: 'long' }); // Estrarre il mese in testo
   var annoText = meseDate.getFullYear(); // Estrarre l'anno
   mesecolumn.textContent = meseText + ' ' + annoText;
   row.appendChild(mesecolumn);
   
   var mjoulecolumn = document.createElement('td');
   mjoulecolumn.classList.add("text-end");

   mjoulecolumn.textContent = record.rapporto.toFixed(2);
   row.appendChild(mjoulecolumn);
   
   // Aggiungi la riga alla tabella
   tableBody.appendChild(row);
 });

 
}



function renderDataInTemplateEnergia(data, from_date, to_date) {
// Seleziona l'elemento della tabella nel tuo template
 var tableBody = document.getElementById('data-table-body-energia');
 
 // Svuota il contenuto precedente della tabella
 tableBody.innerHTML = '';
 
 // Itera sui dati e crea righe della tabella per ogni record
 data.forEach(function(record) {
   var row = document.createElement('tr');
   
   // Crea le colonne della tabella per ogni campo del record
   var mesecolumn = document.createElement('td');
   var meseDate = new Date(record.mese);
   var meseText = meseDate.toLocaleString('default', { month: 'long' }); // Estrarre il mese in testo
   var annoText = meseDate.getFullYear(); // Estrarre l'anno
   mesecolumn.textContent = meseText + ' ' + annoText;
   row.appendChild(mesecolumn);
   
   var mjoulecolumn = document.createElement('td');
   mjoulecolumn.classList.add("text-end");

   mjoulecolumn.textContent = record.rapporto.toFixed(2);
   row.appendChild(mjoulecolumn);
   
   // Aggiungi la riga alla tabella
   tableBody.appendChild(row);
 });

 // Aggiungi altre operazioni di rendering o manipolazione della tabella se necessario
}



function renderDataInTemplate(data, from_date, to_date) {
// Seleziona l'elemento della tabella nel tuo template
 var tableBody = document.getElementById('data-table-body-produzione');
 
 // Svuota il contenuto precedente della tabella
 tableBody.innerHTML = '';
 
 // Itera sui dati e crea righe della tabella per ogni record
 data.forEach(function(record) {
   var row = document.createElement('tr');
   
   // Crea le colonne della tabella per ogni campo del record
   var industriesServedColumn = document.createElement('td');
   industriesServedColumn.textContent = record.industries_served;
   row.appendChild(industriesServedColumn);
   
   var totalQuantityColumn = document.createElement('td');
   totalQuantityColumn.classList.add("text-end");
   totalQuantityColumn.textContent = record.total_quantity;
   row.appendChild(totalQuantityColumn);

   var totalMQColumn = document.createElement('td');
   totalMQColumn.classList.add("text-end");
   totalMQColumn.textContent = parseFloat(record.total_mq).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
   row.appendChild(totalMQColumn);

   var totalKgColumn = document.createElement('td');
   totalKgColumn.classList.add("text-end");
   totalKgColumn.textContent = record.total_kg;
   row.appendChild(totalKgColumn);
   
   // Aggiungi la riga alla tabella
   tableBody.appendChild(row);
 });

 // Aggiungi altre operazioni di rendering o manipolazione della tabella se necessario
} 

// Funzioni che vengono chiamate una volta che il DOM è caricato
// Inizializzano i grafici con i dati di default dell'ultimo anno



function fetchDataAndUpdateCharts(url, updateChartFunction, renderDataFunction) {
  fetch(url)
      .then(response => response.json())
      .then(data => {
          // Elabora i dati ricevuti e aggiorna il grafico nel tuo template
          updateChartFunction(data, from_date, to_date);
          renderDataFunction(data, from_date, to_date);
      })
      .catch(error => console.log(error));
}

// Funzione per aggiornare i dati di produzione
function fetchAndUpdateProduzione(fromDate, toDate) {
  var url = produzioneUrl + "?from_date=" + fromDate + "&to_date=" + toDate;
  console.log("url produzione dalla funzione: " + url)
  fetchDataAndUpdateCharts(url, updateChartWithData, renderDataInTemplate);
}

// Funzione per aggiornare i dati di energia
function fetchAndUpdateEnergia(fromDate, toDate) {
  var url = energiaUrl + "?from_date=" + fromDate + "&to_date=" + toDate;
  console.log("url energia dalla funzione: " + url)
  fetchDataAndUpdateCharts(url, updateChartWithDataEnergia, renderDataInTemplateEnergia);
}

// Funzione per aggiornare i dati di gas
function fetchAndUpdateGas(fromDate, toDate) {
  var url = gasUrl + "?from_date=" + fromDate + "&to_date=" + toDate;
  console.log("url gas dalla funzione: " + url)
  fetchDataAndUpdateCharts(url, updateChartWithDataGas, renderDataInTemplateGas);
}
 
