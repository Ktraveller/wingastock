document.addEventListener("DOMContentLoaded", function () {

    const filterButton =
        document.getElementById("ordersFilterButton");

    const filters =
        document.getElementById("ordersFilters");

    const filterButtons =
        document.querySelectorAll(".order-filter");

    const orderCards =
        document.querySelectorAll(".order-card");

    const ordersList =
        document.getElementById("ordersList");

    const emptyState =
        document.getElementById("ordersEmpty");

    const totalOrders =
        document.getElementById("totalOrders");

    const activeOrders =
        document.getElementById("activeOrders");

    const completedOrders =
        document.getElementById("completedOrders");

    const browseProductsButton =
        document.getElementById("browseProductsButton");


    /* =====================================================
       FILTER BUTTON
    ====================================================== */

    if (filterButton && filters) {

        filterButton.addEventListener("click", function () {

            filters.classList.toggle("show");

        });

    }


    /* =====================================================
       UPDATE SUMMARY
    ====================================================== */

    function updateSummary() {

        const total =
            orderCards.length;

        let active = 0;

        let completed = 0;


        orderCards.forEach(function (card) {

            const status =
                card.dataset.status;


            if (
                status === "pending" ||
                status === "processing"
            ) {

                active++;

            }


            if (status === "completed") {

                completed++;

            }

        });


        if (totalOrders) {
            totalOrders.textContent = total;
        }


        if (activeOrders) {
            activeOrders.textContent = active;
        }


        if (completedOrders) {
            completedOrders.textContent = completed;
        }

    }


    /* =====================================================
       UPDATE EMPTY STATE
    ====================================================== */

    function updateEmptyState() {

        const visibleOrders =
            document.querySelectorAll(
                ".order-card:not([hidden])"
            );


        if (visibleOrders.length === 0) {

            if (emptyState) {
                emptyState.classList.add("show");
            }


            if (ordersList) {
                ordersList.style.display = "none";
            }

        } else {

            if (emptyState) {
                emptyState.classList.remove("show");
            }


            if (ordersList) {
                ordersList.style.display = "";
            }

        }

    }


    /* =====================================================
       FILTER ORDERS
    ====================================================== */

    filterButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const selectedFilter =
                button.dataset.filter;


            filterButtons.forEach(function (item) {

                item.classList.remove("active");

            });


            button.classList.add("active");


            orderCards.forEach(function (card) {

                const status =
                    card.dataset.status;


                if (
                    selectedFilter === "all" ||
                    selectedFilter === status
                ) {

                    card.hidden = false;

                } else {

                    card.hidden = true;

                }

            });


            updateEmptyState();

        });

    });


    /* =====================================================
       BROWSE PRODUCTS
    ====================================================== */

    if (browseProductsButton) {

        browseProductsButton.addEventListener(
            "click",
            function () {

                window.location.href =
                    "index.html";

            }
        );

    }


    /* =====================================================
       VIEW ORDER
    ====================================================== */

    document
        .querySelectorAll(".order-view-button")
        .forEach(function (button) {

            button.addEventListener(
                "click",
                function () {

                    const card =
                        button.closest(".order-card");

                    if (!card) {
                        return;
                    }


                    const orderNumber =
                        card.querySelector(
                            ".order-number"
                        );


                    if (orderNumber) {

                        alert(
                            "Opening " +
                            orderNumber.textContent +
                            "..."
                        );

                    }

                }
            );

        });


    /* =====================================================
       INITIAL STATE
    ====================================================== */

    updateSummary();

    updateEmptyState();

});