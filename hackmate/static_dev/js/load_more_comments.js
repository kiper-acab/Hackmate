let offset = 0;
const limit = 10;
const commentsContainer = document.querySelector('.comments');
let isLoading = false;
const vacancyId = document.getElementById('vacancy-id').value;

window.onscroll = function () {
    if (commentsContainer && window.innerHeight + window.scrollY >= commentsContainer.offsetHeight && !isLoading) {
        loadMoreComments();
    }
};


function loadMoreComments() {
    isLoading = true;
    offset += limit;

    const vacancyId = document.getElementById('vacancy-id').value;
    fetch(`/api/comments/${vacancyId}/?offset=${offset}&limit=${limit}`)
        .then(response => response.json())
        .then(data => {
            data.forEach(comment => {
                const commentElement = createCommentElement(comment, comment.current_user, comment.is_admin);
                commentsContainer.appendChild(commentElement);
            });
            isLoading = false;
        })
        .catch(error => {
            console.error('Ошибка загрузки комментариев:', error);
            isLoading = false;
        });
}

function createCommentElement(comment, currentUser = '', isSuperuser = false) {
    const commentCard = document.createElement('div');
    commentCard.classList.add('comment');

    const header = document.createElement('header');
    header.classList.add('comment-header');

    const userLink = document.createElement('a');
    userLink.href = `/auth/profile/${comment.user}/`;
    userLink.classList.add('user-a');

    const userSpan = document.createElement('span');
    userSpan.classList.add('comment-user');

    const avatar = document.createElement('img');
    avatar.src = comment.user.profile_image || '/static/img/default-avatar.jpg';
    avatar.classList.add('user-image');
    avatar.alt = `${comment.user}'s avatar`;

    const usernameText = document.createTextNode(comment.user);

    userSpan.appendChild(avatar);
    userSpan.appendChild(usernameText);
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
        deleteLink.href = `/vacancies/delete_comment/${comment.id}`;
        deleteLink.classList.add('delete-link-form');
        deleteLink.textContent = '❌';
        figure.appendChild(deleteLink);
    }

    header.appendChild(userLink);
    header.appendChild(figure);

    const textParagraph = document.createElement('p');
    textParagraph.classList.add('comment-text');
    textParagraph.textContent = comment.comment;

    commentCard.appendChild(header);
    commentCard.appendChild(textParagraph);

    return commentCard;
}
