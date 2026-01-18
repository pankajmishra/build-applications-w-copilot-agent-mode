
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Delete all existing data
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel', description='Marvel Superheroes')
        dc = Team.objects.create(name='DC', description='DC Superheroes')

        # Create Users
        users = [
            User.objects.create(email='ironman@marvel.com', username='Iron Man', team=marvel),
            User.objects.create(email='captain@marvel.com', username='Captain America', team=marvel),
            User.objects.create(email='batman@dc.com', username='Batman', team=dc),
            User.objects.create(email='superman@dc.com', username='Superman', team=dc),
        ]

        # Create Workouts
        pushups = Workout.objects.create(name='Pushups', description='Do 20 pushups')
        running = Workout.objects.create(name='Running', description='Run 5km')
        pushups.suggested_for.set([marvel, dc])
        running.suggested_for.set([marvel, dc])

        # Create Activities
        Activity.objects.create(user=users[0], activity_type='Pushups', duration=15, date=timezone.now().date())
        Activity.objects.create(user=users[1], activity_type='Running', duration=30, date=timezone.now().date())
        Activity.objects.create(user=users[2], activity_type='Pushups', duration=10, date=timezone.now().date())
        Activity.objects.create(user=users[3], activity_type='Running', duration=25, date=timezone.now().date())

        # Create Leaderboard
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=90)

        # Ensure unique index on email field in users collection
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.user.create_index([('email', 1)], unique=True)
        self.stdout.write(self.style.SUCCESS('Database populated with test data and unique index created on user email.'))
