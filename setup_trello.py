import os
from trello import TrelloClient

client = TrelloClient(os.getenv("TRELLO_API_KEY"), token=os.getenv("TRELLO_TOKEN"))

def print_hook(hook):
    print(f"{hook.desc} -> {hook.callback_url} (Active: {hook.active})")

def delete_all_webhooks():
    for hook in client.list_hooks():
        print_hook(hook)
        hook.delete()


def list_orgs():
    for org in client.list_organizations():
        print(f"{org.id} {org.name}")

if __name__ == "__main__":
    # delete_all_webhooks()
    # list_orgs()

    org = client.get_organization(os.getenv("TRELLO_ORG_ID"))

    for board in org.all_boards():
        print(f"{board.name}")

        hook = client.create_hook( os.getenv("ULTRAHOOK_CALLBACK_URL"), board.id, desc="Ludus" )
        if hook:
            print_hook(hook)
        else:
            print("failed to create hook")


