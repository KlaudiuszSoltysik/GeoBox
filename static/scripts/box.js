var userComments = document.getElementsByClassName('bin-icon');
var comments = document.getElementsByClassName('comment');
const csrftoken = getCookie('csrftoken');
var commentsCount = 5;
const loadComments = document.getElementById('load-comments');

loadComments.addEventListener('click', () => {
    commentsCount += 5;
    hideComments();
    hideBtn();
});

document.addEventListener('DOMContentLoaded', () => {
    hideComments();
    hideBtn()
});

function hideComments() {
    for (var com of comments) {
        com.style.display = 'flex';
    }

    for (var i = commentsCount; i < comments.length; i++) {
        comments[i].style.display = 'none';
    }
}

function hideBtn () {
    if (commentsCount >= comments.length) {
        loadComments.style.display = 'none'
    }
}


function deleteComment(id, self) {
    Confirm.open({
        title: 'Confirm',
        message: 'Are you sure you want to delete your comment?',
        onok: () => {
            fetch(`/delete-comment/${id}`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrftoken,
                }
            }).then(response => response.json())
            .then(data => {
                if (JSON.parse(data['success'])) {
                    self.parentNode.parentNode.remove();
                    comments = document.getElementsByClassName('comment');
                    hideComments();
                    hideBtn();
                }
            });
        }
      }); 
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const Confirm = {
    open (options) {
        options = Object.assign({}, {
            title: '',
            message: '',
            okText: 'OK',
            cancelText: 'Cancel',
            onok: () => {},
            oncancel: () => {}
        }, options);
        
        const html = `
            <div class='confirm'>
                <div class='confirm-window'>
                    <div class='confirm-titlebar'>
                        <span class='confirm-title'>${options.title}</span>
                        <button class='confirm-close'>&times;</button>
                    </div>
                    <div class='confirm-content'>${options.message}</div>
                    <div class='confirm-buttons'>
                        <button class='confirm-button confirm-button-ok confirm-button-fill'>${options.okText}</button>
                        <button class='confirm-button confirm-button-cancel'>${options.cancelText}</button>
                    </div>
                </div>
            </div>
        `;

        const template = document.createElement('template');
        template.innerHTML = html;

        const confirmEl = template.content.querySelector('.confirm');
        const btnClose = template.content.querySelector('.confirm-close');
        const btnOk = template.content.querySelector('.confirm-button-ok');
        const btnCancel = template.content.querySelector('.confirm-button-cancel');

        confirmEl.addEventListener('click', e => {
            if (e.target === confirmEl) {
                options.oncancel();
                this._close(confirmEl);
            }
        });

        btnOk.addEventListener('click', () => {
            options.onok();
            this._close(confirmEl);
        });

        [btnCancel, btnClose].forEach(el => {
            el.addEventListener('click', () => {
                options.oncancel();
                this._close(confirmEl);
            });
        });

        document.body.appendChild(template.content);
    },

    _close (confirmEl) {
        confirmEl.classList.add('confirm-close');

        confirmEl.addEventListener('animationend', () => {
            document.body.removeChild(confirmEl);
        });
    }
};
