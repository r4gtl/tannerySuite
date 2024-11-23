function updateChart(url) {
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            var labels = [];
            var quantities = [];

            for (var i = 0; i < data.length; i++) {
                labels.push(data[i].industries_served);
                quantities.push(data[i].total_quantity);
            }

            var ctx = document.getElementById('produzione_ultimo_anno').getContext('2d');
            var myChart = new Chart(ctx, {
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
};


function renderizzaGrafico(url) {

fetch(url)
  .then(response => response.json())
  .then(data => {
    // Recupera i dati per il rapporto del gas e dell'energia
    var rapportoGas = data.rapporto_gas;
    var rapportoEnergia = data.rapporto_energia;

    // Recupera i mesi per l'asse X
    var mesi = rapportoGas.map(item => item.mese);

    // Recupera i valori del rapporto del gas per l'asse Y
    var valoriGas = rapportoGas.map(item => item.rapporto);

    // Recupera i valori del rapporto dell'energia per l'asse Y
    var valoriEnergia = rapportoEnergia.map(item => item.rapporto);

    // Crea il grafico utilizzando Chart.js
    var ctx = document.getElementById('grafico').getContext('2d');
    var grafico = new Chart(ctx, {
      type: 'line',
      data: {
        labels: mesi,
        datasets: [
          {
            label: 'Rapporto Gas',
            data: valoriGas,
            borderColor: 'red',
            fill: false
          },
          {
            label: 'Rapporto Energia',
            data: valoriEnergia,
            borderColor: 'blue',
            fill: false
          }
        ]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  })
  .catch(error => {
    //console.error('Si è verificato un errore:', error);
  });
};