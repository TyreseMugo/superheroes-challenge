from app import app
from models import SuperPower, Champion, ChampionPower, db
import random

with app.app_context():
    Champion.query.delete()
    SuperPower.query.delete()
    ChampionPower.query.delete()

    print("🦸‍♀️ Seeding superpowers...")

    powers_data = [
        {"name": "super strength", "description": "grants the wielder incredible physical prowess"},
        {"name": "flight", "description": "bestows the ability to soar through the skies with great speed"},
        {"name": "superhuman senses", "description": "heightens the user's senses to extraordinary levels"},
        {"name": "elasticity", "description": "allows the user to stretch their body to amazing lengths"}
    ]

    for data in powers_data:
        power = SuperPower(**data)
        db.session.add(power)

    db.session.commit()

    print("🦸‍♀️ Seeding champions...")

    champions_data = [
        {"name": "Kara Zor-El", "super_name": "Supergirl"},
        {"name": "Jennifer Walters", "super_name": "She-Hulk"},
        {"name": "Barbara Gordon", "super_name": "Batgirl"},
        {"name": "Janet van Dyne", "super_name": "Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"}
    ]

    for data in champions_data:
        champion = Champion(**data)
        db.session.add(champion)

    db.session.commit()

    print("🦸‍♀️ Adding powers to champions...")

    strengths = ["Strong", "Weak", "Average"]

    champions = Champion.query.all()
    powers = SuperPower.query.all()

    for champion in champions:
        for _ in range(random.randint(1, 3)):
            power = random.choice(powers)
            strength = random.choice(strengths)

            champion_power = ChampionPower(champion_id=champion.id, power_id=power.id, strength=strength)
            db.session.add(champion_power)
            print(champion_power)

    db.session.commit()

    print("🦸‍♀️ Done seeding!")
