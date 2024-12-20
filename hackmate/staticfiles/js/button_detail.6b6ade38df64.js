document.addEventListener('DOMContentLoaded', function () {
  const respondButton = document.querySelector('#respond-button');

  if (respondButton) {
      respondButton.addEventListener('click', function () {
          const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

          fetch(window.location.href, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': csrftoken,
              },
              body: JSON.stringify({ action: 'respond' }),
          })
              .then(response => response.json())
              .then(data => {
                  alert(data.message);
              })
              .catch(error => console.error('Error:', error));
      });
  }
});
