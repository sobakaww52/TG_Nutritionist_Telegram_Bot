 const registrationsCtx = document.getElementById('registrationsChart').getContext('2d');
  const registrationsChart = new Chart(registrationsCtx, {
      type: 'line',
      data: {
          labels: statsData.byDates.map(item => item.date),
          datasets: [{
              label: 'Регистрации',
              data: statsData.byDates.map(item => item.count),
              borderColor: 'rgb(75, 192, 192)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              tension: 0.1,
              fill: true
          }]
      },
      options: {
          responsive: true,
          plugins: {
              legend: {
                  display: true,
                  position: 'top'
              }
          },
          scales: {
              y: {
                  beginAtZero: true,
                  ticks: {
                      stepSize: 1
                  }
              }
          }
      }
  });

  // График распределения по целям
  const goalsCtx = document.getElementById('goalsChart').getContext('2d');
  const goalsChart = new Chart(goalsCtx, {
      type: 'doughnut',
      data: {
          labels: ['Похудение', 'Улучшение', 'Режим'],
          datasets: [{
              data: [
                  statsData.goals.weight_loss,
                  statsData.goals.improvement,
                  statsData.goals.mode
              ],
              backgroundColor: [
                  'rgba(220, 53, 69, 0.8)',
                  'rgba(25, 135, 84, 0.8)',
                  'rgba(255, 193, 7, 0.8)'
              ],
              borderColor: [
                  'rgb(220, 53, 69)',
                  'rgb(25, 135, 84)',
                  'rgb(255, 193, 7)'
              ],
              borderWidth: 1
          }]
      },
      options: {
          responsive: true,
          plugins: {
              legend: {
                  position: 'bottom'
              }
          }
      }
  });