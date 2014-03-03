import os
import urlparse
import json

import vim
import requests
from requests.auth import HTTPDigestAuth
from pygerrit.salting import check_hash, AuthObject

# Until I can get the kerberos auth figured out,
# I made a SSH Tunnel and just do all the things I want to.
URL_END_POINT = 'http://localhost:8081'  # 'http(s)://<YOUR GIT URL>/'
XSSI_STRING = ")]}'"


def _gerrit_status(auth_object):
	"""
	Fetch the changes which are open and you are the owner of.
	GET /?q=is:open+owner:self
	"""
	# TODO(Sid): Move this to a decorator
	if check_hash(auth_object._password, auth_object._hash) is not True:
		raise ValueError('Bad password?')

	query_params = '?q=is:open+owner:self'
	authentication_url = urlparse.urljoin(URL_END_POINT, '/a/changes/')
	basic_auth = (USER, auth_object._password)
	digest_auth = HTTPDigestAuth(*basic_auth)

	auth_response = requests.get(
			authentication_url + query_params,
			auth=digest_auth)
	if auth_response.status_code == 200:
		return json.loads(auth_response.text.replace(XSSI_STRING, ''))
	else:
		raise ValueError(
				'Received non 200 response %d. Text: %s'
				% (auth_response.status_code, auth_response.text))

def gerrit_status_wrapper():
	vim.command("call gv#default(g:gerrit_password",)
	plugin_path = vim.eval("g:gv_plugin_root")
	print plugin_path

	# TODO(Sid): Extract this boilerplate
	config = json.load(os.path.join(
		plugin_path, 'config/config.json'))
	auth_object = AuthObject(
		password=config['password'],
		username=config['username'])
	data = _gerrit_status(auth_object)

	# Create a buffer
	vim.command(":badd gerrit_status")
	vim.command(":setlocal buftype=nofile")
	vim.command(":setlocal bufhidden=wipe")
	vim.command(":setlocal buftype=nowrite")
	# Now write to the buffer

def www_auth(response):

	"""
	Breaks up the www-authenticate into its parts. Returns a
	dictionary with keys as 'basic', 'negotiate' etc. Tells you
	how to make your next move.
	Negotiate, mutual authenticate, basic, digest auth
	etc.
	"""
	auth_fields = {}
	for field in response.headers.get("www-authenticate", "").split(","):
			kind, __, details = field.strip().partition(" ")
			auth_fields[kind.lower()] = details.strip()
	return auth_fields