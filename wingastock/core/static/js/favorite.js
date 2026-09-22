


document.addEventListener("DOMContentLoaded", function () {


    const grid =
        document.getElementById("favoritesGrid");


    const countElement =
        document.getElementById("favoritesCount");


    const filterButton =
        document.getElementById("favoritesFilterButton");


    const filters =
        document.getElementById("favoritesFilters");


    const clearButton =
        document.getElementById("clearFavoritesButton");


    const appData = document.getElementById("appData");

    const product_link = appData.dataset.productsUrl;



    /*
    =========================================================
    FILTER BUTTON
    =========================================================
    */

    if (filterButton && filters) {

        filterButton.addEventListener(
            "click",
            function () {

                filters.classList.toggle("show");

            }
        );

    }



    /*
    =========================================================
    GRID CHECK
    =========================================================
    */

    if (!grid) {
        return;
    }



    /*
    =========================================================
    SAVE ORIGINAL ORDER
    =========================================================
    */

    const originalOrder =
        Array.from(
            grid.querySelectorAll(
                ".favorite-product-card"
            )
        );



    /*
    =========================================================
    FILTER / SORT BUTTONS
    =========================================================
    */

    document
        .querySelectorAll(".favorite-filter")
        .forEach(function (button) {


            button.addEventListener(
                "click",
                function () {


                    const sortType =
                        this.dataset.sort;


                    sortProducts(sortType);



                    /*
                    Remove active
                    */

                    document
                        .querySelectorAll(
                            ".favorite-filter"
                        )
                        .forEach(function (item) {

                            item.classList.remove(
                                "active"
                            );

                        });



                    /*
                    Add active
                    */

                    this.classList.add("active");

                }
            );

        });



    /*
    =========================================================
    SORT PRODUCTS
    =========================================================
    */

    function sortProducts(type) {


        let cards =
            Array.from(
                grid.querySelectorAll(
                    ".favorite-product-card"
                )
            );


        if (!cards.length) {
            return;
        }



        /*
        DEFAULT
        */

        if (type === "default") {

            cards = [...originalOrder];

        }



        /*
        NAME A-Z
        */

        else if (type === "name") {

            cards.sort(function (a, b) {

                const nameA =
                    a.dataset.name || "";

                const nameB =
                    b.dataset.name || "";

                return nameA.localeCompare(nameB);

            });

        }



        /*
        NEWEST
        */

        else if (type === "date") {

            cards.sort(function (a, b) {

                return (
                    Number(
                        b.dataset.date || 0
                    )
                    -
                    Number(
                        a.dataset.date || 0
                    )
                );

            });

        }



        /*
        PRICE LOW
        */

        else if (type === "price-low") {

            cards.sort(function (a, b) {

                return (
                    Number(
                        a.dataset.price || 0
                    )
                    -
                    Number(
                        b.dataset.price || 0
                    )
                );

            });

        }



        /*
        PRICE HIGH
        */

        else if (type === "price-high") {

            cards.sort(function (a, b) {

                return (
                    Number(
                        b.dataset.price || 0
                    )
                    -
                    Number(
                        a.dataset.price || 0
                    )
                );

            });

        }



        /*
        MOST VIEWED
        */

        else if (type === "views") {

            cards.sort(function (a, b) {

                return (
                    Number(
                        b.dataset.views || 0
                    )
                    -
                    Number(
                        a.dataset.views || 0
                    )
                );

            });

        }



        /*
        PUT SORTED CARDS BACK
        */

        cards.forEach(function (card) {

            grid.appendChild(card);

        });

    }



    /*
    =========================================================
    UPDATE COUNT
    =========================================================
    */

    function updateCount() {


        const total =
            grid.querySelectorAll(
                ".favorite-product-card"
            ).length;


        if (countElement) {

            countElement.textContent =
                total;

        }

    }



    /*
    =========================================================
    REMOVE INDIVIDUAL FAVORITE
    =========================================================
    */

    document
        .querySelectorAll(".remove-favorite")
        .forEach(function (button) {


            button.addEventListener(
                "click",
                function (event) {


                    event.preventDefault();

                    event.stopPropagation();


                    const card =
                        this.closest(
                            ".favorite-product-card"
                        );


                    if (!card) {
                        return;
                    }



                    /*
                    Remove only from page.
                    Connect this section to your
                    existing favorite backend endpoint
                    when you want permanent deletion.
                    */

                    card.remove();


                    updateCount();


                    showEmptyState();

                }
            );

        });



    /*
    =========================================================
    CLEAR ALL
    =========================================================
    */

    if (clearButton) {


        clearButton.addEventListener(
            "click",
            function () {


                const cards =
                    grid.querySelectorAll(
                        ".favorite-product-card"
                    );


                if (!cards.length) {
                    return;
                }



                const confirmed =
                    window.confirm(
                        "Remove all favorite products from this page?"
                    );


                if (!confirmed) {
                    return;
                }



                cards.forEach(function (card) {

                    card.remove();

                });


                updateCount();


                showEmptyState();

            }
        );

    }



    /*
    =========================================================
    EMPTY STATE
    =========================================================
    */

    function showEmptyState() {


        const cards =
            grid.querySelectorAll(
                ".favorite-product-card"
            );


        if (cards.length > 0) {
            return;
        }


        let empty =
            document.getElementById(
                "favoritesEmpty"
            );


        if (empty) {

            empty.style.display = "flex";

            return;

        }



        empty =
            document.createElement("section");


        empty.id =
            "favoritesEmpty";


        empty.className =
            "favorites-empty";


        empty.innerHTML = `

            <div class="empty-icon">

                <i class="far fa-heart"></i>

            </div>


            <h2>
                No Favorite Products"
            </h2>


            <p>
                You have not added any products to your favorites yet."
            </p>


            <a
                href="${product_link}"
                class="browse-products-button"
            >

                <i class="fas fa-shopping-bag"></i>

                Browse Products

            </a>

        `;


        grid.parentNode.appendChild(empty);


        grid.classList.remove("show");

    }


});

