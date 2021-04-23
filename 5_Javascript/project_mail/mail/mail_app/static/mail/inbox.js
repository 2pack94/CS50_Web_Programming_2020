// Escape HTML Tags to prevent XSS.
// This is needed for all user supplied strings that are inserted into the DOM (as innerHTML).
// Strings that are inserted as a value of an HTML attribute should not be escaped,
// because they don't get interpreted as HTML and in this case it's not possible
// to break out of the HTML attribute to inject Javascript.
function escapeHtml(string) {
    return string
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// History API: https://developer.mozilla.org/en-US/docs/Web/API/History
// Explained in the next lecture 6_User_Interfaces
window.onpopstate = function(event) {
    if (!event.state) {return}
    let section = event.state.section;
    let id = event.state.id;
    if (section == 'compose') {
        loadComposeEmail(false);
    } else if (section == 'inbox' || section == 'sent' || section == 'archive') {
        loadMailbox(section, false);
    } else if (section == 'email') {
        loadEmail(id, false);
    }
}

// add_history: if true push an entry in the browser session history
function loadComposeEmail(add_history = true) {
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-detail-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Clear composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
    document.querySelector('#send-email-error').innerHTML = '';

    if (add_history) {
        history.pushState({section: 'compose'}, "", '/compose');
    }
}

function loadMailbox(mailbox, add_history = true) {
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#email-detail-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';

    if (add_history) {
        history.pushState({section: mailbox}, "", '/' + mailbox);
    }

    // Show the mailbox name
    document.querySelector('#mailbox-header').innerHTML =
        `${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}`;
    
    // Wait some ms before loading the emails to avoid a race condition.
    // When mark as unread or archiving an email and immediately going back to the mailbox view
    // (send a GET request to get the list of emails), the modification to the email
    // might not be fully present in the database yet and the change might not show.
    setTimeout(() => getEmails(mailbox), 50);
}

// id: id of the email (as it is stored in the backend database)
function loadEmail(id, add_history = true) {
    // Show the email content and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-detail-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    if (add_history) {
        history.pushState({section: 'email', id: id}, "", '/email/' + id);
    }

    openEmail(id);
}

// from: https://docs.djangoproject.com/en/3.1/ref/csrf/#ajax
// Function to get the CSRF token from the CSRF token cookie.
// The CSRF token must be used in the header of each POST or PUT request.
// Alternative solutions:
//  1. Disable CSRF protection in Django with the decorator @csrf_exempt
//  2. A CSRF token could be added to the inbox.html template from the index view and
//     read from the DOM with Javascript. But the CSRF token will get invalid after every request.
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function sendEmail() {
    // API Description:
    // {
    //     recipients: comma-separated string of all users to send an email to,
    //     subject: string,
    //     body: string with the E-Mail text
    // }
    document.querySelector('#send-email-error').innerHTML = '';

    fetch('/emails', {
        method: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        credentials: 'same-origin',
        body: JSON.stringify({
            recipients: document.querySelector('#compose-recipients').value,
            subject: document.querySelector('#compose-subject').value,
            body: document.querySelector('#compose-body').value
        })
    })
    // return JSON body data as well as the "ok" property from the response header
    .then(response => response.json().then(data => ({is_ok: response.ok, body: data})))
    .then(result => {
        if (!result.is_ok) {
            document.querySelector('#send-email-error').innerHTML = "Error: " + result.body.error;
            return
        }

        // redirect to sent emails view
        loadMailbox('sent');
    })
    .catch(error => {
        console.log('Error:', error);
    });

    return false
}

function getEmails(mailbox) {
    // Get a list of emails associated to a mailbox type from the backend and display them.
    fetch(`/emails/${mailbox}`)
    .then(response => response.json().then(data => ({is_ok: response.ok, body: data})))
    .then(result => {
        if (!result.is_ok) {
            console.log("Error: " + result.body.error);
            return
        }

        let emails = result.body;
        if (emails.length == 0) {
            document.querySelector('#emails-list').innerHTML = '<ul><li>No E-Mails</ul></li>';
            return
        }

        // for/in loops over keys and for/of loops over values.
        let email_list = '';
        for (email of emails) {
            let email_addr = email.sender;
            if (mailbox == 'sent') {
                email_addr = 'To: ' + email.recipients;
            }
            let bg_color_style = "";
            let extra_font_option = "";
            if (!email.read) {
                bg_color_style = "background-color: #d9d9e4;";
                extra_font_option = "font-weight-bold";
            }

            // Add a data attribute with the email id to each email container.
            // This can be used later when clicking on the E-Mail.
            email_list += `
                <div data-email-id="${email.id}" class="container p-2 border" style="${bg_color_style}">
                    <div class="row no-gutters">
                        <div class="col-3 text-truncate ${extra_font_option}">
                            ${email_addr}
                        </div>
                        <div class="col-6 text-truncate">
                            ${escapeHtml(email.subject)}
                        </div>
                        <div class="col-3 text-right timestamp">
                            ${email.timestamp}
                        </div>
                    </div>
                </div>
            `
        }
        document.querySelector('#emails-list').innerHTML = email_list;

        // add callback functions to each email container to open the email when clicked
        const email_containers = document.querySelectorAll("#emails-list .container");
        for (email_container of email_containers) {
            // https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener#the_event_listener_callback
            // The event listener callback function gets an Event object as parameter
            email_container.addEventListener('click', function(event) {
                // currentTarget: A reference to the currently registered target for the event (email_container).
                // (Another solution: The "this" keyword inside an event handler
                // is set to the DOM element on which the handler is registered.)
                // access the email id in the HTML data attribute
                loadEmail(event.currentTarget.dataset.emailId);
            })
        }
    })
    .catch(error => {
        console.log('Error:', error);
    });
}

function openEmail(id) {
    fetch(`/emails/${id}`)
    .then(response => response.json().then(data => ({is_ok: response.ok, body: data})))
    .then(result => {
        if (!result.is_ok) {
            console.log("Error: " + result.body.error);
            return
        }

        let email = result.body;
        let email_body = escapeHtml(email.body)
        // regex to replace newlines with <br>.
        // from: https://stackoverflow.com/questions/784539/how-do-i-replace-all-line-breaks-in-a-string-with-br-elements/784547#784547
        email_body = email_body.replace(/(?:\r\n|\r|\n)/g, '<br>');
        // replace whitespace characters with HTML whitespace (to allow for consecutive whitespaces).
        email_body = email_body.replace(/(?:\s)/g, '&nbsp;');
        document.querySelector('#email-detail-header').innerHTML = escapeHtml(email.subject);
        document.querySelector('#email-detail-time').innerHTML = email.timestamp;
        document.querySelector('#email-detail-from').innerHTML = email.sender;
        document.querySelector('#email-detail-to').innerHTML = email.recipients;
        document.querySelector('#email-detail-body').innerHTML = email_body;

        // add event listeners for the buttons on the page (overwrite previous event handler)
        // history.back() goes to the previous page in session history
        document.querySelector('#back-to-mailbox').onclick = () => history.back();
        document.querySelector('#mark-unread').onclick = () => {
            emailPut(id, {read: false});
            history.back();
        }

        let archive_btn = document.querySelector('#archive');
        // If the user received this email enable the archive button.
        // The archive status should be toggled.
        // Note that its possible to make the hidden button visible again by modifying the HTML in the browser.
        let user_mail = document.querySelector('#user').innerHTML;
        if (email.recipients.includes(user_mail)) {
            archive_btn.style.display = 'inline';
        } else {
            archive_btn.style.display = 'none';
        }
        if (email.archived) {
            archive_btn.innerHTML = 'Unarchive';
        } else {
            archive_btn.innerHTML = 'Archive';
        }
        archive_btn.onclick = () => {
            emailPut(id, {archived: !email.archived});
            history.back();
        }

        // Reply Button: go to the compose email view and pre-fill the fields
        // (Reply all not supported)
        document.querySelector('#reply').onclick = () => {
            loadComposeEmail();
            let reply_recipients = email.sender;
            if (email.sender == user_mail) {
                reply_recipients = email.recipients;
            }
            // Only prepend 'Re:' to the subject, if isn't already there
            let re_prefix = 'Re: ';
            let reply_subject = email.subject;
            if (reply_subject.substring(0, re_prefix.length) != re_prefix) {
                reply_subject = re_prefix + reply_subject;
            }
            let reply_body = 
                `On ${email.timestamp} ${email.sender} wrote:\n` +
                `${email.body}\n` +
                '___________________________________________________\n'

            document.querySelector('#compose-recipients').value = reply_recipients;
            document.querySelector('#compose-subject').value = reply_subject;
            document.querySelector('#compose-body').value = reply_body;
        }

        // mark as read
        if (!email.read) {
            emailPut(id, {read: true});
        }
    })
    .catch(error => {
        console.log('Error:', error);
    });
}

// send a PUT request to the backend to update properties of an existing email.
function emailPut(id, data_put) {
    fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data_put),
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        credentials: 'same-origin'
    })
    .then(result => {
        if (!result.ok) {
            console.log("Error: " + result.body.error);
            return
        }
    })
    .catch(error => {
        console.log('Error:', error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => loadMailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => loadMailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => loadMailbox('archive'));
    document.querySelector('#compose').addEventListener('click', loadComposeEmail);

    document.querySelector('#compose-form').onsubmit = sendEmail;

    // By default, load the inbox
    loadMailbox('inbox');
});
