# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================
# Related Video: https://www.youtube.com/watch?v=vbDquubczDo

from models import session, User, Comment, Post, Category, Tag


# ==========================================================================================
# CREATE FUNCTIONS
# ==========================================================================================
def add_user(username: str, email: str):
    user = session.query(User).filter_by(username=username, email=email).first()
    if user:
        print(f"User with username:{username} and email:{email} already exists")
        return
    user = User(username=username, email=email)
    session.add(user)
    session.commit()
    print(f"User '{username}' added.")


def add_category(name: str):
    category = Category(name=name)
    session.add(category)
    session.commit()
    print(f"Category '{name}' added.")


def add_tag(name: str):
    tag = Tag(name=name)
    session.add(tag)
    session.commit()
    print(f"Tag '{name}' added.")


def add_post(
    username: str,
    title: str,
    content: str,
    category_name: str,
    tags: list[str] = list(),
):
    user = session.query(User).filter_by(username=username).first()
    category = session.query(Category).filter_by(name=category_name).first()
    if not user or not category:
        print("User or category not found.")
        return
    post = Post(title=title, content=content, user=user, category=category)
    session.add(post)
    for tag_name in tags:
        tag = session.query(Tag).filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            session.add(tag)
            session.commit()
        post.tags.append(tag)
    session.commit()
    print(f"Post '{title}' added by '{username}'.")


def add_comment(username: str, post_id: int, content: str):
    user = session.query(User).filter_by(username=username).first()
    post = session.query(Post).filter_by(id=post_id).first()
    if not user or not post:
        print("User or post not found.")
        return
    comment = Comment(content=content, user=user, post=post)
    session.add(comment)
    session.commit()
    print(f"Comment added to post with id '{post_id}' by '{username}'.")


# ==========================================================================================
# READ FUNCTIONS
# ==========================================================================================
def get_posts_by_category(category_name: str):
    category = session.query(Category).filter_by(name=category_name).first()
    if not category:
        print(f"Category '{category_name}' not found.")
        return []
    return category.posts


def get_posts_by_tags(tags_names: list[str]):
    return session.query(Tag).filter(Tag.name.in_(tags_names)).all()


def print_all_user_posts(user: User):
    print(f"User: {user.username}")
    for post in user.posts:
        print(f" - Post: {post.title}, Tags: {[tag.name for tag in post.tags]}")

        for comment in post.comments:
            print(f"   - Comment: {comment.content} by {comment.user.username}")


def get_user_posts_paginated(
    username: str, limit: int = 10, offset: int = 0
) -> list[Post]:
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print(f"User with username:{username} doesn't exist")
        return []

    posts = (
        session.query(Post)
        .filter(Post.user == user)
        .limit(limit)
        .offset(offset * limit)
        .all()
    )

    return posts


# ==========================================================================================
# DELETE FUNCTIONS
# ==========================================================================================
def delete_post(id: int):
    post = session.query(Post).filter_by(id=id).first()
    if not post:
        print(f"Post with id:'{id}' not found.")
        return

    session.delete(post)
    session.commit()
    print(f"Post with '{id}' deleted.")


def delete_comment(comment_id: int):
    comment = session.query(Comment).filter_by(id=comment_id).first()
    if not comment:
        print(f"Comment with ID '{comment_id}' not found.")
        return

    session.delete(comment)
    session.commit()
    print(f"Comment with ID '{comment_id}' deleted.")


# ==========================================================================================
# UPDATE FUNCTIONS
# ==========================================================================================
def update_post(
    post_id: int,
    new_title: str | None = None,
    new_content: str | None = None,
    new_category_name: str | None = None,
    new_tags: str | None = None,
):
    post = session.query(Post).filter_by(id=post_id).first()
    if not post:
        print(f"Post with id '{post_id}' not found.")
        return

    # Update post attributes if new values are provided
    post.title = new_title if new_title else post.title
    post.content = new_content if new_content else post.content

    if new_category_name and post.category.name != new_category_name:
        category = session.query(Category).filter_by(name=new_category_name).first()
        if category:
            post.category = category
        else:
            print(f"Category '{new_category_name}' not found.")

    if new_tags:
        post.tags.clear()
        for tag_name in new_tags:
            tag = session.query(Tag).filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                session.add(tag)

            post.tags.append(tag)

    session.commit()
    print(f"Post with id '{post_id}' updated successfully.")


def update_comment(comment_id: int, new_content: str):
    comment = session.query(Comment).filter_by(id=comment_id).first()
    if not comment:
        print(f"Comment with ID '{comment_id}' not found.")
        return

    comment.content = new_content
    session.commit()
    print(f"Comment with ID '{comment_id}' updated successfully.")


# ==========================================================================================
# VARIABLES
# ==========================================================================================
USERNAME = "TestUser"
CATEGORY = "Technology"
TAG = "Tech"

# Create Operations
print(
    "======================================================================================"
)
print("\n\nCreate Operations:")
add_user(USERNAME, "test@example.com")
add_category(CATEGORY)
add_tag(TAG)
add_post(
    USERNAME,
    "Understanding SQLAlchemy Through Examples",
    "A deep dive into SQLAlchemy ORM for real scenarios.",
    CATEGORY,
    [TAG],
)
add_comment(USERNAME, 1, "This is a fascinating topic!")

# Read Operations
print(
    "======================================================================================"
)
print("\n\nRead Operations:")
tags = get_posts_by_tags([TAG, "Cooking"])
print(f"\nPosts by Tag: [{TAG}, Cooking]")
for tag in tags:
    for post in tag.posts:
        print(f"Post: {post.title}, user: {post.user.username}")

category_posts = get_posts_by_category(CATEGORY)
print(f"\nPosts by Category: {CATEGORY}")
for post in category_posts:
    print(f" - Post: {post.title}, user: {post.user.username}")

category_posts = get_posts_by_category("None")
print("\nPosts by Category: None")
for post in category_posts:
    print(f" - Post: {post.title}, user: {post.user.username}")

user = session.query(User).filter_by(username=USERNAME).first()
print_all_user_posts(user)

posts = get_user_posts_paginated(USERNAME)
print(f"\nUser {USERNAME} has {len(posts)} posts!")

# Update Operations
print(
    "======================================================================================"
)
print("\n\nUpdate Operations:")
update_post(1, new_title="An updated example of SQLAlchemy")
update_post(1, new_content="Now you know how to do this! Congratulations!")
update_comment(1, "I have updated my comment")

# Delete Operations
print(
    "======================================================================================"
)
print("\n\nDelete Operations:")
print(f"There are {session.query(Comment).count()} comments")
delete_comment(1)
print(f"There are now {session.query(Comment).count()} comments")

print(f"\nThere are {session.query(Post).count()} posts")
delete_post(1)
print(f"There are now {session.query(Post).count()} posts")
