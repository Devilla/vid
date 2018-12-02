from beem import Steem as Whaleshares
from smoke import Steem as Smoke
from steem import Steem as Steem

from beem.account import Account

class SteemManager:
    def __init__(self, keys):
        '''
        Parameters:
        ___________

        keys: (list)
        The posting keys
        '''
        self.s = Steem(keys=keys, nodes=["https://api.steemit.com", "https://rpc.buildteam.io"])
        
    def post_in_steem(self, title, body, username, tags):
        '''
        Posts in steem and returns details
        
        Parameters:
        ___________
        title: (string)
        The title of the post
        
        body: (string)
        The body of the post
        
        username: (string)
        The username of the poster
        
        tags: (list)
        Tags of the post

        Returns:
        ________
        post_details (json):
        JSON details about the post that was just made
        '''
        
        post_details = self.s.commit.post(title, body, username, tags=tags)
        return post_details
        

    def get_payout(self, post_details):
        '''
        Parameters:
        ___________
        
        post_details (json):
        JSON details about the post that was just made
        
        Returns: 
        
        total_payout (int):
        Returns the total payout in int in terms of steem
        '''
        permlink = post_details['operations'][0][1]['permlink']
        author = post_details['operations'][0][1]['author']
        payout_params = self.s.steemd.get_content(author, permlink)
        total_payout = float(payout_params['total_payout_value'].split()[0]) + float(payout_params['total_pending_payout_value'].split()[0])
        return total_payout


class SmokeManger:
    def __init__(self, keys):
        '''
        Parameters:
        ___________

        keys: (list)
        The posting keys
        '''
        self.s = Steem(nodes=["https://rpc.smoke.io/"], keys=keys)
        
    def post_in_smoke(self, title, body, username, tags):
        '''
        Posts in smoke and returns details
        
        Parameters:
        ___________
        title: (string)
        The title of the post
        
        body: (string)
        The body of the post
        
        username: (string)
        The username of the poster
        
        tags: (list)
        Tags of the post

        Returns:
        ________
        post_details (json):
        JSON details about the post that was just made
        '''
        
        post_details = self.s.commit.post(title, body, username, tags=tags)
        return post_details
        

    def get_payout(self, post_details):
        '''
        Parameters:
        ___________
        
        post_details (json):
        JSON details about the post that was just made
        
        Returns: 
        
        total_payout (int):
        Returns the total payout in int in terms of smoke
        '''
        permlink = post_details['operations'][0][1]['permlink']
        author = post_details['operations'][0][1]['author']
        payout_params = self.s.steemd.get_content(author, permlink)
        total_payout = float(payout_params['total_payout_value'].split()[0]) + float(payout_params['total_pending_payout_value'].split()[0])
        return total_payout

class WhalesharesManger:
    def __init__(self, keys):
        '''
        Parameters:
        ___________

        keys: (list)
        The posting keys
        '''
        self.whaleshares = Whaleshares(nodes=["https://rpc.wls.services/"], keys=['5KL69ew5BebPAA6QbWYEBCykmYoNJ8YMojVRgsaVM8VZ2mJ4xYA'])
        
    def post_in_whaleshares(self, title, body, username, tags):
        '''
        Posts in smoke and returns details
        
        Parameters:
        ___________
        title: (string)
        The title of the post
        
        body: (string)
        The body of the post
        
        username: (string)
        The username of the poster
        
        tags: (list)
        Tags of the post

        Returns:
        ________
        post_details (json):
        JSON details about the post that was just made
        '''
        
        post_details = self.s.post(title=title, body=body, author=username, tags=tags)
        return post_details
        

    def get_payout(self, username):
        '''
        Get all earned by that account 
        
        Parameters:
        ___________
        
        username (str):
        JSON details about the post that was just made
        '''
        acc = Account(username,steem_instance=t_Steem)
        total_balance = acc.get_balances()
        payout_params = self.s.steemd.get_content(author, permlink)
        return float(str(total_balance['total'][0]).split(' ')[0])