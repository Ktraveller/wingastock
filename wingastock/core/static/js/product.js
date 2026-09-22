/* =========================================================
   PROFILE SORT DROPDOWN + PRODUCT SORTING
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       ELEMENTS
       ===================================================== */

    const sortButton = document.getElementById("profileSortButton");
    const sortDropdown = document.getElementById("profileSortDropdown");
    const productsGrid = document.getElementById("productsGrid");


    /* =====================================================
       PROFILE SORT DROPDOWN
       ===================================================== */

    function toggleProfileSort(event) {

        if (event) {
            event.stopPropagation();
        }

        if (!sortButton || !sortDropdown) {
            return;
        }

        const isOpen = sortDropdown.classList.toggle("show");

        sortButton.setAttribute(
            "aria-expanded",
            isOpen ? "true" : "false"
        );
    }


    /* =====================================================
       MAKE FUNCTION AVAILABLE TO INLINE HTML
       
       Your HTML uses:
       
       onclick="toggleProfileSort(event)"
       
       Therefore it must be attached to window.
       ===================================================== */

    window.toggleProfileSort = toggleProfileSort;


    /* =====================================================
       CLOSE DROPDOWN WHEN CLICKING OUTSIDE
       ===================================================== */

    document.addEventListener("click", function (event) {

        if (!sortButton || !sortDropdown) {
            return;
        }

        const wrapper = document.querySelector(
            ".profile-sort-wrapper"
        );

        if (!wrapper) {
            return;
        }

        if (!wrapper.contains(event.target)) {

            sortDropdown.classList.remove("show");

            sortButton.setAttribute(
                "aria-expanded",
                "false"
            );
        }
    });


    /* =====================================================
       PRODUCT SORTING
       ===================================================== */

    function sortProducts(type) {

        if (!productsGrid) {
            return;
        }

        /*
         * Get only product cards
         */
        const cards = Array.from(
            productsGrid.querySelectorAll(".product-card")
        );

        if (cards.length === 0) {
            return;
        }


        /* =================================================
           SORT BY NAME
           ================================================= */

        if (type === "name") {

            cards.sort(function (a, b) {

                const nameA = (
                    a.dataset.name || ""
                )
                    .trim()
                    .toLowerCase();

                const nameB = (
                    b.dataset.name || ""
                )
                    .trim()
                    .toLowerCase();

                return nameA.localeCompare(
                    nameB,
                    undefined,
                    {
                        numeric: true,
                        sensitivity: "base"
                    }
                );
            });
        }


        /* =================================================
           SORT BY DATE
           ================================================= */

        else if (type === "date") {

            cards.sort(function (a, b) {

                const dateA = parseInt(
                    a.dataset.date || "0",
                    10
                );

                const dateB = parseInt(
                    b.dataset.date || "0",
                    10
                );

                /*
                 * Newest first
                 */
                return dateB - dateA;
            });
        }


        /* =================================================
           RE-APPEND CARDS
           ================================================= */

        cards.forEach(function (card) {

            productsGrid.appendChild(card);

        });


        /* =================================================
           CLOSE DROPDOWN AFTER SORTING
           ================================================= */

        if (sortDropdown) {

            sortDropdown.classList.remove("show");

        }

        if (sortButton) {

            sortButton.setAttribute(
                "aria-expanded",
                "false"
            );
        }
    }


    /* =====================================================
       MAKE FUNCTION AVAILABLE TO INLINE HTML
       
       Your HTML uses:
       
       onclick="sortProducts('name')"
       onclick="sortProducts('date')"
       
       Therefore it must be attached to window.
       ===================================================== */

    window.sortProducts = sortProducts;


    /* =====================================================
       CLOSE DROPDOWN WITH ESCAPE KEY
       ===================================================== */

    document.addEventListener("keydown", function (event) {

        if (event.key === "Escape") {

            if (!sortDropdown) {
                return;
            }

            sortDropdown.classList.remove("show");

            if (sortButton) {

                sortButton.setAttribute(
                    "aria-expanded",
                    "false"
                );
            }
        }
    });


    /* =====================================================
       INITIAL ARIA STATE
       ===================================================== */

    if (sortButton && sortDropdown) {

        sortButton.setAttribute(
            "aria-expanded",
            "false"
        );

    }

});