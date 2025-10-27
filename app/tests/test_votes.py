from app import models
import pytest

# class Votes(Base) :

#     __tablename__ = "Votes"

#     user_id = Column(Integer, ForeignKey("Users.id",ondelete="CASCADE"),primary_key=True)
#     post_id = Column(Integer, ForeignKey("Posts.id",ondelete="CASCADE"),primary_key=True)

# pass session, as we make the change directly to the database.
@pytest.fixture
def test_votes(test_user,test_posts,session) :
    new_vote = models.Votes(user_id=test_user['id'],post_id=test_posts[3].id)
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts) : 
    data = {
        "post_id" : test_posts[3].id,
        "dir":1
    }
    res = authorized_client.post("/votes",json = data)
    assert res.status_code == 201



def test_vote_twice_on_post(authorized_client, test_posts,test_votes) : 
    data = {
        "post_id" : test_posts[3].id,
        "dir":1
    }
    res = authorized_client.post("/votes",json = data)
    assert res.status_code == 409

def test_delete_vote(authorized_client, test_posts,test_votes) : 
    data = {
        "post_id" : test_posts[3].id,
        "dir":0
    }
    res = authorized_client.post("/votes",json = data)
    assert res.status_code == 201

def test_delete_vote_non_exist(authorized_client, test_posts) : 
    data = {
        "post_id" : test_posts[3].id,
        "dir":0
    }
    res = authorized_client.post("/votes",json = data)
    assert res.status_code == 404



def test_vote_post_non_exist(authorized_client, test_posts) : 
    data = {
        "post_id" : 8000000,
        "dir":0
    }
    res = authorized_client.post("/votes",json = data)
    assert res.status_code == 404

def test_vote_unauthorized_user(client, test_posts): 
    data = {
        "post_id" : test_posts[0].id,
        "dir":1
    }
    res = client.post("/votes",json = data)
    assert res.status_code == 401