GvPython from pygerrit import gerrit_api
GvPython from pygerrit import salting

" DESC: Import python libs that are needed
fun! pymode#init(plugin_root, paths) "{{{

    if g:gv_python == 'disable'
        if g:gv_warning
            call gv#error("GV requires vim compiled with +python. Most of features will be disabled.")
        endif
        return
    endif


	echom 'Here in a/gv.vim'
    GvPython import sys, vim
    GvPython sys.path.insert(0, vim.eval('a:plugin_root'))
    GvPython sys.path = vim.eval('a:paths') + sys.path

endfunction "}}}

" DESC: Show error
fun! gv#error(msg) "{{{
    execute "normal \<Esc>"
    echohl ErrorMsg
    echomsg "[gerrit-vim]: error: " . a:msg
    echohl None
endfunction "}}}

" DESC: Check variable and set default value if it not exists
fun! gv#default(name, default) "{{{
    if !exists(a:name)
        let {a:name} = a:default
        return 0
    endif
    return 1
endfunction "}}}


fun! gv#gvshowstatus() "{{{
	" Call the function that will display things on the
	" screen.
	gerrit_api.gerrit_status_wrapper()

endfunction "}}}

