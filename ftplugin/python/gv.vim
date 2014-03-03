" Hook up the key mapping for the commands to
" a functions defined in the autoload/ dir
if !gv#default('g:gv_init', 1)
	call gv#init(expand('<sfile>:p:h:h:h'), g:gv_paths)

if g:gv_show_status != ""
	exe "nnoremap " . g:gv_show_status . " :GvShowStatus<CR>"

command! GVShowStatus call gv#gvshowstatus()
