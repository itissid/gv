import os
import urlparse
import json

import vim
import requests
from requests.auth import HTTPDigestAuth
from pygerrit.salting import check_hash, AuthObject

# Until I can get the kerberos auth figured out,
# I made a SSH Tunnel and just do all the things I want to.
XSSI_STRING = ")]}'"
PROJECT_JSON_KEY = 'project'
BRANCH_JSON_KEY = 'branch'
SUBJECT_JSON_KEY = 'subject'
CHANGE_ID_KEY = 'change_id'


def auth_and_get_result(query_string=None):
	"""
	Does some boiler plate managemnet for authorization and
	getting data based on the query_string.
	TODO(sid): Implement different types of auth schemes
	based on variables set in the
	"""
	plugin_path = vim.eval("g:gv_plugin_root")
	auth_method = vim.eval("g:gv_auth_method")
	url_end_point = vim.eval("g:gv_root_url")
	password_auth_method_name = vim.eval("g:gv_password_auth_scheme_name")

	def _inner_auth_and_get_result(f):
		def _inner_(*args, **kwargs):
			#TODO(Sid): Instead of branches try calling a
			# method that returns an instance of the AuthObject that you
			# can use to make the REST requesnt?
			if auth_method == password_auth_method_name:
				# TODO(Sid): Remove me to another method
				config = json.load(open(os.path.join(
					plugin_path, 'config/config.json')))
				auth_object = AuthObject(
					password=config['password'],
					username=config['username'])
				basic_auth = (auth_object.username, auth_object.password)
				digest_auth = HTTPDigestAuth(*basic_auth)

				authentication_url = urlparse.urljoin(url_end_point, '/a')
				# In case the query string was parameterized
				if 'format_params' in kwargs:
					_query_string = query_string.format(**kwargs['format_params'])
				else:
					_query_string = query_string

				auth_response = requests.get(
						authentication_url + _query_string,
						auth=digest_auth)
				if auth_response.status_code == 200:
					kwargs['response'] = json.loads(
							auth_response.text.replace(XSSI_STRING, ''))
				else:
					raise ValueError(
							'Received non 200 response %d. Text: %s'
							% (auth_response.status_code, auth_response.text))
			else:
				# Here will go the future auth schemes that gerrit requires.
				raise ValueError('Auth scheme not recognized.')
			return f(*args, **kwargs)
		return _inner_
	return _inner_auth_and_get_result


@auth_and_get_result(
	query_string='/changes/?q=is:open+owner:self&o=CURRENT_REVISION')
def gerrit_status(response=None):

	response.sort(key=lambda x: (
				x[PROJECT_JSON_KEY],
				x[BRANCH_JSON_KEY],
				x[SUBJECT_JSON_KEY]))

	# Create a buffer
	gerrit_status_buffer_name = vim.eval('g:gerrit_status_buffer_name')
	vim.command(":badd %s" % gerrit_status_buffer_name)
	vim.command("vert sb %s" % gerrit_status_buffer_name)
	vim.command(":setlocal buftype=nofile")
	vim.command(":setlocal bufhidden=wipe")
	vim.command(":setlocal modifiable")
	vim.command("let g:gerrit_change_id_lookup={}")
	gerrit_status_buffer = None

	# Now write to the buffer
	# TODO(Sid): Figure out the encoding issues
	# Figure out a display format
	for b in vim.buffers:
		if b.name and b.name.find(gerrit_status_buffer_name) >= 0:
			gerrit_status_buffer = b
	gerrit_status_buffer[:] = None
	gerrit_status_buffer.append(20 * "-")
	for change in response:
		project_name = change[PROJECT_JSON_KEY].encode('utf-8')
		branch_name = change[BRANCH_JSON_KEY].encode('utf-8')
		subject = change[SUBJECT_JSON_KEY].encode('utf-8')

		change_id = change[CHANGE_ID_KEY].encode('utf-8')
		partial_change_id = change_id[0:10]
		revision_lookup_id = "%s~%s~%s" % (
				project_name, branch_name,
				change[CHANGE_ID_KEY].encode('utf-8'))
		gerrit_status_buffer.append("P| %s" % project_name)
		gerrit_status_buffer.append(("    B| %s" % branch_name))
		gerrit_status_buffer.append(
				("        S| (%s..) %s" % (partial_change_id, subject)))
		store_command = ":let g:gerrit_change_id_lookup[\"%s\"] = \"%s\"" % (
				change_id, revision_lookup_id)
		vim.command(store_command)
	gerrit_status_buffer.append(20 * "-")
	vim.command(":setlocal noma")


@auth_and_get_result(
		query_string='/changes/{change_id}/revisions/{revision_id}/files/')
def display_change_contents(
	response=None, format_params={}):
	"""
	Given an item selected from the gerrit status
	change window. If you invoke the right key bindings
	you can see the changes that are part of the latest patch
	You must call this function with a non null value of the change_id and the
	revision_id.
	Here is the documentation for this:
	https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#list-files
	format_params should have the following =
		{'change_id': None, 'revision_id': None}
	"""
	print response


@auth_and_get_result(
		query_string='/changes/{change_id}/revisions/{revision_id}/files/{file_id}/contents')
def display_file_contents(
		response=None, format_params={}):
	"""
	format_params should have the following = {
		'change_id': ..., 'revision_id': ..., 'file_id': ...
	}
	"""
	print response
