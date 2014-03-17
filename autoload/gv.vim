echom 'Here in a/gv.vim'

" DESC: Import python libs that are needed
fun! gv#init(plugin_root, paths) "{{{

    if g:gv_python == 'disable'
        if g:gv_warning
            call gv#error("GV requires vim compiled with +python. Most of features will be disabled.")
        endif
        return
    endif


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
	GvPython from pygerrit import gerrit_api
	GvPython from pygerrit import salting
	GvPython gerrit_api.gerrit_status()
	" In general I feel unconfomfortable adding
	" this binding here. Perhaps there should be a better
	" API for callback that does some post actions.
	nnoremap <buffer> <C-g>v "zyiw:call gv#display_change_contents(@z)<CR>

endfunction "}}}

fun! gv#display_change_contents(contents) "{{{
	echo a:contents
	" Pick the change ID and rev id in the lookup
	" built by the previous call. Then display the
	" changes in the new buffer. 3 buffers will be
	" created. Top one for displaying the commit message and the file list.
	" The middle one the file contents and the
	" bottom one showing the comments
endfunction "}}}
