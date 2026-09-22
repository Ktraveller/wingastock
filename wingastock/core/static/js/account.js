document.addEventListener("DOMContentLoaded", function () {

    const settingsButton =
        document.getElementById("accountSettingsButton");

    const profileButton =
        document.getElementById("profileButton");

    const loginButton =
        document.getElementById("accountLoginButton");

    const menuItems =
        document.querySelectorAll(".account-menu-item");


    /* Settings */

    if (settingsButton) {

        settingsButton.addEventListener("click", function () {

            console.log("Account settings");

        });

    }


    /* Profile */

    if (profileButton) {

        profileButton.addEventListener("click", function () {

            console.log("Open profile");

        });

    }


    /* Account menu */

    menuItems.forEach(function (item) {

        item.addEventListener("click", function () {

            const action =
                item.dataset.action;

            console.log("Account action:", action);

        });

    });


    /* Sign in */

    if (loginButton) {

        loginButton.addEventListener("click", function () {

            console.log("Open login");

        });

    }


    const contactButton = document.querySelector(
        '[data-action="contact"]'
    );

    if (!contactButton) return;

    contactButton.addEventListener("click", function () {

        const message = prompt(
            "Contact Wingastock\n\n" +
            "Please enter your message:"
        );

        // User cancelled or entered nothing
        if (!message || message.trim() === "") {
            return;
        }

        const whatsappNumber = "255622652290";

        const whatsappMessage =
            "Hello Wingastock Team,\n\n" +
            message.trim();

        const whatsappURL =
            "https://wa.me/" +
            whatsappNumber +
            "?text=" +
            encodeURIComponent(whatsappMessage);

        window.open(whatsappURL, "_blank");
    });


});