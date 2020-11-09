"""Favoris"""

import datetime

from django.core.paginator import Paginator

from ..models import Favorite


class AuxilliariesFavorites:
    """docstring for AuxilliariesFavorites"""

    def __init__(self):
        """Init"""
        pass

    def get_context_favorites(self, request, user_id, favoris_status):
        """Get context of favorites list"""
        favorite_user = Favorite.objects.filter(
            user__id=request.session["user_id"]
        ).order_by("-date_engistrement")
        pre_resultats = []
        for favorite in favorite_user:
            favorite.date_engistrement += datetime.timedelta(hours=1)
            pre_resultats.append([favorite, favorite.substitut, favorite.product])

        paginator = Paginator(pre_resultats, 9)
        page = request.GET.get("page")
        try:
            resultats = paginator.page(page)
        except Exception as e:
            resultats = paginator.page(1)
        context = {
            "user_id": user_id,
            "favoris_status": favoris_status,
            "numero_page": page,
            "resultats": resultats,
        }
        return context
