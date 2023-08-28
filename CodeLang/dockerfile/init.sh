# init shell script

# git config
git config --list
git config --global credential.helper store
git config --global user.email "vhukzhang@tencent.com"
git config --global user.name "vhukzhang"
git config --global credential.helper store
git config --list


# zsh config
sed -i 's/robbyrussell/ys/' ~/.zshrc
sed -i 's/plugins=(git)/plugins=(git zsh-syntax-highlighting zsh-autosuggestions)/' ~/.zshrc


# vim config'
# https://dougblack.io/words/a-good-vimrc.html
# https://vimdoc.sourceforge.net/htmldoc/options.html

# 参考: https://blog.csdn.net/rudy_yuan/article/details/81055649?spm=1001.2101.3001.6650.6&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-6-81055649-blog-118491698.pc_relevant_multi_platform_whitelistv3&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-6-81055649-blog-118491698.pc_relevant_multi_platform_whitelistv3&utm_relevant_index=10
# touch ~/.vimrc
# echo "syntax on" >> ~/.vimrc
# echo "set ruler" >> ~/.vimrc
# echo "set showcmd" >> ~/.vimrc
# echo "set number" >> ~/.vimrc
# echo "set history=1000" >> ~/.vimrc
# echo "set hlsearch" >> ~/.vimrc
# echo "set encoding=utf-8" >> ~/.vimrc
# echo "set cursorline" >> ~/.vimrc
# echo "set showmatch" >> ~/.vimrc
# echo "set softtabstop=4" >> ~/.vimrc
# echo "set tabstop=4" >> ~/.vimrc
# echo "set expandtab" >> ~/.vimrc
# echo "set shiftwidth=4" >> ~/.vimrc
# echo "set autoindent" >> ~/.vimrc
# echo "%retab!" >> ~/.vimrc

# curl -sLf https://gitee.com/HGtz2222/VimForCpp/raw/master/install.sh -o ./install.sh && bash ./install.sh




# brew install protoc-gen-go  # fail
