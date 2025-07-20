import init_django_orm  # noqa: F401

from db.models import Race, Skill, Player, Guild
import json


def main() -> None:
    with open('players.json', 'r', encoding='utf-8') as f:
        players_data = json.load(f)

    for player in players_data:
        # Отримуємо або створюємо расу
        race_data = player.get('race', {})
        race_obj, _ = Race.objects.get_or_create(
            name=race_data.get('name'),
            defaults={'description': race_data.get('description', '')}
        )

        # Створюємо навички раси (якщо їх нема)
        skills = race_data.get('skills', [])
        for skill in skills:
            Skill.objects.get_or_create(
                name=skill.get('name'),
                defaults={
                    'bonus': skill.get('bonus', ''),
                    'race': race_obj
                }
            )

        # Отримуємо або створюємо гільдію (може бути None)
        guild_data = player.get('guild')
        if guild_data:
            guild_obj, _ = Guild.objects.get_or_create(
                name=guild_data.get('name'),
                defaults={'description': guild_data.get('description')}
            )
        else:
            guild_obj = None

        # Отримуємо або створюємо гравця
        Player.objects.get_or_create(
            nickname=player.get('nickname'),
            defaults={
                'email': player.get('email', ''),
                'bio': player.get('bio', ''),
                'race': race_obj,
                'guild': guild_obj,
            }
        )


if __name__ == "__main__":
    main()
