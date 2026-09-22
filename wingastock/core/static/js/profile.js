document.addEventListener("DOMContentLoaded", function () {

    const editButton = document.getElementById("profileEditButton");

    const saveButton = document.getElementById("saveProfileButton");

    const formCard = document.querySelector(".profile-form-card");

    const fullNameInput = document.getElementById("fullName");
    const emailInput = document.getElementById("email");
    const phoneInput = document.getElementById("phone");
    const locationInput = document.getElementById("location");

    const profileName = document.getElementById("profileName");
    const profileEmail = document.getElementById("profileEmail");


    let editing = false;


    /* =====================================================
       EDIT PROFILE
    ====================================================== */

    if (editButton) {

        editButton.addEventListener("click", function () {

            editing = !editing;


            if (editing) {

                fullNameInput.disabled = false;
                emailInput.disabled = false;
                phoneInput.disabled = false;
                locationInput.disabled = false;

                formCard.classList.add("editing");

                editButton.innerHTML =
                    '<i class="fas fa-times"></i>';

                editButton.setAttribute(
                    "aria-label",
                    "Cancel editing"
                );

                fullNameInput.focus();

            } else {

                fullNameInput.disabled = true;
                emailInput.disabled = true;
                phoneInput.disabled = true;
                locationInput.disabled = true;

                formCard.classList.remove("editing");

                editButton.innerHTML =
                    '<i class="fas fa-edit"></i>';

                editButton.setAttribute(
                    "aria-label",
                    "Edit profile"
                );

            }

        });

    }


    /* =====================================================
       SAVE PROFILE
    ====================================================== */

    if (saveButton) {

        saveButton.addEventListener("click", function () {

            const name =
                fullNameInput.value.trim();

            const email =
                emailInput.value.trim();


            if (name !== "") {

                profileName.textContent = name;

            }


            if (email !== "") {

                profileEmail.textContent = email;

            }


            fullNameInput.disabled = true;
            emailInput.disabled = true;
            phoneInput.disabled = true;
            locationInput.disabled = true;

            formCard.classList.remove("editing");

            editing = false;


            editButton.innerHTML =
                '<i class="fas fa-edit"></i>';

            editButton.setAttribute(
                "aria-label",
                "Edit profile"
            );


            saveButton.innerHTML =
                '<i class="fas fa-check"></i> Saved';


            setTimeout(function () {

                saveButton.innerHTML =
                    '<i class="fas fa-save"></i> Save changes';

            }, 1800);

        });

    }


    /* =====================================================
       CHANGE PASSWORD
    ====================================================== */

    const changePasswordButton =
        document.getElementById("changePasswordButton");


    if (changePasswordButton) {

        changePasswordButton.addEventListener(
            "click",
            function () {

                alert(
                    "Change password will be available after account login is connected."
                );

            }
        );

    }


    /* =====================================================
       SECURITY
    ====================================================== */

    const securityButton =
        document.getElementById("securityButton");


    if (securityButton) {

        securityButton.addEventListener(
            "click",
            function () {

                alert(
                    "Security settings will be available after account login is connected."
                );

            }
        );

    }

});