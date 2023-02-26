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
        (214, User.travellers.get_leader_by_country(), "countries_visited"),
        (215, User.travellers.get_leader_by_city(), "visited_cities"),
        (216, User.travellers.get_leader_by_capital(), "visited_cities"),
        (217, User.objects.get_leader_of_leaders(), "awards"),
    }

    for detail in special_scenarios:
        assign_badge(detail[0], detail[1], detail[2])
