let offset = 0;
const limit = 10;
const vacanciesContainer = document.querySelector('.vacancies');
let isLoading = false;
let lastScrollTop = 0;
let scrollThreshold = 40;

window.addEventListener('scroll', handleScroll);

function handleScroll() {
    const scrollTop = window.scrollY;
    const isScrollingDown = scrollTop - lastScrollTop > 0;
    const scrolledEnough = scrollTop - lastScrollTop > scrollThreshold;

    if (isScrollingDown && scrolledEnough && isBottomOfPage() && !isLoading) {
        loadMoreVacancies();
    }

    lastScrollTop = scrollTop;
}

function isBottomOfPage() {
    return window.innerHeight + window.scrollY >= document.body.offsetHeight;
}

function loadMoreVacancies() {
    isLoading = true;
    offset += limit;

    fetch(`/api/vacancies/?offset=${offset}&limit=${limit}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            data.forEach(vacancy => {
                const vacancyElement = createVacancyElement(vacancy);
                vacanciesContainer.appendChild(vacancyElement);
            });
            isLoading = false;
        })
        .catch(error => {
            console.error('Ошибка загрузки вакансий:', error);
            isLoading = false;
        });
}

function createVacancyElement(vacancy) {
    const card = document.createElement('div');
    card.classList.add('card', 'w-75', 'mb-3');

    const cardBody = document.createElement('div');
    cardBody.classList.add('card-body');

    const title = document.createElement('h5');
    title.classList.add('card-title');
    title.textContent = vacancy.title;

    const description = document.createElement('p');
    description.classList.add('card-text');
    description.textContent = vacancy.description;

    const userInfo = document.createElement('a');
    userInfo.href = vacancy.creater.profile_url;
    userInfo.classList.add('user-info');

    const avatar = document.createElement('img');
    avatar.src = vacancy.creater.profile_image || '/static/img/default-avatar.jpg';
    avatar.alt = 'User Avatar';
    avatar.classList.add('avatar');
    userInfo.appendChild(avatar);

    const username = document.createElement('p');
    username.classList.add('username');
    username.textContent = vacancy.creater.username;
    userInfo.appendChild(username);

    const detailLink = document.createElement('a');
    detailLink.href = vacancy.vacancy_url;
    detailLink.classList.add('grow-button');
    detailLink.textContent = 'Детальнее';

    cardBody.appendChild(title);
    cardBody.appendChild(description);
    cardBody.appendChild(userInfo);
    cardBody.appendChild(detailLink);

    card.appendChild(cardBody);

    return card;
}