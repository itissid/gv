" Hook up the key mapping for the commands to
" a functions defined in the autoload/ dir
echom 'Here in f/p/gv.vim'
call gv#init(expand('<sfile>:p:h:h:h'), g:gv_paths)

if g:gv_show_status != ""
	exe "nnoremap " . g:gv_show_status . " :GvShowStatus<CR>"
endif

command! -nargs=0 GvShowStatus call gv#gvshowstatus()
