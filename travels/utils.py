from travels.constants import MOST_AWARDS_ID, MOST_CAPITALS_VISITED_ID, MOST_CITIES_VISITED_ID, \
    MOST_COUNTRIES_VISITED_ID
from travels.models import Badge
from users.models import User


def recalculate_platform_badges() -> None:
    def assign_badge(badge_id, user, criteria):
        award = Badge.objects.get(id=badge_id)
        if user and (
            not award.users.last()
            or getattr(user, criteria) > getattr(award.users.last(), criteria)
        ):
            award.users.clear()
            award.users.add(user)

    special_scenarios = {
        (MOST_COUNTRIES_VISITED_ID, User.travellers.get_leader_by_country(), "countries_visited"),
        (MOST_CITIES_VISITED_ID, User.travellers.get_leader_by_city(), "visited_cities"),
        (MOST_CAPITALS_VISITED_ID, User.travellers.get_leader_by_capital(), "visited_cities"),
        (MOST_AWARDS_ID, User.objects.get_leader_of_leaders(), "awards"),
    }

    for detail in special_scenarios:
        assign_badge(detail[0], detail[1], detail[2])
