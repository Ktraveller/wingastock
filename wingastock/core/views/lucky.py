from django.shortcuts import render
import random
from django.utils import timezone


def lucky(request):

    # Make user access lucky only one in day
    today = str(timezone.now().date())

    message = ""

    if request.method == "POST":

        # Verify day
        if request.COOKIES.get("last_lucky_date") == today:
            return render(
                request,
                "lucky/home_l.html",
                {
                    "message": "Umeshajaribu leo. Rudi kesho."
                }
            )


        selected_gift = request.POST.get("lucky")

        # Gift array
        gifts = ["vocha", "book", "pen", "points"]

        # Random select gift
        selected_gift_random = random.choice(gifts)


        # Comparing selected gift and random list
        if selected_gift == selected_gift_random:


            if selected_gift == "vocha":

                vocha_win_chance = int(
                    request.COOKIES.get("vocha_win_chance", 0)
                )

                win = vocha_win_chance + 1

                if win == 10:
                    message = "Umejishindia vocha ya Tsh 1000 mtandao wowote!"
                    vocha_win_chance = 0
                else:
                    message = (
                        "Hongera! umeongeza nafasi ya kushinda "
                        + selected_gift
                    )
                    vocha_win_chance = win



            elif selected_gift == "book":

                book_win_chance = int(
                    request.COOKIES.get("book_win_chance", 0)
                )

                win = book_win_chance + 1

                if win == 10:
                    message = "Umejishindia daftari jipya!"
                    book_win_chance = 0
                else:
                    message = (
                        "Hongera! umeongeza nafasi ya kushinda "
                        + selected_gift
                    )
                    book_win_chance = win



            elif selected_gift == "pen":

                pen_win_chance = int(
                    request.COOKIES.get("pen_win_chance", 0)
                )

                win = pen_win_chance + 1

                if win == 10:
                    message = "Umejishindia peni 3!"
                    pen_win_chance = 0
                else:
                    message = (
                        "Hongera! umeongeza nafasi ya kushinda "
                        + selected_gift
                    )
                    pen_win_chance = win



            elif selected_gift == "points":

                points = int(
                    request.COOKIES.get("points", 0)
                )

                win = points + 1

                if win == 10:

                    points = 0

                    bonus_gift = random.choice(
                        ["vocha", "book", "pen"]
                    )

                    if bonus_gift == "vocha":
                        message = (
                            "Umejishindia vocha ya Tsh 1000 "
                            "mtandao wowote!"
                        )

                    elif bonus_gift == "book":
                        message = "Umejishindia daftari jipya!"

                    elif bonus_gift == "pen":
                        message = "Umejishindia peni 3!"

                else:
                    message = (
                        "Hongera! umeongeza nafasi ya kushinda "
                        + selected_gift
                    )

                    points = win



            # Create response using render()
            response = render(
                request,
                "lucky/home_l.html",
                {
                    "message": message
                }
            )


            # Save cookies
            response.set_cookie(
                "last_lucky_date",
                today
            )


            if selected_gift == "vocha":
                response.set_cookie(
                    "vocha_win_chance",
                    vocha_win_chance
                )

            elif selected_gift == "book":
                response.set_cookie(
                    "book_win_chance",
                    book_win_chance
                )

            elif selected_gift == "pen":
                response.set_cookie(
                    "pen_win_chance",
                    pen_win_chance
                )

            elif selected_gift == "points":
                response.set_cookie(
                    "points",
                    points
                )


            return response

        else:

            message = (
                "Hongera! umepata nafasi ya kujaribu tena baadae."
            )

            response = render(
                request,
                "lucky/home_l.html",
                {
                    "message": message
                }
            )

            response.set_cookie(
                "last_lucky_date",
                today
            )

            return response


    return render(
        request,
        "lucky/home_l.html",
        {
            "message": message
        }
    )