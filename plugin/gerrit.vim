" Contains all the code that is GLOBAL to the plugin. Like turning off turning
" on the plugin, setting paths needed for python scripts etc

call gv#default('g:gv_python', 'python')
call gv#default('g:gv_paths', [])
call gv#defualt('g:gv_show_status', '<C-c>ga')
call gv#default('g:gv_plugin_root', expand('<sfile>:p:h:h'))

if g:gv_python != 'disable' && (g:gv_python == 'python3' || !has('python') && has('python3'))
    let g:gv_python = 'python3'
    command! -nargs=1 GvPython python3 <args>

elseif g:gv_python != 'disable' && has('python')
    let g:gv_python = 'python'
    command! -nargs=1 GvPython python <args>

else
    let g:gv_python = 'disable'

endif
