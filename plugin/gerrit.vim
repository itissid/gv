" Contains all the code that is GLOBAL to the plugin. Like turning off turning
" on the plugin, setting paths needed for python scripts etc

call gv#default('g:gv_python', 'python')
call gv#default('g:gv_paths', [])
call gv#default('g:gv_show_status', '<C-c>ga')
call gv#default('g:gv_show_changes', '<C-c>gv')
call gv#default('g:gv_plugin_root', expand('<sfile>:p:h:h'))
" Set me to ppoint to a valid git URI
call gv#default('g:gv_root_url', 'https://git.knewton.net/')
" Set this to be oauth,kerberos what have you...
call gv#default('g:gv_password_auth_scheme_name', 'password')
call gv#default('g:gv_auth_method', g:gv_password_auth_scheme_name)

if g:gv_python != 'disable' && (g:gv_python == 'python3' || !has('python') && has('python3'))
    let g:gv_python = 'python3'
    command! -nargs=1 GvPython python3 <args>

elseif g:gv_python != 'disable' && has('python')
    let g:gv_python = 'python'
    command! -nargs=1 GvPython python <args>

else
    let g:gv_python = 'disable'

endif
