from stravalib import Client
from flask import Flask, render_template, redirect, url_for, request, jsonify, current_app
from app.oauth import oauth_bp


@oauth_bp.route("/login")
def login():
    c = Client()
    url = c.authorization_url(client_id=current_app.config['STRAVA_CLIENT_ID'],
                              redirect_uri=url_for('oauth.logged_in', _external=True),
                              approval_prompt='auto')
    return render_template('login.html', authorize_url=url)


@oauth_bp.route("/strava-oauth")
def logged_in():
    """
    Method called by Strava (redirect) that includes parameters.
    - state
    - code
    - error
    """
    error = request.args.get('error')
    state = request.args.get('state')
    if error:
        return render_template('login_error.html', error=error)
    else:
        code = request.args.get('code')
        client = Client()
        access_token = client.exchange_code_for_token(client_id=current_app.config['STRAVA_CLIENT_ID'],
                                                      client_secret=current_app.config['STRAVA_CLIENT_SECRET'],
                                                      code=code)
        # Probably here you'd want to store this somewhere -- e.g. in a database.
        strava_athlete = client.get_athlete()

        return render_template('login_results.html', athlete=strava_athlete, access_token=access_token)
