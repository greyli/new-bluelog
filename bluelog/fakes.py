import random

from faker import Faker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func

from bluelog.extensions import db
from bluelog.models import Admin, Category, Post, Comment, Link

fake = Faker()


def fake_admin():
    admin = Admin(
        username='admin',
        blog_title='Bluelog',
        blog_sub_title="No, I'm the real thing.",
        name='Mima Kirigoe',
        about='Um, l, Mima Kirigoe, had a fun time as a member of CHAM...'
    )
    admin.set_password('helloflask')
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):
    category = Category(name='Default')
    db.session.add(category)

    i = 0
    while i < count - 1:
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    for _ in range(count):
        category_count = db.session.execute(select(func.count(Category.id))).scalars().one()
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            category=db.session.get(Category, random.randint(1, category_count)),
            timestamp=fake.date_time_this_year()
        )

        db.session.add(post)
    db.session.commit()


def fake_comments(count=500):
    for _ in range(count):
        post_count = db.session.execute(select(func.count(Post.id))).scalars().one()
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=random.choice([True, True, True, True, False]),
            from_admin=random.choice([False, False, False, False, True]),
            post=db.session.get(Post, random.randint(1, post_count))
        )
        db.session.add(comment)
    db.session.commit()


def fake_replies(count=50):
    for _ in range(count):
        comment_count = db.session.execute(select(func.count(Comment.id))).scalars().one()
        post_count = db.session.execute(select(func.count(Post.id))).scalars().one()
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=db.session.get(Comment, random.randint(1, comment_count)),
            post=db.session.get(Post, random.randint(1, post_count))
        )
        db.session.add(comment)
    db.session.commit()


def fake_links():
    twitter = Link(name='Twitter', url='https://twitter.com')
    facebook = Link(name='Facebook', url='https://facebook.com')
    linkedin = Link(name='LinkedIn', url='https://linkedin.com')
    google = Link(name='Google', url='https://google.com')
    db.session.add_all([twitter, facebook, linkedin, google])
    db.session.commit()
