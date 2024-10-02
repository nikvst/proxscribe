from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
async def main_page_view(request):
    user = await request.auser()
    return redirect("subscription", subscription_id=user.subscription_id)
