//drop down arrow
document.addEventListener('DOMContentLoaded', () => {
    const usernameDropdown = document.querySelector('.dropdown');

    usernameDropdown.addEventListener('click', () => {
        const dropdownContent = usernameDropdown.querySelector('.dropdown-content');
        dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
    });

    document.addEventListener('click', (event) => {
        if (!usernameDropdown.contains(event.target)) {
            const dropdownContent = usernameDropdown.querySelector('.dropdown-content');
            dropdownContent.style.display = 'none';
        }
    });
});

/* follower - following -section */

var tablinks = document.getElementsByClassName("following-links");
var tabcontents = document.getElementsByClassName("following-contents");

function opentab(tabname, event) {
    for (tablink of tablinks) {
        tablink.classList.remove("active-link");
    }
    for (tabcontent of tabcontents) {
        tabcontent.classList.remove("active-tab");
    }
    event.currentTarget.classList.add("active-link");
    document.getElementById(tabname).classList.add('active-tab');
}



/* comments */

function toggleComments(postId) {
    var commentSection = document.getElementById('comment-section-' + postId);
    if (commentSection.style.display === 'none' || commentSection.style.display === '') {
        commentSection.style.display = 'block';
    } else {
        commentSection.style.display = 'none';
    }
}

function addComment(postId) {
    var commentInput = document.getElementById('comment-input-' + postId);
    var commentsContainer = document.getElementById('comments-container-' + postId);

    var newComment = commentInput.value.trim();

    if (newComment !== '') {
        var commentDiv = document.createElement('div');
        commentDiv.className = 'comment';

        var userInfoDiv = document.createElement('div');
        userInfoDiv.className = 'user-info';

        var userImg = document.createElement('img');
        userImg.src = '{{ user.profile.profile_img.url }}'; // Set the actual path to the user's DP
        userImg.alt = 'User DP';

        var usernameSpan = document.createElement('span');
        usernameSpan.className = 'username';
        usernameSpan.innerText = '{{ user.username }}'; // Set the actual username dynamically

        userInfoDiv.appendChild(userImg);
        userInfoDiv.appendChild(usernameSpan);

        commentDiv.appendChild(userInfoDiv);

        var commentText = document.createElement('p');
        commentText.className = 'comment-text';
        commentText.innerText = newComment;

        commentDiv.appendChild(commentText);

        commentsContainer.appendChild(commentDiv);
        commentInput.value = '';
    }
}