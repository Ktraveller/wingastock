document.addEventListener("DOMContentLoaded", function () {

    const filterButton =
        document.getElementById("deliveryFilterButton");

    const filters =
        document.getElementById("deliveryFilters");

    const filterItems =
        document.querySelectorAll(".delivery-filter");

    const cards =
        document.querySelectorAll(".delivery-card");

    const list =
        document.getElementById("deliveryList");

    const emptyState =
        document.getElementById("deliveryEmpty");

    const totalRequests =
        document.getElementById("totalRequests");

    const activeRequests =
        document.getElementById("activeRequests");

    const processedRequests =
        document.getElementById("processedRequests");

    const createButton =
        document.getElementById("createDeliveryButton");


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

        let active = 0;
        let processed = 0;

        cards.forEach(function (card) {

            const status =
                card.dataset.status;

            if (
                status === "pending" ||
                status === "processing"
            ) {
                active++;
            }


            if (status === "processed") {
                processed++;
            }

        });


        totalRequests.textContent = cards.length;

        activeRequests.textContent = active;

        processedRequests.textContent = processed;

    }


    /* =====================================================
       UPDATE EMPTY STATE
    ====================================================== */

    function updateEmptyState() {

        const visibleCards =
            document.querySelectorAll(
                ".delivery-card:not([hidden])"
            );


        if (visibleCards.length === 0) {

            emptyState.style.display = "flex";

            list.style.display = "none";

        } else {

            emptyState.style.display = "none";

            list.style.display = "";

        }

    }


    /* =====================================================
       FILTER REQUESTS
    ====================================================== */

    filterItems.forEach(function (button) {

        button.addEventListener("click", function () {

            const selectedFilter =
                button.dataset.filter;


            filterItems.forEach(function (item) {

                item.classList.remove("active");

            });


            button.classList.add("active");


            cards.forEach(function (card) {

                const status =
                    card.dataset.status;


                if (
                    selectedFilter === "all" ||
                    status === selectedFilter
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
       VIEW REQUEST
    ====================================================== */

    document
        .querySelectorAll(".delivery-view-button")
        .forEach(function (button) {

            button.addEventListener(
                "click",
                function () {

                    const card =
                        button.closest(".delivery-card");

                    if (!card) {
                        return;
                    }


                    const requestNumber =
                        card.querySelector(
                            ".delivery-request-number strong"
                        );


                    if (requestNumber) {

                        alert(
                            "Opening " +
                            requestNumber.textContent +
                            "..."
                        );

                    }

                }
            );

        });


    /* =====================================================
       CREATE REQUEST
    ====================================================== */

    if (createButton) {

        createButton.addEventListener(
            "click",
            function () {

                alert(
                    "Create Delivery Request"
                );

            }
        );

    }


    /* =====================================================
       INITIAL STATE
    ====================================================== */

    updateSummary();

    updateEmptyState();

});