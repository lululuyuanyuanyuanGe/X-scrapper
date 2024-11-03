from twikit import Client

# Convert user name to numerical ID
def NameToID(name, client):
    user = client.get_user_by_screen_name(name)
    user_id = user.id
    return user_id