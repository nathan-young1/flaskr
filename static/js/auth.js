function authHandler(endpoint) {
    form = document.getElementById("authForm")
    username = form.username.value
    password = form.password.value

    // Do not login if the fields are empty
    if (username === "" || password === "") return false

    var xhr = new XMLHttpRequest();
    xhr.open("POST", endpoint, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(
        {
            username: username,
            password: password
        }
    ))

    // When a response is received from the server.
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            response = JSON.parse(xhr.response)

            // If authentication was successful go to dashboard page
            if (response.auth_result) {
                // Show alert dialog if reset password.
                if (endpoint == "/forgotPassword")
                    alert("Password has been changed successfully.")

                window.location.href = '/dashboard'

            } else {
                // When authentication fails
                validation_text = document.getElementById("validation_text")
                validation_text.classList.remove("d-none")
                validation_text_is_showing = true

                // Initialize form fields onfocus only once
                if (form.username.onfocus === null || form.password.onfocus === null) {
                    hide_validation_text = () => {
                        if (validation_text_is_showing) {
                            validation_text.classList.add("d-none")
                        }
                    }
                    form.username.onfocus = hide_validation_text
                    form.password.onfocus = hide_validation_text
                }
            }
        }
    }
}