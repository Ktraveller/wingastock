
/* =================================================
   FAVORITE BUTTON
================================================= */

function toggleFavorite(button) {

    const icon = button.querySelector("i");

    if (!icon) {
        return;
    }


    if (icon.classList.contains("far")) {

        icon.classList.remove("far");
        icon.classList.add("fas");

        button.classList.add("is-favorite");

    } else {

        icon.classList.remove("fas");
        icon.classList.add("far");

        button.classList.remove("is-favorite");

    }

}



/* =================================================
   ACCOUNT MODAL
================================================= */

function openAccountModal() {

    const modal =
        document.getElementById("accountModal");

    if (!modal) {
        return;
    }


    modal.classList.add("active");

    modal.setAttribute(
        "aria-hidden",
        "false"
    );


    document.body.classList.add("modal-open");

}



function closeAccountModal() {

    const modal =
        document.getElementById("accountModal");

    if (!modal) {
        return;
    }


    modal.classList.remove("active");

    modal.setAttribute(
        "aria-hidden",
        "true"
    );


    document.body.classList.remove("modal-open");

}



/* =================================================
   ESC KEY
================================================= */

document.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Escape") {

            closeAccountModal();

        }

    }
);



/* =================================================
   IMAGE ERROR FALLBACK
================================================= */

document.addEventListener(
    "error",
    function (event) {

        if (
            event.target &&
            event.target.tagName === "IMG"
        ) {

            event.target.style.display = "none";


            const parent =
                event.target.parentElement;


            if (
                parent &&
                !parent.querySelector(
                    ".product-image-placeholder"
                )
            ) {

                const placeholder =
                    document.createElement("div");


                placeholder.className =
                    "product-image-placeholder";


                placeholder.innerHTML =
                    '<i class="fas fa-image"></i>';


                parent.appendChild(
                    placeholder
                );

            }

        }

    },
    true
);





function toggleLanguageMenu(event) {

    event.stopPropagation();

    const dropdown =
        document.getElementById("languageDropdown");

    if (!dropdown) return;

    dropdown.classList.toggle("show");
}


/* Close when clicking outside */

document.addEventListener("click", function (event) {

    const switcher =
        document.querySelector(".language-switcher");

    const dropdown =
        document.getElementById("languageDropdown");

    if (!switcher || !dropdown) return;

    if (!switcher.contains(event.target)) {

        dropdown.classList.remove("show");

    }

});


/* Close with Escape */

document.addEventListener("keydown", function (event) {

    if (event.key === "Escape") {

        const dropdown =
            document.getElementById("languageDropdown");

        if (dropdown) {
            dropdown.classList.remove("show");
        }

    }

});

