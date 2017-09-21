from __future__ import absolute_import

from sentry import options
from sentry.integrations import OAuth2Integration

options.register('slack.client-id')
options.register('slack.client-secret')
options.register('slack.verification-token')


class SlackIntegration(OAuth2Integration):
    id = 'slack'
    name = 'Slack'

    oauth_access_token_url = 'https://slack.com/api/oauth.access'
    oauth_authorize_url = 'https://slack.com/oauth/authorize'
    oauth_client_id = options.get('slack.client-id')
    oauth_client_secret = options.get('slack.client-secret')
    oauth_scopes = (
        'bot',
        'chat:write:bot',
        'commands',
        'team:read',
    )

    def build_integration(self, state):
        data = state['data']
        return {
            'external_id': data['team_id'],
            'name': data['team_name'],
            'metadata': {
                'bot_access_token': data['bot']['bot_access_token'],
                'bot_user_id': data['bot']['bot_user_id'],
            }
        }

    def build_identity(self, state):
        data = state['oauth2']
        return {
            'access_token': data['access_token'],
            'scopes': data['scope']
        }
