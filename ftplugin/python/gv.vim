" Hook up the key mapping for the commands to
" a functions defined in the autoload/ dir
call gv#init(expand('<sfile>:p:h:h:h'), g:gv_paths)
call gv#default('g:gerrit_status_buffer_name', 'gerrit_status')

if g:gv_show_status != ""
	exe "nnoremap " . g:gv_show_status . " :GvShowStatus<CR>"
	command! -nargs=0 GvShowStatus call gv#gvshowstatus()
endif

if g:gv_show_changes != ""

	exe "nnoremap " . g:gv_show_changes . " :GvShowChanges<CR>"
	command! -nargs=0 GvShowChanges call gv#gvshowchanges()
endif
