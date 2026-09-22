/* =========================================================
   MOBILE SIDEBAR
   ========================================================= */

function toggleMobileSidebar() {

    const sidebar = document.getElementById("left-holder-101");
    const overlay = document.getElementById("mobile-sidebar-overlay");

    if (!sidebar) {
        console.error("Sidebar #left-holder-101 not found");
        return;
    }

    /* Desktop */
    if (window.innerWidth > 767) {
        return;
    }

    const isOpen = sidebar.classList.contains("mobile-open");

    if (isOpen) {

        /* =========================
           CLOSE SIDEBAR
           ========================= */

        sidebar.classList.remove("mobile-open");

        sidebar.style.setProperty(
            "transform",
            "translateX(-105%)",
            "important"
        );

        sidebar.style.setProperty(
            "visibility",
            "hidden",
            "important"
        );

        sidebar.style.setProperty(
            "opacity",
            "0",
            "important"
        );


        if (overlay) {

            overlay.classList.remove("active");

            overlay.style.setProperty(
                "opacity",
                "0",
                "important"
            );

            overlay.style.setProperty(
                "visibility",
                "hidden",
                "important"
            );

            overlay.style.setProperty(
                "pointer-events",
                "none",
                "important"
            );
        }


        document.body.classList.remove(
            "mobile-menu-open"
        );


    } else {

        /* =========================
           OPEN SIDEBAR
           ========================= */

        sidebar.classList.add("mobile-open");

        sidebar.style.setProperty(
            "display",
            "block",
            "important"
        );

        sidebar.style.setProperty(
            "transform",
            "translateX(0)",
            "important"
        );

        sidebar.style.setProperty(
            "visibility",
            "visible",
            "important"
        );

        sidebar.style.setProperty(
            "opacity",
            "1",
            "important"
        );


        if (overlay) {

            overlay.classList.add("active");

            overlay.style.setProperty(
                "opacity",
                "1",
                "important"
            );

            overlay.style.setProperty(
                "visibility",
                "visible",
                "important"
            );

            overlay.style.setProperty(
                "pointer-events",
                "auto",
                "important"
            );
        }


        document.body.classList.add(
            "mobile-menu-open"
        );
    }
}


/* =========================================================
   CLOSE SIDEBAR AFTER CLICKING A MENU LINK
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const sidebar =
            document.getElementById("left-holder-101");

        if (!sidebar) {
            return;
        }

        const links =
            sidebar.querySelectorAll("a");

        links.forEach(function (link) {

            link.addEventListener(
                "click",
                function () {

                    if (window.innerWidth <= 767) {

                        closeMobileSidebar();

                    }

                }
            );

        });

    }
);


/* =========================================================
   CLOSE FUNCTION
   ========================================================= */

function closeMobileSidebar() {

    const sidebar =
        document.getElementById("left-holder-101");

    const overlay =
        document.getElementById("mobile-sidebar-overlay");


    if (sidebar) {

        sidebar.classList.remove(
            "mobile-open"
        );

        sidebar.style.setProperty(
            "transform",
            "translateX(-105%)",
            "important"
        );

        sidebar.style.setProperty(
            "visibility",
            "hidden",
            "important"
        );

        sidebar.style.setProperty(
            "opacity",
            "0",
            "important"
        );
    }


    if (overlay) {

        overlay.classList.remove(
            "active"
        );

        overlay.style.setProperty(
            "opacity",
            "0",
            "important"
        );

        overlay.style.setProperty(
            "visibility",
            "hidden",
            "important"
        );

        overlay.style.setProperty(
            "pointer-events",
            "none",
            "important"
        );
    }


    document.body.classList.remove(
        "mobile-menu-open"
    );
}


/* =========================================================
   RESET WHEN RESIZING TO DESKTOP
   ========================================================= */

window.addEventListener(
    "resize",
    function () {

        if (window.innerWidth > 767) {

            const sidebar =
                document.getElementById(
                    "left-holder-101"
                );

            const overlay =
                document.getElementById(
                    "mobile-sidebar-overlay"
                );


            if (sidebar) {

                sidebar.classList.remove(
                    "mobile-open"
                );

                sidebar.style.removeProperty(
                    "transform"
                );

                sidebar.style.removeProperty(
                    "visibility"
                );

                sidebar.style.removeProperty(
                    "opacity"
                );

                sidebar.style.removeProperty(
                    "display"
                );
            }


            if (overlay) {

                overlay.classList.remove(
                    "active"
                );

                overlay.style.removeProperty(
                    "opacity"
                );

                overlay.style.removeProperty(
                    "visibility"
                );

                overlay.style.removeProperty(
                    "pointer-events"
                );
            }


            document.body.classList.remove(
                "mobile-menu-open"
            );
        }

    }
);