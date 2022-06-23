from App.models.user import User

def test_new_user():
    """GIVEN a User model
    WHEN  a new User is created
    THEN check the email and passwordfields are definde correctly 
    """
    user = User('coco@titi.fr', 'a new photo', 'monPasssword', 'MonSurnom')
    assert user.email == 'coco@titi.fr'
    assert user.photo == 'a new photo'
    assert user.password == 'monPasssword'
    assert user.name == 'MonSurnom'