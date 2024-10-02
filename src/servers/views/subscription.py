import base64

from django.http import HttpResponse
from django.shortcuts import render, aget_object_or_404

from users.models import User


async def subscription_view(request, subscription_id):
    user = await aget_object_or_404(User, subscription_id=subscription_id)
    clients = (
        user.clients.filter(enable=True)
        .select_related("inbound")
        .order_by("inbound__priority")
    )

    links = [client.connection_url async for client in clients]

    user_agent = request.META.get("HTTP_USER_AGENT", "").lower()
    if "mozilla" in user_agent or "chrome" in user_agent or "safari" in user_agent:
        # for browsers
        return render(
            request,
            "servers/subscriptions.html",
            {
                "user": user,
                "links": links,
            },
        )
    else:
        # for vpn-clients
        return HttpResponse(
            base64.b64encode("%20\n".join(links).encode("utf-8")).decode("utf-8")
        )
