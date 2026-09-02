import random
import secrets

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models.aggregates import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from core.models import CustomerSpin


@login_required(login_url="customer_login")
def spin_page(request):
    """
    Display the spin wheel page.
    """
    return render(request, "lucky/lucky_c.html")



@login_required(login_url="customer_login")
@transaction.atomic
def spin(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "success": False,
                "message": "Invalid request."
            },
            status=405
        )

    user = request.user

    today = timezone.localdate()


    # =========================================================
    # CHECK IF CUSTOMER ALREADY PLAYED TODAY
    # =========================================================

    already_played = CustomerSpin.objects.filter(
        customer=user,
        play_date=today
    ).exists()


    if already_played:

        return JsonResponse(
        {
            "success": False,
            "already_played": True,
            "message": (
                "You have already played today. "
                "Come back tomorrow."
            ),
            "points": (
                CustomerSpin.objects
                .filter(
                    customer=user
                )
                .aggregate(
                    total=Sum("points")
                )
                .get("total")
                or 0
            ),
            "reward_count": (
                CustomerSpin.objects
                .filter(
                    customer=user
                )
                .order_by("-created_at")
                .values_list(
                    "reward_count",
                    flat=True
                )
                .first()
                or 0
            ),
        }
    )

    # =========================================================
    # REWARD OPTIONS
    # =========================================================

    rewards = [
        "vocha",
        "points",
        "loss",
        "post_chance",
        "points",
        "vocha",
        "loss",
        "post_chance",
    ]

    reward_type = random.choice(rewards)


    # =========================================================
    # GET PREVIOUS TOTAL POINTS
    # =========================================================

    previous_points = (
        CustomerSpin.objects
        .filter(
            customer=user
        )
        .aggregate(
            total=Sum("points")
        )
        .get("total")
        or 0
    )


    # =========================================================
    # GET PREVIOUS VOUCHER COUNT
    #
    # reward_count stores the voucher progress.
    # =========================================================

    previous_vouchers = (
        CustomerSpin.objects
        .filter(
            customer=user
        )
        .order_by("-created_at")
        .values_list(
            "reward_count",
            flat=True
        )
        .first()
        or 0
    )


    # =========================================================
    # DEFAULT VALUES
    # =========================================================

    reward = "LOSS"

    message = ""

    points_earned = 0

    voucher_count = previous_vouchers

    congratulations = False


    # =========================================================
    # POINTS
    # =========================================================

    if reward_type == "points":

        points_earned = 10

        total_points = (
            previous_points +
            points_earned
        )

        reward = "10 POINTS"

        message = (
            "🎉 Congratulations! "
            "You won 10 points. "
            f"Your total points are now "
            f"{total_points}."
        )


        # Save today's points

        CustomerSpin.objects.create(
            customer=user,
            reward=reward,
            reward_count=previous_vouchers,
            points=points_earned,
            play_date=today
        )


    # =========================================================
    # VOCHA
    # =========================================================

    elif reward_type == "vocha":

        voucher_count = (
            previous_vouchers +
            1
        )

        reward = "VOCHA"


        # =====================================================
        # REACHED 5 VOUCHERS
        # =====================================================

        if voucher_count >= 5:

            congratulations = True

            message = (
                "🎉 Congratulations! "
                "You have collected 5 vouchers!"
            )


            # Clear voucher progress

            CustomerSpin.objects.create(
                customer=user,
                reward=reward,
                reward_count=0,
                points=0,
                play_date=today
            )


        # =====================================================
        # LESS THAN 5 VOUCHERS
        # =====================================================

        else:

            message = (
                "🎟️ Congratulations! "
                "You won 1 voucher. "
                f"Your voucher progress is "
                f"{voucher_count}/5."
            )


            CustomerSpin.objects.create(
                customer=user,
                reward=reward,
                reward_count=voucher_count,
                points=0,
                play_date=today
            )


    # =========================================================
    # LOSS
    # =========================================================

    elif reward_type == "loss":

        reward = "LOSS"

        message = (
            "❌ Sorry! You didn't win anything "
            "this time. Come back tomorrow!"
        )


        CustomerSpin.objects.create(
            customer=user,
            reward=reward,
            reward_count=previous_vouchers,
            points=0,
            play_date=today
        )


    # =========================================================
    # POST CHANCE
    # =========================================================

    elif reward_type == "post_chance":

        reward = "POST"

        message = (
            "📢 Congratulations! "
            "You won a chance to post."
        )


        CustomerSpin.objects.create(
            customer=user,
            reward=reward,
            reward_count=previous_vouchers,
            points=0,
            play_date=today
        )


    # =========================================================
    # CALCULATE FINAL TOTAL POINTS
    # =========================================================

    final_points = (
        previous_points +
        points_earned
    )


    # =========================================================
    # CONGRATULATIONS URL
    # =========================================================

    congratulations_url = ""


    if congratulations:

        congratulations_url = (
            "/spin/congratulations/"
        )


    # =========================================================
    # JSON RESPONSE
    # =========================================================

    return JsonResponse(
        {
            "success": True,

            "reward_type": reward_type,

            "reward": reward,

            "message": message,

            "points": final_points,

            "points_earned": points_earned,

            "reward_count": (
                0
                if congratulations
                else voucher_count
            ),

            "congratulations": congratulations,

            "congratulations_url": (
                congratulations_url
            ),
        }
    )


@login_required(login_url="customer_login")
def congratulations(request):

    return render(
        request,
        "lucky/congratulations.html"
    )