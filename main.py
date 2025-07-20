import init_django_orm  # noqa: F401
from db.models import Race, Skill, Player, Guild
import json


def main() -> None:
    with open("players.json", "r", encoding="utf-8") as f:
        players_data = json.load(f)

    # players_data — це словник, де ключі — ніки, значення — дані гравців
    for nickname, player in players_data.items():
        race_data = player.get("race", {})
        race_obj, _ = Race.objects.get_or_create(
            name=race_data.get("name"),
            defaults={"description": race_data.get("description", "")},
        )

        skills = race_data.get("skills", [])
        for skill in skills:
            Skill.objects.get_or_create(
                name=skill.get("name"),
                defaults={"bonus": skill.get("bonus", ""), "race": race_obj},
            )

        guild_data = player.get("guild")
        if guild_data:
            guild_obj, _ = Guild.objects.get_or_create(
                name=guild_data.get("name"),
                defaults={"description": guild_data.get("description")},
            )
        else:
            guild_obj = None

        Player.objects.get_or_create(
            nickname=nickname,
            defaults={
                "email": player.get("email", ""),
                "bio": player.get("bio", ""),
                "race": race_obj,
                "guild": guild_obj,
            },
        )


if __name__ == "__main__":
    main()
