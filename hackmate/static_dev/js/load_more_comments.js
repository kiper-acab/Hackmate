let offset = 0;
const limit = 10;
const commentsContainer = document.querySelector('.comments');
let isLoading = false;
const vacancyId = document.getElementById('vacancy-id').value;

window.addEventListener('scroll', handleScroll);

function handleScroll() {
    if (isBottomOfPage() && !isLoading) {
        loadMoreData(`/api/comments/${vacancyId}/?offset=${offset}&limit=${limit}`, appendVacancies);
    }

    if (commentsContainer && isBottomOfElement(commentsContainer) && !isLoading) {
        loadMoreData(`/api/comments/?vacancy_id=${vacancyId}&offset=${offset}&limit=${limit}`, appendComments);
    }
}

function isBottomOfPage() {
    return window.innerHeight + window.scrollY >= document.body.offsetHeight;
}

function isBottomOfElement(element) {
    return window.innerHeight + window.scrollY >= element.offsetHeight;
}

function loadMoreData(url, callback) {
    isLoading = true;
    offset += limit;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            callback(data);
            isLoading = false;
        })
        .catch(error => {
            console.error('Ошибка загрузки данных:', error);
            isLoading = false;
        });
}

function appendVacancies(data) {
    data.forEach(vacancy => {
        const vacancyElement = createCommentElement(vacancy, vacancy.current_user, vacancy.is_admin);
        commentsContainer.appendChild(vacancyElement);
    });
}

function appendComments(data) {
    data.forEach(comment => {
        const commentElement = createCommentElement(comment, data.current_user, data.is_admin);
        commentsContainer.appendChild(commentElement);
    });
}

function createCommentElement(comment, currentUser = '', isSuperuser = false) {
    const commentCard = document.createElement('div');
    commentCard.classList.add('comment');

    const header = document.createElement('header');
    header.classList.add('comment-header');

    const userLink = document.createElement('a');
    userLink.href = comment.user_url;
    userLink.classList.add('user-a');

    const userSpan = document.createElement('span');
    userSpan.classList.add('comment-user');

    const avatar = document.createElement('img');
    avatar.src = comment.user.profile_image || '/static/img/default-avatar.jpg';
    avatar.classList.add('user-image');
    avatar.alt = `${comment.user}'s avatar`;

    const usernameText = document.createTextNode(comment.user);

    userSpan.append(avatar, usernameText);
    userLink.appendChild(userSpan);

    const figure = document.createElement('figure');

    const dateSpan = document.createElement('span');
    dateSpan.classList.add('comment-date');
    dateSpan.textContent = new Date(comment.created_at).toLocaleString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });

    figure.appendChild(dateSpan);

    if (comment.user === currentUser || comment.user === isSuperuser) {
        const deleteLink = document.createElement('a');
        deleteLink.href = `/vacancy/delete_comment/${comment.id}/`;
        deleteLink.classList.add('delete-link-form');
        deleteLink.textContent = '❌';
        figure.appendChild(deleteLink);
    }

    header.append(userLink, figure);

    const textParagraph = document.createElement('p');
    textParagraph.classList.add('comment-text');
    textParagraph.textContent = comment.comment;

    commentCard.append(header, textParagraph);

    return commentCard;
}