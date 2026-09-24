/* =========================================================
   PRODUCT DATA FROM DJANGO
========================================================= */

const productData =
    document.getElementById("productData");


/* =========================================================
   NORMALIZE IMAGE URL
   Converts HTTP image URLs to HTTPS
========================================================= */

function normalizeImageUrl(url) {

    if (!url) {
        return "";
    }

    return url.replace(
        /^http:\/\//i,
        "https://"
    );
}


/* =========================================================
   GET PRODUCT DATA
========================================================= */

function getProductData() {

    if (!productData) {
        console.error("Product data element not found.");
        return null;
    }

    return {

        reactUrl:
            productData.dataset.reactUrl || "",

        title:
            productData.dataset.title || "",

        description:
            productData.dataset.description || "",

        price:
            productData.dataset.price || "",

        seller:
            productData.dataset.seller || "",

        phone:
            productData.dataset.phone || "",

        location:
            productData.dataset.location || "",

        uploaded:
            productData.dataset.uploaded || "",

        image:
            normalizeImageUrl(
                productData.dataset.image || ""
            ),

        url:
            productData.dataset.url ||
            window.location.href
    };
}


/* =========================================================
   GET CSRF TOKEN
========================================================= */

function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {

        const cookies =
            document.cookie.split(";");

        for (let i = 0; i < cookies.length; i++) {

            const cookie =
                cookies[i].trim();

            if (
                cookie.substring(
                    0,
                    name.length + 1
                ) === name + "="
            ) {

                cookieValue =
                    decodeURIComponent(
                        cookie.substring(
                            name.length + 1
                        )
                    );

                break;
            }
        }
    }

    return cookieValue;
}


/* =========================================================
   DOM READY
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {


        /* =====================================================
           GET ELEMENTS
        ===================================================== */

        const mainImage =
            document.getElementById(
                "mainProductImage"
            );

        const thumbnails =
            document.querySelectorAll(
                ".product-thumbnail"
            );

        const favoriteButton =
            document.getElementById(
                "favoriteButton"
            );

        const shareButton =
            document.getElementById(
                "shareButton"
            );

        const likeButton =
            document.getElementById(
                "like-btn"
            );

        const dislikeButton =
            document.getElementById(
                "dislike-btn"
            );


        /* =====================================================
           PRODUCT THUMBNAILS
        ===================================================== */

        thumbnails.forEach(
            function (thumbnail) {

                thumbnail.addEventListener(
                    "click",
                    function () {

                        if (!mainImage) {
                            return;
                        }

                        const imageUrl =
                            normalizeImageUrl(
                                this.dataset.image || ""
                            );

                        if (!imageUrl) {
                            return;
                        }

                        mainImage.src =
                            imageUrl;


                        /* Remove active class
                           from all thumbnails */

                        thumbnails.forEach(
                            function (item) {

                                item.classList.remove(
                                    "active"
                                );

                            }
                        );


                        /* Add active class
                           to selected thumbnail */

                        this.classList.add(
                            "active"
                        );
                    }
                );
            }
        );


        /* =====================================================
           FAVORITE BUTTON
           Client-side favorite toggle
        ===================================================== */

        if (favoriteButton) {

            favoriteButton.addEventListener(
                "click",
                function () {

                    const icon =
                        favoriteButton.querySelector(
                            "i"
                        );

                    if (!icon) {
                        return;
                    }


                    /* Currently not favorite */

                    if (
                        icon.classList.contains(
                            "far"
                        )
                    ) {

                        icon.classList.remove(
                            "far"
                        );

                        icon.classList.add(
                            "fas"
                        );

                        favoriteButton.classList.add(
                            "active"
                        );

                    }

                    /* Currently favorite */

                    else {

                        icon.classList.remove(
                            "fas"
                        );

                        icon.classList.add(
                            "far"
                        );

                        favoriteButton.classList.remove(
                            "active"
                        );
                    }
                }
            );
        }


        /* =====================================================
           REACTION FUNCTION
        ===================================================== */

        async function reactToProduct(
            reaction
        ) {

            const data =
                getProductData();

            if (!data) {
                return;
            }

            if (!data.reactUrl) {

                console.error(
                    "Reaction URL is missing."
                );

                return;
            }


            try {

                const csrfToken =
                    getCookie("csrftoken");


                const response =
                    await fetch(
                        data.reactUrl,
                        {
                            method: "POST",

                            headers: {

                                "Content-Type":
                                    "application/x-www-form-urlencoded",

                                "X-CSRFToken":
                                    csrfToken || "",

                                "X-Requested-With":
                                    "XMLHttpRequest"
                            },

                            body:
                                "reaction=" +
                                encodeURIComponent(
                                    reaction
                                )
                        }
                    );


                if (!response.ok) {

                    throw new Error(
                        "Reaction request failed: HTTP " +
                        response.status
                    );
                }


                const result =
                    await response.json();


                /* =============================================
                   UPDATE LIKE COUNT
                ============================================= */

                const likeCount =
                    document.getElementById(
                        "like-count"
                    );

                if (
                    likeCount &&
                    result.likes !== undefined
                ) {

                    likeCount.textContent =
                        result.likes;
                }


                /* =============================================
                   UPDATE DISLIKE COUNT
                ============================================= */

                const dislikeCount =
                    document.getElementById(
                        "dislike-count"
                    );

                if (
                    dislikeCount &&
                    result.dislikes !== undefined
                ) {

                    dislikeCount.textContent =
                        result.dislikes;
                }


                /* =============================================
                   UPDATE BUTTON STATES
                ============================================= */

                if (likeButton) {

                    if (
                        reaction === "like"
                    ) {

                        likeButton.classList.add(
                            "active"
                        );

                    }

                    else {

                        likeButton.classList.remove(
                            "active"
                        );
                    }
                }


                if (dislikeButton) {

                    if (
                        reaction === "dislike"
                    ) {

                        dislikeButton.classList.add(
                            "active"
                        );

                    }

                    else {

                        dislikeButton.classList.remove(
                            "active"
                        );
                    }
                }

            }

            catch (error) {

                console.error(
                    "Reaction failed:",
                    error
                );
            }
        }


        /* =====================================================
           LIKE BUTTON
        ===================================================== */

        if (likeButton) {

            likeButton.addEventListener(
                "click",
                function () {

                    reactToProduct(
                        "like"
                    );

                }
            );
        }


        /* =====================================================
           DISLIKE BUTTON
        ===================================================== */

        if (dislikeButton) {

            dislikeButton.addEventListener(
                "click",
                function () {

                    reactToProduct(
                        "dislike"
                    );

                }
            );
        }


        /* =====================================================
           SHARE PRODUCT
        ===================================================== */

        if (shareButton) {

            shareButton.addEventListener(
                "click",
                async function () {

                    const data =
                        getProductData();


                    if (!data) {

                        console.error(
                            "Product data is missing."
                        );

                        return;
                    }


                    const productUrl =
                        data.url ||
                        window.location.href;


                    /* =========================================
                       SHARE TEXT
                    ========================================= */

                    const shareText =
                        `${data.title}\n\n` +

                        `Price: ${data.price}\n\n` +

                        `Description:\n` +
                        `${data.description}\n\n` +

                        `Seller: ${data.seller}\n` +

                        `Phone: ${data.phone}\n` +

                        `Location: ${data.location}\n` +

                        `Uploaded: ${data.uploaded}\n\n` +

                        `View product:\n` +
                        `${productUrl}`;


                    /* =========================================
                       TRY TO SHARE ACTUAL PRODUCT IMAGE
                    ========================================= */

                    try {

                        if (data.image) {

                            const imageUrl =
                                normalizeImageUrl(
                                    data.image
                                );


                            console.log(
                                "Product image URL:",
                                imageUrl
                            );


                            const response =
                                await fetch(
                                    imageUrl,
                                    {
                                        method: "GET"
                                    }
                                );


                            if (!response.ok) {

                                throw new Error(
                                    "Image request failed: HTTP " +
                                    response.status
                                );
                            }


                            const blob =
                                await response.blob();


                            const file =
                                new File(
                                    [
                                        blob
                                    ],

                                    "wingastock-product.jpg",

                                    {
                                        type:
                                            blob.type ||
                                            "image/jpeg"
                                    }
                                );


                            /* =====================================
                               CHECK FILE SHARING SUPPORT
                            ===================================== */

                            if (
                                navigator.share &&
                                navigator.canShare &&
                                navigator.canShare(
                                    {
                                        files: [
                                            file
                                        ]
                                    }
                                )
                            ) {

                                await navigator.share(
                                    {
                                        title:
                                            data.title,

                                        text:
                                            shareText,

                                        files: [
                                            file
                                        ]
                                    }
                                );

                                return;
                            }
                        }


                        /* =========================================
                           NORMAL WEB SHARE FALLBACK
                        ========================================= */

                        if (
                            navigator.share
                        ) {

                            await navigator.share(
                                {
                                    title:
                                        data.title,

                                    text:
                                        shareText,

                                    url:
                                        productUrl
                                }
                            );

                            return;
                        }


                        /* =========================================
                           CLIPBOARD FALLBACK
                        ========================================= */

                        if (
                            navigator.clipboard &&
                            navigator.clipboard.writeText
                        ) {

                            await navigator.clipboard.writeText(
                                shareText
                            );


                            alert(
                                "Product information copied."
                            );

                            return;
                        }


                        alert(
                            "Sharing is not supported on this browser."
                        );

                    }

                    catch (error) {


                        /* =====================================
                           USER CANCELLED SHARE
                        ===================================== */

                        if (
                            error &&
                            error.name ===
                                "AbortError"
                        ) {

                            console.log(
                                "Share cancelled."
                            );

                            return;
                        }


                        console.error(
                            "Share failed:",
                            error
                        );


                        /* =====================================
                           NORMAL SHARE FALLBACK
                        ===================================== */

                        try {

                            if (
                                navigator.share
                            ) {

                                await navigator.share(
                                    {
                                        title:
                                            data.title,

                                        text:
                                            shareText,

                                        url:
                                            productUrl
                                    }
                                );

                                return;
                            }

                        }

                        catch (fallbackError) {

                            if (
                                fallbackError &&
                                fallbackError.name ===
                                    "AbortError"
                            ) {

                                return;
                            }


                            console.error(
                                "Normal share failed:",
                                fallbackError
                            );
                        }


                        /* =====================================
                           CLIPBOARD FALLBACK
                        ===================================== */

                        try {

                            if (
                                navigator.clipboard &&
                                navigator.clipboard.writeText
                            ) {

                                await navigator.clipboard.writeText(
                                    shareText
                                );


                                alert(
                                    "Product information copied."
                                );
                            }

                        }

                        catch (clipboardError) {

                            console.error(
                                "Clipboard fallback failed:",
                                clipboardError
                            );

                        }
                    }
                }
            );
        }


        /* =====================================================
           WHATSAPP SHARE
        ===================================================== */

        const whatsappButton =
            document.getElementById(
                "whatsappButton"
            );


        if (whatsappButton) {

            whatsappButton.addEventListener(
                "click",
                function () {

                    const data =
                        getProductData();


                    if (!data) {
                        return;
                    }


                    let phone =
                        data.phone || "";


                    /* =========================================
                       CLEAN TANZANIA PHONE NUMBER
                    ========================================= */

                    phone =
                        phone.replace(
                            /\D/g,
                            ""
                        );


                    if (
                        phone.startsWith(
                            "0"
                        )
                    ) {

                        phone =
                            "255" +
                            phone.substring(
                                1
                            );
                    }


                    if (
                        phone.startsWith(
                            "+"
                        )
                    ) {

                        phone =
                            phone.substring(
                                1
                            );
                    }


                    /* =========================================
                       WHATSAPP MESSAGE
                    ========================================= */

                    const message =
                        `${data.title}\n\n` +

                        `Price: ${data.price}\n\n` +

                        `Description:\n` +
                        `${data.description}\n\n` +

                        `Seller: ${data.seller}\n` +

                        `Phone: ${data.phone}\n` +

                        `Location: ${data.location}\n` +

                        `Uploaded: ${data.uploaded}\n\n` +

                        `View product:\n` +
                        `${data.url || window.location.href}`;


                    const whatsappUrl =
                        "https://wa.me/" +
                        phone +
                        "?text=" +
                        encodeURIComponent(
                            message
                        );


                    window.open(
                        whatsappUrl,
                        "_blank"
                    );
                }
            );
        }

    }
);